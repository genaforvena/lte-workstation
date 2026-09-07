# Design/audit task sweep — 2026-09-07

## Scope

This sweep covers executable Markdown plans in `docs/superpowers/plans/` and `docs/plans/`,
plus current repository design/audit artifacts that describe work rather than merely recording a
closed result. Literature reviews and historical result-only reports are not silently treated as
implementation plans; they are listed as excluded scope and need an explicit operator ask before
becoming code work.

## Findings

The plan checkboxes are not authoritative. Seven older implementation plans still contain only
`[ ]` markers even though corresponding tools and landed commits exist. Conversely, the three
2026-09-07 expansion plans explicitly say `plan only`, and the scripts layout chain is still open
at `propose-layout-and-tasks`. The ledger therefore needs a reconciliation task per plan, with a
real artifact and an explicit `DONE`, `BLOCKED`, or `DECLINED` disposition for every internal step.

The sweep chain is `design-audit-task-sweep-20260907`. Its TSV contains one ordered task for each
plan/design family. A task may close only after it has checked the plan's internal steps against
code, artifacts, wiring, and verification evidence; a green self-test alone is insufficient.

## Initial evidence

- `rtk python3 scripts/mesh-task --test` passed.
- `tests/test-mesh-task-ledger-sync.sh` passed.
- `tests/test-mesh-task-audit-complete.sh` passed.
- The model plan's Python entrypoints were incorrectly invoked through `bash` during the sweep;
  both `scripts/mesh-model-bench --test` and `scripts/mesh-model-resolve --test` exited 2 with
  shell syntax errors. This is recorded as an open repair task, not a pass.
- `tg-scripts-layout-audit-20260907` remains active at `inventory-and-map`/`propose-layout-and-
  tasks`; its map explicitly forbids bulk moves before enumerator and installed-path evidence.

## Required disposition

Every row in `docs/plans/2026-09-07-design-audit-task-sweep.tsv` is a durable mesh task. For each
row, the owner must either execute the plan's remaining work, or publish a concrete refusal/block
with the missing authority, dependency, or safety boundary. “Design exists” and “tests exist” are
not closure evidence.

