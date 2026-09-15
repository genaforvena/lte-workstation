# Health warning triage: `health-warning/1acc36a9d73a0cdecc37`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/1acc36a9d73a0cdecc37/triage`

## Verdict

The direct→relay warning is a recurring carrier/NAT degradation, not a local
UDP failure and not a safe substrate change. Current state is mixed: phaedra
is direct and imac-rozalia is relayed. Keep observing; do not alter routing,
DNS, firewall, VPN, or Tailscale state from this triage.

## Evidence

- `mesh-dash --once check` at 23:38:28Z showed both peers online and the
  fleet path summary `direct=2 relay=0 offline=6`.
- `mesh-path-watch --once` at 23:39:19Z returned `QUIET (peers=8 direct=1
  relay=1 offline=6 ...)`, with `imac-rozalia=relay` and `phaedra=direct`.
- `tailscale status --json` confirmed `imac-rozalia online:true` and
  `phaedra online:true`.
- `~/.mesh/path-watch.log` records repeated direct↔relay transitions for both
  peers through 23:39:19Z. The same tape records `netweather udp=true` at
  19:54Z, 20:54Z, 21:54Z, and 22:54Z; no `[path-udp-blocked]` root-cause
  line appears in the inspected recent window.
- The standalone `mesh-netweather` command is not installed; the path-watch
  tape is the available netweather evidence.

## Verification

```text
mesh-dash --once check                                             PASS
mesh-task queue --dispatch --owner health                          PASS
mesh-task check dispatch health-warning/1acc36a9d73a0cdecc37/triage health  exit 0
MESH_TASK_ACTOR=health mesh-task take health-warning/1acc36a9d73a0cdecc37 triage  PASS
mesh-path-watch --once                                             PASS (current sample)
tailscale status --json                                            PASS (both peers online)
```

No substrate state was changed.
