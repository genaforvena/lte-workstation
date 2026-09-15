# Table-52 LAN exception: current scope and collision preflight

Date: 2026-09-13 UTC  
Owner: `vpn`  
Status: **preflight only; no routing mutation made**

## Current FIB and connected scope

`mesh-card --refresh` at 19:17:24Z reports a live invariant violation: exit-node
`phaedra`, default egress on `tailscale0`, and `100.76.0.1` swallowed by table 52.
Direct read-only observation at 19:17:55Z confirms `enp42s0` is UP with
`100.76.232.165/16`, connected route `100.76.0.0/16`, DHCP gateway `100.76.0.1`,
and default route via that gateway. The policy rule at priority 5270 sends unmarked
traffic to table 52; its default is `tailscale0`. `ip route get 100.76.0.1` and
`ip route get 100.76.254.254` select `tailscale0` / table 52. The main table has
the matching connected route on `enp42s0`.

This target changed while the investigation was running. Read-only state around
19:14Z showed `100.74.109.122/16` with `100.74.0.1`; at 19:17:55Z it showed
`100.76.232.165/16` with `100.76.0.1`; at 19:29Z it was back to
`100.74.110.140/16` with `100.74.0.1`. The healer refused both observed CGNAT
prefixes. The repair scope therefore cannot be a permanently hard-coded
`100.74/16` or `100.76/16`: at application time it must be the one prefix proven
connected to `enp42s0`, with its gateway proven on that prefix. A one-shot throw
would become stale when DHCP changes the connected prefix; do not install one
without the dynamic healer deployed. Abort and re-derive if the interface
address, connected route, or gateway changes before application.

## Peer-route collision evidence

At the 19:17:55Z and 19:29Z observations, table 52 had its default via
`tailscale0`, its existing throws, and peer `/32` routes, with no route inside
either observed connected `/16`. `tailscale status --json` listed no peer
address in either prefix. Read-only `ip route get` checks for every registered
peer IPv4 all selected `tailscale0`, including active exit node `phaedra`
(`100.94.116.17`); none overlapped either candidate connected prefix. A throw
must be added only for the exact connected prefix and must leave all peer `/32`
entries untouched. Recheck this proof immediately before any write.

## Baseline and coordination

- Public fetch to `https://api.ipify.org` returned `38.49.216.141`; the FIB for
  `1.1.1.1` remains `tailscale0` / table 52.
- `mesh-health` at 19:22:04Z reported this node PASS and `phaedra` PASS; it also
  reported other peers offline or SSH-unreachable. `mesh-card --refresh` reports
  the swallowed LAN invariant. These are the before-state records.
- `mesh-dms --list` showed no armed switches before this preflight.
- The rejected chain `exit-node-lan-cgnat-repair-20260912` still has open healer,
  deployment, and independent-verification steps under its rejected parent. Its
  first-step static target is stale for the current `100.76/16` observation.
- Substrate HOLD requests were sent to the other active windows. Only `sound`
  had returned an explicit hold acknowledgment at the initial receipt time;
  subsequent pane checks received acknowledgments from `opencode`, `genome`,
  `tg`, `senses`, `witness`, `tg-roz`, `job`, `pub`, and `sound`. `wake` became
  available and its hold was re-sent; `health`, `discover`, `adint`, `hire`, and
  `haunt` have not yet returned substantive hold acknowledgments. No ownership
  claim or DMS was made while holds remained unconfirmed.

## Proposed bounded change and rollback

After a connected-prefix-aware healer is landed and deployed, only if a fresh
pre-write check proves one connected CGNAT prefix on `enp42s0`, no table-52 peer
`/32` collision, and all other operators have acknowledged the hold: add
`throw <that-exact-prefix> table 52`. Expected result: the gateway FIB lookup
continues to the connected `enp42s0` route, while public egress and every
existing Tailscale peer `/32` stay on `tailscale0`. Rollback is to delete only
the exact throw route added. Use `mesh-dms` before the change; verify FIB,
`mesh-health`, refreshed `mesh-card`, and a real public fetch before cancelling
it. If any prefix or collision check changes, do not apply.

No route, rule, Tailscale setting, or healer deployment was changed during this
preflight.
