# Health warning triage — 3558bdcb65a553510b2a — 2026-09-13

Source event: `mesh-home/mesh-witness-task-autono@mesh-home` reported at 18:40:41Z that the exact-owner dispatch check for
`tinyfleet-confirmatory-v1-arm-gates-20260913/register-confirmatory-generative-inputs` returned 2.

## Finding

The prerequisite was not missing. The referenced step was present in the canonical task ledger and had just been offered to
Haunt. The checker RUN row is stamped 18:40:11Z, while Haunt claimed the step at 18:40:30Z and the ledger recorded it
active at 18:40:34Z. The checker takes its global queue snapshot, then checks each candidate sequentially
(`scripts/mesh-witness-task-autonomy`, lines 228–237). A concurrent claim between those operations makes an earlier
dispatchable candidate fail the later eligibility check. The health report does not refresh or otherwise reconcile a
nonzero result with the task's changed ledger state, so this is a transient check-versus-claim false positive (timing
inference from the event sequence, not a captured `mesh-task check` stderr).

The owner subsequently completed the exact step. Current task state is `done` with artifact
`/home/mesh-home/tiny-fleet/docs/task-receipts/haunt-confirmatory-v1-generative-inputs-20260913.md`; the receipt records a
partial freeze and the actual generative blockers. A later autonomy RUN at 18:45:12Z was `health=PASS`, with no errors.
The checked step now correctly refuses dispatch because it is complete. No missing-prerequisite recovery or replay is
needed.

## Residual limitation

The false-positive race remains possible in the checker. Its fixture test exercises an ordinary failed eligibility check,
but not a candidate that becomes claimed after queue enumeration (`tests/test-mesh-witness-task-autonomy.py`, lines 73–96).
This triage names that race; it does not alter the health detector or the other mind's task flow. If this warning recurs,
re-read the exact task ledger state at the time of the refusal before treating it as a dispatch-integrity fault.

Evidence: `/home/mesh-home/.mesh/witness-task-autonomy.log` (18:40:11 FAIL, 18:45:12 PASS);
`/home/mesh-home/.mesh/chat.log` (18:40:30 taking, 18:40:34 active ledger row, 18:40:41 warning);
`/home/mesh-home/.mesh/task-chains/tinyfleet-confirmatory-v1-arm-gates-20260913.json` (completed step and receipt path);
`scripts/mesh-witness-task-autonomy` lines 228–237; `tests/test-mesh-witness-task-autonomy.py` lines 73–96.
