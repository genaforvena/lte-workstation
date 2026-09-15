# Health warning triage: phaedra DERP latency

Date: 2026-09-14  
Owner: health / mesh-home  
Task: `health-warning/9a7cd36c3e345443f840/triage`

## Verdict

The 2026-09-13 20:39Z sample was a real high-latency DERP observation: phaedra recorded
`udp=true derp=Ashburn lat_ms=32.4`; the board warning compared it with an 8.7 ms baseline.
At 21:39Z the nearest relay changed to Toronto and measured 8.9 ms. Subsequent samples moved
between regions: New York City at 15.8 and 18 ms, then Toronto at 7.7 and 7.5 ms. This supports
intermittent, region-dependent relay latency. The tape does not establish that the router VPN or
Anthropic application egress degraded.

The current check pane at 21:03Z reports local egress `OK`, loss 0%, and 0 bad results among 438
24-hour attributed checks (38 un-attributed). Its VPN section independently says SS/trojan/WG are
up but no WireGuard client has handshaken in over 24 hours; 0 clients are active or idle, with 12
stale and 4 never-used provisioned clients. That is an idle-client/WG freshness warning, not evidence
that the DERP sample broke active egress. No route or other substrate change is indicated.

## Evidence

- Read-only SSH inspection of `phaedra:~/.mesh/path-watch.log` confirmed the exact 20:39Z event,
  the 21:39Z follow-up, and hourly samples through 2026-09-14 20:39Z. The follow-up day remained
  `udp=true`; Toronto samples were mostly 6.8–11.1 ms, with New York City samples of 16.2–17.7 ms.
- `scripts/mesh-path-watch` currently groups the rolling baseline by nearest-DERP region and emits
  the region and sample count in a latency alert. The historical board line omits the region, so
  its quoted baseline cannot be independently reconstructed from the tape alone.
- `mesh-dash --once check` completed at 2026-09-14T21:03:49Z–21:03:58Z. It showed `PATH: DEGRADED`
  with one relay among eight peers, and the separate VPN/egress readings above. Earlier one-shot
  invocations exceeded 30 seconds without captured output; the later one-shot succeeded, so this is
  a latency observation rather than a confirmed pane failure.
- `mesh-vpn-health --edge` at 21:03:28Z reported SS/trojan/WG up, no WG handshake in >24h, and
  0 active / 0 idle clients. The one-shot pane reported current egress OK.
- No routing, DNS, firewall, VPN, or exit-node state was changed. The existing route hold remains
  in force pending operator release.

Disposition: the specific DERP warning was real but recovered on the next sample from another
region; router-VPN/application-egress attribution remains a known measurement limitation. Keep the
separate fleet PATH and WireGuard-client freshness findings visible under their own evidence.
