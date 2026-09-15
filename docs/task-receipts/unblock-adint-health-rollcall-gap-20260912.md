# Health roll-call dependency — 2026-09-12

This receipt covers the adint-owned resolver rows referring to
`unblock/health/cbde274272e707fa/resolve`:

- `unblock/adint/d90da73d5110a5b0/resolve`
- `unblock/adint/1d15ed751f6252cf/resolve`
- `unblock/adint/f458021d2883e765/resolve`

## Fresh read-only evidence

`rtk mesh-health` at `2026-09-12T04:53:17Z` reported `mesh-home` and `phaedra` reachable, six
devices offline (GL-MT3000, Redmi 10, ilya, imozerov-Default-string, imozerov-IdeaPad-3-15IIL05,
and rip), and `imac-rozalia` with SSH authentication refused. `rtk mesh-fleet-health` at the same
time independently marked the six devices offline and the iMac `NO-SSHD`; it warned
`PATH: DEGRADED OK` and reported no reachable owner capable of restoring the peers. No routing,
DNS, firewall, VPN, peer, or remote-device state was changed.

## Disposition and exact retry condition

The dependency remains external: restore Tailscale connectivity on the six devices, or identify a
currently reachable authorized owner who can do so, and provide a working SSH-authorized identity
for the iMac. Then run a fresh `rtk mesh-health` and resume the Health-owned resolver only when those
checks pass. Until that event, leave the Health parent blocked on `event:roll-call-delta`.

The live parent status is blocked under owner `health` with that same retry event. Prior evidence is
in `docs/task-receipts/unblock-adint-d1c3bb93602d31d9-resolve-20260912.md` and
`docs/task-receipts/unblock-health-cbde274272e707fa-resolve-20260911.md`.
