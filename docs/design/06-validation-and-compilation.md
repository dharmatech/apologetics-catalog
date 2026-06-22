# Validation and Compilation

## Validation Phases

Validation should be layered.

Recommended phases:

```text
discovery
parse
envelope
schema
vocabulary
identity
references
graph
outputs
```

The discovery phase finds and validates the root project manifest, resolves
manifest-relative content include and exclude patterns, rejects empty include
matches, and determines the dataset file set. Manifest rules are defined in
[v0.1 Project Manifest](13-project-manifest.md).

The parser phase loads YAML and reports syntax errors.

The envelope phase validates document-level fields such as `schema_version` and
`kind`, including whether the declared schema version is supported. In v0.1,
content document schema versions must match the root manifest schema version.

The schema phase validates each entity's required fields and local structure
against the schema files for the declared schema version.

The vocabulary phase validates controlled values such as relationship types,
argument roles, question types, question statuses, agent types, position
stances, position statuses, interpretation methods, and assumption categories.
It should validate core values and declared project-level extensions.

The identity phase validates entity IDs, detects duplicate IDs, and confirms
that every entity declares its own stable `id`. ID format, collision, and
rename rules are defined in [v0.1 ID Conventions](12-id-conventions.md).

The references phase validates cross-file and cross-entity references.

The graph phase validates dataset-level graph consistency.

The outputs phase validates generated artifacts where practical.

JSON Schema should be used where practical for editor support, autocomplete,
and local document or entity validation.

The compiler remains responsible for cross-file references, global identity,
and graph semantics.

If parsing or envelope validation fails for a document, deeper validation for
that document should be skipped.

If an entity fails schema validation, graph checks involving that invalid entity
should be skipped.

The compiler should collect as many independent diagnostics as practical while
avoiding noisy cascading errors when an earlier phase already explains the root
cause.

---

## Validation Requirements

Validation should include:

* project manifest validation
* manifest content include and exclude validation
* empty include match validation
* schema validation
* document envelope validation
* schema version validation
* content schema version matching validation
* required field validation
* duplicate ID detection
* explicit entity ID validation
* ID format validation
* retired ID reuse validation when migration metadata exists
* reference validation
* reference field naming validation
* topic reference validation
* question hierarchy validation
* question type validation
* question status validation
* relationship validation
* claim relationship validation
* controlled vocabulary validation
* vocabulary extension declaration validation
* unknown vocabulary value validation
* argument role validation
* agent type validation
* position holder validation
* position claim stance validation
* position status validation
* interpretation method validation
* assumption category validation
* provenance validation
* locator validation
* source rights metadata validation
* evidence quotation validation
* section list validation
* orphan node detection
* consistency checking
* first-class relationship validation

Examples:

* missing references
* duplicate identifiers
* missing `schema_version`
* unsupported `schema_version`
* missing or invalid `kind`
* mixed document versions without a supported migration path
* invalid relationship types
* invalid topic references
* invalid parent question references
* invalid question types
* invalid question statuses
* invalid claim relationship endpoints
* unknown vocabulary values without explicit extension declarations
* malformed vocabulary extension declarations
* invalid argument roles
* invalid agent types
* missing or invalid position holders
* invalid position claim stances
* invalid position statuses
* invalid interpretation methods
* invalid assumption categories
* invalid provenance source references
* malformed locators
* exact quotations attached to abstract sources
* sections represented as maps keyed by ID instead of lists of records
* references to nonexistent entities
* first-class relationships whose `from_id` or `to_id` targets do not exist
* content files whose `schema_version` differs from the root manifest
* include patterns that match no files

The compiler should reject invalid datasets.

Duplicate ID diagnostics should report every known source location for the
collision, not only the first or last record encountered.

---

## Normalized Catalog

After validation succeeds, YAML should compile into a normalized catalog.

The normalized catalog is the compiler's canonical intermediate representation.

It should preserve:

* every entity by stable `id`
* entity `kind`
* first-class `Relationship` records
* provenance and rights metadata
* source file and location metadata where practical
* schema version used for validation

IDs are globally unique across all entity kinds.

The compiler should not build a full normalized catalog from an invalid dataset.

Diagnostics may still use partial parse or schema context when validation fails.

Example:

