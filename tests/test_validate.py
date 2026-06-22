from pathlib import Path

from typer.testing import CliRunner

from apologetics_catalog.cli import app
from apologetics_catalog.validator import validate_project

runner = CliRunner()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_current_dataset_validates() -> None:
    result = validate_project(Path("apologetics.yaml"))

    assert result.diagnostics == []
    assert result.content_files


def test_cli_validate_current_dataset() -> None:
    result = runner.invoke(app, ["validate"])

    assert result.exit_code == 0
    assert "Validation passed:" in result.stdout


def test_missing_manifest_reports_error(tmp_path: Path) -> None:
    result = validate_project(tmp_path / "missing.yaml")

    assert [diagnostic.code for diagnostic in result.diagnostics] == ["E001"]


def test_empty_include_pattern_reports_error(tmp_path: Path) -> None:
    manifest = tmp_path / "apologetics.yaml"
    write(
        manifest,
        """
schema_version: "0.1"
kind: project
project:
  id: project.test
  title: "Test"
content:
  include:
    - content/**/*.yaml
""".lstrip(),
    )

    result = validate_project(manifest)

    assert [diagnostic.code for diagnostic in result.diagnostics] == ["E004"]


def test_schema_version_mismatch_reports_error(tmp_path: Path) -> None:
    manifest = tmp_path / "apologetics.yaml"
    write(
        manifest,
        """
schema_version: "0.1"
kind: project
project:
  id: project.test
  title: "Test"
content:
  include:
    - content/**/*.yaml
""".lstrip(),
    )
    write(
        tmp_path / "content" / "question.yaml",
        """
schema_version: "0.2"
kind: question
question:
  id: question.test
  title: "Test?"
""".lstrip(),
    )

    result = validate_project(manifest)

    assert [diagnostic.code for diagnostic in result.diagnostics] == ["E003"]


def test_duplicate_id_reports_all_locations(tmp_path: Path) -> None:
    manifest = tmp_path / "apologetics.yaml"
    write(
        manifest,
        """
schema_version: "0.1"
kind: project
project:
  id: project.test
  title: "Test"
content:
  include:
    - content/**/*.yaml
""".lstrip(),
    )
    write(
        tmp_path / "content" / "one.yaml",
        """
schema_version: "0.1"
kind: claim
claim:
  id: claim.same
  question_id: question.test
  summary: "One"
""".lstrip(),
    )
    write(
        tmp_path / "content" / "two.yaml",
        """
schema_version: "0.1"
kind: claim
claim:
  id: claim.same
  question_id: question.test
  summary: "Two"
""".lstrip(),
    )

    result = validate_project(manifest)

    assert [diagnostic.code for diagnostic in result.diagnostics].count("E005") == 2


def test_unresolved_reference_reports_error(tmp_path: Path) -> None:
    manifest = tmp_path / "apologetics.yaml"
    write(
        manifest,
        """
schema_version: "0.1"
kind: project
project:
  id: project.test
  title: "Test"
content:
  include:
    - content/**/*.yaml
""".lstrip(),
    )
    write(
        tmp_path / "content" / "claim.yaml",
        """
schema_version: "0.1"
kind: claim
claim:
  id: claim.test
  question_id: question.missing
  summary: "Test"
""".lstrip(),
    )

    result = validate_project(manifest)

    assert [diagnostic.code for diagnostic in result.diagnostics] == ["E006"]
