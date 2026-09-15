# Health warning triage: `5f08bc9d369377aa`

The warning is stale and terminal, not an active delivery outage.

- Live ledger entry `/home/mesh-home/.mesh/chat-deliver-ledger.json` records message `5f08bc9d369377aa` as `status=failed`, `terminal_reason=age-expiry`, target `genome`, failed at `2026-09-11T14:15:06Z`.
- The delivery log records a later successful delivery to `genome` at `2026-09-11T15:13:39Z` (`msg:0e0546407c7d567b`, attempt 1), followed by additional successful `genome` deliveries.
- No code, routing, VPN, DNS, firewall, or other substrate state was changed.

Conclusion: close this warning as a bounded historical age-expiry; continue watching for a fresh unpredicted delivery failure.
