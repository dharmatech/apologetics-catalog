# v0.1 Position Attribution

## Purpose

This document defines how v0.1 should attribute positions to holders.

It explains how to distinguish:

* the source that establishes a position
* the source a position uses as evidence
* official statements
* representative sources
* historical reconstructions
* dataset-author synthesis

The schema allows `Position.provenance` to be optional, but substantive modeled
positions should not remain unsupported in practice.

---

## Attribution Principle

A `Position` says that a holder has a stance toward one or more claims.

The dataset should be able to explain why that attribution is being made.

For v0.1, every substantive position should have either:

* provenance on the `Position`
* at least one sourced `Argument`, `Interpretation`, or `Relationship`
  supporting the attribution
* an explicit dataset-author synthesis with provenance

This is a modeling guideline, not a new required field in the low-level schema.

The goal is to avoid unsupported labels such as "Arian position" or "Nicene
position" without any modeled basis for the attribution.

---

## Source of Position vs Source Used by Position

Distinguish the source that establishes a position from the source that the
position uses in its argument.

Example:

```text
source of position:
  an official Jehovah's Witness publication explaining the teaching

source used by position:
  Colossians 1:15 as evidence appealed to by the position
```

Use `Position.provenance` for sources that establish or justify attribution of a
position to a holder.

Use `Evidence`, `Interpretation`, `Argument`, and `Relationship` for sources
the position appeals to.

A Bible verse alone should not be treated as provenance that a tradition holds a
particular stance.

Scripture can be evidence used by an argument. Attribution to the holder should
come from a representative, official, historical, or explicitly synthesized
holder-related source.

---

## Holder-Specific Attribution Standards

Different holder types need different attribution standards.

For a modern organization, prefer official or representative publications.

Examples:

```text
official website
published doctrinal manual
authorized article
formal statement
```

For a council, creed, confession, or synod, prefer primary documents or direct
conciliar records.

Examples:

```text
creed
canon
council document
formal declaration
```

For a historical person or movement, allow historical reconstruction when direct
sources are fragmentary or mediated.

Examples:

```text
surviving fragments
ancient summaries
hostile reports
modern historical analysis
```

For a broad tradition, representative sources and dataset-author synthesis are
acceptable, but the synthesis should be identified as such.

---

## Dataset-Author Synthesis

Dataset-author synthesis is acceptable when the catalog needs a neutral summary
of a holder's position.

The provenance should make clear that the wording is a dataset-authored
summary, not a direct quotation or official formula.

Example:

```yaml
provenance:
  attributed_to:
    type: dataset_contributor
    name: "Dataset author"
  work:
    title: "Apologetics Viewpoint Catalog"
```

When a synthesis depends on multiple sources, represent those sources through
the related sourced `Evidence`, `Interpretation`, `Argument`, or `Relationship`
records until the provenance model grows an explicit `based_on` field.

Do not imply that synthesized wording came directly from a tradition, council,
author, or source unless it is quoted or directly supported.

---

## Arian and Historical Reconstruction Caution

Historical Arian positions need special care.

The evidence may be fragmentary, mediated through opponents, or reconstructed
from later historical analysis.

Use conservative attribution status values.

Prefer:

```text
historical
attributed
disputed
```

Avoid `official` unless the record is grounded in a direct formal source from
the holder or a clearly identified authoritative body.

Historical reconstruction should not be presented as equivalent to a modern
organization's official statement.

---

## Thin-Slice Minimums

The first YAML slice should not block on exhaustive position-history research.

For each major position in v0.1, provide at least one of:

* an official or representative attribution source
* a historical reconstruction source
* explicit dataset-author synthesis with provenance

Scripture-based argument modeling may proceed in parallel, but Scripture
evidence does not replace position attribution.

Recommended minimums:

| Holder Type | Minimum Attribution Basis |
| --- | --- |
| Modern organization | One official or representative publication. |
| Council or creed | One primary creed, canon, declaration, or council source. |
| Historical movement | One historical source or reconstruction source. |
| Broad tradition | One representative source or explicit dataset synthesis. |

This keeps the first dataset grounded without turning the first pass into a
full historical bibliography.

---

## Claim Stance Status Rules

`claim_stances.status` describes the strength or standing of the attribution.

It does not describe whether the claim itself is true.

Use `official` when the stance is grounded in a formal statement by the holder
or an authorized body.

Examples:

```text
official doctrinal publication
creed
confession
council document
formal declaration
```

Use `common` when the stance is widely represented in reliable secondary or
representative sources but is not necessarily formal.

Do not infer `common` from one isolated source.

Use `historical` when the stance is attributed to a historical person, group, or
movement in its historical context.

Use `attributed` when a source claims the holder has this stance, but the basis
is limited or not yet fully assessed.

Use `disputed` when the attribution itself is contested.

Conservative escalation rule:

```text
If unsure, use the weaker status.
```

Do not infer `official` from common usage.

Do not infer `common` from one source.

For fragmentary historical positions, avoid `official` unless there is a direct
formal source.

---

## Examples

Modern organization:

```yaml
positions:
  - id: position.jw.christology.created_being
    holder:
      type: tradition
      id: tradition.jehovahs_witnesses
    claim_stances:
      - claim_id: claim.jesus_created
        stance: affirms
        status: official
    provenance:
      work:
        source_id: source.publication.jw.official_christology_summary
```

Council or creed:

```yaml
positions:
  - id: position.nicene.christology.uncreated
    holder:
      type: council
      id: agent.council.nicaea_325
    claim_stances:
      - claim_id: claim.jesus_uncreated
        stance: affirms
        status: official
    provenance:
      work:
        source_id: source.creed.nicaea_325
```

Historical reconstruction:

```yaml
positions:
  - id: position.arian.christology.created_being
    holder:
      type: tradition
      id: tradition.arian
    claim_stances:
      - claim_id: claim.jesus_created
        stance: affirms
        status: historical
    provenance:
      work:
        source_id: source.history.arian_christology_summary
```

These examples are illustrative. Actual source IDs should be chosen when real
sources are added to the dataset.

---

## Validation Guidance

The compiler may later warn when a substantive position has neither provenance
nor sourced explanatory material.

Potential warning:

```text
W007 position has no attribution support
```

This should be a warning rather than a v0.1 schema error, because early data
entry may legitimately create placeholders during drafting.
