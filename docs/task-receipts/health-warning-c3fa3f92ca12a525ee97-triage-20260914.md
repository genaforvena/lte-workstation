# Triage historical egress and peer-state warning

Task: `health-warning/c3fa3f92ca12a525ee97/triage`  
Source: 2026-09-12T21:58:16Z `check-stream` delta

The source records an older egress failure, imac-rozalia offline, and no
Tailscale status marker for win-q6gl9fir3qi. The current one-shot check pane
at 20:20:35Z on 2026-09-14 reports egress OK with 0% loss. It still reports
high local load making peer reachability probes unreliable, zero LAN peers,
and degraded Phaedra VPN client status. The doctor row is a 48-minute-old
cache (FAIL=0, WARN=33), not a fresh comprehensive result. A targeted
20:24Z Tailscale sample shows imac-rozalia online and active via relay
Helsinki; win-q6gl9fir3qi is online but inactive via relay. Thus the warning's
old offline/no-marker observations are superseded, while the Windows peer is
still idle.

The configured Tailscale exit-node dependency remains a known single-point
availability risk, and LAN presence remains UNKNOWN under the high-load probe
warning. The prior [health-warning-17d878bb98da052bc55c](health-warning-17d878bb98da052bc55c-triage-20260914.md)
receipt documents that route policy, local gateway, and LAN visibility gap.
No fresh evidence here justifies changing routing, DNS, VPN, firewall, or
Tailscale configuration. No substrate state was changed.

## Verification

- `rtk mesh-dash --once check` at 20:20:35Z: egress OK, 0% loss, no LAN peers,
  high-load reachability warning, degraded Phaedra client status, stale doctor
  cache.
- `rtk tailscale status --json` at 20:24Z: imac-rozalia online/active via
  relay `hel`; win-q6gl9fir3qi online/inactive via relay `hel`.
- Read the existing exit-node/LAN visibility triage; its disposition remains
  consistent with the current pane.
