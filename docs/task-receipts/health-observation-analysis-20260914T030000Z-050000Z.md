# Health observation analysis: 2026-09-14 03:00–05:00Z

Task: `20260914T030000Z-050000Z/analyze-observation`  
Source: `observation-window:20260914T030000Z-050000Z`  
Interval: `[2026-09-14T03:00:00Z, 2026-09-14T05:00:00Z)`

## Coverage and findings

The admission report declares complete readable coverage: 523 rows from `chat.log` (391),
`witness.log` (60), and `sensors.log` (72), with no duplicates. I independently counted those
timestamp-bounded source rows. The report is evidence-complete; sampled sensor fields still describe
their sample times only.

- **Local device-event counts crossed the learned floor twice.** `device-churn.log` records
  `CHURN delta=26` at 03:10:02Z and `delta=34` at 04:55:02Z, both above the floor of 24; both
  messages say `candidates=none`, which is not evidence of no device change. In the matching
  `udev-stream.log` intervals I found only the same PCI `hwmon` path: two rows before the first
  count (seqnums 10576–10577) and four before the second (10721–10722, 10741–10742). The signed
  rows identify the mesh probe; the unsigned rows do not. That stream has no named veth/net/queue
  row in these intervals. The remaining 24 and 30 counter increments are unmatched counts, not
  proof of lost broadcasts or hardware failure; `sgap` is an outstanding gauge, not a per-window
  loss count. Existing `device-churn-attribution-20260913` and `device-churn-live-join-20260913`
  tasks are complete. The present evidence does not name a device or process, so attribution remains
  an explicit blind spot.
- **The iMac path failed again and remains externally gated.** At 04:09Z both mesh-home and
  phaedra `path-watch` reported `imac-rozalia` crossing direct→relay. Watchdogs reported SSH
  unreachable at 04:15Z, unreachable again from phaedra at 04:21Z, and not on tailnet with no LAN
  fallback at 04:36Z. The exact health task `health-warning/8dc5571ba68f5efaacc4/triage` is already
  dependency-blocked with retry `event:roll-call-delta`; its receipt records no reachable iMac
  owner/path and no configured LAN fallback. I did not duplicate it or probe the unavailable peer.
  Relay use alone does not establish local UDP failure or a router cause. The previous
  `mesh-path-watch-hourly-relay-repeat-20260912` task is complete.
- **Witness samples show steady reflex reporting with intermittent unknowns.** All 60 rows report
  `reflex=OK` and `nodes=3/11`; `minds_live` is 15 in 50 rows and UNKNOWN in 10. The ask metric
  is explicitly unknown in 16 rows; among 44 known samples, `ask_p90_h` rises from 162.3h to
  164.3h while `ask_resolve` stays 0.746. The two witness-task-autonomy warnings in the interval
  have completed health triages (`health-warning/abf1c10121b164e63970` and
  `health-warning/60d9aee61f6de3396fdc`); no fresh recovery task is warranted here.
- **Historical room and resource samples are variable, not continuous-state evidence.** Of 24
  `room_sense` samples, 19 were UNCERTAIN, 3 PRESENT, and 2 OFFLINE. `cpu_load1` ranged 8.41–133.73
  (median 21.115); `mem_used_pct` ranged 18.0–45.0% (median 23.95%). These samples do not
  establish occupancy or sustained load between ticks.

## Current state observed separately from the historical window

The required `mesh-dash --once check` completed at 05:25:59Z and rendered a degraded fleet view:
2 SSH-reachable nodes, 8 down, 1 direct peer, 7 offline, with `PROBE-WARNING: LOCAL LOAD HIGH`.
The pane showed load1 117.37/16 cores, vitals load 131.41/16 and 70°C, and GPU VRAM at 11,596 of
12,288 MiB (94%) with 0% utilization. Its doctor section was cached at 04:32:13Z (53 minutes old,
FAIL=2/WARN=33), so those doctor findings are cached, not a fresh diagnosis. The one-shot also
reported 138 organ states (23 alarm, 28 stale, 87 quiet), with only three alarm rows shown; I do not
read the omitted rows as clear.

The refreshed live card and a read-only FIB check exposed a separate current routing fault:
`mesh-card --exit-node-lan` reports `100.76.0.1` swallowed in table 52. The live main table has
`100.76.0.0/16 dev enp42s0 src 100.76.27.91` and `default via 100.76.0.1 dev enp42s0`, while
table 52 has `default dev tailscale0` and `ip route get 100.76.0.1` selects `dev tailscale0 table
52`. `mesh-exit-node-lan-heal --check` exits 1 and explicitly refuses this prefix because
`100.76.0.0/16 is not RFC1918`; it also reports its Docker and rescue legs as no-op. The matching
2026-09-12 repair chain is rejected for a stale live-prefix mismatch; both its remaining genome
repair and health verification dispatch checks returned 2. The existing code gate at
`scripts/mesh-exit-node-lan-heal:1118` only admits `ipaddress.is_private` prefixes. I created the
fresh, evidence-bound chain `exit-node-lan-cgnat-live-repair-20260914` in
`task-receipts/exit-node-lan-cgnat-live-repair-20260914.tsv` for genome-owned guard work, coordinated
deployment, and independent health verification. No route, rule, DNS, VPN, or remote-node state was
changed during this analysis.

The standalone `mesh-reflex-health` read at 05:06 reported 36 fresh reflexes, plus explicit blind or
unavailable organs and stale value artifacts. It says the lan-newdevice and wifi-link reflexes are
running while their source reads are old, and kbd-activity/wifi-rf are absent on this node; those
are known source limitations rather than dead reflexes. The current high-load probe warning and
offline peers remain live health concerns, separate from the completed two-hour evidence window.

## Disposition

The observation report is complete, so this task can close with evidence rather than being retried.
The two device-event bursts remain unattributed within the existing source coverage; the recurring
iMac reachability issue stays blocked on `event:roll-call-delta`; and the witness warnings are already
settled. The current routing healer refusal has its own fresh linked follow-up above. No broad
network change is safe from this analysis frame; any future route application must use the new task's
live-prefix proof and the single-writer/dead-man protocol in `docs/coordination.md`.

## Verification

- Re-read the generated admission report and independently counted 391/60/72 bounded source rows.
- Re-read bounded sensor and witness rows and computed sample counts/ranges from their logged values.
- Compared both device-churn windows to timestamped udev rows; read the existing attribution and
  live-join receipts and task states.
- Read the current check pane, `mesh-card --exit-node-lan`, `ip route get`, table 52, and `ip rule`;
  ran only `mesh-exit-node-lan-heal --check` for the healer. No route write was attempted.
- Verified the old CGNAT repair child steps refused dispatch (exit 2), then created the new linked
  three-step task chain. This receipt is the artifact for the completed analysis task.
