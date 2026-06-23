# Web UI Reasoning Browser

## Purpose

This document defines the first read-only web UI for browsing an apologetics
catalog.

The immediate problem is reviewability. Once a topic contains many claims,
arguments, interpretations, assumptions, evidence records, sources, and
relationships, raw YAML is no longer the best way to inspect chains of
reasoning.

The browser should let a user start from an entity such as:

```text
claim.jesus_created
```

and expand outward to see what supports it, challenges it, responds to it,
depends on it, qualifies it, or is otherwise related to it.

The UI is a review and exploration tool. It is not an authoring interface in
the first version.

---

## Goals

The first web UI should:

* provide an entity-centered way to browse catalog data
* make relationship direction and type visible
* make chains of reasoning easy to follow
* show competing perspectives without deciding which one is correct
* support controlled expand/collapse exploration
* expose evidence quotations, sources, locators, and provenance
* support shareable snapshots of a selected view
* handle graph-shaped data without confusing tree users

The first UI should be useful for reviewing the initial Christology topic:

```text
Is Jesus a created being?
```

but it should not hard-code Christology concepts.

---

## Non-Goals

The first web UI should not include:

* editing YAML records
* creating, deleting, or renaming entities
* source import workflows
* automatic argument evaluation
* truth ranking
* debate scoring
* collaborative comments
* authentication or publishing workflows
* full graph layout as the primary interface

These may be considered later, but the first browser should stay read-only.

---

## Core Concept

The canonical data model is graph-shaped.

Entities are connected by first-class relationships. A claim may be supported
by several arguments, challenged by other arguments, contradicted by another
claim, and connected to evidence through interpretations.

The browser should present a tree-shaped projection of that graph.

This means:

* the data remains a graph
* the UI starts from one selected root entity
* each expanded node shows immediate related entities
* repeated entities and cycles are detected
* the user controls how far to expand

The UI should not pretend that the catalog is actually a tree.

---

## Primary Workflow

The main workflow is:

1. Search for or enter an entity ID.
2. Open the entity as the root node.
3. Review the first-level relationship groups.
4. Expand selected related nodes.
5. Follow chains of reasoning and response.
6. Export the current expanded view when useful.

Example starting point:

```text
claim.jesus_created
```

The first level might show:

* interpretations that support the claim
* arguments that challenge the claim
* the claim that contradicts it
* responses connected through the relationship graph

The user can then expand a Trinitarian response, then a JW response to that
response, and so on.

---

## Entity-Centered Navigation

The first browser should be entity-centered rather than topic-page-centered.

Any entity can be opened as the root:

```text
claim.jesus_created
argument.trinitarian.john_1_3_created_things_response
interpretation.jw.colossians_1_16.all_other_things_scope
evidence.nwt_2013.colossians.1_16.all_other_things_created
```

This allows the same data to be explored from different starting points.

Topic overview pages may be added later, but they are not required for the
first browser.

---

## Node Display

Each node should show enough information to decide whether to expand it.

Common fields:

* entity kind
* entity ID
* summary or title
* perspective badge, when available
* source or provenance badge, when available
* relationship label from the parent

Evidence nodes should also show:

* quotation or paraphrase
* source title
* locator type and value
* rights or attribution, if available

Interpretation nodes should show:

* method
* summary
* attribution or tradition, if available
* main evidence reference

Argument nodes should show:

* role
* summary
* attribution or tradition, if available

Assumption nodes should show:

* category
* summary
* attribution or provenance, if available

Source nodes should show:

* source type
* title
* edition or date, if available
* URL, if available
* rights information, if available

---

## Relationship Display

Relationships should be visible as labeled branches between nodes.

The branch label should come from the relationship type:

```text
supports
challenges
responds_to
uses
depends_on
qualifies
contradicts
related_to
```

Direction must be clear.

For example, when viewing `claim.jesus_created`, a relationship where an
argument points to the claim should be rendered as:

