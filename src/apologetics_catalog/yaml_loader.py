from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

from apologetics_catalog.diagnostics import Diagnostic, Severity


@dataclass(frozen=True)
class SourceLocation:
    file: Path
    line: int | None = None
    column: int | None = None

    def to_diagnostic(
        self,
        *,
        code: str,
        message: str,
        severity: Severity = Severity.ERROR,
    ) -> Diagnostic:
        return Diagnostic(
            severity=severity,
            code=code,
            message=message,
            file=str(self.file),
            line=self.line,
            column=self.column,
        )


@dataclass(frozen=True)
class LoadedYamlDocument:
    path: Path
    data: Any

    def location(self) -> SourceLocation:
        return SourceLocation(file=self.path)


def load_yaml_document(
    path: Path,
) -> tuple[LoadedYamlDocument | None, list[Diagnostic]]:
    yaml = YAML(typ="rt")

    try:
        data = yaml.load(path.read_text(encoding="utf-8"))
    except YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        line = None if mark is None else mark.line + 1
        column = None if mark is None else mark.column + 1
        return None, [
            Diagnostic(
                severity=Severity.ERROR,
                code="E002",
                message=f"YAML parse error: {exc}",
                file=str(path),
                line=line,
                column=column,
            )
        ]

    return LoadedYamlDocument(path=path, data=data), []


def location_for_key(path: Path, mapping: Any, key: str) -> SourceLocation:
    line: int | None = None
    column: int | None = None
    try:
        raw_line, raw_column = mapping.lc.key(key)
    except (AttributeError, KeyError, TypeError):
        return SourceLocation(file=path)

    if raw_line is not None:
        line = raw_line + 1
    if raw_column is not None:
        column = raw_column + 1
    return SourceLocation(file=path, line=line, column=column)


def location_for_sequence_item(path: Path, sequence: Any, index: int) -> SourceLocation:
    line: int | None = None
    column: int | None = None
    try:
        raw_line, raw_column = sequence.lc.item(index)
    except (AttributeError, KeyError, TypeError):
        return SourceLocation(file=path)

    if raw_line is not None:
        line = raw_line + 1
    if raw_column is not None:
        column = raw_column + 1
    return SourceLocation(file=path, line=line, column=column)
