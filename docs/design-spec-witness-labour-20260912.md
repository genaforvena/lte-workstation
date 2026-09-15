# Witness labour-tape design spec audit — 2026-09-12

Audited `docs/superpowers/specs/2026-07-24-witness-labour-tape-design.md` against its
implementation, deployed command paths, focused self-tests, and live witness panes. This is an
audit receipt; no implementation code was changed.

## Findings

- **Rolling labour tree: implemented and verified.** `scripts/mesh-labor` provides
  `--balance --rolling`, groups the rolling five-hour count by window, and computes a trailing
  checksum using the independent ISO-string tally. `bash scripts/mesh-labor --test` passed GATE5
  (counts and zero), GATE5b (exclusive lower boundary and a deliberately divergent mutated parser),
  and the remaining labor checks. The deployed `~/.local/bin/mesh-labor` is a regular copy with the
  same SHA-256 as the source (`624ff7a7…b040d8f2`).
- **Standalone witness render: implemented and verified.** `scripts/mesh-witness` calls the live
  labor command, places the tree after measurements and before the resource footer, and prints a
  loud fallback on failure. The deployed path resolves to the source symlink
  (`f1de8cc…d7db0713`). `python3 scripts/mesh-witness --test` exited 0 with `smoke-test: ok`; a live
  `python3 scripts/mesh-witness --pane --embed` render showed the tree, per-window accounts, and a
  trailing computed `0`.
- **The spec's promise-ledger footer is absent from the current renderer.** The live standalone
  output contains the labour tree, resource ledger, task witness, and raw ledger tail, but no
  `promise ledger` section. `mesh-promises` contributes to ask metrics elsewhere in the witness
  code; that does not satisfy the spec's promised-footer requirement. This is an implementation
  divergence requiring a decision or follow-up, not a completed spec item.
- **The spec's integration assertion is stale for the named dash route.** Live
  `mesh-dash --once witness` rendered `WITNESS TASKS — structured unfinished work` from
  `~/.mesh/tasks.journal`, with task-state tags such as `OPEN_UNOWNED` and `QUEUED`; it did not
  render the labour tree. The standalone `mesh-witness --pane --embed` output is real evidence for
  that renderer only, not proof that this dash route composes it. The top-level labour tree itself
  reports per-window counts (including `witness` and `tg`), without task attribution tags.
- **The optional window override remains intentionally deferred.** The spec's interface paragraph
  mentions `--window-hours N`, while its open-question paragraph parks it and the implementation
  plan explicitly excludes it. Current behavior uses `MESH_LABOR_WINDOW_H`, matching `--budget`.
  Resolve the spec's internal ambiguity before treating the override as an unmet implementation
  obligation.
- **Integration suite limitation:** the prior same-day plan audit recorded
  `scripts/mesh-dash --test` failing its unrelated `mesh-forage` division-of-labour pane assertion
  after a 180-second run. The current audit did not rerun that expensive suite; its result is
  documented in `docs/design-audit-witness-labour-20260912.md`.

## Evidence and source identity

```text
scripts/mesh-labor   624ff7a739d609382ec722a555148617b9471755d256c4278e57b8e5b040d8f2
~/.local/bin/mesh-labor same SHA-256 as source
scripts/mesh-witness f1de8ccdaf7834404c4e6c7fec1e6cd9fb6fc6569196bbb2a9a6d862d7db0713
~/.local/bin/mesh-witness resolves to scripts/mesh-witness
scripts/mesh-dash    3fb9fb18622af512197d91ff048147c3d8d0736e3024b44f7e154ddf58526f22
```

Commands run:

- `bash scripts/mesh-labor --test` — PASS.
- `python3 scripts/mesh-witness --test` — PASS, exit 0.
- `python3 scripts/mesh-witness --pane --embed` — live tree present, trailing balance `0`.
- `mesh-dash --once witness` — task-journal view only; no labour section.
- `tmux list-panes -a` — no pane named `witness`; live sessions are `mesh-home` windows.

## Remaining obligation

Treat the standalone labour renderer as implemented, while leaving fused-pane integration and the
missing promise-ledger footer unresolved. The next action is to identify the intended live host for
`mesh-witness --pane` and either wire/verify that route or revise the spec to name the actual route;
then reconcile the absent promise footer and close only the requirements that have live evidence.
