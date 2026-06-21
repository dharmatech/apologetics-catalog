# Architecture

## Canonical Source Format

Human-authored YAML files.

Example:

```text
/content
```

The YAML files represent the source of truth.

YAML is the canonical authoring and interchange format.

Other interfaces may be built on top of the same model, but they should read
from and write to the canonical YAML source unless the project deliberately
changes its storage model.

---

## Authoring Organization

YAML files should be organized for human authoring and review.

The preferred initial organization is topic-centered or question-centered rather
than fully normalized by entity type.

Example:

```text
/content/questions/christology/created-being/question.yaml
/content/questions/christology/created-being/claims.yaml
/content/questions/christology/created-being/sources.yaml
/content/questions/christology/created-being/evidence.yaml
/content/questions/christology/created-being/interpretations.yaml
/content/questions/christology/created-being/arguments.yaml
/content/questions/christology/created-being/relationships.yaml
```

For very small datasets, a single topic file may also be acceptable.

Example:

```text
/content/questions/christology/created-being.yaml
```

The authoring layout should follow human workflow.

The compiler should normalize the loaded YAML into one global graph.

Stable identifiers, not file paths, define entity identity.

File paths are organizational.

Generated outputs may be normalized by entity type or graph structure.

---

## YAML Document Shape

YAML documents should use a predictable envelope.

Topic-centered files should declare a schema version and document kind, then
group records into named sections.

Example:

```yaml
schema_version: 0.1

kind: topic

question:
  id: question.christology.created_being
  title: "Is Jesus a created being?"

claims:
  - id: claim.jesus_created
    question_id: question.christology.created_being
    summary: >
      Jesus is a created being.

evidence:
  - id: evidence.colossians.firstborn
    source_id: source.scripture.colossians.1.15
    quotation: "firstborn of all creation"
```

Single-record files should use the same envelope pattern.

Example:

```yaml
schema_version: 0.1

kind: claim

claim:
  id: claim.jesus_created
  question_id: question.christology.created_being
  summary: >
    Jesus is a created being.
```

Sections containing multiple records should be lists of records, not maps keyed
by ID.

Preferred:

```yaml
claims:
  - id: claim.jesus_created
    question_id: question.christology.created_being
```

Avoid:

```yaml
claims:
  claim.jesus_created:
    question_id: question.christology.created_being
```

Every entity must declare its own stable `id`.

The compiler should not infer canonical IDs from file paths, titles, or section
names.

References should use explicit `_id` fields for single references and `_ids`
fields for lists.

Examples:

```yaml
question_id: question.christology.created_being
source_id: source.scripture.colossians.1.15
tradition_id: tradition.jehovahs_witnesses
evidence_id: evidence.colossians.firstborn
from_id: argument.trinitarian.firstborn_rank
to_id: interpretation.jw.colossians.firstborn
target_ids:
  - claim.jesus_created
depends_on_ids:
  - assumption.firstborn_means_first_created
```

YAML list order may be preserved for readability and default display, but list
order should not imply truth, strength, priority, or dependency.

If ordering has semantic meaning, it should be represented explicitly.

Examples:

```yaml
display_order: 1
sequence: 2
```

---

## Validation and Compiler Layer

A compiler/validator processes all YAML files.

Example:

```text
/compiler
```

Responsibilities:

* schema validation
* reference validation
* duplicate detection
* graph construction
* normalization into a global graph
* consistency checking
* output generation

The compiler functions similarly to a traditional programming language compiler.

YAML should be treated as source code rather than unstructured data.

---

## Versioning

All datasets and schemas should include explicit version information.

Example:

```yaml
schema_version: 0.1
```

Future schema changes should support migrations where practical.
