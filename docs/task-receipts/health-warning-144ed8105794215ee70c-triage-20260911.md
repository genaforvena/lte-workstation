# Health warning triage: imac-rozalia chronic suppression roll-up

- Task: `health-warning/144ed8105794215ee70c/triage`
- Owner: `health`
- Warning observed: 2026-09-11T01:21:51Z; chronic signature `35f22fafd26a`, repeated `100.121.88.110 — SSH unreachable` within its measured recurrence window.
- Targeted recheck: 2026-09-11T23:16Z.

## Evidence

- `tailscale ping --c 1 --timeout 5s imac-rozalia`: pong in 7 ms via direct endpoint `5.227.25.156:55351`.
- `nc -vz -w 3 100.121.88.110 22`: TCP/22 succeeded.
- `ssh -o BatchMode=yes -o ConnectTimeout=5 100.121.88.110 true`: reached the host, then failed with `Permission denied (publickey,password,keyboard-interactive)`.
- The one-shot dashboard still reports fleet reachability as degraded and warns that high local load makes its probes unreliable. These direct targeted results establish current iMac reachability; they do not establish that other peers are reachable.

## Verdict

This warning is a chronic SSH-authentication failure currently rendered as `SSH unreachable`: the iMac is online over a direct Tailscale path and accepts TCP/22, but this node's SSH credentials are refused. No routing, VPN, or other substrate change is indicated. Credential or SSH-service repair requires the iMac owner; retain the recurring signature as known degraded SSH access and recheck after that owner changes the target state.
