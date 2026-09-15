# Health warning triage: imac-rozalia chronic suppression roll-up

- Task: `health-warning/ebcbe63cb6ea8ca3ab7e/triage`
- Checked: 2026-09-11T23:20Z

`tailscale ping --c 1 --timeout 5s imac-rozalia` reached the iMac via DERP `hel` in 1.178s; direct connection was not established. `nc -vz -w 3 100.121.88.110 22` succeeded. A verbose batch SSH attempt completed transport and then exhausted public-key authentication, ending `Permission denied (publickey,password,keyboard-interactive)` with rc 255.

The chronic `SSH unreachable` roll-up therefore remains a degraded SSH-authentication/path condition, not evidence of a local outage. No routing, VPN, firewall, or other substrate change is indicated. Keep credential/service repair with the iMac owner and recheck on a fresh roll-call delta.
