# VPN warning triage: `health-warning/a6cd61d4957263666c1b`

- Checked: `2026-09-13T11:51–11:53Z` on `mesh-home`
- Task: `health-warning/a6cd61d4957263666c1b/triage`
- Source: `mesh-vpn-health@mesh-home`, `2026-09-13T11:50:48Z` reported external
  SS `:443` and trojan `:8443` probes failing twice while this node's egress
  probes were clean.

## Finding

A fresh read-only `mesh-vpn-health` run at `11:52:54Z` no longer reproduced
either external failure: it reported SS, trojan, and WG processes up, trojan
certificate valid with 62 days remaining, and the existing no-recent-WG-client
handshake degradation. This makes the new `:443`/TLS failure transient or
unreproduced from this vantage; the cause is unknown.

The client-plane issue remains real and predates this alert: current output
still has 16 configured WG peers with 0 active, 0 idle, 12 stale, and 4 never
seen. A prior receipt (`docs/task-receipts/health-warning-2f0fa058a7b225686f83-triage-20260911.md`)
records the same persistent condition. No VPN, routing, DNS, firewall, or
Tailscale state was changed. The read-only run took 3.35s; no resource shortage
or retry wait blocked diagnosis.

## Evidence

- `/home/mesh-home/.mesh/vpn-health.log`: warning at `11:50:48Z`, followed by
  `11:52:54Z` showing `SS:up`, `trojan:up`, `wg:up`, and a valid certificate.
- `mesh-vpn-health` at `11:52:54Z`: alert not reproduced; no recent WG peer
  handshakes and client roster remains 0 active / 0 idle / 12 stale / 4 never.
- `docs/task-receipts/health-warning-2f0fa058a7b225686f83-triage-20260911.md`:
  earlier evidence of the continuing WG client-plane degradation.

## Disposition

Close this episode as a transient/unreproduced external-probe failure with
unknown cause. Keep the chronic WG client unavailability as a known unresolved
degradation; do not restart or rotate the VPN without an operator decision.
