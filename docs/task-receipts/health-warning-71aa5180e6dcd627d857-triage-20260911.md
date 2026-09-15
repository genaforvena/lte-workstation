# Health warning triage: imac-rozalia

- Task: `health-warning/71aa5180e6dcd627d857/triage`
- Owner: `health`
- Observed: 2026-09-11T22:59Z
- Source warning: watchdog reported `imac-rozalia` unreachable at `100.121.88.110`.

## Evidence

- The check pane reports local load high and says broad reachability probes are unreliable.
- `tailscale status --json`: peer is `Online=true`, `Active=true`, using relay `hel`.
- `tailscale ping --c 1 imac-rozalia`: pong in 2.213 s via DERP `hel`; direct connection was not established.
- `nc -vz -w 3 100.121.88.110 22`: TCP/22 succeeded.
- `ssh -o BatchMode=yes -o ConnectTimeout=5 100.121.88.110 true`: transport reached the host, then failed with `Permission denied (publickey,password,keyboard-interactive)`.
- Recent `mesh-trace` shows a relay-to-direct recovery at 22:54Z, followed by the current relay path; this is path churn, not proof the node is offline.

## Verdict

The warning's “not on tailnet” diagnosis is stale for this observation: the peer is online and reachable over its relay. SSH authentication remains the known failure boundary. No substrate change is indicated; follow-up belongs with the iMac SSH credential/service owner. The fleet-wide load warning limits broad probe conclusions, so the current verdict is based on targeted Tailscale and TCP/SSH checks.
