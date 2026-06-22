# Initial Scope and Success Criteria

## Initial Scope

The first implementation should focus on a single question:

```text
Is Jesus a created being?
```

Initial sources:

* John 1:1
* John 1:3
* Colossians 1:15-17
* Revelation 3:14
* Proverbs 8:22
* Hebrews 1:3
* Hebrews 1:6
* Philippians 2:6-11

The initial Scripture evidence should follow
[v0.1 Scripture Sources](14-scripture-sources.md), including concrete
translation sources, full-book-name locators, source-specific quotations, and
short quotation policy.

Initial positions:

* Jehovah's Witnesses
* Arian
* Nicene Trinitarian

Initial deliverables:

* YAML dataset
* schema validation
* compiler prototype
* JSON generation
* HTML generation
* graph visualization
* command-line query interface

The first apologetics dataset should follow the authoring rules in
[v0.1 Modeling Guidelines](11-modeling-guidelines.md), especially the rules for
neutral summaries, representative-first modeling, symmetrical treatment of major
positions, and minimum completeness for a modeled position.

---

## Success Criteria

The project should successfully model competing interpretations of evidence without embedding truth judgments into the core data model.

The architecture should remain sufficiently general that the same schema can later represent non-theological domains without requiring fundamental redesign.
