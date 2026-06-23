from __future__ import annotations

import json
from collections.abc import Mapping
from datetime import date, datetime
from importlib import resources
from pathlib import Path
from typing import Any

from apologetics_catalog.catalog import Catalog, EntityRecord

WEB_SCHEMA_VERSION = "0.1"
DEFAULT_WEB_OUTPUT_DIR = Path("generated/web")
WEB_STATIC_PACKAGE = "apologetics_catalog.web_static"
STATIC_ASSET_NAMES = ("index.html", "app.js", "style.css")
EXPECTED_WEB_FILES = ("catalog.json", "index.html")

OUTGOING_LABELS = {
    "responds_to": "Responds to",
    "supports": "Supports",
    "challenges": "Challenges",
    "contradicts": "Contradicts",
    "qualifies": "Qualifies",
    "uses": "Uses",
    "depends_on": "Depends on",
    "narrows": "Narrows",
    "broadens": "Broadens",
    "related_to": "Related",
}

INCOMING_LABELS = {
    "responds_to": "Responded to by",
    "supports": "Supported by",
    "challenges": "Challenged by",
    "contradicts": "Contradicts",
    "qualifies": "Qualified by",
    "uses": "Used by",
    "depends_on": "Depended on by",
    "narrows": "Narrowed by",
    "broadens": "Broadened by",
    "related_to": "Related",
}

GROUP_ORDER = {
    ("outgoing", "contradicts"): 1,
    ("incoming", "contradicts"): 1,
    ("incoming", "challenges"): 2,
    ("outgoing", "challenges"): 3,
    ("incoming", "responds_to"): 4,
    ("outgoing", "responds_to"): 5,
    ("incoming", "supports"): 6,
    ("outgoing", "supports"): 7,
    ("incoming", "uses"): 8,
    ("outgoing", "uses"): 9,
    ("incoming", "depends_on"): 10,
    ("outgoing", "depends_on"): 11,
    ("incoming", "qualifies"): 12,
    ("outgoing", "qualifies"): 13,
    ("outgoing", "narrows"): 14,
    ("incoming", "narrows"): 14,
    ("outgoing", "broadens"): 15,
    ("incoming", "broadens"): 15,
    ("outgoing", "related_to"): 16,
    ("incoming", "related_to"): 16,
}


