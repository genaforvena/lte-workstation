# Health-warning triage: `health-warning/2f0fa058a7b225686f83`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/2f0fa058a7b225686f83/triage`

## Verdict

The warning is a real, persistent-but-known VPN degradation on phaedra, not a
safe local repair. SS, trojan, and WireGuard services are up, but no WireGuard
client has a recent handshake; clients are effectively cut off. The current
mesh is still degraded through carrier/NAT relay behavior. No restart, rotation,
routing, DNS, firewall, Tailscale, or VPN mutation was performed.

## Evidence

The dispatched warning says:

```text
[vpn-down] phaedra VPN DOWN — SS:up trojan:up wg:up | SS :443 unreachable externally 2x
(local path CLEAN: net=up(loss=0%) ts=Running/online=true); no WG client handshake in >24h
(all peers idle?) | trojan cert ok (65d left); WG 16 peers, newest handshake 987752s ago;
clients: 0 active / 0 idle / 12 stale / 4 never (16 provisioned) — CLIENTS CUT OFF.
DIAGNOSE READ-ONLY; do NOT restart/rotate a working VPN without operator
(memory never-touch-working-vpn).
```

The current read-only `mesh-vpn-health` run at 2026-09-11T23:41:36Z reports
`phaedra VPN DEGRADED`, with SS/trojan/WG up, no handshake in >24h, 16 peers,
and `0 active / 0 idle / 12 stale / 4 never` clients. Current `mesh-dash`
also reports 40% egress loss and relay/NAT degradation. Tailscale itself is
online on mesh-home (`100.81.222.19`); exit-node and LAN-access preferences
remain present, so this evidence does not justify changing local substrate.

## Verification

```text
mesh-dash --once check                                      # state captured
mesh-task check dispatch health-warning/2f0fa058a7b225686f83/triage health  # exit 0
MESH_TASK_ACTOR=health mesh-task take health-warning/2f0fa058a7b225686f83 triage  # claimed
mesh-vpn-health                                             # current degradation reproduced
tailscale status --json                                     # self online
mesh-task status health-warning/2f0fa058a7b225686f83       # active before completion
```

Known limitation: the probe distinguishes service/process reachability from
usable external SS/WireGuard client access; idle peers and carrier/NAT relay
behavior can keep the service up while clients remain stale.
