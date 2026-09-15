# Triage historical Tailscale path and health snapshot

Task: `health-warning/81ddb47e12e9b28795e3/triage`  
Source warning: 2026-09-12T18:53:01Z `check-stream` delta

The warning reports `win-q6gl9fir3qi` changing from active/direct to idle and
`imac-rozalia` remaining active via relay Helsinki. A targeted current
`tailscale status --json` read at 20:24Z on 2026-09-14 shows the Windows peer
still online but idle (`Online=true`, `Active=false`, relay `hel`, no current
direct endpoint); iMac is online and active via relay `hel`. This corroborates
the Windows peer's idle state, but does not show an outage or identify a path
cause. The historical direct-to-idle transition itself has no current repair
indicated.

The fresh one-shot `mesh-dash --once check` at 20:20Z showed egress OK at 0%
loss, but also high local load making fleet reachability probes unreliable,
zero LAN peers, and a degraded Phaedra VPN status. Its doctor row was a
48-minute-old cache (FAIL=0, WARN=33), so it is not a fresh doctor verdict.
LAN presence and router reachability remain unknown; no LAN or route change is
justified from this warning. No routing, DNS, firewall, VPN, or Tailscale state
was changed.

## Verification

- `rtk mesh-dash --once check` at 20:20:35Z: egress OK, zero LAN peers,
  high-load probe warning, doctor cache age 48m.
- `rtk tailscale status --json` at 20:24Z: Windows peer online/inactive via
  relay `hel`; iMac online/active via relay `hel`.
- No fresh doctor run or authenticated remote read was performed. Keep the
  peer idle status and LAN visibility limit explicit; revisit if a fresh pane
  or peer event shows a materially different state.
