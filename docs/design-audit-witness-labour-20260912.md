# Witness labour-tape plan audit — 2026-09-12

Audited `docs/superpowers/plans/2026-07-24-witness-labour-tape.md` against the current source,
deployed command paths, focused tests, rendered witness output, and the live `witness` tmux window.
This is an audit receipt; no implementation files were changed.

## Findings

- **Task 1 is implemented and its focused test passes.** `scripts/mesh-labor` contains
  `independent_window_tally`, `do_balance_rolling`, the `--balance --rolling` dispatch, and GATE5
  checks for per-window grouping, zero balance, exclusive lower-bound handling, and a mutated
  parser divergence. `bash scripts/mesh-labor --test` ended `PASS`.
- **The deployed `mesh-labor` path is a symlink to the current source**,
  `/home/mesh-home/.local/bin/mesh-labor -> /home/mesh-home/lte-workstation/scripts/mesh-labor`.
  It is not a separate deployed copy. `mesh-labor --balance --rolling` renders the budget and
  expense accounts, per-window rows, and a trailing checksum.
- **Task 2 is implemented and its focused test passes.** `scripts/mesh-witness` has the
  `MESH_LABOR_BIN` injection, `_labour_tree()` live call, primary labour section before the resource
  footer, and failure fallback. `python3 scripts/mesh-witness --test` ended `smoke-test: ok`. The
  deployed `mesh-witness` path is likewise a symlink to the workspace source. A real
  `python3 scripts/mesh-witness --pane --embed` render showed the labour tree directly after the
  measurement block and the resource ledger below it.
- **The rolling checksum was transiently non-zero in a live render.** One render showed 256 turns
  and a trailing `1`; an immediate traced render showed 255 and `0`, and five further runs showed
  `0`. The tally and independent checksum parse the live spend log in separate reads, so an append
  between those reads is a plausible explanation, but this audit did not prove the cause. The
  fixture test passes and did not exercise concurrent log growth.
- **Task 3's recorded integration expectation does not match the current `mesh-dash` route.**
  `timeout 20 scripts/mesh-dash --once witness` rendered `WITNESS TASKS — structured unfinished
  work` from `tasks.journal`, with no labour section. The live `mesh-home:witness.0` pane showed the
  same task surface; `witness.1` is the Codex prompt. The standalone witness renderer does show the
  labour tree, but the current witness dash frame does not compose it. The plan's assertion that
  this command is the host of the fused labour pane is therefore stale or needs a newly identified
  integration path.
- **The full dash suite fails on an unrelated pane-wiring assertion.**
  `timeout 30 scripts/mesh-dash --test` exited 124, so it was rerun with a 180-second cap. The
  longer run exited 1 with `smoke-test: FAIL (minds frame missing the division-of-labour axis —
  mesh-forage output not wired into the pane)`. This does not identify a labour-tree regression, but
  it prevents the plan's expected `smoke-test: ok` from being claimed.

## Reproduction record

- `bash scripts/mesh-labor --test` — PASS, including GATE5 and GATE5b.
- `python3 scripts/mesh-witness --test` — PASS (`smoke-test: ok`).
- `mesh-labor --balance --rolling` — live tree rendered; first observed trailing checksum was `1`.
- `python3 scripts/mesh-witness --pane --embed` — live labour tree rendered; subsequent traced tree
  had checksum `0`.
- `timeout 20 scripts/mesh-dash --once witness` — task-journal panel rendered, no labour tree.
- `timeout 30 scripts/mesh-dash --test` — timed out with status 124.
- `timeout 180 scripts/mesh-dash --test` — FAIL, status 1; missing mesh-forage division-of-labour
  pane axis.

Source hashes at audit time:

```text
scripts/mesh-labor  624ff7a739d609382ec722a555148617b9471755d256c4278e57b8e5b040d8f2
scripts/mesh-witness f1de8ccdaf7834404c4e6c7fec1e6cd9fb6fc6569196bbb2a9a6d862d7db0713
scripts/mesh-dash    2fe1e601eea544a5841fc45660bcd0ad750142e41acd36da62f9ee0d7ec2d423
```

## Remaining obligation

Reconcile the stale Task 3 integration claim with the current task-only `mesh-dash --once witness`
route, then verify the actual intended live pane path. The full dash smoke failure also needs its
separate mesh-forage wiring investigation. Do not mark the plan's fused-pane integration complete
from the standalone `mesh-witness` render alone.
