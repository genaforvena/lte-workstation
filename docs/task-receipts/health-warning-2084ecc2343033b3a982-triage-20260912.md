# Health warning triage: `health-warning/2084ecc2343033b3a982/triage`

Checked on `mesh-home` at 2026-09-12 15:26–15:27 UTC after the exact-owner dispatch check passed and `MESH_TASK_ACTOR=health` took the row.

## Current evidence

- The task repeats the prior check warning's two persisted doctor failures (egress through `tailscale0`; exit node `n2sbt7yy6t11CNTRL`) and four static warning categories. This is a new warning key, not a distinct repair scope.
- A fresh read-only `ip route get 100.76.0.1` returned `dev tailscale0 table 52 src 100.81.222.19`, confirming the gateway path is still captured by the exit-node policy table.
- The VPN-owned `exit-node-lan-cgnat-repair-20260912` chain remains at step 1 (`prove-and-restore-live-route`, owner `vpn`); its steps 2–3 remain open. Health's step 4 (`independent-route-verification`) is still open and must wait for those prerequisites.
- The existing triage receipt `health-warning-7b63457806f1930a08a3-triage-20260912.md` has the current pane and fleet evidence. This repeated warning does not independently re-test its four static doctor categories or probe the LAN while the route is captured.
- No route, DNS, firewall, WireGuard, or Tailscale state was changed by health.

## Disposition

This is a repeated observation of the already-owned LAN-visibility fault. The known blind spot persists until VPN completes the repair chain; retain step 4 for independent verification. No additional substrate action is warranted from this duplicate warning. Next: after VPN completes steps 1–3, check dispatch for `exit-node-lan-cgnat-repair-20260912/independent-route-verification`, take only on exit 0, then verify FIB and LAN.
