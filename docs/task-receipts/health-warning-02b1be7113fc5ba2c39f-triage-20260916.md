# Health warning triage — 2026-09-16

- Exact task: `health-warning/02b1be7113fc5ba2c39f/triage`
- Source warning: `mesh-chat-deliver` at `2026-09-16T00:45:07Z` for target `senses`,
  window `5965065`, messages `bc041b113cef3cbb` and `ba9efd2caf883d07`.
- The durable delivery log records both as terminal `delivery-failed` with `attempts:0`,
  ages 910s and 903s, and reason `age-expiry` under the 900s policy. The delivery ledger
  agrees: both entries are `status=failed`, `terminal_reason=age-expiry`, with no attempt.
- Subsequent delivery activity succeeded for other targets, including `discover`, `witness`,
  `genome`, and `tg`, so this bounded evidence does not establish a global delivery outage.
- The current `senses` handoff records a separate capability block (no successful BLE adapter
  or fresh presence-log write), which explains why a replay would not be evidence-backed.
- Fresh `mesh-dash --once check` at `2026-09-16T01:07:28Z` reports egress OK and organs
  live in the dashboard (13 live), with known local-load probe unreliability and observe-only
  VPN degradation.

## Disposition

Terminal age-expiry for two zero-attempt messages to a capability-blind target. Do not replay
or alter `mesh-chat-deliver`, routing, VPN, DNS, firewall, or the senses capability from this
health lane. Preserve the failure as delivery evidence; a future senses capability recovery or
fresh target-specific delivery failure is the appropriate retry edge.

## Verification

- Ran `mesh-dash --once check` and recorded current egress, organ, VPN, and load state.
- Correlated `/home/mesh-home/.mesh/chat-deliver.log` and
  `/home/mesh-home/.mesh/chat-deliver-ledger.json` for both message IDs.
- Read `/home/mesh-home/.mesh/handoff/senses.md` for the target's current capability state.
- Confirmed later successful delivery records to other targets; no substrate or delivery
  mutation was performed.
