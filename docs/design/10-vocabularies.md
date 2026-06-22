# v0.1 Controlled Vocabularies

## Purpose

This document defines the design-level controlled vocabulary contract for
`schema_version: "0.1"`.

It defines:

* the initial built-in vocabulary categories
* the minimal seed values for each category
* which vocabularies may be extended by a project
* how project extensions are declared
* how author-facing relationship types differ from compiler-generated graph
  edge types

This document is a human-readable design contract. Machine-readable vocabulary
files may be added later under the versioned schema directory.

---

## Vocabulary Policy

Controlled fields should validate against the vocabulary set for the document's
declared `schema_version`.

Built-in vocabulary IDs should be short lower-snake-case values.

Examples:

```text
yes_no
supports
scripture
lexical
official
```

Unknown vocabulary values should be validation errors unless they are declared
as project extensions for an extensible vocabulary.

Project extensions should be explicit, reviewable, and namespaced.

Examples:

```text
project.appeals_to_liturgical_usage
org.example.some_relation
```

Extension entries require:

```text
id
label
description
```

Built-in entries should also have labels and descriptions in the eventual
machine-readable vocabulary files, but the design docs may refer to them by ID
when the meaning is obvious.

Vocabulary entries may optionally carry validation metadata such as:

```text
inverse
symmetric
allowed_from
allowed_to
```

Not every v0.1 entry needs complete validation metadata. Missing metadata means
the validator should enforce the value's existence, but not infer additional
connection constraints from that entry.

---

## Extensibility

Vocabularies are closed by default.

Projects may extend only vocabularies explicitly marked extensible.

| Vocabulary | Extensible in v0.1 | Notes |
| --- | --- | --- |
| document_kinds | no | Schema-level document shapes. |
| question_types | no | Extend later through schema evolution if needed. |
| question_statuses | no | Lifecycle values should remain stable. |
| source_types | yes | Source genres and media types vary by dataset. |
| agent_types | yes | Attribution and holder categories vary by domain. |
| holder_types | yes | Mirrors agent/tradition holder usage. |
| locator_types | yes | Source location schemes vary by source type. |
| rights_statuses | no | Keep legal/status categories conservative. |
| provenance_agent_types | yes | Provenance attribution roles vary by source and project. |
| position_stances | no | Core stance semantics should stay stable. |
| position_statuses | no | Attribution status should stay stable. |
| argument_roles | yes | Projects may need domain-specific argument roles. |
| relationship_types | yes | Main extension point for domain-specific links. |
| interpretation_methods | yes | Interpretive methods vary by domain. |
| assumption_categories | yes | Premise categories vary by domain. |
| generated_edge_types | no | Compiler output vocabulary, not author input. |

Project-specific values in extensible vocabularies must be declared before use.

---

## Extension Declaration

Vocabulary extensions should be project-level, not file-local. In v0.1, they
should be declared in the root project manifest defined by
[v0.1 Project Manifest](13-project-manifest.md).

Example:

```yaml
schema_version: "0.1"

kind: project

project:
  id: project.apologetics
  title: "Apologetics Viewpoint Catalog"

vocabulary_extensions:
  relationship_types:
    - id: project.appeals_to_liturgical_usage
      label: "Appeals to liturgical usage"
      description: >
        Used when an argument appeals to historical worship practice.
      inverse: project.liturgical_usage_appealed_to_by
      symmetric: false
      allowed_from:
        - Argument
      allowed_to:
        - Claim
        - Interpretation
```

Extension metadata beyond `id`, `label`, and `description` is optional in
v0.1.

---

## Author Relationship Types and Generated Edge Types

Author-written `Relationship.type` values are for first-class relationships:

* argumentative links
* interpretive links
* claim-to-claim links
* question-to-question links
* dependency links
* response links
* links that need provenance, summaries, qualifiers, or diagnostics

Structural references should usually be written as direct fields on records.

Examples:

```yaml
claim:
  question_id: question.christology.created_being
```

```yaml
evidence:
  source_id: source.bible.bsb
```

```yaml
question:
  topic_ids:
    - topic.christology
```

The graph projection may emit structural edge types derived from those direct
fields.

Generated edge examples:

```text
has_question
has_source
has_topic
held_by
classified_as
work_instance_of
```

These generated edge types are not valid author-written `Relationship.type`
values in v0.1 unless a later schema version explicitly makes them author
facing.

---

## Document Kinds

Document kinds identify the shape of a YAML document.

They are not project-extensible in v0.1.

```text
project
topic
question
claim
tradition
agent
position
source
evidence
interpretation
assumption
argument
relationship
```

---

## Question Types

Question types classify the kind of issue being modeled.

They are not project-extensible in v0.1.

