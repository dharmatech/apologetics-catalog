# Relationships and Arguments

## Argument

A reasoned statement that supports, challenges, qualifies, clarifies, or
responds to another entity.

An argument performs an inferential move from evidence, interpretation, or
assumptions toward a claim or another argument.

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

Arguments should not duplicate interpretation content.

They should use or relate to interpretations through first-class relationships.

---

## Relationship

An explicit, typed connection between two entities.

Some relationships are simple structural references and may be represented
directly on the relevant node.

Examples:

```yaml
claim:
  question_id: question.christology.created_being
```

```yaml
evidence:
  source_id: source.bible.bsb
```

Argumentative or interpretive relationships should be modeled as first-class
records when they need their own provenance, explanation, qualifiers, or
validation.

Examples:

```yaml
id: relationship.jw.colossians_firstborn.supports_created

type: supports

from_id: interpretation.jw.colossians.1.15.firstborn

to_id: claim.jesus_created

summary: >
  This interpretation is used to support the claim
  that Jesus is a created being.
```

```yaml
id: relationship.trinitarian.firstborn.challenges_jw

type: challenges

from_id: argument.trinitarian.firstborn_rank

to_id: interpretation.jw.colossians.1.15.firstborn

summary: >
  The argument challenges the interpretation that
  firstborn means first-created.
```

```yaml
id: relationship.jw.firstborn_response.responds_to_rank_objection

type: responds_to

from_id: argument.jw.firstborn_created_order_response

to_id: argument.trinitarian.firstborn_rank

summary: >
  The response answers the rank or preeminence objection
  by restating the created-order reading.
```

```yaml
id: relationship.jw.created_from_firstborn.uses_interpretation

type: uses

from_id: argument.jw.created_from_firstborn

to_id: interpretation.jw.colossians.1.15.firstborn

summary: >
  The argument uses the interpretation that firstborn means first-created.
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

## Claim Relationships

Claims may relate to other claims.

Opposing claims should be separate `Claim` records connected by a first-class
relationship.

Example:

```yaml
id: relationship.claims.created_vs_not_created

type: contradicts

from_id: claim.jesus_created

to_id: claim.jesus_not_created

summary: >
  These claims cannot both be true in the same sense.
```

Other claim-to-claim relationships may include:

```text
entails
qualifies
narrows
broadens
depends_on
```

The system should use the existing first-class `Relationship` model for
claim-to-claim relationships rather than introducing a separate mechanism.

---

## Relationship Types

The system should use controlled vocabulary values.

Core author-facing relationship type values should be defined by the active
schema version. The initial v0.1 seed set and extension policy are defined in:

```text
/docs/design/10-vocabularies.md
```

Author-written `Relationship.type` values should be reserved for
argumentative, interpretive, claim-to-claim, question-to-question, dependency,
response, or other metadata-bearing connections.

Structural graph edge names such as `has_source`, `has_question`, `held_by`,
and `classified_as` may be emitted by the compiler from direct reference fields,
but they are not necessarily valid author-written `Relationship.type` values in
v0.1.

Author-facing relationship examples:

```text
supports
challenges
contradicts
entails
qualifies
narrows
broadens
depends_on
uses
responds_to
contrasts_with
related_to
interprets
```

Avoid unrestricted free-form relationship types.

Custom relationship types must be declared as vocabulary extensions before use.

Example:

```yaml
vocabulary_extensions:
  relationship_types:
    - id: project.appeals_to_liturgical_usage
      label: "Appeals to liturgical usage"
      description: >
        Used when an argument appeals to historical worship practice.
```

Argumentative relationships should usually be represented as first-class
relationship records rather than anonymous edges.

Simple structural relationships may remain as direct references when they do not
need independent provenance or explanation.

Relationship type vocabulary entries may define graph behavior and validation
metadata.

Examples:

```yaml
id: contradicts
label: "Contradicts"
symmetric: true
allowed_from:
  - Claim
allowed_to:
  - Claim
```

```yaml
id: entails
label: "Entails"
symmetric: false
inverse: entailed_by
allowed_from:
  - Claim
allowed_to:
  - Claim
```

Symmetric relationship types may eventually support diagnostics for duplicate
reverse edges.

---

## Question Relationships

Questions may have one primary parent through `parent_question_id`.

Non-hierarchical links between questions should use first-class relationships.

Example:

```yaml
id: relationship.questions.created_being.related_to_firstborn_meaning

type: related_to

from_id: question.christology.created_being

to_id: question.christology.firstborn_meaning

summary: >
  The created-being question is related to the interpretation
  of firstborn language.
```

---

## Graph Representation

The entire dataset should be representable as a graph.

Node types:

```text
Question
Topic
Claim
Position
Tradition
Agent
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
uses
responds_to
cites
interprets
belongs_to
held_by
classified_as
related_to
```

First-class relationship records may be rendered as graph edges in generated
views, but the canonical graph should preserve the relationship record and its
metadata.

Generated graph edges should identify whether they came from an explicit
first-class relationship or from a derived structural reference.

Example edge origins:

```text
explicit_relationship
derived_reference
```

This enables:

* visualization
* graph analysis
* dependency analysis
* argument exploration
* future graph databases
