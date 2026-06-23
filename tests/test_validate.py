import json
from pathlib import Path

from typer.testing import CliRunner

from apologetics_catalog.cli import app
from apologetics_catalog.validator import validate_project
from apologetics_catalog.web import export_catalog_json

runner = CliRunner()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def normalize_output(text: str) -> str:
    return " ".join(text.split())


def test_current_dataset_validates() -> None:
    result = validate_project(Path("apologetics.yaml"))

    assert result.diagnostics == []
    assert result.content_files


def test_cli_validate_current_dataset() -> None:
    result = runner.invoke(app, ["validate"])

    assert result.exit_code == 0
    assert "Validation passed:" in result.stdout


def test_cli_show_nwt_evidence() -> None:
    result = runner.invoke(app, ["show", "evidence.nwt_2013.colossians.1_15.firstborn"])

    assert result.exit_code == 0
    assert "Evidence" in result.stdout
    assert (
        "New World Translation of the Holy Scriptures (2013 Revision)" in result.stdout
    )
    assert "firstborn of all creation" in result.stdout
    assert "Jehovah's Witnesses" in result.stdout
    assert "Claim: Jesus is a created being." in result.stdout


def test_cli_show_claim_uses_direction_labels() -> None:
    result = runner.invoke(app, ["show", "claim.jesus_created"])

    assert result.exit_code == 0
    assert "Supported by" in result.stdout
    assert "Contradicts" in result.stdout
    assert "Jehovah's Witnesses" in result.stdout
    assert "affirms" in result.stdout


def test_cli_show_missing_id_suggests_matches() -> None:
    result = runner.invoke(app, ["show", "evidence.nwt_2013.colossians"])

    assert result.exit_code == 1
    assert "No entity found for id: evidence.nwt_2013.colossians" in result.stdout
    assert "evidence.nwt_2013.colossians.1_15.firstborn" in result.stdout


def test_cli_build_web_generates_viewer_files(tmp_path: Path) -> None:
    output = tmp_path / "web"

    result = runner.invoke(app, ["build-web", "--output", str(output)])

    assert result.exit_code == 0, result.stdout
    assert (output / "catalog.json").is_file()
    assert (output / "index.html").is_file()
    assert (output / "app.js").is_file()
    assert (output / "style.css").is_file()

    data = json.loads((output / "catalog.json").read_text(encoding="utf-8"))
    assert data["schema_version"] == "0.1"
    assert data["generated_at"] is None
    assert data["project"]["id"] == "project.apologetics"
    assert (
        data["entities"]["claim.jesus_created"]["label"] == "Jesus is a created being."
    )
    assert (
        data["entities"]["evidence.nwt_2013.colossians.1_15.firstborn"]["details"][
            "source_label"
        ]
        == "New World Translation of the Holy Scriptures (2013 Revision)"
    )
    assert (
        data["entities"]["evidence.nwt_2013.colossians.1_15.firstborn"]["details"][
            "source_short_label"
        ]
        == "NWT 2013"
    )
    assert (
        "relationship.trinitarian.john_1_3_response.challenges_created_claim"
        in data["indexes"]["incoming"]["claim.jesus_created"]
    )

    relationship = next(
        item
        for item in data["relationships"]
        if item["id"] == "relationship.jw.colossians_firstborn.supports_created"
    )
    assert relationship["labels"]["incoming"] == "Supported by"
    assert relationship["labels"]["outgoing"] == "Supports"


def test_web_export_is_deterministic() -> None:
    result = validate_project(Path("apologetics.yaml"))

    assert result.catalog is not None
    assert export_catalog_json(result.catalog) == export_catalog_json(result.catalog)


def test_cli_serve_web_no_build_requires_existing_files(tmp_path: Path) -> None:
    output = tmp_path / "missing-web"

    result = runner.invoke(
        app,
        ["serve-web", "--no-build", "--output", str(output)],
    )

    assert result.exit_code == 1
    output_text = normalize_output(result.stdout)
    assert "catalog.json not found" in output_text
    assert "run apologetics-catalog build-web first" in output_text


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
