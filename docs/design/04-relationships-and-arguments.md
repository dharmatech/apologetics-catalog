# Relationships and Arguments

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
  question_id: question.christology.created_being
```

```yaml
evidence:
  source_id: source.scripture.colossians.1.15
```

Argumentative or interpretive relationships should be modeled as first-class
records when they need their own provenance, explanation, qualifiers, or
validation.

Examples:

```yaml
id: relationship.jw.colossians_firstborn.supports_created

type: supports

from_id: interpretation.jw.colossians.firstborn

to_id: claim.jesus_created

summary: >
  This interpretation is used to support the claim
  that Jesus is a created being.
```

```yaml
id: relationship.trinitarian.firstborn.challenges_jw

type: challenges

from_id: argument.trinitarian.firstborn_rank

to_id: interpretation.jw.colossians.firstborn

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

First-class relationships allow the system to distinguish:

* the entities being related
* the type of relationship
* who asserts or explains the relationship
* where that assertion originated
* any qualifications or limits on the relationship

Structural references should remain lightweight.

Argumentative relationships should preserve their own metadata.

---

## Relationship Types

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

## Graph Representation

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
