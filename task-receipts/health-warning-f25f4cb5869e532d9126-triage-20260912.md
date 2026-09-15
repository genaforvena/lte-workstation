# Health warning triage: `health-warning/f25f4cb5869e532d9126`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/f25f4cb5869e532d9126/triage`

## Verdict

The 2026-09-11 16:39Z alert records a real DERP latency spike at Toronto (27.5 ms), followed by 8.7 ms one hour later. A second Toronto spike at 19:39Z (29 ms) fell to 14.6 ms at 20:39Z and 8.1 ms at 21:39Z. Phaedra's latest available netweather sample, 2026-09-12 15:39Z, is Toronto at 7.4 ms with UDP true; its 15:59Z path state is 2 direct, 0 relay, 6 offline. This supports intermittent DERP latency with recovery, not a persistent relay-path failure.

The alert text's inference that router-VPN egress or Anthropic access is degrading is not established by this signal. DERP netcheck latency is a relay-region path measurement, and the tape does not measure application egress. No routing, DNS, firewall, VPN, or exit-node change is indicated by this task.

There is a concrete detector limitation to retain: phaedra's installed `/root/.local/bin/mesh-path-watch` has SHA-256 `317253ae7a5b7cf51d35ee6c99d55eb7e3e004868b5112622fa7083a0312ddd59` and still emits the pooled `2× rolling baseline` warning. The repository source has SHA-256 `384ba31d7dae563cccf8b0ab024d5b812e69529202868fb3b223ff636ff8cf97` and now computes a same-region baseline. The same-region correction is present in source but is not deployed on phaedra; region-mixed comparisons remain a known blind spot on that node.

## Evidence and verification

- The exact board event is in `/home/mesh-home/.mesh/chat.log` at `2026-09-11T16:39:04Z`.
- Read-only SSH inspection of `phaedra:~/.mesh/path-watch.log` showed `16:39 Toronto 27.5`, `17:39 Toronto 8.7`, `19:39 Toronto 29`, `20:39 Toronto 14.6`, `21:39 Toronto 8.1`, then later hourly samples; UDP was true for the cited netweather rows.
- Read-only phaedra state at `2026-09-12T15:59:01Z`: `direct=2 relay=0 offline=6`; latest netweather sample at `15:39:01Z`: Toronto, 7.4 ms.
- Read-only comparison of installed and repository `mesh-path-watch` confirmed the old pooled alert wording is deployed while repository source uses same-region samples.
- The live check pane still reports fleet reachability 2/10 and tailscale0 egress with an exit-node SPOF. Those are separate known fleet risks; this DERP sample does not diagnose or clear them.

Disposition: recovered intermittent DERP-latency warning; its egress attribution is a known measurement blind spot. Keep the fleet egress/SPOF alarm open under its own evidence and track deployment of the same-region detector separately.
