# Triage historical Phaedra DERP-latency warning

Task: `health-warning/6ea8a6da5b41c9a87b5c/triage`  
Source: `mesh-path-watch@mesh-home` FYI at 2026-09-13T10:39:04Z

The warning was an early signal: measured Phaedra DERP latency of 22.5 ms was
over twice its then-rolling 8.85 ms baseline. The current path-watch sample at
20:44:01Z on Sep 14 reports Phaedra direct; the targeted Tailscale status read
shows it online and active with a current endpoint. The 20:39Z one-shot check
pane reports egress OK with 0% loss and a 24-hour record of 0 bad samples.
Thus the historical DERP sample no longer describes Phaedra's currently
observed path or the present egress result.

The configured Phaedra exit-node dependency remains a known single-node
availability risk. This receipt does not treat one recovered direct path as a
resilience fix or establish Phaedra's own upstream state. No route, VPN, DNS,
firewall, or Tailscale state was changed.

## Verification

- `rtk mesh-path-watch --status` at 20:44:01Z: Phaedra direct; path watcher OK.
- `rtk tailscale status --json` at about 20:44Z: Phaedra online and active with
  endpoint `38.49.216.141:41641`.
- `rtk mesh-dash --once check` at 20:38:58Z: egress OK, loss 0%, 0/436 bad
  samples in the 24-hour summary.
- No active egress failure or fresh relay-path fault appeared in these reads.
