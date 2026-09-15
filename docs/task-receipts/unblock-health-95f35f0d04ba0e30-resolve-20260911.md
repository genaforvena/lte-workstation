# Health self-unblock resolver receipt — 2026-09-11

Task: `unblock/health/95f35f0d04ba0e30/resolve`

## Fresh evidence

Local `mesh-health --once` at `2026-09-11T21:41:46Z` reported `mesh-home`
and `phaedra` passing, six peers offline, and:

```text
SKIP imac-rozalia 100.121.88.110 — SSH unreachable
```

From the reachable owner `phaedra`, the iMac answered a Tailscale ping:

```text
pong from imac-rozalia (100.121.88.110) via 5.227.25.156:55351 in 141ms
```

SSH remained unauthorized for both tested identities:

```text
root@100.121.88.110: Permission denied (publickey,password,keyboard-interactive).
mesh@100.121.88.110: Permission denied (publickey,password,keyboard-interactive).
```

## Disposition

Phaedra supplies network observation but not the missing SSH authority or a
safe actuator for the offline peers. No routing, DNS, firewall, VPN, or peer
configuration was changed. Keep the parent warning blocked; retry after
operator-provided SSH authority or an actionable roll-call delta.
