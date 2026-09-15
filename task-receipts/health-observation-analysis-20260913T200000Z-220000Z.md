# Health observation analysis: 2026-09-13 20:00–22:00Z

Task: `20260913T200000Z-220000Z/analyze-observation`  
Source: `observation-window:20260913T200000Z-220000Z`  
Interval: `[2026-09-13T20:00:00Z, 2026-09-13T22:00:00Z)`

## Coverage and findings

The admission report is complete: 343 unique events, no exact duplicates, from `chat.log` (211),
`witness.log` (60), and `sensors.log` (72). I checked those bounded rows against device-churn,
udev, the existing Docker/veth observer receipt, warning triages, and the live health pane.

- **Kernel device churn continued, but the retained event names do not show a comparable veth
  burst.** The 24 five-minute accumulator intervals comprise 9 `CHURN`, 3 `TICK`, and 12 `QUIET`
  rows, totaling 183 seqnum increments (maximum 35 in one interval). All 36 udev-stream rows in
  the interval are `change` events for the same `hwmon2` DEVPATH; none names a veth, container,
  USB device, or other endpoint. The device-churn field `candidates=none` is a USB-age inference,
  not evidence that no device was removed, and the global seqnum does not attribute these increments
  to a particular source.
- **The prior read-only Docker/veth capture remains an honest empty read.** The completed
  `device-churn-live-join-20260913/capture-veth-container-join` receipt records Docker 29.1.3 with
  zero running containers and zero network events during its two-second capture at 20:38Z. Later
  accumulator increments occurred, but every udev-stream row through 21:51Z still names only
  `hwmon2`; this interval therefore supplied no comparable virtual-network event to join. No
  duplicate capture task is warranted. On the next named veth/container-network burst, run
  `scripts/mesh-docker-veth-join --seconds 60`; do not infer ownership from temporal proximity.
- **Five-minute local samples show intermittent high load, not a measured continuous episode.**
  `cpu_load1` ranged 9.68–143.44 on 16 cores (median 20.845; 16/24 samples above 16, 6 above 32,
  and 3 above 64). Memory use ranged 18.6–48.7% (median 27.9%). Room sensing was UNCERTAIN in 11
  samples, OFFLINE in 7, and PRESENT in 6. The load-audit board reported a 93% Python process at
  20:12, but the sampled peaks do not establish that process as the cause of churn or reachability.
- **Witness coverage remains partial alongside a stable reflex result.** Reflex was `OK` in all
  60 rows and the node count stayed 4/11. Eight rows had unknown live-mind counts; ten had unknown
  ask fields. Where known, resolve ratio stayed 0.746 and stale-ask p90 rose from 155.3h to 157.3h.
  These unknowns are missing observations, not zeroes; the old ask backlog remains visible.
- **Both in-window health-fail events have receipts, with one exact failure branch still blind.**
  The 20:00 witness-autonomy alert was triaged as a valid stalled-progress alarm and recovered after
  witness updates. The 20:27 journal alert recovered on the next scheduled run; its exact exit-1
  branch remains unknown because subprocess stderr was not retained. Both warning chains are marked
  complete in the authoritative chat/task ledger. At 20:32 the doctor board reported 2 FAIL/34 WARN
  (egress through `tailscale0` and configured exit-node risk); at 21:31 it reported 3 FAIL/33 WARN,
  adding the real `mesh-selfcare` smoke failure. Its focused receipt attributes that failure to a
  fixture timing race, records five subsequent passing smoke runs, and leaves aggregate doctor
  confirmation pending.

## Current pane and disposition

The one-shot `mesh-dash --once check` at 22:18Z still shows 3 SSH/0 LAN/7 down fleet nodes,
unreliable reachability probes, GPU VRAM at 88%, and the same 3 FAIL/33 WARN doctor result cached
from 21:31Z (about 46 minutes old). The pane still names egress on `tailscale0`, the configured
exit-node SPOF, and `mesh-selfcare` smoke-test failure. The selfcare focused tests passed after the
fixture correction, but there is no fresh aggregate doctor result in this observation; treat that
clearance as unverified until the next safe aggregate refresh. Routing/VPN state remains an explicit
known alarm, not something changed by this analysis.

No new device-churn task was created because the retained udev stream shows no veth/container event
after the completed observer capture. The precise retry condition is the next named veth or
container-network burst, when the bounded 60-second observer can see a live event. No substrate
configuration was changed.

## Verification and sources

- Confirmed the generated report interval, `evidence_complete=yes`, 343 source rows, and zero
  deduplication in `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260913T200000Z-220000Z.md`.
- Processed the bounded source spans: `/home/mesh-home/.mesh/chat.log:60917-61127`,
  `/home/mesh-home/.mesh/witness.log:4929-4988`, and
  `/home/mesh-home/.mesh/sensors.log:55682-55753`.
- Summarized all 24 device-churn intervals at `/home/mesh-home/.mesh/device-churn.log:5055-5078`
  and all 36 udev rows at `/home/mesh-home/.mesh/udev-stream.log:5699-5734`.
- Read `docs/task-receipts/device-churn-live-join-20260913.md`,
  `task-receipts/health-observation-analysis-20260913T190000Z-210000Z.md`, and
  `docs/task-receipts/health-mesh-selfcare-smoke-triage-20260913.md` to preserve prior findings,
  capture conditions, and smoke-test status.
- `git diff --check` passed. No code or substrate state was changed.