def build_web_output(catalog: Catalog, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    catalog_path = output_dir / "catalog.json"
    _write_text_atomic(catalog_path, export_catalog_json(catalog))
    written.append(catalog_path)

    static_root = resources.files(WEB_STATIC_PACKAGE)
    for asset_name in STATIC_ASSET_NAMES:
        asset = static_root.joinpath(asset_name)
        output_path = output_dir / asset_name
        output_path.write_bytes(asset.read_bytes())
        written.append(output_path)

    return written


def export_catalog_json(catalog: Catalog) -> str:
    return (
        json.dumps(
            export_catalog(catalog),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def export_catalog(catalog: Catalog) -> dict[str, Any]:
    relationships = [
        _relationship_record(catalog, relationship)
        for relationship in sorted(catalog.relationships, key=lambda item: item.id)
    ]

    return {
        "schema_version": WEB_SCHEMA_VERSION,
        "generated_at": None,
        "generator": {"name": "apologetics-catalog"},
        "project": _project_record(catalog),
        "entities": {
            entity_id: _entity_record(catalog, entity)
            for entity_id, entity in sorted(catalog.entities.items())
            if entity.kind != "relationship"
        },
        "relationships": relationships,
        "indexes": {
            "outgoing": _relationship_index(catalog, direction="outgoing"),
            "incoming": _relationship_index(catalog, direction="incoming"),
        },
    }


def missing_web_files(output_dir: Path) -> list[Path]:
    return [
        output_dir / name
        for name in EXPECTED_WEB_FILES
        if not (output_dir / name).is_file()
    ]


def _project_record(catalog: Catalog) -> dict[str, Any]:
    project = next(
        (entity for entity in catalog.entities.values() if entity.kind == "project"),
        None,
    )
    if project is None:
        return {"id": "", "title": ""}
    return {
        "id": project.id,
        "title": _string_value(project.data.get("title")),
    }


def _entity_record(catalog: Catalog, entity: EntityRecord) -> dict[str, Any]:
    return {
        "id": entity.id,
        "kind": entity.kind,
        "label": _entity_label(entity),
        "summary": _entity_summary(entity),
        "details": _entity_details(catalog, entity),
        "perspective": _entity_perspective(catalog, entity),
    }


def _entity_details(catalog: Catalog, entity: EntityRecord) -> dict[str, Any]:
    details = {
        key: _json_value(value) for key, value in entity.data.items() if key != "id"
    }

    if entity.kind == "evidence":
        source = catalog.get(_string_value(entity.data.get("source_id")))
        if source is not None:
            details["source_label"] = _entity_label(source)
            source_short_label = _string_value(source.data.get("short_label"))
            if source_short_label:
                details["source_short_label"] = source_short_label

    if entity.kind == "interpretation":
        evidence = catalog.get(_string_value(entity.data.get("evidence_id")))
        if evidence is not None:
            details["evidence_label"] = _entity_label(evidence)

    return details


def _relationship_record(
    catalog: Catalog, relationship: EntityRecord
) -> dict[str, Any]:
    relationship_type = _string_value(relationship.data.get("type"))
    from_id = _string_value(relationship.data.get("from_id"))
    to_id = _string_value(relationship.data.get("to_id"))

    return {
        "id": relationship.id,
        "type": relationship_type,
        "from_id": from_id,
        "to_id": to_id,
        "summary": _string_value(relationship.data.get("summary")),
        "labels": {
            "outgoing": _outgoing_label(relationship_type),
            "incoming": _incoming_label(relationship_type),
        },
        "group": {
            "outgoing": _outgoing_label(relationship_type),
            "incoming": _incoming_label(relationship_type),
            "outgoing_order": _group_order("outgoing", relationship_type),
            "incoming_order": _group_order("incoming", relationship_type),
        },
        "from_label": _related_entity_label(catalog, from_id),
        "to_label": _related_entity_label(catalog, to_id),
    }


def _relationship_index(
    catalog: Catalog,
    *,
    direction: str,
) -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for entity_id in sorted(catalog.entities):
        relationships = (
            catalog.relationships_from(entity_id)
            if direction == "outgoing"
            else catalog.relationships_to(entity_id)
        )
        if relationships:
            index[entity_id] = [
                relationship.id
                for relationship in sorted(
                    relationships,
                    key=lambda item: _relationship_sort_key(catalog, item, direction),
                )
            ]
    return index


def _relationship_sort_key(
    catalog: Catalog,
    relationship: EntityRecord,
    direction: str,
) -> tuple[int, str, str, str, str]:
    relationship_type = _string_value(relationship.data.get("type"))
    related_id = (
        _string_value(relationship.data.get("to_id"))
        if direction == "outgoing"
        else _string_value(relationship.data.get("from_id"))
    )
    related = catalog.get(related_id)
    related_kind = related.kind if related is not None else ""
    related_label = _entity_label(related) if related is not None else related_id

    return (
        _group_order(direction, relationship_type),
        related_kind,
        related_label,
        related_id,
        relationship.id,
    )


def _entity_perspective(
    catalog: Catalog,
    entity: EntityRecord,
) -> dict[str, str] | None:
    if entity.kind == "position":
        holder = _typed_reference_entity(catalog, entity.data.get("holder"))
        if holder is not None:
            return {"label": _entity_label(holder), "source": "holder"}

    provenance = entity.data.get("provenance")
    if isinstance(provenance, Mapping):
        attributed_to = provenance.get("attributed_to")
        attributed_entity = _typed_reference_entity(catalog, attributed_to)
        if attributed_entity is not None:
            return {
                "label": _entity_label(attributed_entity),
                "source": "provenance.attributed_to",
            }
        if isinstance(attributed_to, Mapping) and isinstance(
            attributed_to.get("name"),
            str,
        ):
            return {
                "label": attributed_to["name"],
                "source": "provenance.attributed_to",
            }
        if provenance.get("work") is not None:
            return {"label": "Dataset synthesis", "source": "provenance.work"}

    if entity.kind == "evidence":
        return {"label": "Source only", "source": "source"}

    return None


def _typed_reference_entity(
    catalog: Catalog,
    value: object,
) -> EntityRecord | None:
    if not isinstance(value, Mapping):
        return None
    referenced_id = value.get("id")
    if not isinstance(referenced_id, str):
        return None
    return catalog.get(referenced_id)


def _entity_label(entity: EntityRecord) -> str:
    if entity.kind == "evidence":
        locator = entity.data.get("locator")
        if isinstance(locator, Mapping) and isinstance(locator.get("value"), str):
            return locator["value"]

    for key in ("title", "name", "summary", "quotation", "proposition"):
        value = entity.data.get(key)
        if isinstance(value, str):
            return _one_line(value)

    return entity.id


def _entity_summary(entity: EntityRecord) -> str:
    for key in ("summary", "description", "proposition", "quotation", "title", "name"):
        value = entity.data.get(key)
        if isinstance(value, str):
            return _one_line(value)
    return _entity_label(entity)


def _related_entity_label(catalog: Catalog, entity_id: str) -> str:
    entity = catalog.get(entity_id)
    if entity is None:
        return entity_id
    return _entity_label(entity)


def _outgoing_label(relationship_type: str) -> str:
    return OUTGOING_LABELS.get(relationship_type, _fallback_label(relationship_type))


def _incoming_label(relationship_type: str) -> str:
    return INCOMING_LABELS.get(relationship_type, _fallback_label(relationship_type))


def _group_order(direction: str, relationship_type: str) -> int:
    return GROUP_ORDER.get((direction, relationship_type), 1000)


def _fallback_label(value: str) -> str:
    if not value:
        return "Related"
    return value.replace("_", " ").title()


def _string_value(value: object) -> str:
    return value if isinstance(value, str) else ""


def _one_line(value: str) -> str:
    return " ".join(value.split())


def _json_value(value: object) -> Any:
    if isinstance(value, datetime | date):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    return value


def _write_text_atomic(path: Path, text: str) -> None:
    temporary_path = path.with_name(f"{path.name}.tmp")
    temporary_path.write_text(text, encoding="utf-8", newline="\n")
    temporary_path.replace(path)
