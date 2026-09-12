# Health warning triage: check-stream delta

Checked 2026-09-12 10:52–10:55 UTC for live task `health-warning/b5f5a3713c087fb8f6e9/triage`.

## Result

The task is live and its warning remains applicable to current state. The FAIL/WARN count comparison in its description is a historical check-stream delta; it is not a current count. Current evidence continues to show the same routing and observability gaps, with no evidence that they have recovered. This was reporting-only; no substrate was changed.

## Evidence

- `mesh-dash --once check` at 10:52:01 UTC showed high local load and explicitly warned that reachability probes were unreliable. The dashboard's doctor cache was from 09:32:30 UTC (3 FAIL/34 WARN, 76 minutes old), so it cannot establish a current count.
- A live `mesh-doctor` run reproduced `FAIL egress rides tailscale0 (overlay/VPN)` and `FAIL exit-node set (...) — SPOF risk`; the output also showed Anthropic reachable. The scan stalled during its later smoke-test phase and was interrupted. No complete current total is claimed.
- `ip route get 1.1.1.1` returned `dev tailscale0 table 52 src 100.81.222.19`, matching the reported egress path.
- `mesh-lan-presence --nodes` exited 1 and reported `UNKNOWN`: no local address in `192.168.8.0/24`, ARP cannot see that subnet, and no known host answered ICMP. Router/LAN state remains unobservable from this node.
- `tailscale status --json`: `phaedra` online and active via relay `tor`, marked as the exit node; `imac-rozalia` online and active via relay `hel`; configured exit-node status online. The single exit-node dependency remains.
- `getent ahostsv4 api.anthropic.com` resolved to `160.79.104.10`, matching the task description.

## Disposition

Keep the route/exit-node and LAN visibility issues open as known health gaps. The check-stream count delta is historical only; rerun `mesh-doctor --comprehensive` after load settles before asserting a fresh total. No routing, DNS, VPN, or firewall state was changed.
