# Health warning triage: Phaedra DERP latency

Task: `health-warning/e080ff604c9aefe1d3eb/triage`  
Source: `mesh-path-watch@phaedra` FYI at 2026-09-13T23:39:05Z

## Finding

The reported sample is present in Phaedra's `~/.mesh/path-watch.log`:
`2026-09-13T23:39:01Z netweather udp=true derp=New_York_City lat_ms=18`. It exceeded twice
the warning's 8.75 ms rolling baseline. Later samples show recovery and region variation: New York
12.8 ms at 00:39Z, Toronto readings mostly 6.8–9.3 ms through 18:39Z, New York 16.2 ms at
19:39Z, and Toronto 11.1 ms at 20:39Z on Sep 14. UDP remained true in these samples. This is a
real, intermittent DERP-latency warning, not evidence of a continuous relay failure.

At 21:09Z, `mesh-path-watch --status` reported Phaedra direct, with 2 direct peers, 0 relay peers,
and 6 offline peers. The live `mesh-dash --once check` at 21:09Z reported current egress OK with
0% loss and 0/438 attributed bad results over 24h; 38 results were unattributed. These readings
show no current local egress failure, while the unattributed sample gap and lack of application-level
measurements limit what can be concluded about router-VPN or Anthropic-access quality.

## Ledger and disposition

I inspected the repository's prior DERP triages and the structured task ledger. No exact active
prerequisite task for this warning or its egress attribution was present; the related open Phaedra
tasks concern unrelated autostash stewardship. Prior DERP triages document the same limitation:
relay latency alone does not establish exit-node or application-egress degradation.

Disposition: recovered intermittent DERP latency; no current egress failure observed. Keep the
Phaedra exit-node dependency and unattributed egress readings visible as known availability and
measurement gaps. No route, DNS, firewall, VPN, or Tailscale state was changed; the existing route
hold remains untouched pending operator release.

## Verification

- `mesh-task check dispatch health-warning/e080ff604c9aefe1d3eb/triage health`: exit 0; task taken
  by health.
- Read-only SSH to `phaedra-direct`: exact 23:39Z warning and subsequent path-watch samples above.
- `mesh-path-watch --status` at 21:09:01Z: Phaedra direct; 0 relays.
- `mesh-dash --once check` at 21:09:39Z–21:09:46Z: egress OK, 0% loss, 0/438 attributed bad,
  38 unattributed.
- `mesh-task replay --json`: no exact open prerequisite beyond this claimed triage.
