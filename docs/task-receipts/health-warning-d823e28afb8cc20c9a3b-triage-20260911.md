# Health warning triage: imac-rozalia chronic suppression roll-up

- Task: `health-warning/d823e28afb8cc20c9a3b/triage`
- Owner: `health`
- Observed: 2026-09-11T23:12Z
- Warning: watchdog's chronic-suppression roll-up repeats `100.121.88.110 — SSH unreachable`.

## Evidence

- `tailscale ping --c 1 imac-rozalia`: pong in 4 ms via `5.227.25.156:55351` (direct endpoint; the earlier 23:08Z receipt observed DERP).
- `nc -vz -w 3 100.121.88.110 22`: TCP/22 succeeded.
- `ssh -o BatchMode=yes -o ConnectTimeout=5 100.121.88.110 true`: authentication refused with `Permission denied (publickey,password,keyboard-interactive)`.
- The one-shot health pane lists imac-rozalia among fleet peers reported down, while warning that local load is high and reachability probes are unreliable.

## Verdict

This pass confirms that the iMac is online and reachable over Tailscale, with SSH transport open. SSH authentication remains broken, so the recurring `SSH unreachable` watchdog wording collapses a credential failure into reachability. The path has improved from the DERP observation in the earlier receipt, but the auth fault persists. No network or substrate change is indicated; leave credential/service repair with the iMac owner and recheck SSH on the next relevant health wake.
