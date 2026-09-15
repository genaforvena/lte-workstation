# Health warning triage: imac-rozalia

- Task: `health-warning/9f3857b18d1c1539ba67/triage`
- Owner: `health`
- Observed: 2026-09-11T22:56Z
- Source warning: `imac-rozalia` reported unreachable at `100.121.88.110`.

## Evidence

- `tailscale status --json`: peer is `Online=true`, `Active=true`, relay `hel`.
- `tailscale ping --c 3 imac-rozalia`: pong in 4 ms via `5.227.25.156:55351`.
- `nc -vz -w 3 100.121.88.110 22`: TCP/22 succeeded.
- `ssh -o BatchMode=yes -o ConnectTimeout=5 100.121.88.110 true`: transport reached the host, then failed with `Permission denied (publickey,password,keyboard-interactive)`.
- `mesh-health`: `SKIP imac-rozalia ... SSH unreachable`.

## Verdict

The node is on the tailnet and reachable; the remaining failure is SSH authentication/configuration, not routing or tailnet reachability. No substrate change was safe or authorized from this evidence. Follow-up belongs with the imac SSH credential/service owner.
