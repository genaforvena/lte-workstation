# Resolver receipt: `unblock/adint/d1c3bb93602d31d9/resolve`

- Checked: `2026-09-12T04:22Z` UTC on `mesh-home`
- Parent dependency: `unblock/health/cbde274272e707fa/resolve`
- Owner check: `rtk mesh-task check dispatch unblock/adint/d1c3bb93602d31d9/resolve adint` exited `0`; claimed with `MESH_TASK_ACTOR=adint rtk mesh-task take unblock/adint/d1c3bb93602d31d9 resolve`.
- Result: **BLOCKED/dependency; no safe local prerequisite can restore the required peers or SSH authority.**

## Fresh evidence

`rtk mesh-health` at `2026-09-12T04:19:51Z` reported `mesh-home` and `phaedra`
passing, these six peers offline, and the iMac SSH-unreachable:

```text
OFFLINE GL-MT3000                        100.105.241.84
OFFLINE Redmi 10                         100.103.99.16
OFFLINE ilya                             100.107.198.111
SKIP  imac-rozalia                     100.121.88.110 — SSH unreachable
OFFLINE imozerov-Default-string          100.125.157.75
OFFLINE imozerov-IdeaPad-3-15IIL05       100.73.170.56
OFFLINE rip                              100.116.125.102
```

The live Tailscale peer map agrees that the six listed devices are offline;
`imac-rozalia` is `online:true`. `mesh-fleet-health` at `04:20:04Z` warned
`LOCAL LOAD HIGH` and explicitly marked non-answers `UNKNOWN(load)`, so I did
not use that report alone to infer devices were down.

As a bounded second vantage, `phaedra` returned no Tailscale reply from each
of the six offline peers. It reached `imac-rozalia` over a direct Tailscale
path; this node also received an iMac Tailscale pong over DERP. However, a
read-only `true` command over SSH to `mesh@100.121.88.110` was refused from
both `mesh-home` and `phaedra`:

```text
Permission denied (publickey,password,keyboard-interactive).
```

This distinguishes iMac network reachability from the missing SSH authority.
The reachable `phaedra` vantage cannot reach the six devices, and no safe
local action or currently reachable authorized owner capable of restoring
them was established. No routing, DNS, firewall, VPN, peer, or remote-device
state was changed.

## Exact prerequisite and retry

An authorized owner must restore Tailscale connectivity on the six named
devices (or provide a currently reachable authorized owner who can do so),
and the operator must provide an SSH-authorized identity for
`imac-rozalia`. Then run a fresh `rtk mesh-health`. Resume the health parent
only when the peers are reachable and the iMac SSH check succeeds. Until then
keep it blocked on `event:roll-call-delta`.
