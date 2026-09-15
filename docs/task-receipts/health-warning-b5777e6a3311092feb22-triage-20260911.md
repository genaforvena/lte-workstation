# Health-warning triage: `health-warning/b5777e6a3311092feb22`

- Checked: `2026-09-11T23:47:52Z`
- Owner: `health` on `mesh-home`
- Subject: `imac-rozalia` (`100.121.88.110`)

## Verdict

The chronic warning remains a degraded access condition, not a local substrate
outage. The iMac is reachable over Tailscale/ICMP and TCP/22, but SSH
authentication is refused. No routing, DNS, firewall, VPN, or Tailscale
mutation is justified from this window; repair remains with the iMac
credential/service owner.

## Fresh evidence

- `mesh-dash --once check`: fleet currently reports `imac-rozalia` down and
  warns that local load makes reachability probes unreliable.
- `tailscale ping --c 1 --timeout 5s imac-rozalia`: pong via `DERP(hel)` in
  283 ms; direct connection was not established (command rc 1 for relay).
- `nc -vz -w 3 100.121.88.110 22`: TCP/22 succeeded.
- `ssh -o BatchMode=yes -o ConnectTimeout=5 100.121.88.110 true`: rc 255,
  `Permission denied (publickey,password,keyboard-interactive)`.
- `mesh-health`: `SKIP imac-rozalia — SSH unreachable`.

The source roll-up's `SSH unreachable` label therefore collapses a reachable
transport with an authentication failure; it is still an unresolved known
blindness, not a newly actionable network fault.

## Verification commands

```text
mesh-dash --once check
mesh-task queue --dispatch --owner health
mesh-task check dispatch health-warning/b5777e6a3311092feb22/triage health  # rc 0
MESH_TASK_ACTOR=health mesh-task take health-warning/b5777e6a3311092feb22 triage
tailscale ping --c 1 --timeout 5s imac-rozalia
nc -vz -w 3 100.121.88.110 22
ssh -o BatchMode=yes -o ConnectTimeout=5 100.121.88.110 true  # rc 255
mesh-health
```

Known limitation: without authorized access to the Mac, this cannot distinguish
an incorrect key from remote SSH account or policy configuration.
