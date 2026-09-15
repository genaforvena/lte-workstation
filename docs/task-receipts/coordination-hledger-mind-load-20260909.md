# Mind/load H-Ledger report — 2026-09-09

Task: `coordination-hledger-reconciliation-extension-20260909/mind-load-report`

## Result

Added `scripts/mesh-hledger-mind-load`, a read-only report over the frozen board and TURN
spend sources. It uses `mesh-task replay --json` for the task population, chat lifecycle
events for reopen/rework evidence, and explicit `task:` tags in `spend.log` for effort.
It writes only the requested report output; it does not write any journal, ledger, task, or
routing state.

The report keeps these axes separate per mind: task volume, tagged TURN effort, age,
rework/reopen, completion, outcome evidence, unattributed tasks, and unknown-source count.
It also publishes denominators for owner, effort attribution, and outcome evidence coverage.

## Live artifact

Report: [`coordination-hledger-mind-load-20260909.report.txt`](coordination-hledger-mind-load-20260909.report.txt)

Frozen cutoff: `2026-09-09T02:54:51Z`

SHA-256: `bc6c15e3a03117903126742e808fe313a7a536b5d19bc6f9a69195836fc70110`

Selected live rows:

```text
mind=genome tasks=53 effort_turns=17 age_seconds=43412 rework_reopen=6 completion=44/53 outcome_evidence=44/44 unattributed=42 unknown=0
mind=tg tasks=58 effort_turns=3 age_seconds=125380 rework_reopen=26 completion=18/58 outcome_evidence=18/18 unattributed=55 unknown=0
mind=witness tasks=27 effort_turns=40 age_seconds=15489 rework_reopen=2 completion=20/27 outcome_evidence=20/20 unattributed=16 unknown=0
coverage=task_owner=330/330 effort_task_attribution=188/6186 outcome_evidence=159/161
```

## Plan comparison and load-balancing signal

This satisfies the extension plan’s requirement to expose volume, effort, age, rework,
completion, and attribution coverage without minting a new `EFFORT` commodity or treating
volume as quality. The live signal is that witness has fewer tasks but more explicitly tagged
TURNs than genome or tg; tg has the largest task count among these three but much lower tagged
effort and completion. These are inspection/load-balancing signals only: attribution coverage
is 188/6186 TURN rows, so missing tags remain visible and no quality or routing conclusion is
authorized.

## Verification

- Red phase: the focused test failed with the production report absent (`rc=127`).
- `tests/test-mesh-hledger-mind-load.sh`: PASS with isolated board, spend, replay, and receipt fixtures.
- `python3 -m py_compile scripts/mesh-hledger-mind-load`: PASS.
- `tests/test-mesh-hledger-reconcile.sh`: PASS.
- Live report generation against current `~/.mesh/chat.log`, `~/.mesh/spend.log`, and task replay: PASS.

Unresolved: independent acceptance of missing/delayed/balanced-incomplete sources and deployed
cadence wiring remains the successor task `reconciliation-acceptance`.
