# Health warning triage: `health-warning/6bcab66469917ab65056`

Date: 2026-09-14  
Owner: health / mesh-home  
Task: `health-warning/6bcab66469917ab65056/triage`

## Finding

The 07:15:55Z `mesh-witness-task-autonomy` failure was a transient dispatch/check race
on the preceding health-owned `/clearclear` recovery task. The chat ledger shows that
`health-warning/eb433dcbffedb86f3aa7/triage` was open and dispatched at 07:11:11Z,
then claimed by `health` at 07:15:23Z (structured active state written at 07:15:30Z).
The witness logged the check failure at 07:15:55Z while its queue snapshot still
counted `active=0`; the exact dispatch check saw the now-active task and returned 2.
That task was subsequently completed at 07:25:02Z with receipt
`task-receipts/health-warning-eb433dcbffedb86f3aa7-triage-20260914.md`.

This is not an outstanding prerequisite or a new substrate fault. The live
`mesh-witness-task-autonomy --once` rerun at 07:31:26Z exited 0 and recorded
`health=PASS ... active=1 ... errors=none`; the active task at that point was this
triage, and no candidate/check contradiction remained.

## Action and remaining state

- Reconstructed the event from the shared chat/structured-task ledger, prior task
  receipt, witness log, and `scripts/mesh-witness-task-autonomy` candidate-check path.
- No code or task dependency change was warranted: the exact conflicting row settled,
  and the current witness run passes. The observer currently treats any nonzero
  exact-owner check as an error, so a future queue/take race may produce another
  transient warning; it should only be changed with a reproduced fixture and scoped
  design review.
- The separate live egress warnings remain: `ip route get 1.1.1.1` returns
  `dev tailscale0 table 52`, and Tailscale reports `phaedra` as the configured online
  exit node. No route, DNS, firewall, VPN, or exit-node setting was changed; those
  remain substrate work requiring its single-writer protocol and owner coordination.

## Verification

- `mesh-task check dispatch health-warning/6bcab66469917ab65056/triage health` — exit 0.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/6bcab66469917ab65056 triage` — claimed by exact owner.
- `mesh-witness-task-autonomy --once` — exit 0; fresh PASS row at 07:31:26Z.
- `ip route get 1.1.1.1` — read-only confirmation of `tailscale0 table 52`.
- `mesh-wake-expect health --ttl 86400 '^== check data.*all text ==$' '^-- pane live .* --$'` — bounded 24-hour prediction for the normalized check-frame header and pane-live footer shape.
