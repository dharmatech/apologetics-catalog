# v0.1 ID Conventions

## Purpose

This document defines practical conventions for stable entity IDs in
`schema_version: "0.1"` YAML.

IDs are author-chosen handles, not generated database keys.

They should be readable enough for authors to work with directly, stable enough
for references and generated outputs, and conservative enough to survive file
moves, UI routing, graph projection, and future migrations.

---

## Core Rules

Every entity record must declare one canonical `id`.

IDs are unique across the entire dataset, not merely within a file, document
kind, or YAML section.

File paths do not define identity.

Moving a record between files must not change its ID.

References resolve by canonical ID across the whole dataset.

Duplicate IDs are validation errors.

The compiler should report every known source location for a duplicate ID so
authors can fix the collision without guessing which record won.

---

## Dataset-Local Identity

In v0.1, entity IDs are globally unique within one dataset.

They are not assumed to be globally unique across every future catalog or
project.

Author-written references should use local entity IDs:

```text
claim.jesus_created
```

Generated outputs that need globally unique external keys may combine the
project ID and local entity ID:

```text
project.apologetics#claim.jesus_created
```

Cross-dataset federation can add stronger namespacing later without making the
v0.1 authoring format noisy.

---

## Allowed Characters

Use lowercase ASCII IDs.

Allowed characters:

```text
a-z
0-9
_
.
```

Do not use:

```text
spaces
hyphens
apostrophes
slashes
colons
Unicode letters
uppercase letters
```

Use dots for hierarchy.

Use underscores inside a slug term.

Preferred:

```text
question.christology.created_being
evidence.bsb.colossians.1_15.firstborn
interpretation.jw.colossians.1_15.firstborn_created_order
```

Avoid:

```text
Question.Christology.CreatedBeing
question/christology/created-being
evidence.bsb.colossians.1.15.firstborn
```

---

## Kind Prefixes

Every top-level entity ID should begin with a kind prefix.

Common prefixes:

```text
project.
topic.
question.
claim.
tradition.
agent.
position.
source.
evidence.
interpretation.
assumption.
argument.
relationship.
```

The prefix remains required even when the record appears in a section whose name
already implies the entity kind.

The prefix improves diagnostics, generated output, graph display, and human
review.

---

## Semantic but Stable

IDs should be semantic but not sentence-derived.

They may hint at the entity's meaning, source, holder, or role.

They should not mirror full display text or summaries.

Changing a `summary`, title, label, or quotation should not normally require an
ID change.

Preferred:

```text
claim.jesus_created
claim.jesus_uncreated
```

Avoid:

```text
claim.jesus_is_the_first_and_greatest_created_being_according_to_colossians
```

---

## Hierarchy and Scope

Use hierarchy when it improves readability or avoids likely collisions.

Do not encode every relationship into an ID.

Good examples:

```text
question.christology.created_being
position.jw.christology.created_being
evidence.bsb.colossians.1_15.firstborn
interpretation.nicene.colossians.1_15.firstborn_preeminence
relationship.jw.colossians_firstborn.supports_created
```

IDs should remain stable if a record is moved to a different file or grouped
under a different topic.

Evidence IDs should usually include a concrete source alias when the same
locator may appear in multiple editions, translations, or source witnesses.

---

## Bible and Source Locator Encoding

For Bible-style references, use:

```text
book.chapter_verse
```

Examples:

```text
john.1_1
colossians.1_15
revelation.3_14
```

For verse ranges, append the ending verse:

```text
philippians.2_6_11
colossians.1_15_17
```

For numbered books, use a leading number followed by an underscore:

```text
1_corinthians.8_6
2_peter.1_1
```

Use the locator encoding as an ID component, not as a replacement for the
structured `locator` field. The structured locator remains authoritative for
source location semantics.

---

## Short Aliases

Short aliases may be used inside IDs when they are declared or obvious from
canonical records.

Examples:

```text
jw
arian
nicene
bsb
```

The alias should correspond to a declared `Tradition`, `Agent`, `Source`, or
other canonical record.

Examples:

```text
tradition.jehovahs_witnesses
source.bible.bsb
position.jw.christology.created_being
interpretation.nicene.colossians.1_15.firstborn_preeminence
```

Aliases in IDs are conveniences, not separate identity records.

If an alias becomes confusing, introduce a new ID through migration rather than
silently changing references.

---

## Relationship IDs

Relationship IDs should describe the connection enough to be reviewable.

They should not try to encode every endpoint in full.

Preferred:

```text
relationship.jw.colossians_firstborn.supports_created
relationship.created.contradicts_uncreated
relationship.nicene.firstborn.challenges_created_reading
```

Avoid:

```text
relationship.interpretation_jw_colossians_1_15_firstborn_created_order_supports_claim_jesus_created
```

The authoritative endpoints remain `from_id` and `to_id`.

---

## Renames and Retired IDs

Treat an ID rename as a migration, not a casual edit.

Avoid renames once data has been published or used by generated outputs.

Never reuse a retired ID for a different entity.

Deleted IDs should remain reserved.

v0.1 records do not need inline old-ID aliases.

ID alias maps, redirects, and migration metadata can be added later when real
migrations require them.

---

## Validation Behavior

The compiler should validate:

* every entity has an explicit `id`
* every ID follows the allowed character rules
* every ID has the expected kind prefix for its entity kind
* IDs are unique across the dataset
* references resolve by canonical ID
* retired IDs are not reused when migration metadata exists

Duplicate ID diagnostics should include all known duplicate locations.

Example:

```text
code: E002
phase: identity
message: Duplicate id: claim.jesus_created
locations:
  - content/questions/christology/created-being/claims.yaml:12
  - content/questions/christology/created-being/nicene.yaml:44
```

ID diagnostics should be deterministic so validation output remains stable in
tests and CI.
