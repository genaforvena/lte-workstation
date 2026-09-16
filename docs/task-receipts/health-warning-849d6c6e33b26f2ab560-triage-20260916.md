# Health warning triage: `849d6c6e33b26f2ab560`

- Task: `health-warning/849d6c6e33b26f2ab560/triage`
- Source: `/home/mesh-home/.mesh/chat.log:68423-68424`, `2026-09-15T22:01:37Z`
- Triage evidence captured: `2026-09-16T10:49:32Z`–`10:49:49Z`

## Disposition

The reported LAN transition was a recovered transient, not an active substrate fault. The
router is still reachable through the known-node ARP fallback, the route still selects the
router interface, and the node's Tailscale identity is online and tagged. No routing, DNS,
firewall, VPN, or other substrate change was made.

The current observation remains qualified: `mesh-lan-presence --nodes` says `router unreachable`
for its normal discovery path and only proves the known GL-MT3000 ARP fallback. This is not a
new all-clear and is retained as a known discovery blind spot. `mesh-doctor --test` separately
reported a real smoke-test failure; that unrelated issue is not folded into this warning's
disposition.

## Evidence

```text
mesh-lan-presence --nodes
mesh-lan-presence: router unreachable — local ARP fallback (known nodes only, no DHCP hostnames)
GL-MT3000  192.168.8.1  ...  PRESENT  node

mesh-health --once
PASS mesh-home 100.81.222.19 (self)
LAN GL-MT3000 192.168.8.1 — reachable off-tailnet
PASS imac-rozalia 100.121.88.110
PASS phaedra 100.94.116.17

ip route get 1.1.1.1
1.1.1.1 via 192.168.8.1 dev enp42s0 src 192.168.8.197 uid 1000

tailscale status --json
self HostName=mesh-home Online=true Tags=[tag:lte-node] TailscaleIPs=[100.81.222.19,...]
peers: phaedra Online=true; imac-rozalia Online=true; WIN-Q6GL9FIR3QI Online=true
```

The egress helper exited `0` but emitted no text, so it is recorded as unknown rather than
treated as positive evidence. The live dash at `2026-09-16T10:48:36Z` independently showed
egress `OK` and the same router-fallback PRESENT state, while also showing current unrelated
doctor failures (`mesh-presence-density`, `snap.cups.cupsd.service`, and
`mesh-roz-channel.path`).

## Result

Recovered transient; current LAN fallback is present and the original warning has no active
repair obligation. Keep the discovery blind spot visible. Reopen only on a fresh LAN delta,
loss of the ARP fallback, route change, or independent egress degradation.
