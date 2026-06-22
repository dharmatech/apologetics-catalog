from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from apologetics_catalog.diagnostics import Diagnostic, Severity
from apologetics_catalog.validator import validate_project

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """Validate and compile apologetics catalog datasets."""


def _format_diagnostic(diagnostic: Diagnostic) -> str:
    location = diagnostic.location_text()
    prefix = f"{location}: " if location else ""
    return f"{prefix}{diagnostic.severity} {diagnostic.code}: {diagnostic.message}"


@app.command()
def validate(
    manifest: Annotated[
        Path,
        typer.Option(
            "--manifest",
            "-m",
            help="Path to the project manifest.",
        ),
    ] = Path("apologetics.yaml"),
    warnings_as_errors: Annotated[
        bool,
        typer.Option(
            "--warnings-as-errors",
            help="Treat warnings as validation failures.",
        ),
    ] = False,
) -> None:
    result = validate_project(manifest)
    console = Console()

    for diagnostic in result.diagnostics:
        style = "red" if diagnostic.severity == Severity.ERROR else "yellow"
        console.print(_format_diagnostic(diagnostic), style=style)

    if result.failed(warnings_as_errors=warnings_as_errors):
        console.print(
            f"Validation failed: {result.error_count} error(s), "
            f"{result.warning_count} warning(s).",
            style="red",
        )
        raise typer.Exit(1)

    console.print(
        f"Validation passed: {len(result.content_files)} content file(s).",
        style="green",
    )
