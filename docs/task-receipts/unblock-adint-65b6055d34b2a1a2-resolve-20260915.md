# Receipt: unblock/adint/65b6055d34b2a1a2/resolve

- Recorded: 2026-09-15T22:27:00Z
- Owner: `adint`
- Parent blocker: `unblock/health/9ad40db2ce1b9976/resolve`
- Exact prerequisite: `wifi-router-router-access-20260913/establish-router-readonly-access`

## Evidence

The router at `192.168.8.1` is reachable from `mesh-home` at the network layer:

```text
ping -c 1 -W 2 192.168.8.1
1 packets transmitted, 1 received, 0% packet loss
rtt min/avg/max/mdev = 0.504/0.504/0.504/0.000 ms
```

The non-mutating SSH probe cannot authenticate:

```text
ssh -o BatchMode=yes -o ConnectTimeout=5 root@192.168.8.1 true
root@192.168.8.1: Permission denied (publickey,password).
```

No router settings, credentials, keys, or logs were changed or stored.

## Narrowest safe next action

The external atom is one of the following operator-supplied evidence paths:

1. Authorize a dedicated read-only router identity for WAN status, uptime, radio state, and
   system-log reads, then notify the mesh that the identity is ready (do not send the private key
   in chat or commit it).
2. Provide a timestamped export of those same fields and the relevant outage/system-log window.

After either path exists, `health` can retry the authenticated read and close its waiting gate.
Until then, the blocker is irreducible from this node: ICMP reachability alone does not provide
router state, and adint must not alter the router.

## Verification

- ICMP reachability probe: passed.
- SSH authentication probe: failed as expected; exit code 255.
- Router mutation: not attempted.
