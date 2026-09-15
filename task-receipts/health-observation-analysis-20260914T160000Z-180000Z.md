# Health observation analysis: 2026-09-14 16:00–18:00Z

Task: `20260914T160000Z-180000Z/analyze-observation`  
Source: `observation-window:20260914T160000Z-180000Z`  
Interval: `[2026-09-14T16:00:00Z, 2026-09-14T18:00:00Z)`

## Admission and recount

The admission report declares complete coverage: 450 rows (318 `chat.log`, 60 `witness.log`,
72 `sensors.log`) and no deduplicated events. I independently recounted the timestamp-bounded
rows and applied the observer's normalized-line hash per source; all three counts match and each
source has zero exact duplicates. The prior `15:00–17:00Z` analysis receipt covers the overlap;
the findings below focus on the new `17:00–18:00Z` hour while retaining relevant events from the
full bounded report.

## Findings

- **Mesh-home uevent attribution remains partial, not evidence of external enumeration.** The
  17:20:03Z and 17:30:03Z device-churn rows each report `CHURN delta=24`, with 18 sequence values
  missing from the namespace-scoped udev listener in each interval. The retained rows name six
  events (three signed probes and three unsigned) per interval; the other 18 remain unknown. The
  mesh-home cross-namespace join task is complete and its receipt documents the same observer
  boundary plus a next-live-CHURN capture trigger. The subsequent 17:35–17:55 mesh-home passes
  were QUIET; 18:00 was a TICK with a complete two-event attribution. No later CHURN occurred in
  this report, so the post-receipt trigger has not fired. No duplicate join task is warranted.
- **Phaedra reported one more small global-counter burst.** Its 17:35:02Z `delta=6` is consistent
  with the four earlier 2026-09-14 reports whose parity receipt classified every sequence value
  as missing/unknown. That exact parity task is complete; it found Phaedra's installed tool older
  than Genome's landed source and says to retry when source and install match and retained rows
  cover the interval. The new row supplies no event identities, so it remains unattributed; no
  device event or external enumeration is inferred, and ownership is not reassigned.
- **Room sensing ended in an explicit short offline run.** During the new hour, 12 five-minute
  samples were `PRESENT` twice, `UNCERTAIN` seven times, and `OFFLINE` three times (17:48–17:58Z).
  These samples do not establish continuous room state. The report provides no camera-level
  recovery evidence, so room presence remains unknown after the last sample; no camera or service
  action was taken.
- **Sparse resource samples show earlier spikes, while the live pane is a separate reading.**
  Across 24 five-minute rows, `cpu_load1` ranges 8.74–146.64 (median 14.955) and memory use
  22.4–48% (median 29.6%). The 17:00–18:00 subset is lower (CPU 11.87–49.35, median 15.225;
  memory 22.4–38.9%, median 29.45%), so the historical spikes do not establish sustained
  saturation. Separately, `mesh-dash --once check` at 18:18Z reports load 27.59/16 and warns
  that reachability probes are unreliable under high local load; its current top process is
  `python3` at 72% CPU. The same pane reports GPU VRAM 64%, 0% utilization, 50C, and no throttle.
  Non-answers from peers are therefore not treated as proof they are down. No process was
  interrupted.
- **Witness coverage is stable only within its sampled subset.** All 60 rows say `reflex=OK` and
  `nodes=4/11`; `minds_live` is UNKNOWN in 3 rows and the ask metric family is UNKNOWN in 13.
  Where present, `ask_resolve` remains 0.741. This does not make the seven unobserved nodes or
  missing ask windows green. The two in-window task-autonomy stall alerts (16:20 and 17:00) were
  already triaged against the exact Genome-owned routing-shadow work; both health triages closed
  after that work made progress, so neither merits a duplicate task.
- **Bluetooth remains an observed blind spot after its retry window advanced.** The 18:21Z
  read-only `mesh-ble-heal --status` reports `DAEMON-SICK`, 1101 wedges, and `last_heal=17:21:01Z`;
  `mesh-ble-heal --test` exits 1 because `bluetoothctl show` has no parseable Powered flag. The
  90-minute cooldown now runs until 18:51:01Z. The dashboard's cached doctor result is older and
  does not override this direct failed read. No radio power-cycle or service restart was
  attempted; retry status and the real-read test after 18:51:01Z.

## Disposition

The complete report is valid and still live; the canonical task ledger showed this exact-owner
step active after my take. Reused the completed cross-namespace and Phaedra parity receipts rather
than filing duplicate attribution work. The remaining uncertainty is named with concrete retry
conditions: another mesh-home `CHURN` with positive `missing` for event-aligned capture, Phaedra
source/install parity plus retained seqnums for attribution, and the BLE cooldown boundary at
18:51:01Z. Room sensing and sampled fleet coverage remain unknown at their stated sample bounds.
No routing, DNS, firewall, VPN, container, device, or service state was changed.

## Verification

- Read `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260914T160000Z-180000Z.md`;
  independently recounted 318/60/72 source rows and zero exact duplicates per tape.
- Compared the overlapping hour with
  `task-receipts/health-observation-analysis-20260914T150000Z-170000Z.md`, then inspected the
  current device-churn log, both exact completed attribution receipts, and their ledger statuses.
- Aggregated all 60 witness rows and 24 samples each for CPU, memory, and room-sense.
- `mesh-dash --once check` completed at 18:18Z; `mesh-health` ran read-only at 18:20Z;
  `mesh-ble-heal --status` and the live-hardware `--test` ran at 18:21Z (test exit 1, as stated).
- No actuator or substrate write was attempted.
