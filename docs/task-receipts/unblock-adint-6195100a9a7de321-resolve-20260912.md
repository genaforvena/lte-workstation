# Health self-unblock receipt — adint/6195100a9a7de321

- Resolver: `unblock/adint/6195100a9a7de321/resolve`
- Parent dependency: `unblock/health/fb535b4b0bde328a/resolve`
- Checked: `2026-09-12T00:16Z`

## Evidence

The fresh local `mesh-health` sweep reports `mesh-home` and `phaedra` reachable,
six peers offline, and `imac-rozalia` SSH-unreachable:

```text
PASS  mesh-home
OFFLINE GL-MT3000
OFFLINE Redmi 10
OFFLINE ilya
SKIP  imac-rozalia — SSH unreachable
OFFLINE imozerov-Default-string
OFFLINE imozerov-IdeaPad-3-15IIL05
OFFLINE rip
PASS  phaedra
```

The same-day read-only vantage-point check recorded in
[`unblock-adint-2d7c9989cda4a033-resolve-20260912.md`](unblock-adint-2d7c9989cda4a033-resolve-20260912.md)
shows that `phaedra` timed out to all six offline peers and the iMac refused
the configured SSH identity. No safe local actuation or authorized reachable
owner is available to restore those devices or credentials.

## Result and exact prerequisite

The dependency is not cleared. Do not change routing, DNS, firewall, VPN,
peer configuration, or remote-node state from this window. Retry only after a
fresh roll-call delta shows the six peers reachable and SSH access to
`imac-rozalia` is authorized, or an authorized reachable owner can perform the
required recovery and provide that evidence. Keep the parent blocked on
`event:roll-call-delta` until then.
