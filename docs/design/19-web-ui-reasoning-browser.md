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

## Data Contract

The browser should read compiled JSON, not source YAML.

YAML remains the canonical authoring format. The Python validator/compiler owns
validation, normalization, relationship indexing, and export generation.

Initial generated path:

```text
generated/web/catalog.json
```

Static viewer assets may also be emitted under:

```text
generated/web/
```

Example files:

```text
generated/web/index.html
generated/web/app.js
generated/web/style.css
generated/web/catalog.json
```

Generated files are disposable build artifacts.

They should not be hand-edited. If generated files are checked into the
repository later for convenience, the source of truth remains the YAML plus the
compiler.

The browser must treat generated JSON as read-only.

---

## JSON Shape

The initial browser export should be UI-oriented rather than raw YAML-shaped.

It should remain faithful to the catalog graph, but it should precompute common
browser needs so the frontend does not need to reverse-engineer relationship
direction, display labels, source summaries, or perspective hints.

The top-level JSON should include at least:

```json
{
  "schema_version": "0.1",
  "generated_at": "2026-06-22T00:00:00Z",
  "generator": {
    "name": "apologetics-catalog"
  },
  "project": {
    "id": "project.apologetics",
    "title": "Apologetics Viewpoint Catalog"
  },
  "entities": {},
  "relationships": [],
  "indexes": {
    "outgoing": {},
    "incoming": {}
  }
}
```

Optional metadata may include:

* generator version
* git commit
* content file list
* content hash
* generated output format version

The JSON schema should be versioned from the beginning. The browser should
reject or warn on unsupported `schema_version` values.

---

## Identity and Denormalization

Entity IDs are the canonical join keys.

Relationships should continue to connect entities by:

```text
from_id
to_id
```

The JSON export may include denormalized fields for UI convenience:

* display label
* short summary
* perspective badge
* source summary
* locator summary
* relationship group label

These fields are convenience data only. They do not create a separate identity
model.

The browser should render entities and relationships from IDs and indexes. If a
denormalized display field is missing, the browser should fall back to the
entity ID or relationship ID.

---

## Entity Export Records

Each exported entity should include enough normalized display data for the
browser to render a collapsed node without loading or deriving additional
records.

Suggested shape:

```json
{
  "id": "claim.jesus_created",
  "kind": "claim",
  "label": "Jesus is a created being.",
  "summary": "Jesus is a created being.",
  "details": {},
  "perspective": {
    "label": "JW",
    "source": "position"
  }
}
```

The exact `details` fields may vary by kind.

Evidence details may include:

```json
{
  "quotation": "all other things were created",
  "paraphrase": null,
  "source_id": "source.bible.nwt_2013",
  "source_label": "New World Translation of the Holy Scriptures (2013 Revision)",
  "locator": {
    "type": "verse",
    "value": "Colossians 1:16"
  }
}
```

Interpretation details may include:

```json
{
  "method": "translation_scope",
  "evidence_id": "evidence.nwt_2013.colossians.1_16.all_other_things_created",
  "related_evidence_ids": []
}
```

Argument details may include:

```json
{
  "role": "response"
}
```

The first exporter should keep enough original fields under `details` to make
the browser useful, but it should avoid dumping every raw YAML field when a
stable display field is better.

---

## Relationship Export Records

Each exported relationship should include:

```json
{
  "id": "relationship.jw.colossians_firstborn.supports_created",
  "type": "supports",
  "from_id": "interpretation.jw.colossians.1_15.firstborn_created_order",
  "to_id": "claim.jesus_created",
  "summary": "The created-order reading of firstborn is modeled as supporting the claim that Jesus is a created being.",
  "labels": {
    "outgoing": "Supports",
    "incoming": "Supported by"
  },
  "group": {
    "outgoing": "Supports",
    "incoming": "Supported by",
    "order": 7
  }
}
```

The exporter, not the browser, should define default group labels and sort
order.

The browser may still have fallback labels for forward compatibility.

---

## Indexes

The export should include relationship indexes:

```json
{
  "indexes": {
    "outgoing": {
      "claim.jesus_created": [
        "relationship.created.contradicts_uncreated"
      ]
    },
    "incoming": {
      "claim.jesus_created": [
        "relationship.jw.colossians_firstborn.supports_created"
      ]
    }
  }
}
```

Indexes should preserve deterministic order.

The browser should use these indexes for expansion rather than scanning all
relationships on every click.

---

## CLI Commands

The first web UI command should be:

```text
apologetics-catalog build-web
```

Default output path:

```text
generated/web/
```

The command should also support:

```text
apologetics-catalog build-web --output path/to/web-output
```

The command should:

* validate the catalog before writing output
* exit nonzero if validation fails
* avoid writing partial output when validation fails
* create the output directory if needed
* write only known generated files
* overwrite known generated files on each successful build
* avoid deleting unrelated files in the output directory
* produce deterministic output when the source catalog has not changed
* avoid opening a browser window

Known generated files for the first version:

```text
catalog.json
index.html
app.js
style.css
```

