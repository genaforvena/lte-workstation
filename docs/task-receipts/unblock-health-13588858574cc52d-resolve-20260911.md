# Health self-unblock resolver receipt — 2026-09-11

Task: `unblock/health/13588858574cc52d/resolve`

## Fresh evidence

The live one-shot dash at `2026-09-11T21:37:45Z` reports two healthy nodes
(`mesh-home`, `phaedra`), six offline peers, and `imac-rozalia` as `NOSSH`
despite ICMP reachability. The local `mesh-health --once` at
`2026-09-11T21:34:38Z` independently recorded the same six offline peers and
`SKIP imac-rozalia — SSH unreachable`.

The reachable owner `phaedra` can reach the iMac at the network layer:

```text
pong from imac-rozalia (100.121.88.110) via 5.227.25.156:55351 in 141ms
```

But SSH authority remains unavailable from that owner:

```text
root@100.121.88.110: Permission denied (publickey,password,keyboard-interactive).
mesh@100.121.88.110: Permission denied (publickey,password,keyboard-interactive).
```

## Disposition

The reachable owner supplies observation only; it does not supply the missing
SSH authority or a safe actuator for the six offline peers. No routing, DNS,
firewall, VPN, or peer configuration was changed. Keep the parent warning
blocked and retry after operator-provided SSH authority or a new roll-call
delta with an actionable owner.
