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

question_id: question.christology.created_being

summary: >
  Jesus is a created being.
```

```yaml
id: claim.jesus_not_created

question_id: question.christology.created_being

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

tradition_id: tradition.jehovahs_witnesses

claim_ids:
  - claim.jesus_created
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

A work, edition, translation, manuscript, publication, council, article, book,
dataset, or other source of evidence.

A `Source` may represent either an abstract work or a concrete edition,
translation, manuscript, or publication.

Exact quotations should normally point to the concrete source whose wording is
being quoted.

Abstract sources are useful for grouping related concrete sources, but they are
not sufficient for exact quotation wording.

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

---

## Evidence

A specific piece of evidence extracted from a concrete source at a locator.

Evidence should contain the specific quoted, paraphrased, or structured material
being used, not merely a reference.

Example:

```yaml
id: evidence.colossians.1.15.firstborn

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

Example:

```yaml
id: interpretation.jw.colossians.1.15.firstborn

evidence_id: evidence.colossians.1.15.firstborn

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

## Stable Identifier Strategy

Identifiers should be stable and semantic.

Every entity should declare its own `id` explicitly.

File paths and titles may suggest an ID, but they do not define identity.

Preferred:

```text
question.christology.created_being
claim.jesus_created
source.bible.bsb
evidence.colossians.1.15.firstborn
```

Avoid identifiers that depend upon display wording.
