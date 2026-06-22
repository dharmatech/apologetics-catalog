from dataclasses import dataclass
from fnmatch import fnmatchcase
from pathlib import Path, PurePosixPath
from typing import Any

from ruamel.yaml.comments import CommentedMap, CommentedSeq

from apologetics_catalog.diagnostics import Diagnostic, Severity, ValidationResult
from apologetics_catalog.yaml_loader import (
    LoadedYamlDocument,
    SourceLocation,
    load_yaml_document,
    location_for_key,
    location_for_sequence_item,
)

SUPPORTED_SCHEMA_VERSION = "0.1"
DEFAULT_MANIFEST = Path("apologetics.yaml")

SINGLE_RECORD_SECTIONS = {
    "project",
    "topic",
    "question",
    "claim",
    "tradition",
    "agent",
    "position",
    "source",
    "interpretation",
    "assumption",
    "argument",
    "relationship",
}

LIST_RECORD_SECTIONS = {
    "topics",
    "questions",
    "claims",
    "traditions",
    "agents",
    "positions",
    "sources",
    "evidence",
    "interpretations",
    "assumptions",
    "arguments",
    "relationships",
}

TYPED_REFERENCE_FIELDS = {"holder", "attributed_to"}


@dataclass(frozen=True)
class EntityId:
    id: str
    location: SourceLocation


@dataclass(frozen=True)
class EntityReference:
    id: str
    field: str
    location: SourceLocation


def validate_project(manifest_path: Path = DEFAULT_MANIFEST) -> ValidationResult:
    manifest_path = manifest_path.resolve()
    diagnostics: list[Diagnostic] = []

    if not manifest_path.exists():
        diagnostics.append(
            Diagnostic(
                severity=Severity.ERROR,
                code="E001",
                message="Project manifest not found.",
                file=str(manifest_path),
            )
        )
        return ValidationResult(diagnostics=diagnostics, content_files=[])

    manifest, manifest_diagnostics = load_yaml_document(manifest_path)
    diagnostics.extend(manifest_diagnostics)
    if manifest is None:
        return ValidationResult(diagnostics=diagnostics, content_files=[])

    manifest_errors = _validate_envelope(
        manifest,
        expected_kind="project",
        expected_schema_version=SUPPORTED_SCHEMA_VERSION,
    )
    diagnostics.extend(manifest_errors)
    if manifest_errors:
        return ValidationResult(diagnostics=diagnostics, content_files=[])

    content_files, discovery_diagnostics = _discover_content_files(manifest)
    diagnostics.extend(discovery_diagnostics)
    if discovery_diagnostics:
        return ValidationResult(
            diagnostics=diagnostics, content_files=[str(path) for path in content_files]
        )

    documents: list[LoadedYamlDocument] = []
    for path in content_files:
        document, document_diagnostics = load_yaml_document(path)
        diagnostics.extend(document_diagnostics)
        if document is None:
            continue

        envelope_diagnostics = _validate_envelope(
            document,
            expected_schema_version=SUPPORTED_SCHEMA_VERSION,
        )
        diagnostics.extend(envelope_diagnostics)
        if envelope_diagnostics:
            continue

        documents.append(document)

    id_index: dict[str, list[SourceLocation]] = {}
    references: list[EntityReference] = []

    for document in [manifest, *documents]:
        entity_ids, entity_id_diagnostics = _collect_entity_ids(document)
        diagnostics.extend(entity_id_diagnostics)
        for entity_id in entity_ids:
            id_index.setdefault(entity_id.id, []).append(entity_id.location)
        references.extend(_collect_references(document))

    diagnostics.extend(_duplicate_id_diagnostics(id_index))
    diagnostics.extend(_unresolved_reference_diagnostics(id_index, references))

    return ValidationResult(
        diagnostics=diagnostics,
        content_files=[str(path) for path in content_files],
    )


