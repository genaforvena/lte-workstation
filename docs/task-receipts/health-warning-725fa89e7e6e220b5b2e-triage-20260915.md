# Health warning triage — 2026-09-15

- Exact task: `health-warning/725fa89e7e6e220b5b2e/triage`
- Source warning: 2026-09-14 check-stream reported 1.1.1.1 via `tailscale0` table 52, LAN unknown, and imac-rozalia changing from relay/offline to active/direct.
- Fresh evidence at 2026-09-15T19:16Z: `ip route get 1.1.1.1` returns `via 192.168.8.1 dev enp42s0`; `getent ahostsv4 api.anthropic.com` returns `160.79.104.10`; Tailscale reports `imac-rozalia online=true active=true relay=hel`.
- The current pane independently reports egress OK and both LAN targets up. The old route/LAN warning is therefore superseded; relay status is a working degraded path, not a routing failure. No substrate mutation is justified.
- Disposition: historical check-stream delta closed as superseded by current FIB/DNS/Tailscale evidence.
