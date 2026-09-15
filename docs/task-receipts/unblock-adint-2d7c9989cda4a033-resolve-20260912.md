# Health self-unblock receipt — adint/2d7c9989cda4a033

- Resolver: `unblock/adint/2d7c9989cda4a033/resolve`
- Parent dependency: `unblock/health/cbde274272e707fa/resolve`
- Checked: `2026-09-12T00:09Z`

## Evidence

The local `mesh-health` sweep reported five offline peers and `imac-rozalia`
as SSH-unreachable. The live Tailscale peer map also shows `rip` offline,
which the local sweep omitted. `mesh-fleet-health` reports only this node as
reachable. `phaedra` itself is reachable (`tailscale ping` and batch SSH both
worked).

From `phaedra`, one batch Tailscale-ping pass produced timeouts for all six
offline peers:

```text
GL-MT3000           100.105.241.84  timed out
Redmi 10            100.103.99.16   timed out
rip                 100.116.125.102 timed out
ilya                100.107.198.111 timed out
imozerov-Default-string 100.125.157.75 timed out
imozerov-IdeaPad-3-15IIL05 100.73.170.56 timed out
```

From `phaedra`, `imac-rozalia` answered Tailscale ping in 141 ms, but the
currently configured `mesh` SSH identity was refused:

```text
mesh@100.121.88.110: Permission denied (publickey,password,keyboard-interactive).
```

## Result and exact prerequisite

The reachable `phaedra` node supplies a read-only vantage point, but it cannot
reach any of the six offline devices and has no authorized SSH identity for
the iMac. No routing, DNS, firewall, VPN, peer configuration, or remote device
state was changed. The dependency is not cleared.

To retry safely, the operator must restore Tailscale connectivity on the six
named devices (or identify a reachable, authorized owner who can do so) and
provide an SSH-authorized identity for `imac-rozalia`, then request a fresh
health sweep. Until that evidence arrives, keep the health parent blocked on
`event:roll-call-delta`; do not resume it.
