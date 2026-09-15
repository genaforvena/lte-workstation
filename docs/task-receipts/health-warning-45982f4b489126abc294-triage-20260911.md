# Health-warning triage: `health-warning/45982f4b489126abc294`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/45982f4b489126abc294/triage`

## Verdict

The warning is a chronic, still-present reachability condition for
`imac-rozalia`, not a new local substrate fault and not safely repairable from
this window. The node is currently online in Tailscale and reachable by ICMP,
but only through DERP relay; SSH authentication is refused. No routing, DNS,
firewall, VPN, Tailscale, or other substrate mutation was performed.

## Evidence

Dispatched warning:

```text
[health-fail] imac-rozalia — CHRONIC SUPPRESSION ROLL-UP, not a new fault:
the SAME failure text has recurred inside this host's own measured recurrence
window and each cycle was routed to mesh-trace instead of the board
(chronic sig=35f22fafd26a gap=107393s win=351600s(measured n=15)
suppressed=1). The fault has NOT cleared ... Last text:
100.121.88.110 — SSH unreachable
```

Fresh targeted probes at 2026-09-11T23:44Z:

- `tailscale status --json`: `imac-rozalia` `Online=true`, `Active=true`,
  address `100.121.88.110`, relay `hel`.
- `tailscale ping --c 3 imac-rozalia`: 3/3 replies via `DERP(hel)`, 282 ms;
  direct connection not established.
- `ping -c 3 -W 2 100.121.88.110`: 3/3 replies, 0% loss, average 283.975 ms.
- `ssh -o BatchMode=yes -o ConnectTimeout=5 100.121.88.110 true`:
  `Permission denied (publickey,password,keyboard-interactive)`, rc 255.

This confirms the health row's last failure mode remains observable, while the
node is not currently offline. It is an access/authentication or remote-side
condition requiring the node owner; broad or substrate-changing intervention
is not justified here.

## Verification

```text
mesh-dash --once check
mesh-task queue --dispatch --owner health
mesh-task check dispatch health-warning/45982f4b489126abc294/triage health  # rc 0
MESH_TASK_ACTOR=health mesh-task take health-warning/45982f4b489126abc294 triage
tailscale status --json
tailscale ping --c 3 imac-rozalia
ping -c 3 -W 2 100.121.88.110
ssh -o BatchMode=yes -o ConnectTimeout=5 100.121.88.110 true  # rc 255
```

Known limitation: the probe establishes tailnet/ICMP reachability and the
current SSH authentication result, but cannot distinguish a bad key from a
remote SSH policy or account issue without authorized access to the Mac.
