# Health observation analysis: 2026-09-14 17:00–19:00Z

Task: `20260914T170000Z-190000Z/analyze-observation`  
Source: `observation-window:20260914T170000Z-190000Z`  
Interval: `[2026-09-14T17:00:00Z, 2026-09-14T19:00:00Z)`

## Admission and recount

The admission report declares complete coverage: 538 events (406 `chat.log`, 60 `witness.log`,
72 `sensors.log`), with no deduplicated rows. The source tapes were independently recounted for
this interval; the counts match and exact normalized-line duplicates are zero in each source.

## Findings

- **Fleet reachability is incomplete, and current probe evidence is load-limited.** In the bounded
  window, the pane showed 3 SSH nodes and 7 down, while its own warning said high local load made
  reachability probes unreliable. The fresh 19:34Z pane still shows six offline peers, a live
  egress sample of `OK loss=0%`, and repeats the probe warning. Do not interpret peer non-answers
  as proof of failure while that warning is present. `mesh-health` had mesh-home, Phaedra and iMac
  reachable; other named peers remained offline. No route or tunnel state was changed.
- **iMac path alternation remains unexplained, with current direct-path access unverified.** The
  window's path-watch tape contains 12 imac-rozalia transitions from 17:09Z through 18:59Z,
  alternating direct and relay every ten minutes (six each); UDP was true at 17:54Z and 18:54Z.
  The existing path-flap receipt found no demonstrated cause. A 19:27Z tailscale ping succeeded
  three times via DERP Helsinki, while `tailscale netcheck` reported UDP=true and no direct
  connection. Both ordinary SSH and `tailscale ssh` failed strict host-key verification, so no
  authenticated remote state was established. Do not alter `known_hosts`; retain the existing
  retry triggers in `mesh-path-flap-investigation-20260914.md`.
- **Room sensing is mostly unknown, not a continuous occupancy record.** Across 24 five-minute
  sensor triples, room status was `UNCERTAIN` 15 times, `OFFLINE` 7 times and `PRESENT` twice.
  These samples do not establish a continuous room state or explain the offline samples.
- **Resource readings show intermittent CPU spikes and bounded job OOMs, without evidence of
  global memory pressure.** Across 24 sensor rows, CPU load has median 17.51 and range 11.27–152.95;
  only two samples exceed 64. Memory use ranges 22.1–38.9% (median 27.5%). Two Python OOM events
  occurred at 17:37:14Z and 17:38:00Z at about 2.55 GB RSS each. `journalctl -k` attributes both
  to separate `mesh-heavy` memory-cgroup OOMs, not host/global OOM; memory PSI avg10/avg60 were 0
  and avg300 was 0.19. The 24-hour kill log also includes the expected capped `mesh-caphog` and
  `mesh-capcheck` OOM victims and two `pstree` segfault records. The Python job identities remain
  unattributed, so this is a per-job limit signal rather than proof of host-wide pressure.
- **Uevent source attribution is still incomplete.** Earlier in the interval, the 17:20Z and
  17:30Z rows were `CHURN delta=24`; each retained six events (three signed probes and three
  unsigned) while 18 sequence values were missing. Later TICK rows remained partially attributed.
  The existing Senses receipt defines a read-only Docker/udev join on the next CHURN or positive
  missing-count trigger. A new 19:30Z TICK after the interval had `delta=24`, `missing=18`, and
  `possible-nonprobe=21`. The prescribed capture started at 19:36Z, after that TICK's preceding
  19:25–19:30 interval, so it is a follow-up observation rather than event-aligned evidence.
  Missing sequence values remain unknown; the `hwmon` paths and synthetic probe marks do not
  identify the missing events.
- **Health-warning rows are stale task notices, not fresh independent failures.** Four in-window
  `[health-fail]` notices were checked against the canonical task ledger and triaged in separate
  receipts. The two Phaedra `[strand]` notices point to the same parked stash and steward gate
  already recorded in the witness autoland receipt. No duplicate task or substrate mutation was
  warranted.

## Disposition

No routing, DNS, firewall, VPN, device, container, service or privilege state was changed. Named
uncertainties remain: probe-limited fleet reachability; no authenticated iMac read; mostly unknown
room sensing; two memory-cgroup-limited Python jobs without task attribution; and partially
observed uevent sequence ranges. Follow the prior path-flap retry criteria and capture the exact
next uevent burst; do not infer external enumeration or host-wide memory failure from these rows.

## Verification

- Read the bounded observation report and independently recounted all 538 source rows; duplicate
  count was zero for each source.
- Correlated the window with witness, sensor, path-watch, device-churn, udev-stream, kill-event,
  kernel OOM, prior path-flap and device-churn receipts.
- Refreshed `mesh-dash --once check` at 19:34Z. The pane showed egress OK, six offline peers and
  its high-load reachability warning.
- `mesh-hw-health` reported SMART PASSED, wear 2%, critical warning 0x00, spare 100% (threshold
  1%), zero media errors, maximum thermal 74°C, and `HW: OK`.
- Both SSH methods to imac-rozalia failed host-key verification; no remote authenticated read was
  claimed.
- `scripts/mesh-docker-veth-join --seconds 300 --max-events 1000` completed read-only from
  19:36:08Z to 19:41:08Z. Artifact
  `/home/mesh-home/.mesh/observations/mesh-docker-veth-join-1789414568.jsonl` records zero Docker
  events, zero errors, and an unchanged uevent sequence baseline/final of 12048. Its
  `docker_events_exit=143` is the bounded helper's SIGTERM after the requested interval; this
  later quiet window cannot explain the earlier 19:30Z missing sequence values.
- `scripts/mesh-udev-stream --tail 1000` retained the recent `hwmon` probe rows through 19:29Z;
  those rows do not bridge the 18 missing sequences from the 19:30Z TICK. Subsequent device-churn
  samples at 19:35Z and 19:40Z were QUIET with zero delta and complete interval coverage. Capture
  the next live CHURN or positive-missing TICK with the Senses receipt's exact commands.
