---
name: mesh-invariants
description: Use when adding, editing, or removing a rule or invariant in MESH.md — the shared base instruction every mind receives. Keeps rule IDs unique, the registry rev moving, and both gates green.
---

# Mesh invariants

`MESH.md` (repo root) is the one editable, engine-neutral list of procedural
mesh rules, wake-injected into every mind. A rule edited anywhere else does not
reach all agents. This skill is the only path for changing it.

## Procedure

1. Read `MESH.md` in full. Rules live under `## Rules` as `mesh:N` bullets;
   operator invariants live under `## Invariant registry` as
   `id | owner | scope | precedence | source | preflight` rows with a
   `rev: YYYYMMDD.N` header.
2. Change exactly one thing per edit: add a bullet with a fresh unique ID,
   edit one bullet in place, or add/edit one registry row. English only.
3. Bumping the registry: any registry change bumps `rev` (same day → `N+1`).
   A row's `source` must cite operator-verbatim + date; `preflight` must name
   the live check a claim under it has to record. Never cite a stale `rev`.
4. Verify, by your own hand, both gates:
   - `tests/test-mesh-mind-rules-wake.sh` → PASS
   - `mesh-rules --check <path-to-edited-MESH.md>` → PASS
   A red gate is fixed here, never worked around.
5. Route landing to the owner: `[task]` with `owner: mesh-land/genome` naming
   the rule ID and both gate results. The skill ends at a verified working
   tree, never at a bare push.
6. Announce on the board (`[fyi]`) what changed and its evidence — FYI is the
   announcement, not the durability; the file is.
