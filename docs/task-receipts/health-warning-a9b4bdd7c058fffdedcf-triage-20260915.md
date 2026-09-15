# Health warning triage: stale witness-autonomy alarm

Date: 2026-09-15
Task: `health-warning/a9b4bdd7c058fffdedcf/triage` (owner `health`).

## Finding

The dispatched warning was emitted at 2026-09-15T21:10:54Z and named three
stalled active tasks, including `health-warning/cb9de072194908524114/triage`.
That referenced health task is already DONE with the verified receipt
`docs/task-receipts/health-warning-cb9de072194908524114-triage-20260915.md`.

The live witness ledger confirms the warning is historical: subsequent rows at
21:20:19Z, 21:30:28Z, 21:35:14Z, 21:45:19Z, 21:45:20Z, and 22:00:46Z report
`source=PASS` and `errors=none` (the 21:45 rows also report
`active_recovery_wakes=0`). Later failures at 22:05:57Z, 22:10:25Z, and
22:25:22Z concern different witness/health rows and are not this task's
trigger.

## Verification

- `mesh-dash --once check` at 2026-09-15T22:26:00Z: supervised egress
  4UP/0DOWN, organs 13LIVE/0DARK, GPU healthy; it also reports the known
  high-local-load/probe-reliability warning.
- `mesh-task audit`: this task is RUNNING under `health`; the referenced
  `cb9de072...` task is DONE with its receipt.
- `mesh-task status health-warning/a9b4bdd7c058fffdedcf`: one active step.
- `~/.mesh/witness-task-autonomy.log`: newer PASS rows and later, unrelated
  failures inspected directly.

No routing, DNS, firewall, VPN, device, service, or privilege state changed.
Disposition: stale warning; settle this triage task. The current unrelated
22:25 warning remains visible for its own dispatch/triage chain.
