from collections import defaultdict
from collections.abc import Iterable

from rich.console import Console

from apologetics_catalog.catalog import Catalog, EntityRecord

OUTGOING_LABELS = {
    "responds_to": "Responds to",
    "supports": "Supports",
    "challenges": "Challenges",
    "contradicts": "Contradicts",
    "qualifies": "Qualifies",
    "uses": "Uses",
}

INCOMING_LABELS = {
    "responds_to": "Response from",
    "supports": "Supported by",
    "challenges": "Challenged by",
    "contradicts": "Contradicts",
    "qualifies": "Qualified by",
    "uses": "Used by",
}


def render_entity(console: Console, catalog: Catalog, entity: EntityRecord) -> None:
    console.print(f"[bold]{_kind_title(entity.kind)}[/bold]")
    console.print(f"ID: {entity.id}")

    if entity.kind == "evidence":
        _render_evidence(console, catalog, entity)
        _render_interpretations_for_evidence(console, catalog, entity)
    elif entity.kind == "interpretation":
        _render_interpretation(console, catalog, entity)
    elif entity.kind == "claim":
        _render_claim(console, catalog, entity)
        _render_positions_for_claim(console, catalog, entity)
    elif entity.kind == "position":
        _render_position(console, catalog, entity)
    elif entity.kind == "source":
        _render_source(console, entity)
    elif entity.kind == "relationship":
        _render_relationship(console, catalog, entity)
    else:
        _render_generic(console, entity)

    _render_relationships(console, catalog, entity)


def _render_evidence(
    console: Console,
    catalog: Catalog,
    entity: EntityRecord,
) -> None:
    data = entity.data
    source = catalog.get(str(data.get("source_id", "")))
    locator = data.get("locator")

    if source is not None:
        console.print(f"Source: {_entity_label(source)} ({source.id})")
    if isinstance(locator, dict):
        console.print(f"Locator: {locator.get('value', '')}")
    if isinstance(data.get("quotation"), str):
        console.print(f'Quotation: "{_one_line(data["quotation"])}"')
    if isinstance(data.get("paraphrase"), str):
        console.print(f"Paraphrase: {_one_line(data['paraphrase'])}")


def _render_interpretation(
    console: Console,
    catalog: Catalog,
    entity: EntityRecord,
) -> None:
    data = entity.data
    evidence = catalog.get(str(data.get("evidence_id", "")))

    console.print(f"Summary: {_one_line(str(data.get('summary', '')))}")
    if evidence is not None:
        console.print(f"Evidence: {_entity_label(evidence)} ({evidence.id})")
    attribution = _attribution_label(catalog, entity)
    if attribution:
        console.print(f"Attributed to: {attribution}")


def _render_claim(console: Console, catalog: Catalog, entity: EntityRecord) -> None:
    data = entity.data
    question = catalog.get(str(data.get("question_id", "")))

    console.print(f"Summary: {_one_line(str(data.get('summary', '')))}")
    if isinstance(data.get("proposition"), str):
        console.print(f"Proposition: {_one_line(data['proposition'])}")
    if question is not None:
        console.print(f"Question: {_entity_label(question)} ({question.id})")


def _render_position(console: Console, catalog: Catalog, entity: EntityRecord) -> None:
    data = entity.data
    holder = _typed_reference_entity(catalog, data.get("holder"))

    console.print(f"Summary: {_one_line(str(data.get('summary', '')))}")
    if holder is not None:
        console.print(f"Holder: {_entity_label(holder)} ({holder.id})")
    stances = data.get("claim_stances")
    if isinstance(stances, list) and stances:
        console.print()
        console.print("[bold]Claim Stances[/bold]")
        for stance in stances:
            if not isinstance(stance, dict):
                continue
            claim = catalog.get(str(stance.get("claim_id", "")))
            target = _entity_reference_text(claim, str(stance.get("claim_id", "")))
            console.print(
                f"- {stance.get('stance', '')} ({stance.get('status', '')}): {target}"
            )


def _render_source(console: Console, entity: EntityRecord) -> None:
    data = entity.data

    console.print(f"Title: {_one_line(str(data.get('title', '')))}")
    console.print(f"Type: {data.get('type', '')}")
    for key in ("author", "date", "language", "edition", "url", "accessed"):
        if data.get(key) is not None:
            console.print(f"{key.replace('_', ' ').title()}: {data[key]}")


def _render_relationship(
    console: Console,
    catalog: Catalog,
    entity: EntityRecord,
) -> None:
    data = entity.data
    from_entity = catalog.get(str(data.get("from_id", "")))
    to_entity = catalog.get(str(data.get("to_id", "")))

    console.print(f"Type: {data.get('type', '')}")
    console.print(
        f"From: {_entity_reference_text(from_entity, str(data.get('from_id', '')))}"
    )
    console.print(
        f"To: {_entity_reference_text(to_entity, str(data.get('to_id', '')))}"
    )
    if isinstance(data.get("summary"), str):
        console.print(f"Summary: {_one_line(data['summary'])}")


def _render_generic(console: Console, entity: EntityRecord) -> None:
    for key in ("title", "name", "summary", "description"):
        value = entity.data.get(key)
        if isinstance(value, str):
            console.print(f"{key.title()}: {_one_line(value)}")
            return