```text
Supported by: argument.jw.firstborn_usual_meaning_response
```

When viewing the argument, the same relationship should be rendered as:

```text
Supports: claim.jesus_created
```

The UI should use human-readable labels while preserving raw relationship type
values for inspection.

---

## Relationship Groups

Related nodes should be grouped by relationship type and direction.

Suggested group labels:

* Supported by
* Supports
* Challenged by
* Challenges
* Responded to by
* Responds to
* Used by
* Uses
* Depended on by
* Depends on
* Qualified by
* Qualifies
* Contradicts
* Related

The group labels should make direction obvious.

---

## Stable Ordering

The order of groups and child nodes should be deterministic.

The browser should not reorder nodes unpredictably between runs.

MVP group order:

1. Contradicts
2. Challenged by
3. Challenges
4. Responded to by
5. Responds to
6. Supported by
7. Supports
8. Used by
9. Uses
10. Depended on by
11. Depends on
12. Qualified by
13. Qualifies
14. Narrows
15. Broadens
16. Related
17. Other relationship types alphabetically

Within each group, sort deterministically by:

1. entity kind
2. display title or summary
3. entity ID

Later versions may add user-selectable ordering, but the default must remain
stable.

---

## Expansion Behavior

The UI should avoid expanding too much at once.

Default behavior:

* opening a root shows the root and its first-level relationship groups
* first-level related entities are visible as collapsed child nodes
* expanding a child reveals only that child's immediate related entities
* those newly revealed child entities remain collapsed
* the user chooses each additional expansion explicitly

Core rule:

```text
Expanding a node reveals its immediate related entities, grouped by relationship
type, but those child entities remain collapsed until the user explicitly
expands them.
```

This prevents a single click from producing a large unreadable tree.

Useful MVP controls:

* expand node
* collapse node
* expand one level
* collapse descendants
* copy entity ID
* open entity as root

Later controls may include:

* max-depth expansion
* expand all supports
* expand all challenges
* hide source-only nodes
* hide repeated nodes

---

## Repeated Nodes and Cycles

Because the data is a graph, the same entity may appear in multiple branches.

The browser must detect repeated nodes and cycles.

If an entity has already been expanded elsewhere in the current view, the UI
should not expand it again by default.

Instead it should show a reference node such as:

```text
Already shown above: argument.trinitarian.john_1_3_created_things_response
```

The user may still choose:

* jump to first occurrence
* open as new root
* expand duplicate here, if explicitly allowed

Cycles should never cause infinite expansion.

---

## Perspective and Provenance Styling

The browser should make perspective visible without making the UI look like a
scoreboard.

Perspective may come from:

* `provenance.attributed_to`
* position holder
* source tradition
* dataset synthesis records

Suggested badges:

```text
JW
Trinitarian
Dataset synthesis
Source only
Unattributed
```

Color coding should be restrained and consistent.

Example:

* Jehovah's Witnesses: blue
* Nicene Trinitarian: green
* Dataset synthesis: gray
* Source-only evidence: neutral

The exact colors can change later. The important design requirement is that the
same perspective has the same visual treatment across the tree and exports.

The UI should not use color as the only signal. Badges or labels must also be
present.

---

## Source and Evidence Visibility

Evidence nodes are especially important in apologetics review.

An evidence node should show:

* quotation or paraphrase
* source title
* edition, when relevant
* locator
* source URL, when available

For example, a compact evidence node might display:

```text
Evidence
evidence.nwt_2013.colossians.1_16.all_other_things_created

"all other things were created"

Source: New World Translation of the Holy Scriptures (2013 Revision)
Locator: Colossians 1:16
```

Source edition should be visible when different editions matter, such as 2013
NWT and 1984 NWT reference edition comparisons.

---

## Search and Root Selection

The MVP should support simple root selection:

* enter an exact entity ID
* search by partial ID
* search by title, summary, quotation, or source title

