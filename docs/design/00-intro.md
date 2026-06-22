# Apologetics Viewpoint Catalog

## Introductory Design Document (v0.1)

### Status

Draft

### Purpose

Create a neutral, structured system for cataloging competing viewpoints regarding theological, apologetic, philosophical, historical, legal, scientific, and other interpretive questions.

The system is not intended to determine which position is correct.

Instead, it is intended to represent:

* questions
* claims
* positions
* evidence
* interpretations
* assumptions
* arguments
* provenance
* relationships

in a machine-readable form that can be validated, queried, visualized, analyzed, and transformed into multiple output formats.

### Design Documents

* [Core Philosophy and Vision](01-core-philosophy.md)
* [Architecture](02-architecture.md)
* [Core Data Model](03-core-data-model.md)
* [Relationships and Arguments](04-relationships-and-arguments.md)
* [Provenance and Quotation](05-provenance-and-quotation.md)
* [Validation and Compilation](06-validation-and-compilation.md)
* [Generated Outputs and CLI](07-outputs-and-cli.md)
* [Initial Scope and Success Criteria](08-initial-scope.md)
* [v0.1 YAML Authoring Schema](09-v0.1-schema.md)
* [v0.1 Controlled Vocabularies](10-vocabularies.md)
* [v0.1 Modeling Guidelines](11-modeling-guidelines.md)
* [v0.1 ID Conventions](12-id-conventions.md)
* [v0.1 Project Manifest](13-project-manifest.md)

### Overview

The canonical source format is human-authored YAML.

For authoring convenience, YAML content may be grouped by topic or question.

The YAML files are treated as source code. A compiler/validator checks the source data, constructs the graph, and generates derived outputs.

The foundational model is descriptive rather than prescriptive. It models what a position claims, how evidence is interpreted, and how arguments relate to one another without embedding truth judgments into the core data model.

The initial implementation focuses on a single apologetics question:

```text
Is Jesus a created being?
```

The architecture should remain sufficiently general that the same schema can later represent non-theological domains without requiring fundamental redesign.