| ID | Label | Description |
| --- | --- | --- |
| yes_no | Yes/no | A question answered primarily by affirmation or denial. |
| interpretive | Interpretive | A question about the meaning of a text, source, event, or claim. |
| historical | Historical | A question about what happened or what was believed at a time. |
| comparative | Comparative | A question comparing two or more views, sources, or interpretations. |
| classificatory | Classificatory | A question about how something should be categorized. |
| open | Open | A broad issue that may not have a small fixed answer set. |

---

## Question Statuses

Question statuses describe authoring and schema lifecycle state.

They are not project-extensible in v0.1.

| ID | Label | Description |
| --- | --- | --- |
| draft | Draft | The question is provisional or incomplete. |
| active | Active | The question is part of the current modeled dataset. |
| deprecated | Deprecated | The question remains for compatibility but should not be used for new data. |

---

## Source Types

Source types classify works, editions, publications, media, and other evidence
sources.

Bibliography source modeling guidance is defined in
[v0.1 Bibliography Sources](16-bibliography-sources.md).

They are project-extensible in v0.1.

| ID | Label | Description |
| --- | --- | --- |
| scripture | Scripture | A canonical scriptural work or corpus. |
| translation | Translation | A concrete translation or edition of a work. |
| manuscript | Manuscript | A manuscript witness or handwritten source. |
| critical_text | Critical text | A reconstructed or edited critical text. |
| commentary | Commentary | A commentary on a text, doctrine, event, or argument. |
| lexicon | Lexicon | A lexical or dictionary source. |
| creed | Creed | A creed, confession, or formal statement of belief. |
| council_document | Council document | A source produced by or associated with a council. |
| book | Book | A book or monograph. |
| article | Article | An article, essay, paper, or journal publication. |
| web_page | Web page | A web page or online publication. |
| dataset | Dataset | A structured dataset used as evidence or reference material. |

---

## Agent and Holder Types

Agent types classify entities that can make, hold, transmit, publish, or be
attributed with positions, arguments, interpretations, and claims.

Holder types classify the `holder.type` field used by positions.

Both vocabularies are project-extensible in v0.1.

| ID | Label | Description |
| --- | --- | --- |
| person | Person | An individual human agent. |
| organization | Organization | An institution, publisher, ministry, society, or other organization. |
| council | Council | A council, synod, assembly, or formal deliberative body. |
| tradition | Tradition | A school, movement, denomination, or intellectual tradition. |
| school | School | A named school of thought or interpretive school. |
| movement | Movement | A movement that may not be an institution or formal tradition. |
| dataset_contributor | Dataset contributor | A contributor or editor of the catalog dataset. |

---

## Provenance Agent Types

Provenance agent types classify attribution roles inside provenance metadata.

They are project-extensible in v0.1.

| ID | Label | Description |
| --- | --- | --- |
| author | Author | The attributed author of a statement, work, or argument. |
| editor | Editor | An editor responsible for an edition or publication. |
| translator | Translator | A translator responsible for a translation. |
| compiler | Compiler | A compiler, collector, or arranger of source material. |
| organization | Organization | An institution or organization responsible for publication or attribution. |
| tradition | Tradition | A tradition or movement to which a statement is attributed. |
| council | Council | A council, synod, or deliberative body to which a statement is attributed. |
| dataset_contributor | Dataset contributor | A dataset contributor responsible for a summary or modeling judgment. |

---

## Locator Types

Locator types classify locations within sources.

They are project-extensible in v0.1.

| ID | Label | Description |
| --- | --- | --- |
| verse | Verse | A scriptural or poetic verse reference. |
| chapter | Chapter | A chapter reference. |
| page | Page | A page reference. |
| section | Section | A named or numbered section. |
| paragraph | Paragraph | A paragraph reference. |
| line | Line | A line reference. |
| folio | Folio | A folio reference in a manuscript or archival source. |
| timestamp | Timestamp | A time location in audio or video. |
| canon | Canon | A canon, rule, or numbered conciliar/legal item. |
| article | Article | An article or clause in a structured document. |
| url | URL | A URL used as a locator within an online source. |

---

## Rights Statuses

Rights statuses classify the rights state of a source.

They are not project-extensible in v0.1.

| ID | Label | Description |
| --- | --- | --- |
| public_domain | Public domain | The source is believed to be in the public domain. |
| copyrighted | Copyrighted | The source is copyrighted. |
| licensed | Licensed | The source is available under an explicit license. |
| unknown | Unknown | The rights state is not yet known. |

---

## Position Stances

Position stances describe a holder's stance toward a claim.

They are not project-extensible in v0.1.