Search results should show:

* entity kind
* entity ID
* short summary, title, or quotation
* perspective badge, if available

Selecting a search result opens it as the root.

---

## Deep Links

Every root view should be deep-linkable.

At minimum, a URL should be able to encode:

```text
root entity ID
```

Later, URLs may encode:

* expanded node IDs
* selected relationship filters
* ordering options
* snapshot IDs

Deep links should not mutate the catalog.

---

## Shareable Snapshots

The browser should support exporting the current view as a shareable snapshot.

A snapshot is not the whole catalog. It is the user's selected root plus the
currently expanded tree projection.

The snapshot should preserve:

* root entity
* expanded nodes
* relationship labels
* visible summaries, quotations, and locators
* perspective badges or labels
* repeated-node markers
* deterministic ordering
* catalog version or git commit, when available
* export timestamp

Collapsed branches should not be exported unless the user explicitly chooses an
"export reachable graph" or "export all descendants" mode later.

---

## Export Formats

MVP export formats:

* Markdown
* plain text
* self-contained HTML

Markdown export should be suitable for:

* GitHub issues and pull requests
* notes
* documentation
* review comments

Plain text export should be suitable for:

* forums
* email
* chat
* places where Markdown is not reliable

Self-contained HTML export should be suitable for:

* sharing a read-only interactive snapshot
* local viewing without a server
* preserving fold state, relationship labels, and color badges

The HTML snapshot may include small embedded JavaScript for folding and basic
navigation.

The HTML snapshot should not require access to the original catalog server.

Later export formats may include:

* JSON view state
* PNG image
* SVG image
* static PDF
* graph data for external visualization tools

---

## Snapshot Privacy and Attribution

Snapshots may include copyrighted quotations and source attributions.

The export system should preserve source metadata and should not silently strip
rights or attribution fields.

Each snapshot should include:

* source title
* edition or date, when present
* URL, when present
* locator
* rights status, when present
* generated timestamp

The first version does not need automated quotation-length enforcement, but the
design should allow later export policies to limit or summarize quotations when
needed.

---

## Tree View vs Graph View

The first UI should use a tree projection as the primary interface.

Reasons:

* easier to read
* easier to implement
* easier to export
* easier to review one chain of reasoning at a time
* less likely to become visually noisy

A graph visualizer is still useful, but it should be a later alternate view.

The graph view may eventually help answer questions like:

* which claims have the most responses?
* which evidence is used by multiple positions?
* which assumptions carry many arguments?
* where do cycles or repeated rebuttal patterns occur?

For the MVP, the tree browser is the primary visualization.

---

## MVP Scope

The first implementation should include:

* static or local web app for browsing compiled catalog data
* exact-ID root loading
* simple search
* tree projection from a root entity
* relationship grouping
* stable ordering
* expand/collapse controls
* repeated-node and cycle handling
* perspective badges
* source and provenance display
* Markdown export of current expanded view
* plain text export of current expanded view
* self-contained HTML export of current expanded view

The MVP may read from generated JSON produced by the compiler rather than raw
YAML.

---

## Later Work

Later versions may add:

* graph visualization mode
* side-by-side position comparison
* source-focused browsing
* topic overview pages
* saved named views
* URL-encoded view state
* snapshot diffing
* PNG, SVG, and PDF export
* filtering by tradition, source, entity kind, or relationship type
* keyboard navigation
* accessibility review
* eventually, editing workflows

Editing should remain out of scope until read-only review is useful and stable.

---

## Design Principle

The browser should help a user understand how claims, evidence, interpretations,
assumptions, and arguments connect.

It should not flatten disagreement into a single answer, and it should not hide
the source or perspective behind a node.

The user should always be able to ask:

```text
What is this node?
Who or what is it attributed to?
What source supports it?
What relationship connects it to the current chain?
What can I expand next?
```

If the UI answers those questions clearly, it is doing its job.
