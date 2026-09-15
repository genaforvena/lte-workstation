# Health observation analysis: 2026-09-13 19:00–21:00Z

Task: `20260913T190000Z-210000Z/analyze-observation`
Source: `observation-window:20260913T190000Z-210000Z`
Interval: `[2026-09-13T19:00:00Z, 2026-09-13T21:00:00Z)`

## Coverage and findings

The admission report is complete: 540 unique rows, no exact duplicates, from
`chat.log` (408), `witness.log` (60), and `sensors.log` (72). The report itself
contains coverage counts rather than event details, so I summarized all three
bounded source sets and cross-checked the device-churn, udev, and relevant
health/mail tapes.

- **A short virtual-network event burst dominates the device-churn window.**
  The 24 five-minute accumulator rows contain 13 nonzero `CHURN` deltas and 11
  zero `QUIET` intervals, totaling 1,536 sequence increments. Four consecutive
  intervals from 19:30 through 19:50 account for 1,423 of them: 284, 574, 426,
  and 139. `candidates=none` does not identify or rule out a removed device.
  In the corresponding udev tape, 700 of 728 rows name virtual `veth` paths
  (40 `net`, 660 `queues`); the other 28 are `hwmon`. At 19:40 the stream
  reported 210 kernel events, all unattributed, against a seqnum delta of 426.
  The named `veth`/queue paths establish virtual-network lifecycle activity,
  but the rows have no endpoint or container identity (`name=-`), and their
  count does not reconcile one-to-one with the accumulator delta.
- **The endpoint join remains unobserved.** The completed read-only observer
  receipt records a real two-second Docker read at 20:38 with zero running
  containers and zero network events (uevent sequence 9931→9934). It therefore
  does not bind the 19:30–19:50 burst to a container. Later churn deltas after
  that capture were 14, 15, and 26; no comparable burst followed the capture.
  The existing receipt already names the next useful action: run
  `scripts/mesh-docker-veth-join --seconds 60` during a future live container
  network burst. I opened no duplicate task and made no substrate change.
- **Five-minute load samples show repeated peaks, not a continuous state.**
  `cpu_load1` was above the 16-core count in 19/24 samples, above 32 in 7/24,
  and above 64 in 3/24; the median was 27.335 and maximum 95.84 at 20:53.
  Memory use ranged 18.6–48.7% (median 26.7%). `room_sense` was UNCERTAIN in
  17/24 samples, PRESENT in 6, and OFFLINE in 1. These point samples support
  intermittent high load and uncertain room sensing; they do not prove duration
  or a cause for the uevents or reachability readings.
- **Witness readings retained their known backlog/coverage pattern.** Reflex
  status was OK in all 60 rows. Reachability was 4/11 in 50 rows, 3/11 in 5,
  and 2/11 in 5. Ask fields were unknown in 10 rows; where present, resolve
  ratio remained 0.746 while stale-ask p90 rose from 154.3h to 156.3h across
  the window. This is an old backlog with intermittent unknown samples, not a
  demonstrated cause for another fault.
- **Chat volume is mostly coordination, with a recovered mail-read episode.**
  The 408 rows include 116 task-ledger events, 57 done records, 56 FYIs, 55
  handoffs, and 50 task posts; these are not independent sensor readings. Four
  direct witness-to-Genome delivery failures reported 900-second age expiry;
  their health triages are recorded in the existing delivery receipts. Three
  direct `witness-task-autonomy` alerts were workflow checks, not substrate
  findings. The doctor board went from 3 FAIL/33 WARN at 19:34 (two recent
  `job-mail-lanes.dryrun.log` errors) to 2 FAIL/34 WARN at 20:32, with only the
  two egress FAILs named. The dry-run tape shows Gmail reads failing with a
  truncated traceback from 19:19–19:26 and a successful live read with two new
  messages at 20:53. Recovery is observed; the exact exception cause is not
  retained, so no cause or code change is inferred.

## Disposition

The bounded signal is continued, partly named veth lifecycle churn plus
intermittent high load. The tapes do not establish which container or process
created the veths, explain the remaining seqnum difference, or show that load
caused the probe or device events. Retain that negative causal result. The
completed `device-churn-live-join-20260913` receipt already specifies the
next comparable-burst capture; because no comparable burst followed its empty
live read, no duplicate follow-up task is warranted. No routing, DNS, firewall,
VPN, container, USB, or service configuration was changed.

## Verification and sources

- Confirmed the generated report interval, complete flag, source counts, and
  zero deduplication: `~/.mesh/autopoiesis-observation/analysis/20260913T190000Z-210000Z.md`.
- Processed the full bounded ranges: `~/.mesh/chat.log:60638-61047`,
  `~/.mesh/witness.log:4927-4986`, and `~/.mesh/sensors.log:55646-55717`.
- Summarized all 24 device-churn intervals in `~/.mesh/device-churn.log:5043-5066`
  and the 728 timestamped udev rows in `~/.mesh/udev-stream.log:4989-5716`;
  the named 19:35 veth rows include `udev-stream.log:5417-5446`.
- Checked the mail dry-run entries at `~/.mesh/job-mail-lanes.dryrun.log:1324-1345`
  and doctor board transitions in `~/.mesh/chat.log:60803,61012`.
- Read `task-receipts/health-observation-analysis-20260913T170000Z-190000Z.md`
  and `task-receipts/device-churn-live-join-20260913.md` to avoid duplicating
  the existing attribution work and its next-burst condition.
