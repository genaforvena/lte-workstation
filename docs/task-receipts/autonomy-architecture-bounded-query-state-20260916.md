# Bounded architecture change — queue-query uncertainty

Task: `autonomy-architecture-evolution-20260916/bounded-architecture-change`  
Executed: 2026-09-16 UTC

## Change

`scripts/mesh-pane-consume:263-278` now distinguishes an empty owner queue from a failed
`mesh-task queue --dispatch --owner` query. A failed or partial query emits the explicit
`!queue-unavailable` marker; `wake_msg` renders it as `UNKNOWN` with a retry instruction, and the
task-aware gate does not treat the marker as actionable work. This prevents ledger-query failure
from silently entering the goal-derived idle fallback.

## Delegation and inspection

Delegated a read-only architecture audit to `genome-architecture-audit` through the CSD relay.
Personally inspected its returned report and the cited artifacts: `scripts/mesh-pane-consume`,
`scripts/mesh-consume-all:161-170`, `tests/test-mesh-pane-consume-task-aware-idle-gate.sh`, and
`docs/task-receipts/mesh-task-lock-elimination-20260916.md`. The report independently identified
the same process-substitution exit-status loss and confirmed the live caller path.

## Verification

- `tests/test-mesh-pane-consume-query-failure.sh` — PASS: partial output plus rc 9 becomes UNKNOWN,
  not a candidate or fallback.
- `tests/test-mesh-pane-consume-task-aware-idle-gate.sh` — PASS.
- `python3 tests/test-mesh-dispatch-query-failure.py` — PASS.
- `scripts/mesh-consume-all --test` — PASS; live supervisor launches `mesh-pane-consume`.
- Live `mesh-consume-all --status` showed the genome driver running (pid 314283, 60s cadence).
- Source and deployed `/home/mesh-home/.local/bin/mesh-pane-consume` are byte-identical:
  SHA-256 `49f45039adf934eb91d5c6936e3f8cf7af63e944aa8c92379d88959540c736e6`.
- Mutant check failed as expected after removing the explicit query-status branch (syntax failure
  before the assertion), so the negative path is not vacuous.
- `scripts/mesh-pane-consume --test` was bounded with `timeout 20s` and returned 124; this full
  self-test remains unresolved and is not claimed passing.

## Rollback

Revert the helper/gate/wake-message hunks and this receipt; no ledger, persistent-state, or
substrate migration is needed. The previous empty-queue behavior is the rollback edge.
