# Generated Outputs and CLI

## Generated Outputs

Generated artifacts may include:

```text
/generated/json
/generated/html
/generated/markdown
/generated/python
/generated/typescript
/generated/graph
```

Future targets may include:

```text
/generated/ocaml
/generated/haskell
/generated/lean
```

Generated outputs are derived artifacts.

They are not authoritative.

The YAML source remains the canonical representation.

Generated outputs may reorganize the data into forms optimized for machines.

Examples:

```text
/generated/json/questions.json
/generated/json/claims.json
/generated/json/evidence.json
/generated/json/relationships.json
/generated/graph/full.graph.json
```

Graph databases, search indexes, HTML views, and query-oriented stores should be
treated as generated projections unless the project explicitly changes the
canonical storage model.

---

## Strongly Typed Future

YAML is the authoring format.

The architecture should permit generation of strongly typed representations.

Potential targets:

* Python
* TypeScript
* OCaml
* Haskell
* Lean

The design should not assume any particular implementation language.

---

## Command-Line Interface

Initial commands:

```text
validate
build
graph
query
```

These commands should remain simple and implementation-independent.

The `validate` command should support human-readable diagnostics by default.

It should also support machine-readable JSON output.

Examples:

```text
validate
validate --format json
validate --warnings-as-errors
```

Warnings should not fail validation by default.

The `--warnings-as-errors` option allows stricter CI or release workflows.
