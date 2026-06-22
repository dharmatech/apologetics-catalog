# v0.1 Bibliography Sources

## Purpose

This document defines v0.1 conventions for non-Scripture sources.

It covers official publications, creeds, council documents, books, articles,
web pages, historical sources, and secondary historical reconstructions.

Provenance object shape and validation rules are defined in
[v0.1 Provenance Conventions](17-provenance-conventions.md).

It does not add source quality scoring or reliability ranking. Source quality
and evaluation can be modeled later as a separate layer if needed.

---

## Core Principle

Use `Source.type` to describe what the source is.

Use `Evidence`, `Interpretation`, `Argument`, `Relationship`, and
`Position.provenance` to show how the source is being used.

Do not add a global source-role field in v0.1.

The same source may be:

* an attribution source for one position
* evidence used by an argument elsewhere
* a secondary summary for one historical question
* a primary source for another question

Source roles are contextual, not intrinsic.

---

## Abstract Works and Concrete Sources

Use an abstract `Source` only when it helps group concrete versions of the same
work.

Use concrete `Source` records for the edition, translation, web page, article,
scan, publication, or version actually cited.

Use `work_id` to connect a concrete source to an abstract work.

Example:

```yaml
sources:
  - id: source.creed.nicaea
    type: creed
    title: "Nicene Creed"
    date: 325

  - id: source.creed.nicaea.example_translation
    type: creed
    title: "Nicene Creed, Example Translation"
    work_id: source.creed.nicaea
    language: en
    description: >
      Concrete translation or publication used for quotation.
```

Do not quote from abstract sources.

Exact quotations should cite the concrete source whose wording is being quoted.

---

## Source Identity and Editions

Create separate concrete sources when wording, rights, date, URL, edition,
translation, or locator scheme differs materially.

Examples:

```text
source.book.example_work
source.book.example_work.second_edition
source.article.example_journal_2024
source.web.jw.example_article_2026_06_21
source.creed.nicaea.example_translation
```

For web pages, the concrete source is the page at the URL as accessed.

For books, the concrete source should identify the edition, language, and date
when known.

For creeds and council documents, the abstract source may represent the creed,
canon, or document, while the concrete source represents the edition,
translation, publication, or page being quoted.

---

## Minimum Metadata by Source Type

The base schema requires:

```text
id
type
title
```

The following v0.1 metadata conventions should guide authoring.

### Web Page

Recommended fields:

```text
id
type: web_page
title
url
accessed
rights, when quoting
```

Example:

```yaml
id: source.web.example.official_article
type: web_page
title: "Example Official Article"
url: https://example.org/article
accessed: 2026-06-22
description: >
  Official publication page used for position attribution.
```

### Book

Recommended fields:

```text
id
type: book
title
author, when known
date, when known
edition, when known
language, when known
rights, when quoting
```

Publisher or series details may be recorded in `description` until the schema
adds more bibliographic fields.

### Article

Recommended fields:

```text
id
type: article
title
author, when known
date, when known
url, when online
accessed, when online
language, when known
rights, when quoting
```

Journal, volume, issue, or publication details may be recorded in `description`
until the schema adds more bibliographic fields.

### Creed or Council Document

Recommended fields:

```text
id
type: creed or council_document
title
date, when known
language, when known
edition, when using a concrete edition or translation
url, when online
accessed, when online
rights, when quoting
```

Model the council itself as an `Agent` when needed.

Model the creed, canon, declaration, or document as a `Source`.

### Official Publication

Use the concrete format type:

```text
web_page
book
article
council_document
```

Do not create a separate `official_publication` source type in v0.1.

Explain official or representative status in `description` or in the
`Position.provenance` that uses the source.

### Historical Reconstruction Source

Historical reconstruction sources are usually books, articles, commentaries, or
web pages.

Use the concrete source type and explain the reconstruction role in
`description` or in the position attribution prose.

Do not encode reconstruction status as a global source role.

---

## Web Source Access Metadata

For web pages, include `url` and `accessed` whenever possible.

Example:

```yaml
id: source.web.example.arian_summary
type: web_page
title: "Example Historical Summary of Arian Christology"
url: https://example.org/arian-summary
accessed: 2026-06-22
description: >
  Secondary historical summary used for initial position attribution.
```

If the URL changes later, create or migrate to a new concrete source record
when the accessed page is materially different.

---

## Rights Metadata

Rights metadata is most important when exact quotations are used.

Include rights metadata when known:

```yaml
rights:
  status: copyrighted
  attribution: "Example Publisher"
  url: https://example.org/rights
```

Missing rights metadata should usually be a warning for bibliography sources,
not a schema error, unless exact quotation policy later requires stricter
validation.

For paraphrase-only or attribution-only source records, incomplete rights
metadata should not block v0.1 modeling.

---

## Locators

Use `Evidence.locator` or provenance `locator` to identify the cited location
within a source.

Common locator types:

```text
page
section
paragraph
canon
article
url
timestamp
```

Examples:

```yaml
locator:
  type: page
  value: "42"
```

```yaml
locator:
  type: section
  value: "Christology"
```

```yaml
locator:
  type: canon
  value: "Canon 1"
```

Use the most stable locator available for the concrete source.

---

## Position Attribution Sources

For position attribution, prefer sources appropriate to the holder type.

Modern organizations:

```text
official web pages
authorized articles
published doctrinal works
formal statements
```

Councils, creeds, and confessions:

```text
creeds
canons
council documents
formal declarations
concrete editions or translations of those documents
```

Historical movements:

```text
surviving fragments
ancient reports
modern scholarly reconstructions
representative secondary sources
```

Broad traditions:

```text
representative sources
confessional documents
recognized summaries
explicit dataset-author synthesis
```

The source record describes the publication or document. The provenance or
relationship using the source explains why it establishes attribution.

---

## No Source Quality Scoring in v0.1

Do not add reliability, quality, confidence, or ranking fields to `Source` in
v0.1.

The catalog should record what a source is and how it is used.

Evaluating source quality can be added later as a separate analysis layer.

Until then, use neutral `description` text and precise provenance rather than
global scores.

---

## Validation Guidance

The compiler may later warn when source metadata is incomplete for the source
type.

Potential warning:

```text
W008 incomplete source metadata
```

This should be a warning rather than a v0.1 schema error unless a required
field is missing or exact quotation rules become stricter.
