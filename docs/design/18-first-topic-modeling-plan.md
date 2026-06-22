# First Topic Modeling Plan

## Purpose

This document defines the first thin modeling slice for the apologetics
dataset.

The goal is not to model the whole Christology debate. The goal is to create a
small, valid, reviewable topic that exercises the core data model well enough
to drive the first compiler, validation, JSON, HTML, and graph output.

If this plan exposes missing schema or modeling features while real YAML is
being written, those features can be designed then.

---

## First Question

The first question is:

```text
Is Jesus a created being?
```

Initial ID:

```text
question.christology.created_being
```

The question should belong to:

```text
topic.christology
```

Keep this first question narrow. Do not broaden the first slice into a general
model of Christology, the Trinity, incarnation, eternal generation, or every
historical controversy about the Son.

---

## First Claims

Start with two opposing claims:

```text
claim.jesus_created
claim.jesus_uncreated
```

Draft summaries:

```text
Jesus is a created being.
Jesus is not a created being.
```

Connect them with:

```text
relationship.created.contradicts_uncreated
```

Relationship type:

```text
contradicts
```

Qualified claims can be added later if needed.

Examples:

```text
Jesus is first-created.
Jesus is eternally begotten, not made.
Jesus is the agent through whom creation came to be.
```

Do not add these until the first two-claim contrast validates and renders
cleanly.

---

## First Positions

Start with two positions:

```text
position.jw.christology.created_being
position.nicene.christology.uncreated
```

Initial holders:

```text
tradition.jehovahs_witnesses
tradition.nicene_trinitarian
```

The Jehovah's Witnesses position should affirm:

```text
claim.jesus_created
```

The Nicene Trinitarian position should affirm:

```text
claim.jesus_uncreated
```

It may also reject:

```text
claim.jesus_created
```

Use conservative `claim_stances.status` values according to
[v0.1 Position Attribution](15-position-attribution.md).

For the first pass, use only the Jehovah's Witnesses and Nicene Trinitarian
positions. Defer Arian modeling until the basic contrast validates and the graph
is readable.

---

## Deferred Arian Modeling

Arian modeling is important but should not be part of the first thin slice.

Reasons:

* historical attribution is more complex
* source evidence may be fragmentary or mediated
* position status may require `historical`, `attributed`, or `disputed`
* adding it immediately may obscure whether the basic model works

After the first two-position slice works, Arian modeling can be added as the
first historical-extension pass.

---

## First Scripture Slice

Start with Colossians 1:15.

Use the Scripture conventions in
[v0.1 Scripture Sources](14-scripture-sources.md).

Initial concrete source:

```text
source.bible.bsb
```

Initial abstract source:

```text
source.bible
```

Initial evidence:

```text
evidence.bsb.colossians.1_15.firstborn
```

Locator:

```yaml
locator:
  type: verse
  value: "Colossians 1:15"
```

Keep quotation text short and source-specific.

Do not model every relevant passage in the first pass. John 1:1, John 1:3,
Colossians 1:15-17, Revelation 3:14, Proverbs 8:22, Hebrews 1:3, Hebrews 1:6,
and Philippians 2:6-11 remain in initial scope, but only Colossians 1:15 is
required for the first thin slice.

---

## First Attribution Sources

The first pass should include placeholder source IDs for position attribution
shape, but the exact real-world sources can be selected when the dataset is
created.

Initial placeholder IDs:

```text
source.publication.jw.official_christology_summary
source.creed.nicene.trinitarian_summary
```

Before the dataset is considered complete, these placeholders should be
replaced with real source records or renamed before publication.

The design plan should not turn into bibliography research. It should define
the shape of the first slice.

---

## First Interpretations

Model interpretations before building a larger argument tree.

Initial interpretation IDs:

```text
interpretation.jw.colossians.1_15.firstborn_created_order
interpretation.nicene.colossians.1_15.firstborn_preeminence
```

Draft neutral summaries:

```text
The phrase firstborn over all creation is read as placing the Son within the
created order.
```

```text
The phrase firstborn over all creation is read as indicating rank or
preeminence rather than created status.
```

These are dataset-authored summaries unless sourced wording is added through
provenance or evidence.

---

## First Relationships

The first graph should include these relationship types:

```text
supports
challenges
contradicts
```

Initial relationship targets:

```text
interpretation.jw.colossians.1_15.firstborn_created_order
  supports claim.jesus_created

interpretation.nicene.colossians.1_15.firstborn_preeminence
  supports claim.jesus_uncreated

interpretation.nicene.colossians.1_15.firstborn_preeminence
  challenges interpretation.jw.colossians.1_15.firstborn_created_order

claim.jesus_created
  contradicts claim.jesus_uncreated
```

Exact relationship IDs can be chosen when the YAML is written, following
[v0.1 ID Conventions](12-id-conventions.md).

---

## First Pass Success Criteria

The first topic is modeled enough when validation and generated outputs can show
all of the following:

* one topic
* one question
* two opposing claims
* two positions
* one contradiction relationship between the claims
* one abstract Bible source
* one concrete Bible translation source with rights metadata
* one short Colossians 1:15 evidence record
* one Jehovah's Witnesses interpretation of `firstborn`
* one Nicene Trinitarian interpretation of `firstborn`
* support and challenge relationships connecting interpretations and claims
* minimal attribution provenance for each position
* no orphaned records in the thin slice

The graph should make the basic contrast understandable without embedding a
truth judgment.

---

## Out of Scope for the First Pass

Do not include these in the first modeling pass:

* full Arian historical modeling
* every relevant Scripture passage
* Greek lexical detail
* Hebrew Wisdom tradition analysis
* all Bible translations
* exhaustive Watch Tower bibliography
* exhaustive Nicene source history
* detailed doctrine of eternal generation
* formal truth evaluation
* confidence scoring
* source reliability scoring
* UI polish

These can be added after the first slice validates, compiles, and renders.

---

## Fixture Target

The first topic should eventually double as a canonical example dataset and
validation fixture.

It should be small enough that expected JSON, HTML, and graph output can be
reviewed by humans.

When compiler behavior changes, this fixture should help reveal whether core
modeling behavior changed intentionally.
