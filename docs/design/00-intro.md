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
* objections
* counter-objections
* provenance
* relationships

in a machine-readable form that can be validated, queried, visualized, analyzed, and transformed into multiple output formats.

---

# Core Philosophy

The system should model:

> What does Position X claim?

rather than:

> Which position is true?

Truth evaluation, confidence scoring, ranking, or other evaluative mechanisms may be added in the future as separate layers.

The foundational model should remain descriptive rather than prescriptive.

---

# Long-Term Vision

Although initially developed using apologetics and theology as the first domain, the architecture should be sufficiently general to represent:

* theology
* philosophy
* history
* law
* science
* politics
* competing scholarly interpretations
* competing explanations of evidence

The architecture should be domain-neutral.

The domain-specific content should reside entirely in the data.

---

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

## Generated Outputs

Generated artifacts may include:

```text
/generated/json
/generated/html
/generated/markdown
/generated/python
/generated/typescript
/generated/graph
```

Future targets may include:

```text
/generated/ocaml
/generated/haskell
/generated/lean
```

Generated outputs are derived artifacts.

They are not authoritative.

The YAML source remains the canonical representation.

---

# Versioning

All datasets and schemas should include explicit version information.

Example:

```yaml
schema_version: 0.1
```

Future schema changes should support migrations where practical.

---

# Core Data Model

## Question

A topic or issue being investigated.

Example:

```yaml
id: question.christology.created_being

title: "Is Jesus a created being?"
```

A question acts as a container for competing claims.

---

## Claim

A specific answer or assertion related to a question.

Examples:

```yaml
id: claim.jesus_created

question:
  question.christology.created_being

summary: >
  Jesus is a created being.
```

```yaml
id: claim.jesus_not_created

question:
  question.christology.created_being

summary: >
  Jesus is not a created being.
```

Claims represent propositions.

Questions represent the broader issue under discussion.

---

## Position

A tradition, school, group, or author's support for one or more claims.

Example:

```yaml
id: position.jw.christology

tradition:
  tradition.jehovahs_witnesses
```

A position may support multiple claims.

---

## Tradition

A group, school, denomination, movement, or intellectual tradition.

Example:

```yaml
id: tradition.jehovahs_witnesses

name: "Jehovah's Witnesses"
```

---

## Source

A document, verse, manuscript, publication, council, article, book, or other original source.

Examples:

* Scripture passage
* Church council
* Church father
* Scholarly paper
* Historical document
* Lexicon

Example:

```yaml
id: source.scripture.colossians.1.15

type: scripture

reference: "Colossians 1:15"
```

---

## Evidence

A specific piece of evidence extracted from a source.

Example:

```yaml
id: evidence.colossians.firstborn

source:
  source.scripture.colossians.1.15

quotation: "firstborn of all creation"
```

Multiple evidence items may originate from the same source.

---

## Interpretation

A particular reading or understanding of evidence.

Example:

```yaml
id: interpretation.jw.colossians.firstborn

evidence:
  evidence.colossians.firstborn

summary: >
  Firstborn is interpreted as
  first-created.
```

---

## Assumption

An explicit or implicit premise required by an interpretation.

Example:

```yaml
id: assumption.firstborn_means_first_created

summary: >
  Firstborn denotes membership
  within the created order.
```

Interpretations may depend upon assumptions.

---

## Objection

A challenge directed at a claim, interpretation, or assumption.

Example:

```yaml
id: objection.trinitarian.firstborn

targets:
  - interpretation.jw.colossians.firstborn

summary: >
  Firstborn frequently indicates
  rank or preeminence.
```

---

## Counter-Objection

A response to an objection.

Example:

```yaml
id: counter.jw.firstborn

targets:
  - objection.trinitarian.firstborn
```

---

## Relationship

An explicit, typed connection between two entities.

Some relationships are simple structural references and may be represented
directly on the relevant node.

Examples:

```yaml
claim:
  question: question.christology.created_being
```

```yaml
evidence:
  source: source.scripture.colossians.1.15
```

Argumentative or interpretive relationships should be modeled as first-class
records when they need their own provenance, explanation, qualifiers, or
validation.

Examples:

```yaml
id: relationship.jw.colossians_firstborn.supports_created

type: supports

from: interpretation.jw.colossians.firstborn

to: claim.jesus_created

summary: >
  This interpretation is used to support the claim
  that Jesus is a created being.
```

