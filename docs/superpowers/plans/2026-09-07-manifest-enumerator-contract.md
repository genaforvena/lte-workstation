# Manifest Enumerator Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a checked-in manifest schema and one deterministic enumerator that inventories every regular file in `scripts/` and `job/` without moving or deploying anything.

**Architecture:** `manifest/mesh-manifest.schema.json` defines the TSV field vocabulary and classification contract. `scripts/mesh-manifest` is a dependency-free Python command that walks both source roots, emits stable TSV rows, fails on unknown classifications, and validates installed-basename collisions. A shell fixture test exercises top-level, nested, unit, fixture, generated-cache, and job-lane cases from outside the repository root.

**Tech Stack:** Python 3 standard library, POSIX shell, JSON Schema-shaped checked-in contract, TSV output.

## Global Constraints

- No source files move and no deployed files are changed in this slice.
- `scripts/` and `job/` are both genome source roots; nested regular files must not disappear.
- Every enumerated row records source path, installed basename, domain, kind, deploy policy, cadence policy, and compatibility owner.
- Unknown file classes and duplicate installed basenames are loud failures; no partial-glob fallback is allowed.
- The test must run from a temporary working directory and must not write to the live repository.

### Task 1: Define the manifest vocabulary and fixture matrix

**Files:**
- Create: `manifest/mesh-manifest.schema.json`
- Create: `docs/tg-scripts-layout-manifest-contract-20260907.md`

**Interfaces:**
- Produces the field names and allowed values consumed by `scripts/mesh-manifest` and its test.

- [ ] **Step 1: Record the schema and classification table**

Define the TSV columns as `source_path`, `installed_basename`, `domain`, `kind`, `deploy_policy`, `cadence_policy`, and `compatibility_owner`; define `domain` values `core`, `communication`, `integrations`, `operations`, `tests`, and `ux`; define `kind` values `tool`, `unit`, `asset`, `fixture`, and `library`; define deploy policies `install`, `systemd`, and `none`; define cadence policies `header`, `unit`, and `none`.

- [ ] **Step 2: Document fixture coverage and no-move boundary**

List the six required fixture classes: direct `scripts/mesh-*` tool, nested `scripts/<lane>/mesh-*` tool, `.service`/`.timer` unit, test/fixture input, `__pycache__/*.pyc` generated cache, and `job/mesh-*` tool. State that the first slice only adds inventory and validation; consumers migrate in later slices.

### Task 2: Add the failing contract test

**Files:**
- Create: `tests/test-mesh-manifest.sh`

**Interfaces:**
- Consumes: `scripts/mesh-manifest --check`, `--list`, and `--parity`.
- Produces: a deterministic pass/fail gate for the live tree and a synthetic fixture tree.

- [ ] **Step 1: Write the test before the implementation**

The test must invoke the not-yet-existing command from a temporary directory, assert the live inventory contains both `scripts/` and `job/` rows, assert the six fixture classes in a synthetic tree, assert a duplicate installed basename fails, and assert a file outside the two roots is ignored rather than silently classified.

- [ ] **Step 2: Run the test and verify the expected red failure**

Run `bash tests/test-mesh-manifest.sh` from `/tmp` and expect failure because `scripts/mesh-manifest` does not exist yet.

### Task 3: Implement the deterministic enumerator

**Files:**
- Create: `scripts/mesh-manifest`

**Interfaces:**
- `MESH_REPO=<repo> scripts/mesh-manifest --list` emits a header followed by stable tab-separated rows.
- `MESH_REPO=<repo> scripts/mesh-manifest --check` validates completeness, vocabulary, and basename uniqueness.
- `MESH_REPO=<repo> scripts/mesh-manifest --parity` emits the same source inventory plus an explicit deployed-owner status without mutating either tree.

- [ ] **Step 1: Walk both roots recursively and classify every regular file**

Use Python `os.walk`, prune no directories, sort paths, classify generated `__pycache__/*.pyc` as `asset`/`none`, classify tests and fixture paths as `fixture`, units by suffix as `unit`, executable `mesh-*` files as `tool`, and remaining source files as `library` or `asset`; derive domains from the path and explicit `uxn`/`tests`/`job` boundaries.

- [ ] **Step 2: Make unknowns and collisions fatal**

Reject paths that cannot receive an allowed kind/domain/policy tuple. Reject two installable rows with the same basename and print both source paths. Never emit a partial inventory after an error.

- [ ] **Step 3: Add deployed parity as report-only**

For installable rows, compare `~/.local/bin/<installed_basename>` when present and report `present`, `missing`, or `different`; never copy, delete, or chmod anything.

### Task 4: Run the red-green verification and preserve evidence

**Files:**
- Modify: `docs/tg-scripts-layout-manifest-contract-20260907.md`

- [ ] **Step 1: Run the focused fixture test from outside the repo**

Run `(cd /tmp && bash /home/mesh-home/lte-workstation/tests/test-mesh-manifest.sh)` and require PASS.

- [ ] **Step 2: Run syntax and live checks**

Run `python3 -m py_compile scripts/mesh-manifest`, `scripts/mesh-manifest --check`, and `scripts/mesh-manifest --parity`; record row count, duplicate result, and the six fixture assertions in the contract note.

- [ ] **Step 3: Record the exact rollback and handoff**

State that rollback deletes only the new schema, command, test, plan, and contract note; no existing source or deployed copy is touched. Include the exact next slice: wire one enumerator consumer to `mesh-manifest --list` after the live inventory is reviewed.
