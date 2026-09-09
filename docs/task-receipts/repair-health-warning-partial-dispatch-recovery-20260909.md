# Health-warning partial-create dispatch recovery — 2026-09-09

## Result

`mesh-health-warning-task` now recognizes the exact durable open chain left by
`mesh-task create` when its dispatch side effect fails. It retries
`mesh-task dispatch <chain>` without calling `create` again, replays canonical
state, and advances the warning cursor only after `dispatch=sent`. Existing
blocked and complete terminal dispositions remain accepted.

## Verification

- Red regression: the partial-create fixture failed before the fix because the
  retry called `create <chain>` again and never dispatched the chain.
- Green regression: `python3 tests/test-mesh-health-warning-task.py` passed;
  the retry recorded only `dispatch <exact-chain>` after the failed create.
- `python3 -m py_compile scripts/mesh-health-warning-task` passed.
- Source/deployed parity and the safe live fixture are recorded below after
  mesh-land deployment.

## Handoff

Terminal receipt for `health-warning-partial-dispatch-recovery-20260909/repair-partial-create-dispatch-recovery`.
