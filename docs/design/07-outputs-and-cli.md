# Generated Outputs and CLI

## Generated Outputs

Generated artifacts may include:

```text
generated/json
generated/catalog
generated/html
generated/markdown
generated/python
generated/typescript
generated/graph
```

Future targets may include:

```text
generated/ocaml
generated/haskell
generated/lean
```

Generated outputs are derived artifacts.

They are not authoritative.

The YAML source remains the canonical representation.

Generated outputs may reorganize the data into forms optimized for machines.

Examples:

```text
generated/json/questions.json
generated/json/claims.json
generated/json/evidence.json
generated/json/relationships.json
generated/catalog/catalog.json
generated/graph/full.graph.json
```

Generated output paths should default to the manifest's `outputs.generated_dir`
value, as defined in [v0.1 Project Manifest](13-project-manifest.md).

Graph databases, search indexes, HTML views, and query-oriented stores should be
treated as generated projections unless the project explicitly changes the
canonical storage model.

The normalized catalog output should preserve the compiler's validated
intermediate representation.

The graph output should be a projection derived from that normalized catalog.

Generated graph edges should distinguish first-class relationship records from
derived structural references.

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
migrate
```

These commands should remain simple and implementation-independent.

By default, commands should resolve the project manifest from the current
working directory using:

```text
./apologetics.yaml
```

Commands should also accept:

```text
--manifest path/to/apologetics.yaml
```

Paths inside the manifest should resolve relative to the manifest file, not the
shell's current working directory.

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

The `migrate` command should handle explicit schema migrations.

Examples:

```text
migrate --to 0.2
migrate --to 0.2 --write
migrate --to 0.2 --output migrated/
```

Migration commands should never be implied by `build`.

Without `--write`, migration commands should preview or write to an explicit
output location rather than modifying source files in place.
