# Validation and Compilation

## Validation Requirements

Validation should include:

* schema validation
* required field validation
* duplicate ID detection
* ID format validation
* reference validation
* relationship validation
* controlled vocabulary validation
* argument role validation
* provenance validation
* orphan node detection
* consistency checking
* first-class relationship validation

Examples:

* missing references
* duplicate identifiers
* invalid relationship types
* invalid argument roles
* invalid provenance source references
* references to nonexistent entities
* first-class relationships whose `from` or `to` targets do not exist

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
