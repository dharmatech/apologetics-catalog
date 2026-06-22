# Provenance and Quotation

Scripture-specific quotation, translation, locator, and rights conventions are
defined in [v0.1 Scripture Sources](14-scripture-sources.md).

## Provenance

Interpretations, arguments, relationships, and other derived statements should
support structured provenance metadata.

The system should distinguish:

```text
Source        work, edition, translation, manuscript, publication, or dataset
Locator       location within a source, such as verse, page, or timestamp
Evidence      extracted material from a concrete source at a locator
Interpretation derived reading of evidence
Argument      reasoned statement made by an author, group, or tradition
Relationship  assertion that one entity supports, challenges, qualifies, or
              responds to another entity
Provenance    attribution for a derived statement or relationship
```

Provenance should not replace `Source` or `Evidence`.

Instead, provenance records who made, preserved, published, summarized, or
transmitted a derived statement.

Provenance may include a `locator` when citing a specific page, section,
paragraph, verse, timestamp, or other location within a work.

Example:

```yaml
provenance:

  attributed_to:
    type: author
    name: Example Author

  work:
    source_id: source.publication.example_work
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

The `attributed_to` value may identify or reference an `Agent`, such as an
author, editor, translator, organization, tradition, council, school, or dataset
contributor.

The `locator` value should identify the relevant page, section, paragraph,
verse, timestamp, canon, article, or other location within the cited work.

When a provenance record cites a work already represented as a `Source`, it
should reference that source by stable identifier.

When the provenance belongs to a dataset author's summary, the attribution
should make that clear rather than implying the wording came directly from the
original source.

---

## Source Rights

Sources may include rights and licensing metadata.

Example:

```yaml
rights:
  status: public_domain
  license: CC0
  attribution: "Example Source"
  url: https://example.org/rights
```

Rights metadata may vary by source, edition, translation, or publication.

For exact quotations, the evidence should cite the concrete source whose wording
is quoted, because rights and attribution requirements may differ between
editions or translations.

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

Exact quotations should cite the concrete source, edition, translation, or
publication whose wording is being quoted.

Example:

```yaml
source_id: source.bible.bsb

locator:
  type: verse
  value: "Colossians 1:15"

quotation: "firstborn over all creation"
```

Avoid attaching exact quotation text to an abstract source when the wording
comes from a specific edition or translation.

Evidence quotations should be as short as practical.

Generated outputs may eventually need quote-length, rights, or attribution
rules.

For Scripture evidence, exact quotations should point to the concrete
translation, edition, or original-language source whose wording is quoted.
