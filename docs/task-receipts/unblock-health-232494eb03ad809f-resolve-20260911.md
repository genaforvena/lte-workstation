# Health self-unblock resolver receipt — 2026-09-11

Task: `unblock/health/232494eb03ad809f/resolve`

## Fresh evidence

Local `mesh-health --once` at `2026-09-11T21:34:38Z` reported:

```text
PASS  mesh-home 100.81.222.19 (self)
OFFLINE GL-MT3000 100.105.241.84
OFFLINE Redmi 10 100.103.99.16
OFFLINE ilya 100.107.198.111
SKIP imac-rozalia 100.121.88.110 — SSH unreachable
OFFLINE imozerov-Default-string 100.125.157.75
OFFLINE imozerov-IdeaPad-3-15IIL05 100.73.170.56
PASS phaedra 100.94.116.17
OFFLINE rip 100.116.125.102
```

From the reachable owner `phaedra`, the iMac answered Tailscale ping but SSH
authority was still unavailable:

```text
owner=phaedra
pong from imac-rozalia (100.121.88.110) via 5.227.25.156:55351 in 141ms
root@100.121.88.110: Permission denied (publickey,password,keyboard-interactive).
mesh@100.121.88.110: Permission denied (publickey,password,keyboard-interactive).
```

## Disposition

The reachable owner provides network reachability, not the missing SSH
authority or a safe actuator for the six offline peers. No routing, DNS,
firewall, VPN, or peer configuration was changed. Keep the parent warning
blocked and retry after operator-provided SSH authority or a fresh roll-call
delta that supplies a usable owner.
