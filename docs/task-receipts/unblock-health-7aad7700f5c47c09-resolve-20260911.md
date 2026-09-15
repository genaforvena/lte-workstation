# Health self-unblock resolver receipt — 2026-09-11

Task: `unblock/health/7aad7700f5c47c09/resolve`

## Fresh evidence

Local `mesh-health --once` at `2026-09-11T21:43:43Z` reported `mesh-home`
and `phaedra` passing, six peers offline, and:

```text
SKIP imac-rozalia 100.121.88.110 — SSH unreachable
```

From reachable owner `phaedra`, the iMac answered a Tailscale ping:

```text
pong from imac-rozalia (100.121.88.110) via 5.227.25.156:55351 in 140ms
```

SSH authority remained unavailable for both tested identities:

```text
root@100.121.88.110: Permission denied (publickey,password,keyboard-interactive).
mesh@100.121.88.110: Permission denied (publickey,password,keyboard-interactive).
```

## Disposition

The reachable owner supplies network observation but not the missing SSH
authority or a safe actuator for the offline peers. No routing, DNS, firewall,
VPN, or peer configuration was changed. Keep the parent warning blocked and
retry after operator-provided SSH authority or an actionable roll-call delta.
