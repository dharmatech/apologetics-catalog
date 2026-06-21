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
