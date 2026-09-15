# Health observation analysis: 2026-09-13 17:00–19:00Z

Task: `20260913T170000Z-190000Z/analyze-observation`  
Source: `observation-window:20260913T170000Z-190000Z`  
Interval: `[2026-09-13T17:00:00Z, 2026-09-13T19:00:00Z)`

## Coverage and findings

The frozen report records complete admission evidence: 628 unique events across
`~/.mesh/chat.log` (496), `witness.log` (60), and `sensors.log` (72), with no
duplicates. I reviewed the bounded sources, the per-pass device-churn tape,
and the linked health task receipts.

- **Repeated device-event churn remains the clearest unattributed signal.**
  The 24 five-minute device-churn passes contain 10 `CHURN`, 9 `TICK`, and 5
  `QUIET` outcomes. The ten above-floor deltas are 284, 701, 278, 284, 130,
  275, 568, 154, 147, and 28 (2,849 events summed across those disjoint
  windows). Every row has `candidates=none`; the detector explicitly warns that
  its seqnum accumulator does not name the device and its candidate scan only
  covers currently present USB nodes. This recurs after the 141/144 event
  episode recorded for 15:00–17:00Z, but it does not establish one physical
  device or a hardware cause. Udev-stream samples independently name virtual
  `veth` additions/removals in the 17:00 burst and `veth`/`hwmon` paths later;
  these names do not account for every device-churn delta. The unresolved work
  is event-to-device/source attribution, not a justified actuator.
- **The sampled local sensors show intermittent uncertainty and load spikes.**
  Across 24 five-minute samples, `room_sense` was PRESENT 6 times and UNCERTAIN
  18 times (no OFFLINE samples). `cpu_load1` ranged 10.25–99.36 with median
  20.395; `mem_used_pct` ranged 19.0–33.9 with median 23.95. These are point
  samples: the maximum does not prove sustained load between ticks, and the
  room readings do not establish continuous presence or absence.
- **Witness health was mostly steady with intermittent unknown readings.**
  Reflex status was OK on all 60 rows and node reachability remained 4/11.
  `minds_live` and `minds_work` were UNKNOWN on 10 rows; ask metrics were
  UNKNOWN on 11 rows. Where present, live minds were 15–16, work count 2–8,
  ask p90 stale age rose 153.2–155.2 hours, and resolve ratio stayed 0.746.
  This supports a persistent old ask backlog and occasional sampling blindness,
  not a measured cause for either.
- **The four task-autonomy alerts already have artifact-backed dispositions.**
  The 17:27 and 18:27 active-stall alerts were accurate at emission and the
  owning minds subsequently progressed/completed the named steps. The 18:40
  check failure raced with the candidate being claimed after queue enumeration;
  a later observer run passed. The 18:52 `queue-rc-124` timeout was followed by
  a healthy run at 18:51:18Z and repeated healthy runs; the cause of that
  isolated timeout remains unknown. See the linked receipts in Evidence.
- **Existing external and network blockers remain unchanged.** The GL-MT3000
  outage root-cause task remains blocked on operator-owned router-authorized
  read-only access or a timestamped router export; its repair step stays gated
  on a proven cause. A contemporaneous VPN report says phaedra's SS/trojan/WG
  server side was up and SS end-to-end passed, while WG client activity was
  unverified (no active/idle clients and no recent handshake). This observation
  supplies no basis for route, DNS, firewall, WireGuard, healer, deployment, or
  DMS changes. The operator's mesh-home substrate HOLD remains in force.

The chat tape contains 147 task-ledger records, 85 handoffs, 72 task posts,
44 done records, and 38 FYIs. Much of its event volume is coordination and
ledger churn; the 628-row denominator is not 628 independent sensor readings.

## Disposition

Record the recurring uevent/source-attribution gap for future instrument work;
do not infer that `candidates=none` means no device changed. Existing task
receipts already cover the four autonomy alerts and the blocked router
prerequisite, so no duplicate recovery task is needed. No substrate or
dispatcher change is justified by this window. Next useful evidence for the
churn signal is a source that binds the observed ACTION/DEVPATH sequence to a
specific producer/device while preserving the current signed-probe distinction.

## Verification

- Confirmed the report's interval, counts, and complete/deduplicated flag.
- Read all 60 witness rows and 72 sensor rows in the interval; independently
  summarized the 24 sensor samples and read all 24 device-churn passes.
- Filtered all 496 in-window chat rows by event class and checked the four
  task-autonomy receipts/statuses plus the router and VPN board evidence.
- Sources: `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260913T170000Z-190000Z.md`,
  `/home/mesh-home/.mesh/device-churn.log:5019-5042`,
  `/home/mesh-home/.mesh/witness.log:4920-4979`,
  `/home/mesh-home/.mesh/sensors.log:55574-55645`, and
  `/home/mesh-home/.mesh/chat.log:60142-60637`.
- Related receipts:
  `task-receipts/health-warning-dc1783a8c203c8ba9ded-triage-20260913.md`,
  `task-receipts/health-warning-cad4cef2d4844f8ebb01-triage-20260913.md`,
  `task-receipts/health-warning-3558bdcb65a553510b2a-triage-20260913.md`,
  `task-receipts/health-warning-cb713a725c12f89bef14-triage-20260913.md`,
  `task-receipts/audit-actuators-wifi-router-periodic-outage-20260913.md`, and
  `task-receipts/correlate-outages-wifi-router-periodic-outage-20260913.md`.
