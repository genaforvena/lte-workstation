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
- Source/deployed parity: SHA-256
  `6ab9f9bfbb7018c95f8c779b991b08ccbb33cbe129b2f97eb53fb1625e59d178` for
  both `scripts/mesh-health-warning-task` and
  `~/.local/bin/mesh-health-warning-task` after mesh-land deployment.
- Safe fixture acceptance: `python3 tests/test-mesh-health-warning-task.py`
  passed against a temporary mesh directory, chat log, and fake task command;
  no live task state was mutated.
- Landed commits: `001ffad7` (fix), `8b39a78` (receipt), `1540be9c`
  (regression test), all pushed to `origin/main` by mesh-land/push-heal.

## Handoff

Terminal receipt for `health-warning-partial-dispatch-recovery-20260909/repair-partial-create-dispatch-recovery`.