def _render_interpretations_for_evidence(
    console: Console,
    catalog: Catalog,
    evidence: EntityRecord,
) -> None:
    interpretations = [
        entity
        for entity in catalog.entities.values()
        if entity.kind == "interpretation"
        and (
            entity.data.get("evidence_id") == evidence.id
            or evidence.id in entity.data.get("related_evidence_ids", [])
        )
    ]
    if not interpretations:
        return

    console.print()
    console.print("[bold]Interpretations[/bold]")
    for interpretation in sorted(interpretations, key=lambda item: item.id):
        attribution = _attribution_label(catalog, interpretation)
        prefix = f"{attribution}: " if attribution else ""
        console.print(
            f"- {prefix}{_entity_label(interpretation)} ({interpretation.id})"
        )
        for relationship in catalog.relationships_from(interpretation.id):
            label = OUTGOING_LABELS.get(
                str(relationship.data.get("type")), "Related to"
            )
            target = catalog.get(str(relationship.data.get("to_id", "")))
            console.print(
                f"  {label}: {_entity_reference_text(target, str(relationship.data.get('to_id', '')))}"
            )


def _render_positions_for_claim(
    console: Console,
    catalog: Catalog,
    claim: EntityRecord,
) -> None:
    positions = [
        entity
        for entity in catalog.entities.values()
        if entity.kind == "position" and _position_references_claim(entity, claim.id)
    ]
    if not positions:
        return

    console.print()
    console.print("[bold]Positions[/bold]")
    for position in sorted(positions, key=lambda item: item.id):
        holder = _typed_reference_entity(catalog, position.data.get("holder"))
        holder_text = _entity_reference_text(holder, "")
        stance = _claim_stance_for(position, claim.id)
        console.print(
            f"- {holder_text}: {stance.get('stance', '')} "
            f"({stance.get('status', '')}) ({position.id})"
        )


def _render_relationships(
    console: Console,
    catalog: Catalog,
    entity: EntityRecord,
) -> None:
    grouped: dict[str, list[str]] = defaultdict(list)

    for relationship in catalog.relationships_from(entity.id):
        label = OUTGOING_LABELS.get(str(relationship.data.get("type")), "Related to")
        target = catalog.get(str(relationship.data.get("to_id", "")))
        grouped[label].append(
            _entity_reference_text(target, str(relationship.data.get("to_id", "")))
        )

    for relationship in catalog.relationships_to(entity.id):
        label = INCOMING_LABELS.get(str(relationship.data.get("type")), "Related from")
        source = catalog.get(str(relationship.data.get("from_id", "")))
        grouped[label].append(
            _entity_reference_text(source, str(relationship.data.get("from_id", "")))
        )

    if not grouped:
        return

    console.print()
    console.print("[bold]Relationships[/bold]")
    for label in sorted(grouped):
        console.print(f"{label}")
        for item in _sorted_unique(grouped[label]):
            console.print(f"- {item}")


def _position_references_claim(position: EntityRecord, claim_id: str) -> bool:
    stances = position.data.get("claim_stances")
    if not isinstance(stances, list):
        return False
    return any(
        isinstance(stance, dict) and stance.get("claim_id") == claim_id
        for stance in stances
    )


def _claim_stance_for(position: EntityRecord, claim_id: str) -> dict[str, str]:
    stances = position.data.get("claim_stances")
    if not isinstance(stances, list):
        return {}
    for stance in stances:
        if isinstance(stance, dict) and stance.get("claim_id") == claim_id:
            return {str(key): str(value) for key, value in stance.items()}
    return {}


def _typed_reference_entity(catalog: Catalog, value: object) -> EntityRecord | None:
    if not isinstance(value, dict):
        return None
    referenced_id = value.get("id")
    if not isinstance(referenced_id, str):
        return None
    return catalog.get(referenced_id)


def _attribution_label(catalog: Catalog, entity: EntityRecord) -> str:
    provenance = entity.data.get("provenance")
    if not isinstance(provenance, dict):
        return ""
    attributed_to = provenance.get("attributed_to")
    referenced = _typed_reference_entity(catalog, attributed_to)
    if referenced is not None:
        return _entity_label(referenced)
    if isinstance(attributed_to, dict) and isinstance(attributed_to.get("name"), str):
        return attributed_to["name"]
    return ""


def _entity_reference_text(entity: EntityRecord | None, fallback_id: str) -> str:
    if entity is None:
        return fallback_id
    return f"{_kind_title(entity.kind)}: {_entity_label(entity)} ({entity.id})"


def _entity_label(entity: EntityRecord) -> str:
    if entity.kind == "evidence":
        locator = entity.data.get("locator")
        if isinstance(locator, dict) and isinstance(locator.get("value"), str):
            return locator["value"]

    for key in ("title", "name", "summary", "quotation", "proposition"):
        value = entity.data.get(key)
        if isinstance(value, str):
            return _one_line(value)

    return entity.id


def _kind_title(kind: str) -> str:
    return kind.replace("_", " ").title()


def _one_line(value: str) -> str:
    return " ".join(value.split())


def _sorted_unique(values: Iterable[str]) -> list[str]:
    return sorted(set(values))
