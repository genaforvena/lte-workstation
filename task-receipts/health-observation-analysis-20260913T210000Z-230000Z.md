# Health observation analysis: 2026-09-13 21:00–23:00Z

Task: `20260913T210000Z-230000Z/analyze-observation`\
Source: `observation-window:20260913T210000Z-230000Z`\
Interval: `[2026-09-13T21:00:00Z, 2026-09-13T23:00:00Z)`

## Coverage and findings

The admission report declares complete coverage: 314 unique events, no exact duplicates, from
`chat.log` (182), `witness.log` (60), and `sensors.log` (72). I checked those bounded spans against
the retained device-churn and udev tapes, the in-window health receipts, and a fresh one-shot
`check` pane.

- **Global device churn recurred without a named endpoint in the retained udev stream.** All 24
  five-minute accumulator rows are present: 5 `CHURN`, 8 `TICK`, and 11 `QUIET`, totaling 201
  seqnum increments (maximum 35 in one interval). The 34 named udev rows are all `change` events
  for the same `hwmon2` DEVPATH; none names a veth, container, USB device, or other endpoint. The
  device-churn field `candidates=none` is an age-based USB inference, not proof that no device was
  removed. The global seqnum does not attribute increments to a source. The previously registered
  bounded veth/container observer remains appropriate only on a future named veth or container
  network burst; this window supplies no reason to duplicate it or infer ownership from timing.
- **Local samples show sharp but intermittent CPU load.** Across 24 five-minute readings,
  `cpu_load1` ranged 6.96–143.44 on 16 cores (median 15.99; 12/24 above 16, 6 above 32, and 4
  above 64). Memory use ranged 18.6–35.4% (median 26.75%). Room sensing was `OFFLINE` in 12
  samples, `UNCERTAIN` in 10, and `PRESENT` in 2. These point samples do not establish a continuous
  high-load episode or its cause.
- **Witness reflex stayed green, with gaps in other dimensions.** Reflex was `OK` in all 60 rows
  and node reachability stayed 4/11. Live-mind counts were known in 51 rows (15–16) and unknown in
  9. Ask-resolution ratio stayed 0.746 where reported; stale-ask p90 rose from 156.3h to 158.3h.
  The unknown rows are missing observations, not zeroes.
- **The in-window doctor smoke failure was fixed locally, but aggregate clearance remains
  unverified.** At 21:31Z the board reported 3 FAIL/33 WARN: egress via `tailscale0`, configured
  exit-node SPOF, and `mesh-selfcare` smoke failure. The focused triage receipt reproduces a fixture
  race and records five passing focused runs after its correction. At 22:13Z the health handoff
  says the aggregate `mesh-doctor` refresh was interrupted after recursive `mesh-doctor --help`
  spawning; the 21:31 aggregate therefore remained unresolved. The fresh pane at 23:17Z still
  shows the cached 3 FAIL/33 WARN result. Its egress and exit-node findings remain known substrate
  alarms; this analysis changed no routes or VPN state.
- **One autonomy-audit timeout recovered without identifying its cause.** The 22:27Z
  `audit-rc-124` warning has a completed triage receipt: subsequent scheduled checks passed and a
  fresh `mesh-task audit` took 2.76s. The original timeout's duration, partial output, and cause
  were not retained, so keep that observability gap explicit rather than changing the timeout.
- **Path and organ signals are time-bounded.** `path-watch` reported `imac-rozalia` falling back
  direct-to-relay at 21:04Z and 22:04Z. The current pane reports degraded path with one direct and
  one relay peer, but no cause is established here. An organ keepalive reported `uvc-metadata`
  dark at 21:09Z; the current pane later says all organs are live, so that alert is not a current
  outage claim.

## Current pane and disposition

At 23:17Z, `mesh-dash --once check` showed 3 SSH / 0 LAN / 7 down fleet nodes and degraded path;
egress was currently OK but the 24-hour aggregate remained BAD (0/412, with 60 unattributed).
The cached doctor result remained 3 FAIL/33 WARN. The pane also showed GPU VRAM at 93% with a
critical marker, 23 organ alarms and 29 stale states despite all organs being live, and supervised
loops at 4UP/0DOWN. These are current observed conditions, not inferred causes.

No new device-churn follow-up is warranted without a named veth/container-network event. Preserve
the existing retry condition: run `scripts/mesh-docker-veth-join --seconds 60` on the next such
named burst. The aggregate-doctor recursion and stale confirmation remain open operational work:
inspect the recursion before another aggregate refresh, then verify whether the focused
`mesh-selfcare` clearance reaches the aggregate result. No substrate or service state was changed.

## Verification and sources

- Read `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260913T210000Z-230000Z.md`:
  `evidence_complete=yes`, 314 source rows, zero deduplication.
- Processed the bounded source spans: `/home/mesh-home/.mesh/chat.log:61048-61229`,
  `/home/mesh-home/.mesh/witness.log:4930-4989`, and
  `/home/mesh-home/.mesh/sensors.log:55718-55789`.
- Summarized all 24 five-minute rows at `/home/mesh-home/.mesh/device-churn.log:5067-5090` and
  all 34 named rows at `/home/mesh-home/.mesh/udev-stream.log:5717-5750`.
- Read `docs/task-receipts/health-mesh-selfcare-smoke-triage-20260913.md` and
  `task-receipts/health-warning-triage-47efd3a73e356a062d8b-20260913.md` for the focused smoke
  correction and recovered audit timeout.
- Ran `mesh-dash --once check` at 23:17Z for the current pane. Its doctor section is cached, not a
  fresh aggregate verification.