```yaml
catalog:
  schema_version: "0.1"

  entities:
    claim.jesus_created:
      kind: Claim
      source_ref:
        file: content/questions/christology/created-being.yaml
        line: 42
        column: 5

  relationships:
    relationship.claims.created_vs_not_created:
      kind: Relationship
      type: contradicts
      from_id: claim.jesus_created
      to_id: claim.jesus_not_created
      source_ref:
        file: content/questions/christology/created-being.yaml
        line: 88
        column: 5
```

Source locations may be best-effort initially.

The normalized catalog should be deterministically ordered.

Entity ordering:

```text
kind
id
```

Relationship ordering:

```text
type
from_id
to_id
id
```

---

## Graph Projection

The graph projection is derived from the normalized catalog.

First-class `Relationship` records are canonical data.

Graph edges are generated projections.

Structural references such as `question_id`, `source_id`, `topic_ids`, and
`holder` should become derived graph edges.

First-class relationship records may also be rendered as graph edges.

Edges should record their origin.

Examples:

```text
explicit_relationship
derived_reference
```

Example:

```yaml
graph:
  nodes:
    - id: claim.jesus_created
      kind: Claim

  edges:
    - type: belongs_to
      from_id: claim.jesus_created
      to_id: question.christology.created_being
      origin: derived_reference
      derived_from: claim.jesus_created.question_id

    - id: relationship.claims.created_vs_not_created
      type: contradicts
      from_id: claim.jesus_created
      to_id: claim.jesus_not_created
      origin: explicit_relationship
```

Graph projection ordering should be deterministic.

Edge ordering:

```text
type
from_id
to_id
id
```

---

## Schema Files and Migrations

Schema files should be versioned.

Example:

```text
/schema/0.1/topic.schema.json
/schema/0.1/question.schema.json
/schema/0.1/claim.schema.json
/schema/0.1/relationship.schema.json
/schema/0.1/vocab/question-types.yaml
/schema/0.1/vocab/question-statuses.yaml
/schema/0.1/vocab/relationship-types.yaml
/schema/0.1/vocab/argument-roles.yaml
/schema/0.1/vocab/agent-types.yaml
/schema/0.1/vocab/position-stances.yaml
/schema/0.1/vocab/position-statuses.yaml
/schema/0.1/vocab/interpretation-methods.yaml
/schema/0.1/vocab/assumption-categories.yaml
/schema/0.2/topic.schema.json
```

The compiler should report the schema version and schema file used during
validation when verbose diagnostics are requested.

Migrations should be deterministic.

Migrations should be idempotent where practical.

Migration tests should compare exact output so YAML formatting and ordering
remain reviewable.

The compiler should not silently migrate data during validation or build.

---

## Diagnostics

Validation diagnostics should be precise enough for authors to fix issues
without inspecting compiler internals.

Each diagnostic should include:

```text
severity
code
message
file
entity_id
field
phase
```

Example:

```text
severity: error
code: E003
phase: references
file: content/questions/christology/created-being/claims.yaml
entity_id: claim.jesus_created
field: question_id
message: Referenced question does not exist: question.christology.created_being
```

Severity levels:

```text
error
warning
info
```

Errors make the dataset invalid and block `build`.

Warnings identify questionable, incomplete, unused, or potentially confusing
data. Warnings should not fail validation by default.

Info diagnostics provide optional author guidance.

Diagnostic codes should be stable.

Examples:

```text
E001 missing required field
E002 duplicate id
E003 invalid reference
E004 invalid controlled vocabulary value
W001 orphan node
W002 unused source
W003 missing source rights metadata
W004 unusually long quotation
W005 possible duplicate claim summary
W006 duplicate reverse edge for symmetric relationship
```

Diagnostic ordering should be deterministic.

Recommended ordering:

```text
file path
entity id
field
diagnostic code
message
```

The CLI should support both human-readable diagnostics and machine-readable JSON
diagnostics for editor tooling, CI annotations, and future UI integrations.

CI or stricter local workflows may opt into treating warnings as errors.

---

## Testing Strategy

Example datasets should double as test fixtures.

Recommended structure:

```text
/examples
/tests/fixtures
/tests/fixtures/schema/0.1/valid
/tests/fixtures/schema/0.1/invalid
/tests/fixtures/migrations/0.1-to-0.2
```

The initial apologetics dataset should serve as a canonical validation dataset.

Compiler changes should be continuously tested against these examples.

Generated outputs should be deterministic.

Diagnostic output should also be deterministic so validation tests and CI output
do not churn.

Migration output should be deterministic and covered by exact-output fixtures.

Normalized catalog and graph projection output should be deterministic.
