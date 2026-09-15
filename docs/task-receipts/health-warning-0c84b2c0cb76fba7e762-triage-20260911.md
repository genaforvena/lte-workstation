# Health warning triage: imac-rozalia chronic suppression roll-up

- Task: `health-warning/0c84b2c0cb76fba7e762/triage`
- Owner: `health`
- Observed: 2026-09-11T23:08Z
- Warning: watchdog reported a chronic suppression roll-up for repeated `100.121.88.110 — SSH unreachable` failures. Its own recurrence window confirms this is recurring, not a new fault.

## Evidence

- `tailscale ping --c 1 imac-rozalia`: pong in 1.013 s via DERP `hel`; direct connection was not established (the command exits 1 for this relay result).
- `nc -vz -w 3 100.121.88.110 22`: TCP/22 succeeded.
- `ssh -o BatchMode=yes -o ConnectTimeout=5 100.121.88.110 true`: transport reached the host, then failed with `Permission denied (publickey,password,keyboard-interactive)`.
- The live check pane still lists `imac-rozalia` as `NOSSH`; the targeted checks distinguish the reachable DERP/SSH transport from the refused SSH authentication.

## Verdict

The repeated `SSH unreachable` watchdog text is overbroad for this observation: the iMac is online over DERP and accepts TCP/22. The remaining failure boundary is SSH authentication; direct-path availability is degraded. No network or substrate change is indicated. Keep the authentication follow-up with the iMac SSH credential/service owner and retain this recurring signature as known degraded reachability until that owner resolves it.
