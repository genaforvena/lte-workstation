# GL-MT3000 read-only access probe — 2026-09-15

Task: `wifi-router-router-access-20260913/establish-router-readonly-access`
Owner: `health`

At `2026-09-15T21:51:39Z`, the router address resolver returned `192.168.8.1` for
`router`. The router is therefore reachable on the LAN, but the authorized read-only
path is not available from this node:

```text
timeout 8 ssh -o BatchMode=yes -o ConnectTimeout=5 root@192.168.8.1 \
  'uname -a; uptime; cat /proc/net/dev; logread 2>/dev/null | tail -20'
root@192.168.8.1: Permission denied (publickey,password).
exit 255
```

The repository's `mesh-wan-traffic` probe independently confirmed the same boundary:
`ERROR: cannot read /proc/net/dev from root@100.105.241.84`. No credentials or private
keys were copied into this artifact. No timestamped router export was available locally.

Decision: block on `external-event`; retry when the router authorizes a read-only SSH/API
identity for WAN, uptime, radio, and system-log reads, or when an operator supplies a
timestamped export of those fields covering the outage.
