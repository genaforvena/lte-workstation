# Health-warning triage — `health-warning/67e92a51d3f00476631c`

Checked 2026-09-16 05:37–05:38 UTC on `mesh-home`.

The warning at `/home/mesh-home/.mesh/chat.log:71882` reports two `wake` delivery
failures from 05:05:05Z. Canonical ledger rows for `2f44e7ceab824965` and
`a08476ae441c8462` both show `status=failed`, `terminal_reason=age-expiry`,
target `wake`, and zero attempts. `/home/mesh-home/.mesh/chat-deliver.log:2617–2618`
independently records the same failures, window, and ages (909s and 903s).

This is bounded targeted-delivery expiry, not evidence of a routing, DNS,
firewall, VPN, Tailscale, or node fault. No substrate repair is warranted.

Verification:

- Active crontab contains the one-minute `mesh-chat-deliver` entry.
- `python3 scripts/mesh-chat-deliver --test` — PASS.
- `mesh-health` — PASS for `mesh-home`; GL-MT3000, Redmi 10, iMac-Rozalia,
  and Phaedra reachable. Other listed peers remain offline.
- `mesh-dash --once check` was attempted with a 12-second bound and emitted
  no stream (`status=124`); this remains an observability anomaly, not a pass.

Disposition: **known delivery-edge age-expiry; no substrate repair warranted**.

Delegation decision: no subagent launched. This was a tightly coupled live
triage; ownership, receipt writing, board voice, substrate boundary, and final
verification stayed local. Personally inspected the warning, both ledger rows,
delivery log, crontab, focused self-test, and `mesh-health` output.
