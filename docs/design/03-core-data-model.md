# Core Data Model

Controlled field seed values and extension rules are consolidated in
[v0.1 Controlled Vocabularies](10-vocabularies.md). The initial values shown in
this document should stay consistent with that contract.

Stable entity ID rules are defined in
[v0.1 ID Conventions](12-id-conventions.md).

---

## Topic

A lightweight classification entity used to group questions.

Topics are not the primary debate container.

Questions remain the central issue being investigated.

Example:

```yaml
id: topic.christology

title: "Christology"
```

---

## Question

A topic or issue being investigated.

Questions may be classified by topic, organized into a primary hierarchy, and
linked to related questions.

Non-hierarchical question links should use first-class relationships.

Example:

```yaml
id: question.christology.created_being

title: "Is Jesus a created being?"

question_type: yes_no

status: active

topic_ids:
  - topic.christology

parent_question_id: question.christology.nature_of_christ

description: >
  Concerns whether the Son is a created being
  or eternally divine.
```

A question acts as a container for competing claims.

Initial question type values:

```text
yes_no
interpretive
historical
comparative
classificatory
open
```

Initial question status values:

```text
draft
active
deprecated
```

---

## Claim

A specific answer or assertion related to a question.

Claims represent atomic propositions.

The `summary` field is required and should be author-friendly.

The optional `proposition` field may provide a stricter formulation.

Claims may also include optional `scope` or `qualifiers` fields when the
boundaries of the proposition need clarification.

Examples:

```yaml
id: claim.jesus_created

question_id: question.christology.created_being

related_question_ids:
  - question.christology.firstborn_meaning

summary: >
  Jesus is a created being.

proposition: >
  Jesus is a member of the class of created beings.

scope:
  domain: christology

qualifiers:
  - "with respect to created ontology"
```

```yaml
id: claim.jesus_not_created

question_id: question.christology.created_being

summary: >
  Jesus is not a created being.
```

Claims represent propositions.

Questions represent the broader issue under discussion.

Claims should have one primary `question_id` initially.

Use `related_question_ids` when a claim is relevant to other questions.

Opposing answers should be modeled as separate claims.

Claim opposition, implication, dependency, narrowing, broadening, or
qualification should be represented through first-class relationships.

The model should not use a claim `polarity` field initially.

The compiler should not attempt automatic semantic deduplication of similar
claims initially.

---

## Tradition

A group, school, denomination, movement, or intellectual tradition.

Example:

```yaml
id: tradition.jehovahs_witnesses

name: "Jehovah's Witnesses"
```

---

## Agent

An entity capable of making, holding, publishing, preserving, transmitting, or
being attributed with a claim, argument, interpretation, or position.

Agents may include:

```text
person
organization
council
tradition
dataset_contributor
```

`Tradition` remains a domain concept for schools, movements, denominations, and
intellectual traditions.

`Agent` is the broader attribution and position-holder concept.

Publications are usually modeled as `Source` records rather than `Agent`
records.

A council may be modeled as an `Agent`, while a creed, canon, declaration, or
other resulting text may be modeled as a `Source`.

Example:

```yaml
id: agent.council.nicaea_325

type: council

name: "Council of Nicaea"
```

---

## Position

A stance attributed to a holder in relation to one or more claims.

The `holder` identifies who or what holds the position.

Example:

```yaml
id: position.jw.christology.created_being

holder:
  type: tradition
  id: tradition.jehovahs_witnesses

claim_stances:
  - claim_id: claim.jesus_created
    stance: affirms
    status: official
```

One position should have one holder initially.

If multiple holders share a stance, use separate positions unless a later design
introduces explicit position grouping.

Position-to-claim links should use structured `claim_stances` rather than a
plain `claim_ids` list.

Each `claim_stances` item should identify the claim, the holder's stance toward
the claim, and the attribution status.

Position attribution policy, provenance expectations, and `claim_stances.status`
guidance are defined in
[v0.1 Position Attribution](15-position-attribution.md).

Initial stance values:

```text
affirms
rejects
qualifies
permits
unclear
```

Initial status values:

```text
official
common
historical
disputed
attributed
```

A position may be supported by provenance, such as a publication, council
document, or dataset contributor's summary.

