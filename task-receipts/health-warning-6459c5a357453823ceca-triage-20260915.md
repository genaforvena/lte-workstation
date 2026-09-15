# Health warning triage: phaedra DERP latency

Date: 2026-09-15  
Owner: health / mesh-home  
Task: `health-warning/6459c5a357453823ceca/triage`

## Verdict

The 2026-09-15 02:39Z warning was a real Phaedra-side DERP observation: the
remote `path-watch.log` records `udp=true derp=Toronto lat_ms=22.5`, against
the board's rolling baseline of 8.7 ms. It recovered on the next hourly sample
(`03:39Z`, Toronto, 7.5 ms). Later samples remained variable but mostly low
(6.8–14.5 ms through 20:39Z; 8.5 ms at 17:39Z and 9.5 ms at 19:39Z).

This supports an intermittent, region-sensitive DERP latency warning, not a
confirmed router-VPN or Anthropic application-egress failure. At the live
check, mesh-home egress was OK with 0% loss, and `mesh-path-watch --status`
reported Phaedra direct (`peers=8 direct=2 relay=0 offline=6`). No routing,
DNS, firewall, VPN, or Tailscale state was changed.

## Evidence

- `mesh-dash --once check` at 2026-09-15T20:57:36Z–20:57:38Z: egress OK,
  current loss 0%, Phaedra's fleet path present; it also surfaced the
  separate local-load and stale WireGuard-client warnings.
- Read-only `ssh phaedra` at 20:58Z: exact 02:39Z sample, 03:39Z recovery,
  and hourly samples through 20:39Z; the 20:39Z sample was Toronto 6.8 ms.
- `mesh-path-watch --status` at 20:58Z: Phaedra direct, no relay peers.
- Existing receipts for the same warning class (`health-warning-9a7...` and
  `health-warning-386...`) independently show region changes and recovered
  DERP latency; they do not establish application-egress attribution.

## Disposition

Close as recovered historical early warning. Keep DERP region/latency and
application egress as separate measurements. The current fleet pane's
`PROBE-WARNING: LOCAL LOAD HIGH` and WireGuard-client freshness warning remain
separate health findings.
