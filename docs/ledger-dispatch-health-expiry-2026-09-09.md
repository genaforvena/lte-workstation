# ledger-dispatch-health-expiry-20260909 / hold-expired-health-warning-rows

The expiry bug was in `scripts/mesh-task audit`: every open current step whose
`dispatch_until` had elapsed became `OPEN_UNOWNED`. The 14 historical
`health-warning/*/triage` rows had `dispatch=sent` and expired delivery windows,
so `scripts/mesh-task-journal` counted them as findings and the witness treated
them as fresh work.

The policy now renders only expired, sent `health-warning/*` dispatches as
`HELD_EXPIRED` with `retry=next fresh health warning`. It does not mutate the
ledger or reopen/dispatch the rows. Other expired open tasks remain
`OPEN_UNOWNED`; a fresh or failed health-warning dispatch remains eligible under
the existing policy. The journal accepts `HELD_EXPIRED` without counting it as a
finding.

Verification:

- `python3 tests/test-mesh-task-no-expiry.py` — 13 tests passed.
- `scripts/mesh-task --test` — PASS.
- Live audit: 14 `HELD_EXPIRED` health-warning rows, 0 `OPEN_UNOWNED` rows.
- Live journal rebuild: `chain_steps=368 findings=0 status=PASS`.
- Source/deployed SHA-256 parity verified for `mesh-task` and
  `mesh-task-journal`.