```yaml
id: relationship.trinitarian.firstborn.challenges_jw

type: challenges

from: objection.trinitarian.firstborn

to: interpretation.jw.colossians.firstborn

summary: >
  The objection challenges the interpretation that
  firstborn means first-created.
```

First-class relationships allow the system to distinguish:

* the entities being related
* the type of relationship
* who asserts or explains the relationship
* where that assertion originated
* any qualifications or limits on the relationship

Structural references should remain lightweight.

Argumentative relationships should preserve their own metadata.

---

# Provenance

Interpretations, objections, and other derived statements should support provenance metadata.

Example:

```yaml
provenance:

  source_type: publication

  title: Example Publication

  author: Example Author

  date: 2026

  url: https://example.org
```

The purpose of provenance is to distinguish:

* what a source says
* who made a particular interpretation
* where that interpretation originated

---

# Quotation Separation

The system should distinguish between:

```yaml
quotation:
```

Original source text.

```yaml
paraphrase:
```

Restatement of source content.

```yaml
commentary:
```

Human explanation or interpretation.

These should never be conflated.

---

# Relationship Types

The system should use controlled vocabulary values.

Structural relationship examples:

```text
belongs_to
cites
has_source
has_question
has_tradition
```

Argumentative or interpretive relationship examples:

```text
supports
challenges
qualifies
depends_on
responds_to
contrasts_with
interprets
appeals_to_translation
appeals_to_context
appeals_to_language
appeals_to_history
appeals_to_tradition
```

Avoid unrestricted free-form relationship types.

Argumentative relationships should usually be represented as first-class
relationship records rather than anonymous edges.

Simple structural relationships may remain as direct references when they do not
need independent provenance or explanation.

---

# Validation Requirements

Validation should include:

* schema validation
* required field validation
* duplicate ID detection
* ID format validation
* reference validation
* relationship validation
* controlled vocabulary validation
* orphan node detection
* consistency checking
* first-class relationship validation

Examples:

* missing references
* duplicate identifiers
* invalid relationship types
* references to nonexistent entities
* first-class relationships whose `from` or `to` targets do not exist

The compiler should reject invalid datasets.

---

# Stable Identifier Strategy

Identifiers should be stable and semantic.

Preferred:

```text
question.christology.created_being
claim.jesus_created
source.scripture.colossians.1.15
```

Avoid identifiers that depend upon display wording.

---

# Strongly Typed Future

YAML is the authoring format.

The architecture should permit generation of strongly typed representations.

Potential targets:

* Python
* TypeScript
* OCaml
* Haskell
* Lean

The design should not assume any particular implementation language.

---

# Graph Representation

The entire dataset should be representable as a graph.

Node types:

```text
Question
Claim
Position
Tradition
Source
Evidence
Interpretation
Assumption
Objection
CounterObjection
Relationship
```

Edge types:

```text
supports
challenges
depends_on
responds_to
cites
interprets
belongs_to
```

First-class relationship records may be rendered as graph edges in generated
views, but the canonical graph should preserve the relationship record and its
metadata.

This enables:

* visualization
* graph analysis
* dependency analysis
* argument exploration
* future graph databases

---

# Testing Strategy

Example datasets should double as test fixtures.

Recommended structure:

```text
/examples
/tests/fixtures
```

The initial apologetics dataset should serve as a canonical validation dataset.

Compiler changes should be continuously tested against these examples.

Generated outputs should be deterministic.

---

# Command-Line Interface

Initial commands:

```text
validate
build
graph
query
```

These commands should remain simple and implementation-independent.

---

# Initial Scope

The first implementation should focus on a single question:

```text
Is Jesus a created being?
```

Initial sources:

* John 1:1
* John 1:3
* Colossians 1:15–17
* Revelation 3:14
* Proverbs 8:22
* Hebrews 1:3
* Hebrews 1:6
* Philippians 2:6–11

Initial positions:

* Jehovah's Witness
* Arian
* Nicene Trinitarian

Initial deliverables:

* YAML dataset
* schema validation
* compiler prototype
* JSON generation
* HTML generation
* graph visualization
* command-line query interface

---

# Success Criteria

The project should successfully model competing interpretations of evidence without embedding truth judgments into the core data model.

The architecture should remain sufficiently general that the same schema can later represent non-theological domains without requiring fundamental redesign.
