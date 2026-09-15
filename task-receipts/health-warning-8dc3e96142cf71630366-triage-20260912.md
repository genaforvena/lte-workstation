# Health warning triage: `health-warning/8dc3e96142cf71630366`

Checked 2026-09-12 11:13–11:16 UTC. The task row was open and dispatched; `mesh-task check dispatch health-warning/8dc3e96142cf71630366/triage health` exited 0, and `mesh-task take health-warning/8dc3e96142cf71630366 triage` claimed it.

## Finding

The 2026-09-09 report was accurate as a historical delta, but one peer-path change was transient: `imac-rozalia` is currently active direct, not relayed via `hel`. The LAN visibility and egress warnings remain. `api.anthropic.com` still resolves to `160.79.104.10`. No substrate state was changed.

## Current evidence

- `mesh-card --refresh` (11:13:20Z) reports default egress via `tailscale0`, exit node `phaedra`, and an invariant violation: LAN address `100.74.0.1` is swallowed through Tailscale table 52 rather than the LAN link.
- `ip route get 100.74.0.1` returns `dev tailscale0 table 52 src 100.81.222.19`.
- `mesh-lan-presence --nodes` exits 1 and reports router unreachable / UNKNOWN: no local address in `192.168.8.0/24`, and no known host answered ICMP.
- `tailscale status` shows `imac-rozalia` active direct (`5.227.25.156:55351`) and `phaedra` active direct and serving as exit node. Thus the old imac relay condition has cleared; the phaedra exit-node dependency has not.
- `dig +short A api.anthropic.com` returns `160.79.104.10`, matching the reported A record.
- `resolvectl status` currently lists DNS servers `213.87.2.89` and `217.66.16.35` on `enp42s0`; Tailscale DNS is also configured. These are resolver addresses, distinct from the queried A record.
- A current `mesh-doctor --help` call unexpectedly ran the full interactive doctor (there is no help path). It reproduced the two egress FAILs and WARNs for the default mic device, untimed peer SSH (`mesh-load-audit`), six `librosa-analysis` funnel bypasses, and five absence-as-negative sites. It entered tool smoke tests, then produced no output for 30 seconds; I interrupted it after roughly 90 seconds. It exited 130, so this invocation supplies no completed total. Do not treat the historical 2F/34W count as freshly verified.

## Disposition

Keep the LAN visibility and Tailscale egress / exit-node dependency open as known health gaps. The imac relay item is resolved in the current observation. Comprehensive doctor total remains unresolved because the run stalled in smoke tests. No route, DNS, firewall, or VPN configuration was changed.
