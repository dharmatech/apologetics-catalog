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

## Argument

A reasoned statement that supports, challenges, qualifies, clarifies, or
responds to another entity.

Arguments subsume objections, counter-objections, rebuttals, supporting
arguments, qualifications, and other moves in an argumentative exchange.

Example:

```yaml
id: argument.trinitarian.firstborn_rank

role: objection

summary: >
  Firstborn frequently indicates
  rank or preeminence.
```

Example:

```yaml
id: argument.jw.firstborn_created_order_response

role: response

summary: >
  The phrase firstborn of all creation is read as placing
  the Son within the created order.
```

Common argument roles:

```text
support
objection
response
rebuttal
qualification
clarification
```

Arguments may target claims, interpretations, assumptions, evidence, or other
arguments.

Argument targets should usually be represented through first-class relationship
records so that the support, challenge, qualification, or response can preserve
its own metadata.

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

from: argument.trinitarian.firstborn_rank

to: interpretation.jw.colossians.firstborn

summary: >
  The argument challenges the interpretation that
  firstborn means first-created.
```

```yaml
id: relationship.jw.firstborn_response.responds_to_rank_objection

type: responds_to

from: argument.jw.firstborn_created_order_response

to: argument.trinitarian.firstborn_rank

summary: >
  The response answers the rank or preeminence objection
  by restating the created-order reading.
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

Interpretations, arguments, relationships, and other derived statements should
support structured provenance metadata.

The system should distinguish:

```text
Source        original document, artifact, or text
Evidence      extracted material from a source
Interpretation derived reading of evidence
Argument      reasoned statement made by an author, group, or tradition
Relationship  assertion that one entity supports, challenges, qualifies, or
              responds to another entity
Provenance    attribution for a derived statement or relationship
```

Provenance should not replace `Source` or `Evidence`.

Instead, provenance records who made, preserved, published, summarized, or
transmitted a derived statement.

Example:

```yaml
provenance:

  attributed_to:
    type: author
    name: Example Author

  work:
    source: source.publication.example_work
    title: Example Publication

  date: 2026

  locator:
    type: page
    value: "42"

  url: https://example.org/example-work

  accessed: 2026-06-21
```

The purpose of provenance is to distinguish:

* what a source says
* who made a particular interpretation
* who made a particular argument
* who asserted a relationship between entities
* where a derived statement originated

Common provenance fields:

```text
attributed_to
work
date
locator
url
accessed
edition
language
```

The `attributed_to` value may identify an author, editor, translator,
organization, tradition, council, school, or dataset contributor.

The `locator` value should identify the relevant page, section, paragraph,
verse, timestamp, canon, article, or other location within the cited work.

When a provenance record cites a work already represented as a `Source`, it
should reference that source by stable identifier.

When the provenance belongs to a dataset author's summary, the attribution
should make that clear rather than implying the wording came directly from the
original source.

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
Argument
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
