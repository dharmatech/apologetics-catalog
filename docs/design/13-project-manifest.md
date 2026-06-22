# v0.1 Project Manifest

## Purpose

This document defines how a v0.1 dataset is discovered and configured.

The manifest answers:

* where the dataset root is
* which schema version governs the dataset
* which YAML files are source content
* where generated outputs should be written
* where project-wide vocabulary extensions are declared
* how CLI commands find the dataset

The manifest is project-wide configuration. Content files define records.

---

## Manifest Location

The initial project should use one root manifest:

```text
apologetics.yaml
```

The manifest should live at the repository root.

v0.1 assumes one dataset per repository.

Later versions may allow multiple manifests or nested datasets, but v0.1 should
not require the compiler to guess between datasets.

---

## Manifest Envelope

The manifest uses the same envelope pattern as other YAML documents.

Required envelope fields:

```yaml
schema_version: "0.1"

kind: project
```

The manifest's `schema_version` defines the dataset schema version.

Content files still declare their own `schema_version` and `kind`, but in v0.1
content file schema versions must match the manifest schema version.

Mixed-version datasets should be rejected rather than automatically migrated.

---

## Minimal Manifest Shape

Example:

```yaml
schema_version: "0.1"

kind: project

project:
  id: project.apologetics
  title: "Apologetics Viewpoint Catalog"
  description: >
    A neutral catalog of competing apologetics viewpoints.

content:
  include:
    - content/**/*.yaml
  exclude:
    - generated/**

outputs:
  generated_dir: generated

vocabulary_extensions:
  relationship_types:
    - id: project.appeals_to_liturgical_usage
      label: "Appeals to liturgical usage"
      description: >
        Used when an argument appeals to historical worship practice.
```

Required top-level fields:

```text
schema_version
kind
project
content
```

Optional top-level fields:

```text
outputs
vocabulary_extensions
```

---

## Project Metadata

The `project` object identifies the dataset.

Required fields:

```text
id
title
```

Optional fields:

```text
description
```

The project ID is used by generated outputs when they need an external key that
is unique beyond the local dataset.

Example:

```text
project.apologetics#claim.jesus_created
```

Author-written references inside YAML should still use local entity IDs.

---

## Content Discovery

The `content.include` list is required in v0.1.

Example:

```yaml
content:
  include:
    - content/**/*.yaml
```

Include patterns are resolved relative to the manifest file.

`content.exclude` is optional.

Example:

```yaml
content:
  include:
    - content/**/*.yaml
  exclude:
    - content/drafts/**
```

Exclude patterns are resolved relative to the manifest file and apply after
includes.

Duplicate file matches should be de-duplicated before parsing.

If an include pattern matches no files, validation should fail with an error.

This prevents a project from appearing valid only because no source files were
loaded.

---

## Always-Excluded Paths

The compiler should never scan generated output directories as source content.

The compiler should also skip hidden version-control, tool, and cache
directories.

Always-excluded examples:

```text
.git/**
.codex/**
.agents/**
generated/**
```

The generated output directory from `outputs.generated_dir` is always excluded,
even if an include pattern accidentally matches it.

---

## Generated Outputs

Generated outputs are derived artifacts.

The default generated output directory is:

```text
generated
```

The manifest may override it:

```yaml
outputs:
  generated_dir: build/apologetics
```

Relative output paths resolve relative to the manifest file.

Generated outputs should not be treated as source content.

---

## Vocabulary Extensions

Project-wide vocabulary extensions should be declared in the root manifest in
v0.1.

Individual content files should not declare vocabulary extensions.

Example:

```yaml
vocabulary_extensions:
  relationship_types:
    - id: project.appeals_to_liturgical_usage
      label: "Appeals to liturgical usage"
      description: >
        Used when an argument appeals to historical worship practice.
```

This keeps extension review and validation centralized.

Later versions may allow imported vocabulary files if the extension set grows.

---

## Configuration Ownership

The root manifest owns project-wide configuration in v0.1.

Content files should not override:

* schema version policy
* content roots
* exclude rules
* generated output paths
* vocabulary extension policy

Content files still declare `schema_version` and `kind` so they remain
self-describing, editor-friendly, and easier to validate in isolation.

---

## CLI Root Resolution

When run from the repository root, commands should use:

```text
./apologetics.yaml
```

Commands should also accept an explicit manifest path:

```text
apologetics validate --manifest path/to/apologetics.yaml
apologetics build --manifest path/to/apologetics.yaml
```

If no manifest is found, the command should fail with a clear diagnostic.

If multiple manifests would be discovered by a future search mode, the command
should not guess. It should require `--manifest`.

Paths inside the manifest resolve relative to the manifest file, not the
process current working directory.

Generated output paths also resolve relative to the manifest file unless a later
version explicitly allows absolute paths.

---

## Validation Behavior

The compiler should validate:

* the manifest file exists
* the manifest envelope is valid
* `kind` is `project`
* `schema_version` is supported
* project metadata is present
* `content.include` is present and non-empty
* every include pattern matches at least one file
* excludes are applied after includes
* generated and hidden directories are not scanned
* content file schema versions match the manifest schema version
* vocabulary extensions appear only in the manifest
* generated output paths do not overlap source content

Manifest diagnostics should be emitted before record-level diagnostics when
manifest errors prevent reliable dataset discovery.
