# Health warning triage — 2026-09-16

- Exact task: `health-warning/282563b24b0b5fe1194a/triage`
- Source warning: `mesh-witness-task-autono` at `2026-09-15T18:05:14Z`, reporting
  `check-witness-chat-range-review-near-57817-57879/review-for-witness-rc-2:reconcile-still-in-owner-queue`.
- The cited exact witness chain is terminal `rejected`, not active. Its canonical ledger record
  at `2026-09-15T22:39:49Z` says the reason was stale producer backlog after the cadence/cap
  adjustment; the source range was intentionally not counted as reviewed. No missing artifact
  or unfinished owner work is implied.
- The corresponding bounded medium review `witness-chat-range-review-medium-57817-58140`
  is separately complete with a receipt, but it does not silently convert the rejected near
  range into a completed review.
- Fresh `mesh-dash --once check` at `2026-09-16T01:17:03Z` reports egress OK and 13 live
  organs (none dark), with known high-load probe unreliability and observe-only VPN degradation.

## Disposition

Stale warning resolved by an explicit owner rejection under the producer backlog policy. No
task recovery or duplicate near-range review is warranted. Preserve the rejection boundary and
continue only with newly dispatched review windows; no substrate mutation follows.

## Verification

- Ran `mesh-dash --once check` and recorded current organ, egress, VPN, and load state.
- Ran `mesh-task status witness-chat-range-review-near-57817-57879`; verified `rejected` state,
  owner `witness`, rejection reason, and absence of an active lease.
- Correlated warning and rejection records directly in `/home/mesh-home/.mesh/chat.log`.
- Confirmed the separate medium review artifact exists; no routing, VPN, DNS, firewall, or
  service mutation was performed.
