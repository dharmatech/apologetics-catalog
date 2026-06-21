# Architecture

## Canonical Source Format

Human-authored YAML files.

Example:

```text
/content
```

The YAML files represent the source of truth.

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
