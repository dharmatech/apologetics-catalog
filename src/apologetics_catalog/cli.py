from pathlib import Path
from typing import Annotated
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import typer
from rich.console import Console

from apologetics_catalog.catalog import Catalog
from apologetics_catalog.diagnostics import Diagnostic, Severity
from apologetics_catalog.show import render_entity
from apologetics_catalog.validator import validate_project
from apologetics_catalog.web import (
    DEFAULT_WEB_OUTPUT_DIR,
    build_web_output,
    missing_web_files,
)

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """Validate and compile apologetics catalog datasets."""


def _format_diagnostic(diagnostic: Diagnostic) -> str:
    location = diagnostic.location_text()
    prefix = f"{location}: " if location else ""
    return f"{prefix}{diagnostic.severity} {diagnostic.code}: {diagnostic.message}"


def _print_diagnostics(console: Console, diagnostics: list[Diagnostic]) -> None:
    for diagnostic in diagnostics:
        style = "red" if diagnostic.severity == Severity.ERROR else "yellow"
        console.print(_format_diagnostic(diagnostic), style=style)


def _validated_catalog_or_exit(manifest: Path, console: Console) -> Catalog:
    result = validate_project(manifest)

    if result.failed():
        _print_diagnostics(console, result.diagnostics)
        console.print("Cannot continue because validation failed.", style="red")
        raise typer.Exit(1)

    if result.catalog is None:
        console.print("Cannot continue because no catalog was built.", style="red")
        raise typer.Exit(1)

    return result.catalog


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

    _print_diagnostics(console, result.diagnostics)

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


@app.command()
def show(
    entity_id: Annotated[str, typer.Argument(help="Entity ID to show.")],
    manifest: Annotated[
        Path,
        typer.Option(
            "--manifest",
            "-m",
            help="Path to the project manifest.",
        ),
    ] = Path("apologetics.yaml"),
) -> None:
    result = validate_project(manifest)
    console = Console()

    if result.failed():
        _print_diagnostics(console, result.diagnostics)
        console.print("Cannot show entity because validation failed.", style="red")
        raise typer.Exit(1)

    if result.catalog is None:
        console.print("Cannot show entity because no catalog was built.", style="red")
        raise typer.Exit(1)

    entity = result.catalog.get(entity_id)
    if entity is None:
        console.print(f"No entity found for id: {entity_id}", style="red")
        suggestions = result.catalog.suggestions(entity_id)
        if suggestions:
            console.print()
            console.print("[bold]Suggestions[/bold]")
            for suggestion in suggestions:
                console.print(f"- {suggestion}")
        raise typer.Exit(1)

    render_entity(console, result.catalog, entity)


@app.command("build-web")
def build_web(
    manifest: Annotated[
        Path,
        typer.Option(
            "--manifest",
            "-m",
            help="Path to the project manifest.",
        ),
    ] = Path("apologetics.yaml"),
    output: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            help="Directory for generated web viewer files.",
        ),
    ] = DEFAULT_WEB_OUTPUT_DIR,
) -> None:
    console = Console()
    catalog = _validated_catalog_or_exit(manifest, console)
    written = build_web_output(catalog, output)

    console.print(f"Generated web viewer in {output}", style="green")
    for path in written:
        console.print(f"- {path}")


@app.command("serve-web")
def serve_web(
    manifest: Annotated[
        Path,
        typer.Option(
            "--manifest",
            "-m",
            help="Path to the project manifest.",
        ),
    ] = Path("apologetics.yaml"),
    output: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            help="Directory containing generated web viewer files.",
        ),
    ] = DEFAULT_WEB_OUTPUT_DIR,
    host: Annotated[
        str,
        typer.Option(
            "--host",
            help="Host interface for the local static server.",
        ),
    ] = "127.0.0.1",
    port: Annotated[
        int,
        typer.Option(
            "--port",
            help="Port for the local static server.",
            min=1,
            max=65535,
        ),
    ] = 8000,
    no_build: Annotated[
        bool,
        typer.Option(
            "--no-build",
            help="Serve existing generated files without running build-web first.",
        ),
    ] = False,
) -> None:
    console = Console()

    if no_build:
        missing = missing_web_files(output)
        if missing:
            console.print(
                f"{missing[0]} not found; run apologetics-catalog build-web first",
                style="red",
            )
            raise typer.Exit(1)
    else:
        catalog = _validated_catalog_or_exit(manifest, console)
        build_web_output(catalog, output)

    _serve_static_directory(console, output, host=host, port=port)


class _NoCacheStaticHandler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, format: str, *args: object) -> None:
        return


def _serve_static_directory(
    console: Console,
    directory: Path,
    *,
    host: str,
    port: int,
) -> None:
    resolved_directory = directory.resolve()
    handler = partial(_NoCacheStaticHandler, directory=str(resolved_directory))
    url = f"http://{host}:{port}/"

    try:
        with ThreadingHTTPServer((host, port), handler) as server:
            console.print(f"Serving {resolved_directory} at {url}", style="green")
            console.print("Press Ctrl+C to stop.")
            server.serve_forever()
    except OSError as error:
        console.print(f"Could not start server at {url}: {error}", style="red")
        raise typer.Exit(1) from error
    except KeyboardInterrupt:
        console.print("Stopped.")
