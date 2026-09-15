# Health warning triage: imac-rozalia

- Task: `health-warning/2a8368b3bd4ca25c577c/triage`
- Owner: `health`
- Observed: 2026-09-11T23:05Z
- Warning: watchdog reported `imac-rozalia` unreachable at `100.121.88.110`.

## Evidence

- `tailscale status`: the peer is active and using relay `hel`.
- `tailscale ping --c 1 imac-rozalia`: pong in 1.121 s via DERP `hel`; direct connection was not established (the command exits 1 for this relay result).
- `nc -vz -w 3 100.121.88.110 22`: TCP/22 succeeded.
- `ssh -o BatchMode=yes -o ConnectTimeout=5 100.121.88.110 true`: transport reached the host, then failed with `Permission denied (publickey,password,keyboard-interactive)`.
- The check pane reports local load high and warns that broad reachability probes are unreliable; these targeted checks establish this host's current path without relying on the broad probe.

## Verdict

The `UNREACHABLE` / “not on tailnet” warning is stale or overbroad for this observation: `imac-rozalia` is online over DERP and accepts TCP/22. The remaining known failure boundary is SSH authentication. No network or substrate change is indicated; follow-up belongs with the iMac SSH credential/service owner. Direct-path availability remains degraded, but does not make the node unreachable.
