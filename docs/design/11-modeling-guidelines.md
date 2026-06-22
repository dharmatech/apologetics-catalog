# v0.1 Modeling Guidelines

## Purpose

This document defines practical authoring rules for turning real apologetics
material into v0.1 records.

It does not add new entity types. It explains how to use the existing schema,
controlled vocabularies, provenance model, and relationship model consistently
when building the first dataset.

The goal is a faithful minimal model, not an exhaustive apologetics encyclopedia.

Stable ID choices should follow
[v0.1 ID Conventions](12-id-conventions.md).

Scripture passage modeling should follow
[v0.1 Scripture Sources](14-scripture-sources.md).

Position attribution should follow
[v0.1 Position Attribution](15-position-attribution.md).

Provenance object shape and validation rules should follow
[v0.1 Provenance Conventions](17-provenance-conventions.md).

---

## Authoring Posture

The catalog should describe positions, evidence, interpretations, assumptions,
arguments, and relationships without deciding which position is true.

Author-written summaries should be neutral.

Avoid evaluative wording unless it is part of a quotation.

Avoid words such as:

```text
proves
disproves
clearly
obviously
misreads
refutes
merely
```

Prefer wording such as:

```text
is used to support
is read as
is understood by
is challenged by
is taken to imply
```

Example:

```yaml
summary: >
  This interpretation is used to support the claim that the Son belongs to the
  created order.
```

Do not write:

```yaml
summary: >
  This verse clearly proves that the Son is created.
```

---

## Source Wording and Dataset Wording

Keep source wording separate from dataset wording.

Use `quotation` only for exact source text.

Use `paraphrase` for a restatement of source content.

Use `summary` for dataset-authored descriptions of claims, interpretations,
arguments, relationships, or positions.

Use provenance when a summary is attributed to a source, tradition, author, or
dataset contributor.

Example:

```yaml
evidence:
  id: evidence.bsb.colossians.1_15.firstborn
  source_id: source.bible.bsb
  locator:
    type: verse
    value: "Colossians 1:15"
  quotation: "firstborn over all creation"
```

Example dataset wording:

```yaml
interpretation:
  id: interpretation.jw.colossians.1_15.firstborn_created_order
  evidence_id: evidence.bsb.colossians.1_15.firstborn
  method: lexical
  summary: >
    The phrase firstborn over all creation is read as placing the Son within
    the created order.
```

The interpretation summary should not pretend to be a quotation from the source
unless it is explicitly quoted as evidence.

---

## Atomic Records

Prefer small atomic records.

A `Claim` should usually express one proposition.

An `Interpretation` should usually express one reading of one evidence item or
closely related evidence group.

An `Argument` should usually express one recognizable argumentative move.

An `Assumption` should usually express one reusable premise.

Do not create separate records merely because a paragraph has multiple
sentences. Split records when the distinction matters for stance, provenance,
method, evidence, or relationships.

---

## Granularity Escalation

Start coarse and split only when the data needs it.

Use these rules:

* Start with one `Claim` for the main proposition.
* Split claims when different positions affirm, reject, or qualify different
  parts.
* Start with one `Interpretation` per passage per position.
* Split interpretations when they use materially different methods, evidence,
  or conclusions.
* Start with one `Argument` per recognizable argumentative move.
* Split arguments when they need different provenance, respond to different
  objections, or support different targets.
* Use first-class `Relationship` records when the connection needs provenance,
  explanation, or a specific relationship type.

Granularity can increase as the dataset matures. v0.1 should prioritize a
clear, valid, reviewable first slice.

---

## Representative-First Modeling

The initial dataset should model representative arguments first.

It should not try to capture every variant, sub-argument, or historical
development at the start.

For each major position, prefer:

* one clear position record
* one or two central claims
* a small set of representative passages or sources
* one interpretation per representative passage where useful
* one or two core arguments
* explicit relationships connecting the pieces

Later iterations can add more sources, finer distinctions, and historical
variants.

---

## Symmetrical Treatment

Major positions should receive comparable treatment when possible.

