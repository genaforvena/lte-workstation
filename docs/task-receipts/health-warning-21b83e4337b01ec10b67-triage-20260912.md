# Health warning triage: `health-warning/21b83e4337b01ec10b67/triage`

Checked live on `mesh-home` at 2026-09-12 15:04–15:06 UTC after the failed automatic dispatch was rescheduled and the exact owner row passed `mesh-task check dispatch` (exit 0). The task was then claimed by `MESH_TASK_ACTOR=health`.

## Current evidence

- `mesh-dash --once check` returned exit 0 with the full `check` stream at 15:06:00Z. It showed egress on `tailscale0`, two cached doctor failures (cache timestamp 14:31:30Z), a degraded fleet view, and `LOCAL LOAD HIGH`; the dash explicitly says non-answers are `UNKNOWN(load)`, not down. The separate `mesh-fleet-health` sample at 15:04:01Z likewise marked most peer probes `UNKNOWN(load)`.
- Fresh `mesh-health` at 15:05:10Z passed the local node and `phaedra`; it skipped `imac-rozalia` because SSH authentication was refused. It reported GL-MT3000, Redmi 10, ilya, and both imozerov hosts offline. This does not establish that `imac-rozalia` is offline.
- A fresh `mesh-doctor` run still emitted the two relevant egress failures: egress rides `tailscale0`, and an exit node is set (`n2sbt7yy6t11CNTRL`). It also emitted `WARN mic DEFAULT device broken/busy`; explicit mic capture on `plughw:1,0` passed. The doctor continued into additional checks, so this receipt relies only on those observed lines.
- `mesh-card --refresh` (exit 2) and `ip route get 100.76.0.1` both confirmed the live LAN-sight failure: gateway `100.76.0.1` selects `tailscale0` in table 52. That table has a default via `tailscale0` and no `throw 100.76.0.0/16`. The main table has the connected `100.76.0.0/16` and gateway on `enp42s0`, while the card identifies the LAN prefix as swallowed by the active exit node `phaedra`.
- `mesh-lan-presence --nodes` returned exit 1 / `UNKNOWN`: no local address in `192.168.8.0/24`, router unreachable, and no known host answered ICMP. This is a separate LAN-segment visibility limit.
- Live Tailscale status contradicted the warning's old iMac transition: `imac-rozalia` is now `Online=true`, `Active=true`, relayed by `hel`. GL-MT3000 remains offline (last seen 2026-06-19); `phaedra` is online, active, and currently the exit node (relayed by `tor`). These are point-in-time peer states.
- `resolvectl status` shows physical-link DNS `213.87.2.89` and `217.66.16.35`, matching the warning; Tailscale also supplies `100.100.100.100` and `fd7a:115c:a1e0::53` on its link.
- Recent `mesh-trace` entries show `exit-node-lan-heal` repeatedly refusing the swallowed `100.76.0.0/16` prefix because it is not RFC1918. The live DMS registry reported no armed switches. The distinct ordered chain `exit-node-lan-cgnat-repair-20260912` is already routed to VPN for the substrate repair; health made no route, DNS, firewall, or Tailscale changes.

## Disposition

This warning is not wholly stale: the egress/exit-node doctor failures, mic-default warning, and swallowed LAN gateway remain live. The iMac-offline element is stale; the current tailnet shows it online/active via relay, although SSH authentication remains unavailable. The router-presence sensor remains `UNKNOWN`, and load makes several fleet probes unreliable. The exact unresolved blindness is inward LAN reachability while exit-node routing captures `100.76.0.1`; the VPN-owned repair chain is the next action, after which health's separately assigned verification step must re-check the FIB and LAN reachability.

No substrate mutation was made in this triage.
