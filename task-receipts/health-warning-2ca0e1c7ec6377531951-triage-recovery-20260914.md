# Health warning triage: iMac recovered

Task: `health-warning/2ca0e1c7ec6377531951/triage`

The 08:33Z unreachable warning is cleared as of the fresh recovery evidence gathered on
2026-09-14. At 08:54:37Z the watchdog posted `[health-ok] imac-rozalia — RECOVERED` for
`100.121.88.110`. A live Tailscale status then showed the peer online with a fresh handshake;
`tailscale ping` reached it in 4 ms. A read-only SSH probe over the authenticated Tailscale IP
returned hostname `iMac-Rozalia.lan` and uptime `11 days, 12:06`.

Plain SSH and the `tailscale ssh` wrapper both stopped at missing host-key verification data;
the peer's coordination record advertises no SSH host keys. The successful probe used a temporary
known-hosts file scoped to that authenticated Tailscale peer. It did not change the durable SSH
trust store. The iMac's cause of interruption remains unknown; no LAN route exists here, but the
Tailscale path is currently live.

Disposition: recovered and reachable; close this health warning with the cause unknown. No
routing, DNS, firewall, VPN, Tailscale, or remote-node configuration changed. The resolver receipt
is `task-receipts/unblock-health-807797d851d3d242-resolve-20260914.md`.

Verification: live `tailscale status --json`; `tailscale ping --timeout=8s imac-rozalia` (pong,
4 ms); SSH `hostname; uptime`; `ip route`; and the watchdog recovery line in `~/.mesh/chat.log`.
