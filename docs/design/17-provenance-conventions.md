# v0.1 Provenance Conventions

## Purpose

This document defines the v0.1 provenance object shape and validation policy.

Provenance records attribution. It should answer questions such as:

* who made or preserves a position, interpretation, argument, or relationship
* what work or source supports that attribution
* where in that work the attributed material appears
* whether a statement is dataset-author synthesis

Provenance does not rank reliability, determine truth, or replace evidence.

---

## Core Shape

In v0.1, `provenance` is a single object, not a list.

Example:

```yaml
provenance:
  attributed_to:
    type: author
    name: "Example Author"
  work:
    source_id: source.book.example_work
  locator:
    type: page
    value: "42"
  date: 2026
```

Common fields:

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

No single provenance field is globally required, but provenance should use
structured fields when present.

---

## `attributed_to`

`attributed_to` identifies who or what a derived statement is attributed to.

It should be an object with:

```text
type
id or name
```

Inline attribution example:

```yaml
attributed_to:
  type: author
  name: "Example Author"
```

Referenced attribution example:

```yaml
attributed_to:
  type: council
  id: agent.council.nicaea_325
```

Tradition reference example:

```yaml
attributed_to:
  type: tradition
  id: tradition.jehovahs_witnesses
```

If `id` is present, it must resolve to an existing entity.

If `name` is present without `id`, the attribution is provisional or inline.

`type` should use the controlled provenance-agent vocabulary where possible.

Examples:

```text
author
editor
translator
organization
tradition
council
dataset_contributor
```

If both `id` and `name` are present, the `id` is authoritative and `name` is
display/context metadata.

---

## `work`

`work` identifies the cited work or source that supports the attribution.

Prefer modeled sources:

```yaml
work:
  source_id: source.book.example_work
```

For provisional references, `work.title` may be used before a `Source` record
exists:

```yaml
work:
  title: "Example Publication"
```

If `work.source_id` is present, it must resolve to an existing `Source`.

If `work.title` is used without `source_id`, validation should warn rather than
error.

Once a source is important enough to support a position, quotation, or core
argument, it should become a `Source` record.

---

## `locator`

`provenance.locator` identifies where in the cited work the attributed
statement, interpretation, argument, or relationship appears.

Example:

```yaml
locator:
  type: page
  value: "42"
```

It is different from `Evidence.locator`.

`Evidence.locator` identifies where source evidence appears in the source.

`provenance.locator` identifies where attribution or derived material appears
in the cited work.

Example:

```yaml
evidence:
  source_id: source.bible.bsb
  locator:
    type: verse
    value: "Colossians 1:15"

interpretation:
  provenance:
    work:
      source_id: source.publication.example_commentary
    locator:
      type: page
      value: "88"
```

The `locator` object should follow the shared locator shape:

```text
type
value
label, optional
```

---

## URL and Access Date

`url` and `accessed` may be used as convenience fields, especially for
provisional web references.

Example:

```yaml
provenance:
  work:
    title: "Example Web Article"
  url: https://example.org/article
  accessed: 2026-06-22
```

If `url` is present without `accessed`, validation should warn.

If a modeled `Source` already contains the URL and access metadata, provenance
does not need to repeat them unless doing so helps identify a specific citation.

---

## Where Provenance Belongs

Use `Position.provenance` to explain why a holder is attributed with a stance.

Use `Interpretation.provenance` to identify who makes or represents an
interpretation.

Use `Argument.provenance` to identify who makes, preserves, or summarizes an
argument.

Use `Relationship.provenance` when the relationship itself is attributed.

Use `Claim.provenance` sparingly, for claims directly quoted, formally stated,
or historically attributed.

Use `Evidence.provenance` sparingly. Evidence already has `source_id` and
`locator`; evidence provenance is mostly for extraction, curation, or dataset
process notes.

Do not use `Source.provenance` in v0.1. Source metadata should handle source
identity.

---

## Provenance vs Evidence

Provenance should not replace evidence.

If exact wording matters, create `Evidence` with `source_id`, `locator`, and
`quotation`.

If the purpose is to say who made or preserved an interpretation, argument,
relationship, or position, use provenance.

Do not use provenance merely to identify where quoted wording came from.

Use:

```yaml
evidence:
  source_id: source.bible.bsb
  locator:
    type: verse
    value: "Colossians 1:15"
  quotation: "firstborn over all creation"
```

Not:

```yaml
provenance:
  work:
    source_id: source.bible.bsb
  locator:
    type: verse
    value: "Colossians 1:15"
```

when the record needs exact source wording.

---

## Multi-Source Synthesis

Do not add `based_on` to provenance in v0.1.

For multi-source synthesis, use related sourced records:

```text
Evidence
Interpretation
Argument
Relationship
```

Dataset-author synthesis may use provenance to identify the dataset author, but
the sources behind the synthesis should be represented through modeled records
when they matter.

Example:

```yaml
provenance:
  attributed_to:
    type: dataset_contributor
    name: "Dataset author"
  work:
    title: "Apologetics Viewpoint Catalog"
```

Validation may warn when dataset-author synthesis has no modeled supporting
source records.

---

## Provisional References

Prefer modeled `Source` records and `work.source_id`.

Allow provisional references during drafting:

```yaml
provenance:
  work:
    title: "Example Publication"
  url: https://example.org/example
  accessed: 2026-06-22
```

Unresolved provisional references should be warnings, not errors.

Broken `source_id` and `attributed_to.id` references should be errors.

The first dataset should avoid relying heavily on provisional references.

---

## Validation Severity

Errors:

```text
work.source_id does not resolve
attributed_to.id does not resolve
attributed_to has neither id nor name
attributed_to has an invalid type
locator has an invalid shape
accessed is not a valid date
```

Warnings:

```text
provenance uses work.title without source_id
provenance has url but no accessed date
important attribution record has no provenance
dataset-author synthesis has no modeled supporting source records
```

Provenance validation should not introduce truth, reliability, confidence, or
ranking semantics.

It validates attribution structure, references, and enough metadata for authors
to trace the modeled statement.
