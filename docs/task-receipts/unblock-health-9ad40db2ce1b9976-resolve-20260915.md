# Resolver result — GL-MT3000 read-only access blocker

Resolver: `unblock/health/9ad40db2ce1b9976/resolve`
Parent: `wifi-router-router-access-20260913/establish-router-readonly-access`
Observed at: `2026-09-15T21:51:39Z`

The mesh-owned recovery path is exhausted for this blocker. The router answers on its
LAN address `192.168.8.1`, but the only available noninteractive SSH attempt is refused
by the router's SSH authentication boundary:

```text
root@192.168.8.1: Permission denied (publickey,password).
```

The existing `mesh-wan-traffic` probe also cannot read `/proc/net/dev` because its
router identity is not authorized. No credentials or private keys are copied here.

Required operator action: authorize a read-only SSH/API identity on the GL-MT3000 for
WAN counters, uptime, radio state, and system logs, or place a timestamped export of
those fields covering the outage in a safe operator-provided location. Then rerun the
router-access task and validate the authenticated reads. Until that external event,
the parent must remain blocked; there is no safe mesh-owned command that can grant
router authorization or fabricate the missing outage evidence.

Result: terminal blocker evidence; no `unblock=cleared` claim is made.

Follow-up probe at `2026-09-15T22:20Z`: `ping -c 1 -W 2 192.168.8.1` succeeded
(0% loss, 0.476 ms), while `ssh -o BatchMode=yes -o ConnectTimeout=5
root@192.168.8.1 true` still returned `Permission denied (publickey,password)`.
The resolver was therefore left queued behind
`wifi-router-router-access-20260913/establish-router-readonly-access`; the mesh
created owner-routed recovery task
`unblock/adint/65b6055d34b2a1a2/resolve` for the remaining external prerequisite.
