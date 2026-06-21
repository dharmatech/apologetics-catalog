# Validation and Compilation

## Validation Requirements

Validation should include:

* schema validation
* document envelope validation
* required field validation
* duplicate ID detection
* explicit entity ID validation
* ID format validation
* reference validation
* reference field naming validation
* relationship validation
* controlled vocabulary validation
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
* missing or invalid `kind`
* invalid relationship types
* invalid argument roles
* invalid provenance source references
* sections represented as maps keyed by ID instead of lists of records
* references to nonexistent entities
* first-class relationships whose `from_id` or `to_id` targets do not exist

The compiler should reject invalid datasets.

---

## Testing Strategy

Example datasets should double as test fixtures.

Recommended structure:

```text
/examples
/tests/fixtures
```

The initial apologetics dataset should serve as a canonical validation dataset.

Compiler changes should be continuously tested against these examples.

Generated outputs should be deterministic.
