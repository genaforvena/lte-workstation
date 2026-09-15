# Health-warning triage `20774950d4fe83d98b86` — 2026-09-09

## Disposition

The assigned warning is a known LAN-organ blindness, not a new local failure and not a
repair candidate. The source handoff's LAN probe was UNKNOWN, and a fresh probe at
2026-09-09 reproduced the same condition:

```text
mesh-lan-presence --nodes
mesh-lan-presence: router unreachable — UNKNOWN (no local address in 192.168.8.0/24 ; ARP cannot see that segment from here, and no known host answered ICMP)
HOST                       IP              MAC                STATE    MESH-NODE
?                          192.168.8.0/24  ?                  UNKNOWN
rc=1
```

The current `mesh-doctor --once` still reports the pre-existing egress-over-Tailscale and
exit-node warnings, while all supervised loops are PASS. `tailscale status` is live and
shows `mesh-home` online. No routing, DNS, firewall, VPN, or other substrate state was
changed.

This agrees with `docs/lan-newdevice-disposition-20260907.md`: the LAN organ is absent or
unreachable on this node, and the visible ruling expires at `2026-09-14T18:53:25Z`.
Re-check availability after that expiry; do not re-file the repair class before then.

## Verification

- `mesh-doctor --once`: completed; egress/exit-node FAILs and supervised-loops PASS observed.
- `mesh-lan-presence --nodes`: reproduced UNKNOWN, rc=1.
- `tailscale status`: completed rc=0; `mesh-home` listed online.
- Existing ruling and prior reconciliation reviewed; no substrate mutation performed.
