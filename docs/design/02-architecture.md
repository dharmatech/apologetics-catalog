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
schema_version: "0.1"

kind: topic

question:
  id: question.christology.created_being
  title: "Is Jesus a created being?"
  question_type: yes_no
  status: active
  topic_ids:
    - topic.christology

claims:
  - id: claim.jesus_created
    question_id: question.christology.created_being
    summary: >
      Jesus is a created being.

evidence:
  - id: evidence.bsb.colossians.1_15.firstborn
    source_id: source.bible.bsb
    locator:
      type: verse
      value: "Colossians 1:15"
    quotation: "firstborn over all creation"
```

Single-record files should use the same envelope pattern.

Example:

```yaml
schema_version: "0.1"

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
topic_id: topic.christology
source_id: source.bible.bsb
agent_id: agent.council.nicaea_325
evidence_id: evidence.bsb.colossians.1_15.firstborn
from_id: argument.trinitarian.firstborn_rank
to_id: interpretation.jw.colossians.1_15.firstborn
target_ids:
  - claim.jesus_created
depends_on_ids:
  - assumption.firstborn_means_first_created
```

Typed references may use an object when the reference needs both a target kind
and a target ID.

Example:

```yaml
holder:
  type: tradition
  id: tradition.jehovahs_witnesses
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
schema_version: "0.1"
```

Schema versions should be strings, not numbers, so YAML parsers do not treat
versions such as `0.1` as floating point values.

The `schema_version` field applies to each YAML document.

The compiler should maintain an explicit list of supported schema versions.

The current schema version should be validated directly.

Older supported schema versions should require explicit migration.

Unsupported schema versions should produce clear validation errors.

Mixed document versions should be rejected unless a supported migration path
exists.

The compiler should not silently migrate source documents during `build`.

Migrations should be explicit, deterministic, and reviewed like code.

Migrations should write updated YAML source files or migrated YAML output, not
only transform data in memory.

During early `0.x` versions, schema changes may be breaking.

Migration scripts should be provided where practical.

Generated outputs do not need backward compatibility across schema versions.

Schema files should be stored in versioned directories.

Example:

```text
/schema/0.1/topic.schema.json
/schema/0.1/question.schema.json
/schema/0.1/claim.schema.json
/schema/0.1/relationship.schema.json
/schema/0.2/topic.schema.json
```

Each schema version should have human-readable change notes.

Example:

```text
/docs/schema/CHANGELOG.md
```

---

## Controlled Vocabularies

Controlled vocabularies should live with each schema version. The v0.1 seed
values, extension policy, and distinction between author-facing relationship
types and compiler-generated graph edge types are defined in:

```text
/docs/design/10-vocabularies.md
```

Machine-readable vocabulary files should eventually be generated from or kept
consistent with that design contract.

Examples:

```text
/schema/0.1/vocab/document-kinds.yaml
/schema/0.1/vocab/question-types.yaml
/schema/0.1/vocab/question-statuses.yaml
/schema/0.1/vocab/relationship-types.yaml
/schema/0.1/vocab/argument-roles.yaml
/schema/0.1/vocab/source-types.yaml
/schema/0.1/vocab/agent-types.yaml
/schema/0.1/vocab/holder-types.yaml
/schema/0.1/vocab/locator-types.yaml
/schema/0.1/vocab/rights-statuses.yaml
/schema/0.1/vocab/position-stances.yaml
/schema/0.1/vocab/position-statuses.yaml
/schema/0.1/vocab/interpretation-methods.yaml
/schema/0.1/vocab/assumption-categories.yaml
/schema/0.1/vocab/provenance-agent-types.yaml
/schema/0.1/vocab/generated-edge-types.yaml
```

The compiler should validate controlled fields against the vocabulary files for
the document's declared `schema_version`.

Core vocabulary values should use short field-local IDs.

Examples:

```yaml
kind: topic
question:
  question_type: yes_no
  status: active
source:
  type: scripture
agent:
  type: council
argument:
  role: objection
claim_stance:
  stance: affirms
  status: official
interpretation:
  method: lexical
assumption:
  category: lexical
relationship:
  type: supports
```

Extensions should be declared explicitly at the dataset or project level, not
introduced inline.

Unknown vocabulary values should be validation errors unless they are declared
as extensions in an extensible vocabulary.

Extension IDs should be namespaced.

Examples:

```text
project.appeals_to_liturgical_usage
org.example.some_relation
```

Vocabulary extensions should be dataset-level or project-level, not file-local.

Example:

```yaml
schema_version: "0.1"

kind: project

project:
  id: project.apologetics
  title: "Apologetics Viewpoint Catalog"

vocabulary_extensions:
  relationship_types:
    - id: project.appeals_to_liturgical_usage
      label: "Appeals to liturgical usage"
      description: >
        Used when an argument appeals to historical worship practice.
```

Vocabulary entries should support at least:

```yaml
id: supports
label: "Supports"
description: >
  Indicates that one entity is used to support another entity.
```

Vocabulary entries may later support additional validation metadata.

Examples:

```yaml
inverse: supported_by
symmetric: false
allowed_from:
  - Argument
  - Interpretation
allowed_to:
  - Claim
  - Interpretation
```
