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
