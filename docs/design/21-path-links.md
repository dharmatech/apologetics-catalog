# Path Links

## Status

Draft.

This document defines a first design for shareable path links in the web UI
reasoning browser.

## Purpose

The browser already supports copying an exact view link that preserves detailed
UI state. That is useful for restoring a carefully crafted view, but the URL can
become very long because it stores expanded paths, hidden sections, hidden
nodes, quote state, and node display modes.

Many shareable views do not need to preserve every UI toggle. They only need to
show a clear reasoning chain from the current root node to a selected displayed
node.

Path links should provide a shorter, semantic sharing mechanism:

```text
Show the path from this root entity to this selected entity occurrence.
```

The path should be derived from the catalog graph and the current tree
projection. It should not be a freeform presentation mode.

## First Feature

Add a per-node path-copy affordance for displayed non-root nodes.

```text
click entity ID -> copy path link
```

The first version should avoid adding another full text button to each node
header. Node headers already contain several controls, and a `Copy Path` button
would add visual weight to every displayed node.

Instead, the displayed entity ID should act as the path-copy control:

* in ID mode, the main entity ID is clickable
* in full mode, the smaller entity ID line is clickable
* the root node's ID is not a path-copy control because the root has no path
  from itself
* the clickable ID should have a tooltip such as `Copy path link from root to
  this node`
* the clickable ID should have a subtle hover/focus treatment so it is
  discoverable
* the interaction should be keyboard accessible

If this proves insufficiently discoverable, a later version may add a compact
icon-only button with a tooltip. The first version should not add another large
text button.

When clicked, the browser copies a path link from the current root node to that
specific displayed node occurrence.

This avoids ambiguity. A global "copy current path" button would have to guess
which branch or deepest node the user intended. A per-node action lets the user
say exactly which displayed chain they want to share.

## Path Contents

The first version should include the full displayed entity sequence from the
root to the selected node occurrence.

For example:

```text
claim.jesus_created
interpretation.jw.colossians.1_15.firstborn_created_order
argument.trinitarian.firstborn_not_necessarily_created
argument.jw.firstborn_usual_meaning_response
argument.trinitarian.john_1_3_created_things_response
```

The URL should not store every expanded group or hidden-node setting. It should
store only the semantic entity waypoints needed to reconstruct the selected
chain.

The first version should not try to minimize the waypoint list. If the user
copies a path from the root to a node, the copied link should preserve the exact
displayed entity chain.

The first version should store entity IDs only. It should not store
relationship IDs between adjacent nodes.

Entity-only waypoints are shorter and easier to inspect. If multiple
relationships connect the same adjacent entities, the browser should resolve the
displayed path using deterministic relationship ordering. Relationship-aware
path links may be added later if real ambiguity requires them.

## Rendering A Path Link

When a path link is opened, the browser should render a focused path view.

The first rendering behavior should be:

* show only the nodes on the path
* show nodes in ID mode by default
* show direct quotes by default when available
* show projected quotes by default when available
* auto-expand only the groups needed to reveal the next path node
* hide off-path sibling nodes by default
* preserve normal relationship labels between path nodes
* keep repeated-node and cycle protections active

The result should be a clean chain of reasoning that the user can expand from
if they want more surrounding context.

Opening a path link should not require the exact UI state that existed when the
link was copied. The browser should reconstruct the focused path from the
waypoint list and the current catalog graph.

The browser should expand only the relationship groups and node occurrences
needed to reveal the path. It should not restore unrelated expansion, hiding,
or display-mode state.

The focused path view does not need a special exit mode. The user can open any
entity as a new root or expand outward from path nodes using the normal browser
controls.

## URL Shape

The first version should use a hash fragment:

```text
#path=v1:claim.jesus_created~interpretation.jw.colossians.1_15.firstborn_created_order~argument.trinitarian.firstborn_not_necessarily_created
```

Reasons:

* the path state is client-side
* GitHub Pages does not need to route or understand the path state
* the fragment is not sent to the static host as part of the HTTP request
* `v1:` leaves room for future path encodings

The path should use readable semantic IDs over generated compact aliases.

Earlier possible forms included:

```text
#path=claim.jesus_created~interpretation.jw.colossians.1_15.firstborn_created_order~argument.trinitarian.firstborn_not_necessarily_created
```

The versioned form is preferred for v1.

The encoding should:

* preserve entity IDs exactly
* be URL-safe
* be deterministic
* remain readable enough for debugging
* allow future versioning if the format changes

Existing exact view links use a `#view=...` fragment. Those links should keep
working.

If both a view state and a path state are present, the exact view state should
win because it is more explicit.

## Ambiguity

There may be multiple graph paths between two entity IDs.

The first version avoids this problem by copying the full displayed entity
sequence, not merely a start ID and end ID. The user already selected a
particular displayed occurrence, so the link should preserve that sequence of
waypoints.

When rendering the path, the browser should find each adjacent pair in the
waypoint sequence using the current catalog graph and deterministic relationship
ordering.

If an adjacent waypoint cannot be connected, the browser should show a clear
error rather than inventing a connection.

If a waypoint entity ID no longer exists, the browser should show a clear error
identifying the missing ID.

If adjacent waypoints are connected by more than one relationship, the first
version should use the same deterministic relationship ordering as the normal
browser. If this becomes confusing in real use, a later version may encode
relationship IDs between waypoints.

Later versions may allow manually entered waypoint lists, path search, or path
choice among multiple candidates. Those are not required for the first version.

## Copy Behavior

When copying a path from a displayed node, the implementation should extract the
entity sequence from the node's displayed tree occurrence path. It should not
search the graph again to decide what the user meant.

This preserves the path the user is actually looking at.

After a successful click, the browser should show a status message:

```text
Path link copied.
```

The browser should also update the address bar to the copied path link. This
matches the existing exact view-link behavior and gives the user a fallback if
clipboard access is blocked.

If clipboard access fails, the browser should show:

```text
Path link added to the address bar. Copy it from there.
```

## Testing Target

The first implementation should be tested against the current motivating chain:

```text
claim.jesus_created
interpretation.jw.colossians.1_15.firstborn_created_order
argument.trinitarian.firstborn_not_necessarily_created
argument.jw.firstborn_usual_meaning_response
argument.trinitarian.john_1_3_created_things_response
argument.jw.colossians_1_16_all_other_things_response
argument.trinitarian.nwt_1984_bracketed_other_response
```

The test or manual smoke check should verify that:

* the copied path link opens from GitHub Pages-compatible static hosting
* only the path chain is shown initially
* nodes render in ID mode by default
* direct quotes are visible where available
* projected quotes are visible where available
* off-path sibling nodes are hidden by default
* normal expansion controls still work from the path view

## Relationship To Exact View Links

Path links and exact view links solve different problems.

Exact view links preserve detailed UI state. They are precise but can become
long.

Path links preserve a semantic reasoning chain. They should be much shorter and
more suitable for public sharing, README examples, documentation, email, chat,
and social media.

Both can exist:

* `Copy View Link`: preserve the current UI state
* `Copy Path`: share the chain from the current root to this node

## Relationship To Freeform Presentation

Path links are not freeform presentation documents.

They should not allow arbitrary unrelated nodes to be listed in an invented
order. Every adjacent step in the copied path must be justified by the catalog
relationship graph and the browser's tree projection.

This preserves the core design principle that the browser displays graph-derived
reasoning chains, not manually assembled slide-like outlines.

## Compact Identifiers

The first version should use the catalog's semantic entity IDs in path URLs.

Permanent secondary compact IDs, such as hexadecimal aliases, are not part of
this design. They would shorten URLs, but they would also add identity
management burden, merge-conflict risk, and another identifier authors would
need to preserve.

Generated compact aliases may be explored later, but only with care around
catalog versioning and stale links.

## Future Work

Possible later features:

* manual path entry using one entity ID per line
* path search between two waypoints
* path choice when multiple routes exist
* `Copy Minimal Path` that removes unnecessary waypoints
* compact path encoding
* compression for exact view links
* curated named path links in documentation
* opening a normal browser view from a path view
* exporting a path view as Markdown, plain text, or standalone HTML

## Non-Goals

The first version should not:

* replace exact view-state links
* optimize waypoint lists
* add permanent secondary IDs
* add server-side saved views
* require a database
* rely on GitHub Pages server behavior
* create a freeform presentation mode
* silently connect entities that are not related in the graph

## Design Principle

Path links should make the strongest current browser behavior easy to share: a
clean, graph-derived chain of reasoning from one node to another.

The user should be able to browse naturally, find a compelling endpoint, click
`Copy Path`, and get a shorter link that reconstructs that reasoning chain
without preserving every UI detail.