def _validate_envelope(
    document: LoadedYamlDocument,
    *,
    expected_schema_version: str,
    expected_kind: str | None = None,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    data = document.data

    if not isinstance(data, CommentedMap):
        return [
            document.location().to_diagnostic(
                code="E003",
                message="YAML document must be a mapping with schema_version and kind.",
            )
        ]

    schema_version = data.get("schema_version")
    if schema_version != expected_schema_version:
        diagnostics.append(
            location_for_key(document.path, data, "schema_version").to_diagnostic(
                code="E003",
                message=(
                    f"Expected schema_version {expected_schema_version!r}, "
                    f"found {schema_version!r}."
                ),
            )
        )

    kind = data.get("kind")
    if not isinstance(kind, str):
        diagnostics.append(
            location_for_key(document.path, data, "kind").to_diagnostic(
                code="E003",
                message="Document kind is required.",
            )
        )
    elif expected_kind is not None and kind != expected_kind:
        diagnostics.append(
            location_for_key(document.path, data, "kind").to_diagnostic(
                code="E003",
                message=f"Expected kind {expected_kind!r}, found {kind!r}.",
            )
        )

    return diagnostics


def _discover_content_files(
    manifest: LoadedYamlDocument,
) -> tuple[list[Path], list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    data = manifest.data
    root = manifest.path.parent

    content = data.get("content")
    if not isinstance(content, CommentedMap):
        return [], [
            manifest.location().to_diagnostic(
                code="E003",
                message="Project manifest must define a content mapping.",
            )
        ]

    includes = content.get("include")
    if not _is_string_sequence(includes):
        return [], [
            location_for_key(manifest.path, content, "include").to_diagnostic(
                code="E003",
                message="Project manifest content.include must be a list of glob patterns.",
            )
        ]

    raw_excludes = content.get("exclude")
    if raw_excludes is None:
        excludes: list[str] = []
    elif _is_string_sequence(raw_excludes):
        excludes = list(raw_excludes)
    else:
        return [], [
            location_for_key(manifest.path, content, "exclude").to_diagnostic(
                code="E003",
                message="Project manifest content.exclude must be a list of glob patterns.",
            )
        ]

    outputs = data.get("outputs", {})
    generated_dir = "generated"
    if isinstance(outputs, CommentedMap) and isinstance(
        outputs.get("generated_dir"), str
    ):
        generated_dir = outputs["generated_dir"]

    exclude_patterns = [
        *excludes,
        ".git/**",
        ".codex/**",
        ".agents/**",
        f"{generated_dir}/**",
    ]
    discovered: dict[Path, None] = {}

    for index, pattern in enumerate(includes):
        matches = [
            path
            for path in root.glob(pattern)
            if path.is_file() and not _is_excluded(root, path, exclude_patterns)
        ]
        if not matches:
            diagnostics.append(
                location_for_sequence_item(
                    manifest.path, includes, index
                ).to_diagnostic(
                    code="E004",
                    message=f"Content include pattern matched no files: {pattern}",
                )
            )
            continue
        for path in sorted(matches):
            discovered[path.resolve()] = None

    return list(discovered), diagnostics


def _is_string_sequence(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _is_excluded(root: Path, path: Path, patterns: list[str]) -> bool:
    relative = _relative_posix(root, path)
    return any(_matches_pattern(relative, pattern) for pattern in patterns)


def _matches_pattern(relative_path: str, pattern: str) -> bool:
    normalized_pattern = PurePosixPath(pattern).as_posix()
    if normalized_pattern.endswith("/**"):
        prefix = normalized_pattern[:-3]
        return relative_path == prefix or relative_path.startswith(f"{prefix}/")
    return fnmatchcase(relative_path, normalized_pattern)


def _relative_posix(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _collect_entity_ids(
    document: LoadedYamlDocument,
) -> tuple[list[EntityId], list[Diagnostic]]:
    ids: list[EntityId] = []
    diagnostics: list[Diagnostic] = []
    data = document.data

    if not isinstance(data, CommentedMap):
        return ids, diagnostics

    for section, value in data.items():
        if section in SINGLE_RECORD_SECTIONS:
            if not isinstance(value, CommentedMap):
                diagnostics.append(_invalid_section(document, section, "mapping"))
                continue
            _append_entity_id(document, value, ids, diagnostics)
            continue

        if section == "evidence" and isinstance(value, CommentedMap):
            _append_entity_id(document, value, ids, diagnostics)
            continue

        if section in LIST_RECORD_SECTIONS:
            if not isinstance(value, CommentedSeq):
                diagnostics.append(_invalid_section(document, section, "list"))
                continue
            for index, item in enumerate(value):
                if not isinstance(item, CommentedMap):
                    diagnostics.append(
                        location_for_sequence_item(
                            document.path, value, index
                        ).to_diagnostic(
                            code="E007",
                            message=f"Record section {section!r} must contain mappings.",
                        )
                    )
                    continue
                _append_entity_id(document, item, ids, diagnostics)

    return ids, diagnostics


def _invalid_section(
    document: LoadedYamlDocument,
    section: str,
    expected_shape: str,
) -> Diagnostic:
    return location_for_key(document.path, document.data, section).to_diagnostic(
        code="E007",
        message=f"Record section {section!r} must be a {expected_shape}.",
    )


def _append_entity_id(
    document: LoadedYamlDocument,
    record: CommentedMap,
    ids: list[EntityId],
    diagnostics: list[Diagnostic],
) -> None:
    value = record.get("id")
    location = location_for_key(document.path, record, "id")
    if not isinstance(value, str) or not value:
        diagnostics.append(
            location.to_diagnostic(
                code="E008",
                message="Entity record is missing a string id.",
            )
        )
        return
    ids.append(EntityId(id=value, location=location))


def _collect_references(document: LoadedYamlDocument) -> list[EntityReference]:
    references: list[EntityReference] = []
    _walk_for_references(document.path, document.data, references)
    return references


def _walk_for_references(
    path: Path,
    node: Any,
    references: list[EntityReference],
) -> None:
    if isinstance(node, CommentedMap):
        for key, value in node.items():
            if isinstance(key, str):
                _collect_reference_field(path, node, key, value, references)
            _walk_for_references(path, value, references)
    elif isinstance(node, CommentedSeq):
        for item in node:
            _walk_for_references(path, item, references)


def _collect_reference_field(
    path: Path,
    mapping: CommentedMap,
    key: str,
    value: Any,
    references: list[EntityReference],
) -> None:
    if key == "id":
        return

    if key.endswith("_id") and isinstance(value, str):
        references.append(
            EntityReference(
                id=value,
                field=key,
                location=location_for_key(path, mapping, key),
            )
        )
        return

    if key.endswith("_ids") and isinstance(value, CommentedSeq):
        for index, item in enumerate(value):
            if isinstance(item, str):
                references.append(
                    EntityReference(
                        id=item,
                        field=key,
                        location=location_for_sequence_item(path, value, index),
                    )
                )
        return

    if key in TYPED_REFERENCE_FIELDS and isinstance(value, CommentedMap):
        referenced_id = value.get("id")
        if isinstance(referenced_id, str):
            references.append(
                EntityReference(
                    id=referenced_id,
                    field=f"{key}.id",
                    location=location_for_key(path, value, "id"),
                )
            )


def _duplicate_id_diagnostics(
    id_index: dict[str, list[SourceLocation]],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for entity_id, locations in sorted(id_index.items()):
        if len(locations) < 2:
            continue
        rendered_locations = ", ".join(
            location.file.as_posix() for location in locations
        )
        for location in locations:
            diagnostics.append(
                location.to_diagnostic(
                    code="E005",
                    message=f"Duplicate id {entity_id!r}. Also seen in: {rendered_locations}",
                )
            )
    return diagnostics


def _unresolved_reference_diagnostics(
    id_index: dict[str, list[SourceLocation]],
    references: list[EntityReference],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for reference in references:
        if reference.id in id_index:
            continue
        diagnostics.append(
            reference.location.to_diagnostic(
                code="E006",
                message=f"Unresolved reference {reference.id!r} in {reference.field}.",
            )
        )
    return diagnostics
