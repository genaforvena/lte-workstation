# Health warning triage: imac-rozalia unreachable roll-up

- Task: `health-warning/12aedebfe25b2ebc487f/triage`
- Warning observed: 2026-09-10T21:21:47Z; watchdog classified `100.121.88.110` as unreachable.
- Checked: 2026-09-11T23:29Z, while the dashboard warned local load was high and probes were unreliable.

`tailscale ping --c 1 --timeout 5s imac-rozalia` returned a direct pong in 5 ms via `5.227.25.156:55351`; `nc -vz -w 3 100.121.88.110 22` succeeded. Batch SSH reached the host and was refused at authentication (`Permission denied (publickey,password,keyboard-interactive)`, rc 255).

The warning is a stale or overbroad reachability classification. Current network transport is healthy; SSH authorization remains broken. No routing, VPN, firewall, or peer mutation is indicated. Leave repair with the iMac credential/service owner.
