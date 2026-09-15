# Health warning triage: phaedra DERP latency

Chain: `health-warning/4d2c4874e7bd53838a5b/triage`  
Checked: 2026-09-12 09:05 UTC on `mesh-home`  
Source: `path-watch@phaedra` reported 24.9 ms against an 8.45 ms rolling baseline at 2026-09-09 10:39Z.

## Evidence and disposition

- The prior same-window triage in [health-warning-df0d476b150d7096eae0-triage-20260912.md](health-warning-df0d476b150d7096eae0-triage-20260912.md) read phaedra's path-watch tape. It identifies the exact 10:39Z sample as Chicago at 24.9 ms, followed at 11:39Z by Toronto at 9.4 ms; both samples had UDP true. It also documents later 2026-09-12 05:39Z netcheck at Toronto 7.9 ms, UDP true, with direct=2, relay=0, offline=6 at 05:44Z.
- The warning recurred on 2026-09-11 at 16:39Z (27.5 ms / 8.3 ms baseline) and 19:39Z (29 ms / 8.9 ms baseline). The later 05:39Z sample after those alerts is below threshold, so the available tape supports an intermittent region-sensitive DERP latency signal with subsequent recovery, not a continuous outage.
- The consumed check pane at 08:56Z showed phaedra online with vitals OK and local egress OK. It did not expose a newer phaedra path-watch sample, so I make no claim about latency after 05:39Z.

The specific 2026-09-09 warning was real and recovered on the next hourly sample. DERP latency alone does not prove router-VPN or Anthropic egress degradation; no substrate change is indicated. Keep region changes visible when interpreting this pooled rolling-baseline alert.
