# Provenance and Quotation

## Provenance

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

## Quotation Separation

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