If stale generated files become a real problem, a later command may add an
explicit cleanup option:

```text
apologetics-catalog build-web --clean
```

The first milestone should also include a local static server command:

```text
apologetics-catalog serve-web
```

By default, `serve-web` should run `build-web` first, serve `generated/web/`,
and print the local URL.

Default server address:

```text
http://127.0.0.1:8000/
```

Useful options:

```text
apologetics-catalog serve-web --host 127.0.0.1
apologetics-catalog serve-web --port 8000
apologetics-catalog serve-web --output generated/web
apologetics-catalog serve-web --no-build
```

Server behavior:

* use Python's standard library HTTP server
* bind to `127.0.0.1` by default
* allow `--host 0.0.0.0` only when the user explicitly asks for network
  exposure
* fail clearly if the requested port is unavailable
* run in the foreground until interrupted with `Ctrl+C`
* print the URL once on startup
* avoid opening a browser window automatically
* serve static files only
* expose no editing API and no write endpoints
* send no-cache headers for development, at least for `catalog.json`

When `--no-build` is used, the command should verify that the output directory
already contains the expected files:

```text
index.html
catalog.json
```

If required files are missing, it should fail before starting the server with a
clear message such as:

```text
generated/web/catalog.json not found; run apologetics-catalog build-web first
```

A later `--open` flag may open the browser explicitly, but automatic browser
opening should not be the default behavior.

Serving locally is likely to be the normal workflow because some browsers block
`fetch()` access to local JSON when opening `index.html` through `file://`.

---

## First Implementation Milestone

The first milestone should stop at a useful read-only browser, before snapshot
exports.

It should include:

* `apologetics-catalog build-web`
* `apologetics-catalog serve-web`
* validation before output generation
* default output to `generated/web/`
* `--output` support
* local serving from `127.0.0.1:8000`
* `--host`, `--port`, `--output`, and `--no-build` support for `serve-web`
* foreground server lifetime, stopped with `Ctrl+C`
* no-cache headers for generated browser assets
* `catalog.json` with entities, relationships, incoming indexes, and outgoing
  indexes
* static `index.html`, `app.js`, and `style.css`
* exact-ID root loading
* first-level relationship groups
* expand/collapse behavior
* repeated-node and cycle protection
* basic evidence, source, and perspective display

It should not include yet:

* Markdown snapshot export
* plain text snapshot export
* self-contained HTML snapshot export
* editing
* publishing

Those export features are still part of the broader MVP, but they should follow
after the browser is useful enough to inspect the current catalog.

---

## Implementation Notes

Editable web assets should live in the Python package, not in `generated/`.

Initial source location:

```text
src/apologetics_catalog/web_static/
```

Initial asset files:

```text
index.html
app.js
style.css
```

These files should be included as Python package data so an installed
`apologetics-catalog` CLI can build the browser without relying on a repository
checkout layout.

`build-web` should load package assets through `importlib.resources` rather
than hard-coded paths relative to the current working directory.

The first viewer should use plain HTML, CSS, and JavaScript. It should not add
npm, a bundler, TypeScript, generated minified assets, or a frontend build step.

On every successful `build-web`, the command should copy package assets into
the output directory and overwrite the known generated files:

```text
catalog.json
index.html
app.js
style.css
```

Generated files are disposable. User edits inside `generated/web/` are not
preserved. The command should still avoid deleting unrelated files.

`catalog.json` is the frontend contract and should have focused exporter tests.
Those tests should verify:

* entity export records
* relationship export records
* incoming and outgoing indexes
* stable relationship group labels
* stable ordering
* deterministic output

If `generated_at` or similar build metadata is included, tests should be able
to inject a fixed timestamp.

The browser must render catalog content as text, not HTML. User-controlled
catalog fields such as summaries, quotations, source titles, locators, and
labels should be assigned with text APIs such as `textContent`, not injected
with `innerHTML`.

---

## Implementation Approach

The first implementation should be dependency-light.

Recommended sequence:

1. Add `apologetics-catalog build-web` with the validation-first output
   contract.
2. Write `generated/web/catalog.json`.
3. Include entities, relationships, incoming/outgoing indexes, display labels,
   and perspective/source summaries.
4. Add a static viewer scaffold under `generated/web/`.
5. Add `apologetics-catalog serve-web` using Python's standard library HTTP
   server.
6. Implement exact-ID root loading.
7. Implement first-level relationship groups.
8. Implement expand/collapse and repeated-node detection.
9. Add simple search.
10. Add Markdown and plain text snapshot export.
11. Add self-contained HTML snapshot export.

The MVP can use vanilla HTML, CSS, and JavaScript.

No React, Vite, TypeScript, package bundler, or frontend build step is required
unless the UI grows enough to justify that complexity.

The generated static viewer should normally be served by `serve-web` so browser
JSON loading behavior is predictable across environments.

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

The broader web UI MVP should include:

* Python CLI generation of `generated/web/catalog.json`
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

The MVP should read from generated JSON produced by the compiler rather than
raw YAML.

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
