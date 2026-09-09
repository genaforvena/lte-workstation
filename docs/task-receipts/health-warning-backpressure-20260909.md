# Health-warning backpressure — 2026-09-09

## Result

`mesh-health-warning-task` now admits a new health-warning triage only while
the Health ledger has an empty sent/open queued slot and no more than one
running health-warning triage. When both bounded slots are occupied, it writes
the unchanged cursor and retries the exact source event on a later cadence.
Existing durable partial-create dispatch recovery and blocked/complete
dispositions remain unchanged.

## Verification

- Red regression: the replay fixture failed before the admission gate by
  creating all three historical warning chains while one running and one
  queued slot were occupied.
- Green regression: `python3 tests/test-mesh-health-warning-task.py` passed;
  the full fixture also covers partial-create dispatch recovery, terminal
  dispositions, deduplication, and cursor retention.
- `python3 scripts/mesh-health-warning-task --test` passed.
- `python3 -m py_compile scripts/mesh-health-warning-task` passed.
- `git diff --check` passed.
- Source/deployed parity after `mesh-land --apply`:
  `87365bb9ecf197fc66058dc85ec058672b689c92e5ce98a8a1a10f811c96947d` for
  both `scripts/mesh-health-warning-task` and
  `~/.local/bin/mesh-health-warning-task`.
- Safe fixture used a temporary mesh, chat log, replay ledger, and fake
  `mesh-task`; no live task state was mutated by the regression.
- Pre-fix live dash reported `backlog=3`; this change did not delete,
  reclassify, or falsely terminalize that backlog.
- Landed source commit: `f64a7b97`, pushed by `mesh-land` and deployed locally.

## Handoff

Regression test and this receipt remain to be committed as the task's test
artifact; next action is a path-limited commit followed by `mesh-land
--push-heal`.
