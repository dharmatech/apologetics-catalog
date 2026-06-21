# Validation and Compilation

## Validation Phases

Validation should be layered.

Recommended phases:

```text
parse
envelope
schema
vocabulary
identity
references
graph
outputs
```

The parser phase loads YAML and reports syntax errors.

The envelope phase validates document-level fields such as `schema_version` and
`kind`, including whether the declared schema version is supported.

The schema phase validates each entity's required fields and local structure
against the schema files for the declared schema version.

The vocabulary phase validates controlled values such as relationship types and
argument roles. It should validate core values and declared project-level
extensions.

The identity phase validates entity IDs, detects duplicate IDs, and confirms
that every entity declares its own stable `id`.

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

* schema validation
* document envelope validation
* schema version validation
* required field validation
* duplicate ID detection
* explicit entity ID validation
* ID format validation
* reference validation
* reference field naming validation
* relationship validation
* controlled vocabulary validation
* vocabulary extension declaration validation
* unknown vocabulary value validation
* argument role validation
* provenance validation
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
* unknown vocabulary values without explicit extension declarations
* malformed vocabulary extension declarations
* invalid argument roles
* invalid provenance source references
* sections represented as maps keyed by ID instead of lists of records
* references to nonexistent entities
* first-class relationships whose `from_id` or `to_id` targets do not exist

The compiler should reject invalid datasets.

---

## Schema Files and Migrations

Schema files should be versioned.

Example:

```text
/schema/0.1/topic.schema.json
/schema/0.1/claim.schema.json
/schema/0.1/relationship.schema.json
/schema/0.1/vocab/relationship-types.yaml
/schema/0.1/vocab/argument-roles.yaml
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
