# Health warning triage: `health-warning/df0d476b150d7096eae0`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/df0d476b150d7096eae0/triage`

## Verdict

The specific warning was a real 32 ms netcheck sample, followed by recovery to
7.3 ms one hour later. It does not establish router-VPN degradation: the
nearest DERP changed from New York City at the spike to Toronto on the next
sample, and the alert baseline pools latency samples across DERP regions. Later
samples show another 24.9 ms observation while nearest DERP was Chicago,
followed by Toronto samples near 6–12 ms. This is consistent with intermittent
latency and changing relay selection; it is not evidence for a substrate
change. Treat DERP latency as a coarse path-quality hint, not a direct egress
or Anthropic-lifeline verdict.

## Evidence

- The exact board event exists at `2026-09-09T08:39:04Z` and matches the task
  measurement: 32 ms against an 8.65 ms rolling baseline.
- Read-only inspection of `phaedra:~/.mesh/path-watch.log` shows hourly samples
  around that event: 07:39 New York City 10.8 ms; 08:39 New York City 32 ms;
  09:39 Toronto 7.3 ms; 10:39 Chicago 24.9 ms; 11:39 Toronto 9.4 ms. All had
  `udp=true`.
- The current remote path-watch state at `2026-09-12T05:44:02Z` is
  `direct=2 relay=0 offline=6`; latest netweather sample at 05:39Z is
  `udp=true derp=Toronto lat_ms=7.9`. Recent 02:39, 03:39, and 04:39 samples
  were 7.5, 7.6, and 8.7 ms (the 04:39 sample used New York City).
- In `scripts/mesh-path-watch`, `heavy_lane` records the `Nearest DERP` name
  and first reported DERP latency, but computes the rolling median from the
  last 24 `lat_ms` values without grouping by the recorded DERP region. The
  detector is therefore sensitive to relay-region changes as well as path
  degradation.
- The pane's live `mesh-card --refresh` reports upstream OK. No routing, DNS,
  firewall, VPN, or Tailscale state was changed.

## Verification

```text
Board history exact warning lookup                       PASS
phaedra path-watch status and recent netweather tape     PASS (read-only SSH)
Source inspection of DERP baseline and alert predicate   PASS
Current phaedra state                                    PASS (direct=2 relay=0; UDP=true; 7.9 ms)
```

Follow-up if this signal is tuned: compare like-for-like DERP regions or make
region changes explicit in the alert evidence before interpreting a latency
increase as router-VPN degradation.
