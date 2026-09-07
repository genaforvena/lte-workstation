# hledger coordination review — 2026-09-07

## Finding

`mesh-witness-promises` and `mesh-dispatch` were using hledger only indirectly and
fail-open:

```bash
mesh-promises --feed >/dev/null 2>&1 || true
```

That allowed the witness reflex to continue its lifecycle audit and call
`mesh-dispatch` after a failed promise-feed. The feed's internal `hledger check` was
therefore not a gate on coordination. The reflex also did not run `mesh-promises
--check`, so it did not require the independent board-replay ↔ hledger balance
agreement before dispatch.

`mesh-dispatch` had the same gap: it logged a warning for feed failures and routed
from the last materialized journal.

## Fix

`scripts/mesh-witness-promises` now:

1. requires `mesh-promises --feed` to succeed;
2. requires `mesh-promises --check` to succeed (parity, no negative liabilities,
   replay/balance agreement, and roster check);
3. writes `promise_ledger=PASS|FAIL` into
   `~/.mesh/witness-coordination.summary`;
4. exits non-zero and skips dispatch when either gate fails.

`scripts/mesh-dispatch` now preserves rc=2 as honest `n/a`, but refuses routing on
any other feed failure and records `REFUSED ledger-feed failed ... routing blocked`.

The cron wiring already invokes the repository script directly at
`~/.mesh/reflexes.cron:194`, so no deployed-copy replacement was needed.

## Verification

- `tests/test-mesh-witness-hledger-gate.sh`: PASS. A synthetic feed/check failure
  is loud, writes `promise_ledger=FAIL`, and does not invoke dispatch.
- `tests/test-mesh-dispatch-hledger-gate.sh`: PASS. A synthetic feed failure
  blocks routing.
- `scripts/mesh-dispatch --test`: PASS (258 assertions), including the existing
  ledger materialization check.
- `tests/test-mesh-witness-lifecycle.sh`: PASS.
- `tests/test-mesh-witness-promises.sh`: PASS.
- `bash -n` for the changed script and tests: PASS.
- `git diff --check`: PASS.
- Live `mesh-promises --feed`: PASS (`open=5`, `claim_open=1`, `hold_open=6`,
  `ask_open=11`).
- Live `mesh-promises --check`: PASS for parity, replay agreement, claims,
  holds, asks, and roster.
- Live `mesh-witness-promises`: PASS with `promise_ledger=PASS`; it did not
  dispatch because no retry candidate remained.
- Live `hledger -f ~/.mesh/promises/promises.journal check`: PASS.

## Remaining coordination boundary

The hledger promise journal materializes board obligations. Structured queued
successors that have not yet been posted to the board remain represented by
`~/.mesh/task-chains/*.json`, not as promise-journal rows. The witness summary now
shows both `promise_ledger=...` and the independent chain audit, so a green hledger
balance cannot hide a chain finding. At the final live recheck, the specialist
chain's current `mood-lora-bench` step was `BLOCKED` on `dependency`, retry edge
`2026-09-07T10:25:00Z`, with six queued successors; this remains an open chain
obligation and is not treated as a promise-ledger PASS.
