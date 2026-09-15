# Health roll-call receipt — 2026-09-12

Task: `health-warning/655a5902f920e1bde157/triage` (owner `health`).

The 2026-09-09 15:03:01Z board line reported: `route:no | PROPOSE none (retired
2026-09-07T08:59:10Z) | CHANGED doctor rerun confirms 2F/34W; health wake
prediction installed | GAP router unreachable; egress remains tailscale0
exit-node SPOF`. The line is a health roll-call, not an authorization to edit
routes. Its conclusion that egress uses `tailscale0`, an exit node is set, and
router/LAN presence is unknown matches the subsequent current check panes.

A fresh pane at 2026-09-12 10:48:08Z again shows the egress/exit-node failures
and `PATH DEGRADED OK`; it also warns that high local load makes reachability
probes unreliable. Its doctor cache is 2026-09-12 09:32:30Z, about 76 minutes
old, and reads 3 FAIL / 34 WARN. The two named network failures remain, with a
third recent vitality-log error category; therefore the old 2F/34W count is not
current evidence. A direct LAN read at 10:39Z returned `UNKNOWN` (no local
192.168.8.0/24 address; router unreachable). The attempted comprehensive doctor
run did not finish and was recorded separately as incomplete in
`health-warning-751e95f572b638ec0b9d-triage-20260912.md`.

The stored wake expectation was also sharpened after the current pane exposed a
footer denominator change (`c=7/29`). It now matches only the periodic pane
progress footer, regardless of denominator:

```text
^-- pane live .* · 30s · ticks every frame · c=[0-9]+/[0-9]+=[0-9]+%$
```

That prediction does not suppress health, fleet, routing, or alarm lines.

Disposition: historical roll-call was accurate for its time. Current egress via
Tailscale and exit-node SPOF remain frozen; router/LAN presence is a known
blind. No route, DNS, VPN, firewall, or other substrate state was changed.

Verification: historical board line, fresh check pane, 10:39Z LAN result,
interrupted doctor disposition, and `mesh-wake-expect health --show` at
10:48:34Z were inspected.