For the initial question, this means Jehovah's Witnesses, Arian, and Nicene
Trinitarian positions should each have enough modeled structure to be
understandable.

Comparable treatment does not mean identical record counts.

It means each major position should avoid being represented as a bare label or
unsupported stance while other positions receive detailed arguments and
evidence.

---

## Negative Modeling

Do not create denial records for every proposition a position rejects.

Use `claim_stances` with `stance: rejects` when a position directly rejects an
existing claim.

Create a positive counter-claim when the denial is central and needs its own
evidence, interpretation, or argumentation.

Use `contradicts` or `challenges` relationships when opposition between claims,
interpretations, arguments, or positions matters.

Example:

```yaml
claims:
  - id: claim.jesus_created
    question_id: question.christology.created_being
    summary: >
      Jesus is a created being.

  - id: claim.jesus_uncreated
    question_id: question.christology.created_being
    summary: >
      Jesus is not a created being.

relationships:
  - id: relationship.created.contradicts_uncreated
    type: contradicts
    from_id: claim.jesus_created
    to_id: claim.jesus_uncreated
```

Avoid modeling strawman claims merely because one position rejects them.

---

## Dataset-Author Synthesis

Some summaries will be written by the dataset author as a synthesis of a
tradition, position, source, or argument.

That is acceptable, but the provenance should be clear.

If wording comes directly from a source, model it as evidence with `quotation`.

If wording is the dataset author's neutral restatement, make that clear through
the record's role and, where useful, provenance.

Example:

```yaml
provenance:
  attributed_to:
    type: dataset_contributor
    name: "Dataset author"
  work:
    title: "Apologetics Viewpoint Catalog"
```

Do not imply that dataset-authored summaries are direct statements from a
tradition, council, author, or source unless the evidence supports that
attribution.

---

## Minimal Passage Workflow

For each passage or source excerpt, model the vertical slice in this order:

```text
Source -> Evidence -> Interpretation -> Argument or Relationship -> Claim -> Position
```

For Scripture passages, the `Source` should be a concrete translation, edition,
or original-language text, not the abstract Bible source.

Practical steps:

1. Create or reuse a concrete `Source`.
2. Create `Evidence` with a locator and exact quotation, paraphrase, or data.
3. Create one `Interpretation` for how a position reads the evidence.
4. Create an `Argument` when there is a distinct argumentative move beyond the
   interpretation itself.
5. Connect the interpretation or argument to a claim with a first-class
   `Relationship`.
6. Connect the holder to the claim through a `Position` and `claim_stances`.

Arguments should not duplicate interpretation content. They should use
relationships to connect interpretations, assumptions, evidence, claims, and
other arguments.

---

## Minimum Completeness for a Position

A position is minimally modeled in v0.1 when it has:

* a `Position` record with one holder
* at least one `claim_stances` item
* at least one attribution source, clear position provenance, or explicit
  dataset-author synthesis
* at least one relevant `Evidence` record or clear source used by the position
* at least one `Interpretation` or `Argument` explaining how the evidence or
  provenance connects to the claim
* at least one first-class `Relationship` connecting the explanatory material
  to the claim, argument, or interpretation
* neutral summary wording
* no orphaned claims, evidence, interpretations, assumptions, or arguments in
  that modeled slice

This checklist does not require exhaustive treatment. It prevents a position
from being represented only as a label or unsupported stance.

---

## Initial Colossians 1:15 Slice

The first worked slice can start with Colossians 1:15.

Minimal records may include:

```text
Source:
  concrete Bible translation

Evidence:
  Colossians 1:15 quotation or paraphrase

Interpretation:
  Jehovah's Witnesses reading of "firstborn"
  Nicene Trinitarian reading of "firstborn"

Claims:
  Jesus is a created being
  Jesus is not a created being

Positions:
  Jehovah's Witnesses stance toward the created-being claim
  Nicene Trinitarian stance toward the created-being claim

Relationships:
  interpretation supports claim
  interpretation challenges claim
  claim contradicts claim
```

This is only a starting outline. Additional passages, Arian historical
positioning, source provenance, assumptions, and arguments can be added after
the first slice validates cleanly.