---

## Source

A work, edition, translation, manuscript, publication, council, article, book,
dataset, or other source of evidence.

A `Source` may represent either an abstract work or a concrete edition,
translation, manuscript, or publication.

Exact quotations should normally point to the concrete source whose wording is
being quoted.

Abstract sources are useful for grouping related concrete sources, but they are
not sufficient for exact quotation wording.

Scripture-specific source, locator, evidence, and quotation conventions are
defined in [v0.1 Scripture Sources](14-scripture-sources.md).

Examples:

* Biblical book or corpus
* Bible translation
* Critical text
* Manuscript
* Church council
* Church father
* Scholarly paper
* Historical document
* Lexicon

Example:

```yaml
id: source.bible.bsb

type: translation

title: "Berean Standard Bible"

work_id: source.bible

rights:
  status: copyrighted
  attribution: "Berean Standard Bible"
  url: https://bereanbible.com/
```

---

## Locator

A structured field identifying where material appears within a source.

Locators are not standalone entities initially.

Example:

```yaml
locator:
  type: verse
  value: "Colossians 1:15"
```

Common locator types may include:

```text
verse
page
section
paragraph
timestamp
canon
article
```

If reusable canonical passages or locations become necessary later, the design
may introduce a standalone `Passage` or `Location` entity.

For v0.1 Scripture modeling, biblical books and passages should remain locator
content rather than standalone `Source` or `Passage` records.

---

## Evidence

A specific piece of evidence extracted from a concrete source at a locator.

Evidence should contain the specific quoted, paraphrased, or structured material
being used, not merely a reference.

Example:

```yaml
id: evidence.bsb.colossians.1_15.firstborn

source_id: source.bible.bsb

locator:
  type: verse
  value: "Colossians 1:15"

quotation: "firstborn over all creation"
```

Multiple evidence items may originate from the same source and locator.

The same verse, page, paragraph, or timestamp may yield multiple evidence
records when different excerpts or details matter.

No separate `Citation` entity is required initially.

Citation-like references should be represented with `source_id`, `evidence_id`,
`locator`, provenance, or first-class relationships as appropriate.

---

## Interpretation

A particular reading or understanding of evidence.

An interpretation should say what evidence is taken to mean.

It should not contain the full argument or doctrinal conclusion that may be
drawn from that interpretation.

Prefer one primary `evidence_id`.

Use `related_evidence_ids` when an interpretation synthesizes multiple pieces of
evidence.

The optional `method` field identifies how the evidence is being interpreted.

Example:

```yaml
id: interpretation.jw.colossians.1_15.firstborn

evidence_id: evidence.bsb.colossians.1_15.firstborn

related_evidence_ids:
  - evidence.bsb.revelation.3_14.beginning

method: lexical

summary: >
  Firstborn is interpreted as
  first-created.
```

Initial interpretation method values:

```text
lexical
grammatical
historical
theological
textual
translation
contextual
traditional
```

Arguments should use or relate to interpretations rather than duplicating their
interpretive content.

---

## Assumption

An explicit or implicit premise required by an interpretation.

Assumptions are reusable standalone entities.

The optional `category` field identifies the kind of premise.

Example:

```yaml
id: assumption.firstborn_means_first_created

category: lexical

summary: >
  Firstborn denotes membership
  within the created order.
```

Initial assumption category values:

```text
lexical
historical
theological
methodological
textual
translation
```

Interpretations and arguments may depend upon assumptions.

Dependencies on assumptions should be represented through first-class
relationships.

---

## Stable Identifier Strategy

Identifiers should be stable, semantic, and author-chosen.

Every entity should declare its own `id` explicitly.

File paths and titles may suggest an ID, but they do not define identity.

Detailed ID rules, allowed characters, Bible-reference encoding, alias policy,
collision behavior, and rename policy are defined in
[v0.1 ID Conventions](12-id-conventions.md).

Preferred:

```text
topic.christology
question.christology.created_being
claim.jesus_created
agent.council.nicaea_325
tradition.jehovahs_witnesses
source.bible.bsb
evidence.bsb.colossians.1_15.firstborn
```

Avoid identifiers that depend upon display wording.
