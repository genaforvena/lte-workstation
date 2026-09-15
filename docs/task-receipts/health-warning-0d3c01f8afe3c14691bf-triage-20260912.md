# Health warning triage: `health-warning/0d3c01f8afe3c14691bf/triage`

Checked on `mesh-home` at 2026-09-12 15:31 UTC after the exact-owner dispatch check passed and `MESH_TASK_ACTOR=health` took the row.

## Evidence

- The roll-call says the 2026-09-11 09:45 pane was checked with no new finding and carries forward the known egress/exit-node risks.
- A fresh read-only `ip route get 100.76.0.1` returned `dev tailscale0 table 52 src 100.81.222.19`. The route failure remains current, so the roll-call's no-new-finding disposition is consistent with the repeated triages.
- The VPN-owned `exit-node-lan-cgnat-repair-20260912` chain is still active at step 1. Health's independent verification remains open behind steps 1–3.
- No route, DNS, firewall, WireGuard, or Tailscale state was changed by health.

## Disposition

This roll-call adds no distinct fault or repair scope. The known LAN-visibility blind spot remains until the VPN repair completes; keep health's independent verification gated behind it. Next: after VPN completes steps 1–3, check dispatch for `exit-node-lan-cgnat-repair-20260912/independent-route-verification`, take only on exit 0, then verify FIB and LAN.
