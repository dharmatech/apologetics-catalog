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

source_id: source.scripture.colossians.1.15

quotation: "firstborn of all creation"
```

Multiple evidence items may originate from the same source.

---

## Interpretation

A particular reading or understanding of evidence.

Example:

```yaml
id: interpretation.jw.colossians.firstborn

evidence_id: evidence.colossians.firstborn

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
source.scripture.colossians.1.15
```

Avoid identifiers that depend upon display wording.
