# v0.1 Scripture Sources

## Purpose

This document defines v0.1 conventions for modeling Scripture sources,
locators, evidence, quotations, and passage IDs.

The first apologetics dataset is Scripture-heavy. These rules keep the initial
YAML consistent without introducing a standalone `Passage` entity or a
Bible-reference parser in v0.1.

---

## Source Layering

Use an abstract Bible source for the work or corpus:

```yaml
sources:
  - id: source.bible
    type: scripture
    title: "Bible"
```

Use concrete source records for editions, translations, critical texts, and
original-language texts.

The first concrete translation source should be:

```yaml
sources:
  - id: source.bible.bsb
    type: translation
    title: "Berean Standard Bible"
    work_id: source.bible
    rights:
      status: copyrighted
      attribution: "Berean Standard Bible"
      url: https://bereanbible.com/
```

Exact quotations should point to the concrete source whose wording is quoted.

Do not attach exact quotation text to `source.bible`, because the abstract Bible
source does not identify a specific wording, edition, or translation.

---

## Books and Passages

Biblical books are not separate `Source` records in v0.1.

Treat books, chapters, verses, and ranges as locator content.

Example:

```yaml
source_id: source.bible.bsb
locator:
  type: verse
  value: "Colossians 1:15"
```

Do not introduce a standalone `Passage` entity in v0.1.

Add a `Passage` or `Location` entity later only if the project needs reusable
passage grouping, pericope metadata, canonical passage IDs, or passage-level
analysis independent of a concrete source.

---

## Locator Values

Use `locator.type: verse` for Scripture references.

Use full canonical English book names in `locator.value`.

Preferred:

```yaml
locator:
  type: verse
  value: "Colossians 1:15"
```

Avoid abbreviations:

```yaml
locator:
  type: verse
  value: "Col 1:15"
```

Use simple chapter and verse syntax:

```text
John 1:1
John 1:3
Colossians 1:15-17
Revelation 3:14
Proverbs 8:22
Hebrews 1:3
Hebrews 1:6
Philippians 2:6-11
```

The locator value should remain human-readable.

The compiler does not need a Bible-reference parser in v0.1, but the format
should be regular enough that one can be added later.

---

## Verse Ranges

Use the same locator type for verse ranges:

```yaml
locator:
  type: verse
  value: "Colossians 1:15-17"
```

If a range contains multiple distinct argumentative excerpts, prefer separate
`Evidence` records for the distinct excerpts.

Example:

```yaml
evidence:
  - id: evidence.bsb.colossians.1_15.firstborn
    source_id: source.bible.bsb
    locator:
      type: verse
      value: "Colossians 1:15"
    quotation: "firstborn over all creation"

  - id: evidence.bsb.colossians.1_16.created_through
    source_id: source.bible.bsb
    locator:
      type: verse
      value: "Colossians 1:16"
    paraphrase: >
      The verse describes creation in relation to the Son.
```

One range-level evidence record is acceptable when the whole range functions as
one unit in the argument.

---

## Evidence ID Encoding

Use the ID conventions from
[v0.1 ID Conventions](12-id-conventions.md).

For Scripture evidence IDs, include:

```text
evidence.<source_alias>.<book_slug>.<chapter_verse_or_range>.<excerpt_slug>
```

Examples:

```text
evidence.bsb.john.1_1.word_was_god
evidence.bsb.colossians.1_15.firstborn
evidence.bsb.colossians.1_15_17.creation_scope
evidence.bsb.revelation.3_14.beginning
evidence.bsb.philippians.2_6_11.form_of_god
```

The ID is a stable handle. The structured `locator` remains authoritative for
the source location.

---

## Multiple Translations and Editions

Each translation, edition, critical text, or original-language text should be a
separate concrete `Source`.

Examples:

```text
source.bible.bsb
source.bible.kjv
source.greek.sblgnt
source.hebrew.bhs
```

Each exact quotation should cite the concrete source whose wording is quoted.

Translation comparisons should be modeled as additional evidence,
interpretations, assumptions, arguments, or relationships rather than by
collapsing multiple translations into one source.

---

## Original-Language and Reference Sources

Greek texts, Hebrew texts, lexicons, grammars, commentaries, and critical
editions should be modeled as separate sources when they are used.

Examples:

```text
source.greek.sblgnt
source.lexicon.bdag
source.grammar.example
source.commentary.example
```

The first dataset does not need all of these sources before it can model a
minimal Scripture slice.

Add them when an interpretation or argument actually depends on them.

---

## Rights and Quotation Length

Concrete translation sources should include rights metadata before exact
quotations are modeled from them.

At minimum, include:

```yaml
rights:
  status: copyrighted
  attribution: "Berean Standard Bible"
  url: https://bereanbible.com/
```

Keep Scripture quotations short and passage-specific.

Use `paraphrase` when a longer passage is needed for context and exact wording
is not required.

Do not quote entire multi-verse passages unless the source rights policy allows
that use.

Validation may later warn on unusually long quotations. In v0.1, the key rule
is that exact quotations must cite a concrete source with rights metadata.

---

## Initial Modeling Rule

The first worked Scripture slice should start with one concrete translation
source and one or more short evidence records.

For Colossians 1:15:

```yaml
sources:
  - id: source.bible
    type: scripture
    title: "Bible"

  - id: source.bible.bsb
    type: translation
    title: "Berean Standard Bible"
    work_id: source.bible
    rights:
      status: copyrighted
      attribution: "Berean Standard Bible"
      url: https://bereanbible.com/

evidence:
  - id: evidence.bsb.colossians.1_15.firstborn
    source_id: source.bible.bsb
    locator:
      type: verse
      value: "Colossians 1:15"
    quotation: "firstborn over all creation"
```

Additional translations, original-language texts, lexicons, commentaries, and
critical editions can be added as separate sources when the modeled arguments
need them.
