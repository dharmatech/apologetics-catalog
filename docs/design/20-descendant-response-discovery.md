# Future: Descendant Response Discovery

## Status

Future exploration.

This document records a possible future navigation feature for the web UI
reasoning browser. It is not part of the current browser contract.

## Purpose

When browsing a tree projection of the catalog graph, a user may inspect an
argument and want to know whether any responses appear deeper under that
argument's displayed descendants.

For example, a node may use an interpretation or evidence node, and a response
may appear beneath that used node. The response may be semantically correct in
that location, but visually difficult to find through manual expansion.

Descendant response discovery would help the user find nearby responses without
changing the underlying graph or duplicating response nodes into places where
they do not semantically belong.

## Core Idea

Add an explicit navigation aid such as:

```text
Find responses
```

on suitable expanded nodes, especially argument nodes.

When activated, the browser searches the current tree projection below the
selected node and surfaces nearby response nodes. The user can choose a result,
and the browser expands the path needed to reveal that response in its normal
tree location.

The feature should discover and navigate to responses. It should not project,
transclude, or copy response cards into the current node by default.

## Tree Projection Boundary

The search should operate over the current tree projection, not over the whole
graph indiscriminately.

That means:

* search starts from the selected displayed node and path
* search follows the same relationship groups the browser would normally expose
* repeated-node and cycle guards still apply
* the search result should correspond to a path the browser can actually expand

This boundary matters because the catalog is a graph. Searching the unrestricted
graph from a node could surface surprising, cyclic, or semantically distant
results that are not part of the user's current browsing context.

## First Conservative Version

A conservative first version should:

* search descendants breadth-first
* prioritize the nearest response nodes
* identify response-bearing relationship groups such as `Responded to by` and
  `Responds to`
* show a short list of candidate responses
* let the user select one candidate
* expand the existing tree path to the selected candidate
* avoid reordering relationship groups
* avoid duplicating response cards outside their normal graph location

The first version does not need to search the entire catalog, rank responses by
importance, or infer which response is best.

## Relationship To Projected Quotes

Projected quotes and descendant response discovery solve different problems.

Projected quotes are lightweight supporting context. If an argument directly
uses an interpretation or evidence node with quotation text, the browser can
show that quotation near the argument without implying a new relationship.

Response discovery is a navigation feature. It should help the user find
responses buried under the current tree projection, but it should not imply
that the response is directly attached to the current node.

## Modeling Review Signal

If response discovery finds an awkward path, that may be a modeling signal.

For example:

```text
argument A uses evidence E
argument B responds_to evidence E
```

This may be correct if argument B is attacking the evidence itself. But if
argument B is really answering argument A's use of that evidence, the better
model may be:

```text
argument B responds_to argument A
```

The UI feature should not hide modeling problems. It should help reveal them.
Awkward discovered paths should prompt a modeling review rather than automatic
retargeting.

## Non-Goals

This feature should not:

* rewrite YAML relationships
* automatically retarget responses
* display projected response cards by default
* search the unrestricted graph without regard to the current tree path
* replace careful modeling of argument-to-argument responses
* decide which response is strongest

## Open Questions

Later design work should decide:

* whether hidden sections and hidden nodes are searched by default
* whether the search should include only visible relationship group types
* whether results should show distance, path summary, or relationship sequence
* whether the feature should be available on all node kinds or only arguments
* how result selection should interact with URL-encoded view state
* whether exports should include any trace of discovered-but-not-expanded
  responses

## Design Principle

The feature should make buried responses easier to find while preserving the
semantic honesty of the graph.

If a response belongs directly under the current argument, model it that way. If
the response belongs deeper in the tree, descendant response discovery can help
the user get there without pretending the graph says something else.
