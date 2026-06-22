from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from apologetics_catalog.catalog import Catalog


class Severity(StrEnum):
    ERROR = "error"
    WARNING = "warning"


class Diagnostic(BaseModel):
    model_config = ConfigDict(frozen=True)

    severity: Severity
    code: str
    message: str
    file: str | None = None
    line: int | None = None
    column: int | None = None

    def location_text(self) -> str:
        if self.file is None:
            return ""
        if self.line is None:
            return self.file
        if self.column is None:
            return f"{self.file}:{self.line}"
        return f"{self.file}:{self.line}:{self.column}"


class ValidationResult(BaseModel):
    diagnostics: list[Diagnostic]
    content_files: list[str]
    catalog: Catalog | None = None

    @property
    def error_count(self) -> int:
        return sum(
            1
            for diagnostic in self.diagnostics
            if diagnostic.severity == Severity.ERROR
        )

    @property
    def warning_count(self) -> int:
        return sum(
            1
            for diagnostic in self.diagnostics
            if diagnostic.severity == Severity.WARNING
        )

    def failed(self, *, warnings_as_errors: bool = False) -> bool:
        if self.error_count > 0:
            return True
        return warnings_as_errors and self.warning_count > 0
