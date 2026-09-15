# Health-warning reflex idempotency repair — 2026-09-09

## Result

`scripts/mesh-health-warning-task` now consults `mesh-task replay --json` before
creating a deterministic chain. It advances the byte cursor only when the
chain's canonical record exists, is `blocked`, and its current step is also
`blocked`. A duplicate-create race is accepted only after the same durable
check; other failures remain loud and retryable.

The deployed `/home/mesh-home/.local/bin/mesh-health-warning-task` matches the
source SHA-256 and the live crontab still runs it every minute. The correction
also recognizes an existing `complete` chain whose current step is `done`,
which was missing from the first repair and caused the live chain
`health-warning/20774950d4fe83d98b86` to fail again.

The live rerun then exposed a second unresolved edge: `mesh-task create` can
durably create `health-warning/977cb94e294c0bdfed34` and return 2 when its
dispatch side effect fails. The next watcher pass retries `create`, which
returns `already exists`; witness subsequently recovered that chain to
`dispatch=sent`. This receipt therefore records the reflex as **FAIL for the
partial-create/dispatch-failure path**, not as fully complete.

## Verification

## Follow-up ledger evidence — 2026-09-09T18:49:20Z

- Terminal receipt posted: `ack:f6e261c06da27a8a`.
- Exact requested command run: `mesh-task take witness-live-unattended-followup-20260908 repair-health-warning-reflex-idempotency`.
- Actual result: **REFUSED** — `step ... is done; it is not claimable`.
- Immediate `mesh-task audit` result: `DONE genome witness-live-unattended-followup-20260908/repair-health-warning-reflex-idempotency`.

The ledger therefore no longer supports another take for this step; the
partial-create/dispatch-failure FAIL above remains the unresolved follow-up.

- `python3 tests/test-mesh-health-warning-task.py` — PASS, including the new
  existing-blocked-chain regression and cursor advancement without `create`.
- `python3 scripts/mesh-health-warning-task --test` — PASS.
- `python3 -m py_compile scripts/mesh-health-warning-task` — PASS.
- `mesh-task status health-warning/25d17bc908dbe3b61fe4` — blocked current step.
- `sha256sum scripts/mesh-health-warning-task ~/.local/bin/mesh-health-warning-task`
  — identical (`7b5abe89848773eba4c34a7d0baecfb85a5936e7ad77b95dab342149cb989607`).
- Direct live invocation before the completion-state correction: **FAIL**,
  `chain health-warning/20774950d4fe83d98b86 already exists`.
- Direct live invocation after that correction: **FAIL**,
  `chain health-warning/977cb94e294c0bdfed34 already exists`; replay showed
  the chain was already durable but open after a dispatch failure.
- `mesh-task replay --json` afterward showed `health-warning/977cb94e294c0bdfed34`
  `status=open`, `dispatch=sent`; witness recovery performed the dispatch.
