# prove-and-restore-live-route — rejected on current-state mismatch

Date: 2026-09-12 (UTC)  
Task: `exit-node-lan-cgnat-repair-20260912/prove-and-restore-live-route`  
Owner: `vpn`

## Verdict

Rejected before any routing mutation. The task specifies `100.74.0.0/16` and
`100.74.0.1`, but the live LAN on `enp42s0` is `100.76.0.0/16`, with address
`100.76.64.187/16` and DHCP gateway `100.76.0.1`. The requested address is not
on the currently connected LAN. Installing a throw for the stale prefix would
not restore the current gateway; retargeting the write to `100.76.0.0/16`
would change the assigned scope of the task and is not done in this rejection.

The currently wired `mesh-exit-node-lan-heal` has repeatedly refused both
prefixes because RFC6598 is not RFC1918. Its board output at 15:03:02Z and
15:04:03Z specifically reports `LAN 100.76.0.1` / `net 100.76.0.0/16` and
`REFUSED`. That is further evidence that safe application depends on the
separate CGNAT-aware healer work, rather than treating the old target as live.

## Read-only evidence

Captured 2026-09-12 around 15:04Z:

```text
ip -4 addr show dev enp42s0:
  inet 100.76.64.187/16 ... scope global dynamic enp42s0

ip -4 rule show:
  0:    from all lookup local
  5210: from all fwmark 0x80000/0xff0000 lookup main
  5230: from all fwmark 0x80000/0xff0000 lookup default
  5250: from all fwmark 0x80000/0xff0000 unreachable
  5270: from all lookup 52
  32766: from all lookup main
  32767: from all lookup default

main connected route:
  100.76.0.0/16 dev enp42s0 proto kernel scope link src 100.76.64.187 metric 100

ip -4 route get 100.74.0.1:
  100.74.0.1 dev tailscale0 table 52 src 100.81.222.19 uid 1000

ip -4 route get 100.76.0.1:
  100.76.0.1 dev tailscale0 table 52 src 100.81.222.19 uid 1000

ip -4 route get 100.94.116.17:
  100.94.116.17 dev tailscale0 table 52 src 100.81.222.19 uid 1000
```

Table 52 currently has a `default dev tailscale0`, peer `/32` routes for
`100.73.170.56`, `100.80.9.2`, `100.90.21.12`, `100.94.116.17`,
`100.101.237.87`, `100.103.99.16`, `100.105.241.84`, `100.107.198.111`,
`100.114.16.97`, `100.116.125.102`, `100.121.88.110`, and `100.125.157.75`,
plus `100.100.100.100`; the existing exception routes are `throw
38.49.216.141`, `127.0.0.0/8`, `172.17.0.0/16`, and `192.168.8.0/24`.
`tailscale status --json` reports the active exit node `phaedra`
(`100.94.116.17`, Online=true). The `100.76.0.0/16` connected route is not
present in table 52 and no `100.74.0.0/16` connected route exists.

`mesh-dms --list` reported no armed dead-man switches. Multiple other mesh
windows were active, so no hold/ownership claim was initiated after the route
target failed verification. No `ip route`, `ip rule`, or Tailscale setting was
changed; no dead-man switch was armed or cancelled.

## Verification performed

- `mesh-task check dispatch exit-node-lan-cgnat-repair-20260912/prove-and-restore-live-route vpn`: rc 0.
- `MESH_TASK_ACTOR=vpn mesh-task take exit-node-lan-cgnat-repair-20260912 prove-and-restore-live-route`: claimed.
- Read-only route, address, rule, Tailscale status, `mesh-trace --tail 20`,
  `mesh-dms --list`, process, and pane inspections completed.
- No route-change verification was attempted because the exact target check
  failed and no write was authorized by the task's stated live invariant.

## Required correction

Re-derive the connected prefix and gateway at dispatch time. If the intended
target is the currently observed `100.76.0.0/16`, route work must be explicitly
reissued against that live prefix after the CGNAT-aware healer contract and
single-writer holds are ready. Until then the routing substrate is unchanged.
