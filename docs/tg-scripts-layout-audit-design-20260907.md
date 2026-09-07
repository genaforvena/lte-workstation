# TG scripts layout audit — scope and design

Ask: `20260907T150230Z`

The operator extended the existing scripts/code audit: keeping every script in one `scripts/`
directory is itself a maintainability problem. The audit therefore covers repository boundaries,
not only script contents.

## Intended outcome

Produce an evidence-backed map of the current executable surface and a safe, task-sized target
layout. The target must distinguish at least:

- `core`: shared mesh/task/ledger primitives and stable libraries;
- communication: Telegram, board, relay, and delivery surfaces;
- sensors/integrations: hardware, network, phone, and external-system adapters;
- operations: reflexes, watchers, wrappers, migration/deployment tools, and test drivers.

These are audit domains, not an instruction to create directories or move files immediately.

## Method and constraints

1. Inventory actual entrypoints, callers, imports, cron/reflex wiring, service references, tests,
   and generated/installed copies.
2. Classify by runtime role and dependency direction, recording ambiguous cases instead of forcing
   a category.
3. Identify duplicates, dead code, ownership hazards, and relocation risks from repository evidence.
4. Propose a layout and split it into reversible migration tasks with per-move verification and
   rollback. Do not perform bulk moves as part of the audit.

Acceptance requires durable artifacts for the inventory, proposed boundaries, concrete follow-up
tasks, and the verification commands that prove wiring did not regress.

## Frame-step evidence — 2026-09-07T15:12Z

This frame is the boundary/acceptance artifact for the dispatched chain step
`tg-scripts-layout-audit-20260907/frame-scope`, owned by `tg`. It does not claim that the
downstream inventory or target-layout steps are complete; those remain separate owner steps in
`docs/plans/2026-09-07-tg-scripts-layout-audit.tsv`.

The live repository confirms that `scripts/` is an overloaded executable surface: the inventory
contains 1,057 files, 800 executable files, and mixed shell, Python, Swift/Objective-C, service,
timer, fixture, and nested Reticulum assets. Wiring is not confined to that directory: `bootstrap.sh`
and `setup.sh` copy or install scripts, tests invoke repository paths directly, the `job/` lane
imports and launches mesh tools, and `charter/*.md` documents lane-specific boundaries. The
existing `job/README.md` explicitly keeps `job/mesh-job-*` together, so relocation must preserve
that separate lane boundary rather than flatten it into a new generic bucket.

The proposed domains are classification boundaries, not immediate directories. No file was moved
for this frame. Any later move must be one reversible slice, preceded by caller/wiring inventory,
and followed by source-vs-installed parity, syntax, focused `--test`, and the relevant service/cron
resolution checks. Rollback is the inverse move plus restoration of any generated or installed copy;
the migration is not accepted if a command only works from the repository root or if a live reflex
still resolves an old path.

## Verification run

```text
mesh-task status tg-scripts-layout-audit-20260907
  frame-scope [open] owner=tg; inventory-and-map [open] owner=genome;
  propose-layout-and-tasks [open] owner=genome
find scripts -type f | wc -l                         => 1057
find scripts -type f -perm -111 | wc -l             => 800
rg -n '(scripts/|mesh-(tg|chat|board|task|promises|phone|wifi|health|witness))' \
  --glob '!docs/**' --glob '!CLAUDE.md' .             => callers/wiring found in bootstrap.sh,
                                                       setup.sh, job/, tests/, and charters
```

The design file is present and hashes to
`fdf2851eb51d81ff4ca277b82774c6e7199cc7f32b7f4145ba09c5f3dd85a17e`. The verification is
scope-only: it establishes the evidence and acceptance contract while leaving the downstream map,
layout proposal, and all physical moves open.