| ID | Label | Description |
| --- | --- | --- |
| affirms | Affirms | The holder affirms the claim. |
| rejects | Rejects | The holder rejects the claim. |
| qualifies | Qualifies | The holder affirms only a qualified form of the claim. |
| permits | Permits | The holder permits the claim as acceptable but not required. |
| unclear | Unclear | The holder's stance is unclear or disputed. |

---

## Position Statuses

Position statuses describe the attribution strength or standing of a position.

They are not project-extensible in v0.1.

Status escalation rules are defined in
[v0.1 Position Attribution](15-position-attribution.md).

| ID | Label | Description |
| --- | --- | --- |
| official | Official | The position is official or formally stated by the holder. |
| common | Common | The position is commonly associated with the holder. |
| historical | Historical | The position is historically attributed to the holder. |
| disputed | Disputed | The attribution is disputed. |
| attributed | Attributed | The position is attributed but not necessarily formal or common. |

---

## Argument Roles

Argument roles classify the function of an argument record.

They are project-extensible in v0.1.

| ID | Label | Description |
| --- | --- | --- |
| support | Support | An argument offered in support of another entity. |
| objection | Objection | An argument objecting to another entity. |
| response | Response | An argument responding to an objection or argument. |
| rebuttal | Rebuttal | A response that directly attempts to defeat another argument. |
| qualification | Qualification | An argument that narrows or qualifies another entity. |
| clarification | Clarification | An argument that clarifies another entity without directly supporting or challenging it. |

---

## Interpretation Methods

Interpretation methods classify how evidence is being read.

They are project-extensible in v0.1.

| ID | Label | Description |
| --- | --- | --- |
| lexical | Lexical | Interprets wording through word meaning or lexical range. |
| grammatical | Grammatical | Interprets wording through grammar or syntax. |
| historical | Historical | Interprets evidence through historical context. |
| theological | Theological | Interprets evidence through theological categories or doctrine. |
| textual | Textual | Interprets evidence through textual variants or textual history. |
| translation | Translation | Interprets evidence through translation choices or translation comparison. |
| contextual | Contextual | Interprets evidence through literary or argumentative context. |
| traditional | Traditional | Interprets evidence through received tradition or historical reception. |

---

## Assumption Categories

Assumption categories classify reusable premises.

They are project-extensible in v0.1.

| ID | Label | Description |
| --- | --- | --- |
| lexical | Lexical | A premise about word meaning or semantic range. |
| historical | Historical | A premise about historical context or events. |
| theological | Theological | A premise about theological categories or doctrine. |
| methodological | Methodological | A premise about interpretive or argumentative method. |
| textual | Textual | A premise about textual evidence or textual transmission. |
| translation | Translation | A premise about translation practice or translation choice. |

---

## Relationship Types

Relationship types classify author-written first-class relationships.

They are project-extensible in v0.1.

| ID | Label | Direction | Description |
| --- | --- | --- | --- |
| supports | Supports | directional | `from_id` is used to support `to_id`. |
| challenges | Challenges | directional | `from_id` challenges, weakens, or disputes `to_id`. |
| responds_to | Responds to | directional | `from_id` responds to `to_id`. |
| uses | Uses | directional | `from_id` uses `to_id` as evidence, premise, interpretation, or support. |
| depends_on | Depends on | directional | `from_id` depends on `to_id`. |
| interprets | Interprets | directional | `from_id` interprets `to_id`, usually an `Interpretation` interpreting `Evidence`. |
| contradicts | Contradicts | symmetric | `from_id` and `to_id` cannot both be affirmed in the relevant sense. |
| entails | Entails | directional | `from_id` implies `to_id`. |
| qualifies | Qualifies | directional | `from_id` qualifies or limits `to_id`. |
| narrows | Narrows | directional | `from_id` is narrower than `to_id`. |
| broadens | Broadens | directional | `from_id` is broader than `to_id`. |
| contrasts_with | Contrasts with | symmetric | `from_id` is meaningfully contrasted with `to_id`. |
| related_to | Related to | symmetric | `from_id` is related to `to_id` without a more specific relationship. |

Relationship entries may define inverse and validation metadata.

Examples:

```yaml
id: supports
label: "Supports"
description: >
  Indicates that one entity is used to support another entity.
inverse: supported_by
symmetric: false
allowed_from:
  - Argument
  - Interpretation
  - Evidence
  - Assumption
allowed_to:
  - Claim
  - Interpretation
  - Argument
```

```yaml
id: contradicts
label: "Contradicts"
description: >
  Indicates that two claims or positions are mutually incompatible in the
  relevant sense.
symmetric: true
allowed_from:
  - Claim
allowed_to:
  - Claim
```

The compiler should not require complete `allowed_from` and `allowed_to`
coverage for every v0.1 relationship type, but it may use available metadata to
produce better diagnostics.
