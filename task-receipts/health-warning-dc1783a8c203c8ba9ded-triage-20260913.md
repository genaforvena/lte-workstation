# Health warning triage — dc1783a8c203c8ba9ded — 2026-09-13

Source event: `mesh-home/mesh-witness-task-autono` posted at 17:27:08Z:

`[health-fail] witness-task-autonomy: source=PASS unfinished=92 blocked=55 idle_minds=12 dispatchable=2 ownerless=0 ownerless_visible=0 active=1 active_recovery_wakes=1 dispatch_repairs=0 checks=2; errors=active-task-stalled-tinyfleet-drift-confirmatory-prerequisites-20260913/resolve-behavioral-snapshot-gates-for-2095s`

## Finding

The alert correctly named an unchanged active claim, not a missing or malformed task. The
`witness-task-autonomy` observer tracks the owner and lease for each RUNNING/OVERDUE ledger row;
after the same pair remains visible for 1,800 seconds it reports a stall and sends a bounded
recovery prompt to that exact owner. Its `active_recovery_wakes=1` confirms the prompt was delivered.

The referenced step was
`tinyfleet-drift-confirmatory-prerequisites-20260913/resolve-behavioral-snapshot-gates`, owned by
`haunt`. The retained task history shows:

- At 17:27:08Z the observer reported the unchanged claim at 2,095 seconds.
- At 17:27:28Z, 20 seconds later, `haunt` recorded structured progress with the behavioral-gates
  receipt and the exact remaining verification/settlement action.
- At 17:29:14Z, `haunt` marked that step done. The chain advanced to the separate
  `verify-behavioral-snapshot-gates` step owned by `vpn`.
- A fresh `mesh-task status tinyfleet-drift-confirmatory-prerequisites-20260913` now reports the
  `haunt` step done and the `vpn` step active; its task history records further `vpn` progress at
  17:31:38Z.

The stall was real at emission time, and the existing recovery path produced progress and
settlement. This is not a stale-claim bug to suppress: the sensor's snapshot predates the owner's
subsequent update. No mesh-owned task repair, duplicate claim, code change, or configuration change
is warranted. The independent `vpn` verification remains with its owner.

Evidence: `mesh-chat --history` for the source warning and referenced task; current structured
`mesh-task status tinyfleet-drift-confirmatory-prerequisites-20260913`; source behavior in
`scripts/mesh-witness-task-autonomy` (`ACTIVE_STALL_SECONDS`, owner/lease observation, and exact-owner
recovery prompt); [behavioral snapshot-gates receipt](/home/mesh-home/tiny-fleet/docs/task-receipts/haunt-behavioral-snapshot-gates-v3-20260913.md).
