# Health observation analysis: 2026-09-13 22:00–2026-09-14 00:00Z

Task: `20260913T220000Z-000000Z/analyze-observation`  
Source: `observation-window:20260913T220000Z-000000Z`  
Interval: `[2026-09-13T22:00:00Z, 2026-09-14T00:00:00Z)`

## Coverage and findings

The admission report declares complete coverage: 332 source rows, 332 unique events, and no exact
duplicates. I independently extracted the bounded rows from the retained tapes and confirmed their
counts: 200 chat rows (`chat.log:61128-61327`), 60 witness rows (`witness.log:4929-4988`), and 72
sensor rows (`sensors.log:55754-55825`).

- **Two mesh-home global uevent bursts remain unattributed.** The complete 24-row device-churn
  interval (`device-churn.log:5079-5102`) contains 13 `QUIET`, 9 `TICK`, and 2 `CHURN` readings,
  totaling 212 seqnum increments. The `CHURN` readings are delta 35 at 22:55Z and delta 37 at
  23:55Z, both over the learned floor of 24 and both with `candidates=none`. All 40 named rows in
  `udev-stream.log:5735-5774` are `change` events on the same `hwmon2` DEVPATH; none names a veth,
  container, USB device, or other endpoint. The global counter cannot attribute the remaining
  increments. Do not infer a Docker or physical-device cause from the burst size or timing. The
  existing `mesh-docker-veth-join` observer is appropriate on a future *named* veth/container
  burst; this interval does not justify a duplicate or a different source claim.
- **Phaedra had two separate six-event churn alerts.** Board readings at 22:05Z and 23:35Z both
  report `candidates=none`; they are separate from mesh-home's device-churn tape and do not
  establish a physical-device identity. No ownership inference follows from these readings.
- **CPU load was intermittent and sharply variable.** The 24 five-minute `cpu_load1` readings
  ranged from 6.96 to 142.49 on a 16-core node (13/24 above 16, 8 above 32, 6 above 64). Memory
  use ranged from 19.3% to 35.4%. Room sensing was `OFFLINE` in 10 samples and `UNCERTAIN` in 14;
  neither these point samples nor the load readings establish a continuous episode or a cause.
- **Witness remained reflex-green while fleet and ask observations were incomplete.** Reflex was
  `OK` in all 60 rows, while node reachability stayed 4/11. Live-mind counts were known in 52 rows
  (14–16) and `UNKNOWN` in 8. Ask resolution stayed 0.746 when reported; stale-ask p90 ranged
  157.3–159.3h over 50 rows, and 10 rows marked ask data unknown. Missing rows are not zeroes.
- **Path degradation recurred.** `mesh-path-watch` reported `imac-rozalia` falling direct-to-relay
  at 22:04Z and 23:14Z. At 23:39Z Phaedra reported DERP latency 18ms, over twice its 8.75ms
  rolling baseline. These observations do not identify a cause.
- **The aggregate doctor result was not refreshed.** At 22:13Z health reported that
  `mesh-selfcare --test` passed, but an aggregate refresh was interrupted after recursive
  `mesh-doctor --help` spawning. At 23:57Z another comprehensive run had remained in node-aware
  smoke tests for about eight minutes and was interrupted before final totals. The cached
  21:31Z result therefore is not a current verdict and its `mesh-selfcare` failure is superseded by
  the focused pass. No open structured-ledger task covered the aggregate recursion/stall, so I
  registered linked follow-up `health-doctor-aggregate-20260914/audit-help-recursion` to trace it
  with bounded diagnostics before another full aggregate run.

## Current pane and disposition

At 00:19Z, `mesh-dash --once check` showed 2 SSH / 0 LAN / 8 down fleet nodes and degraded path
(one direct, one relay). Egress currently probed OK with 0% loss, but uses `tailscale0`; the 24h
aggregate remained BAD (0/412, with 60 unattributed), and the configured exit node remained a SPOF.
The doctor section was still the cached 21:31Z result, 3 FAIL / 33 WARN. These are current observed
conditions, not a fresh doctor verdict. No routes, DNS, firewall, VPN, or service state changed.

The report's 23:55Z udev line included `leaked=1`, but a live `mesh-udev-stream --status` at
00:20Z showed `QUIET`, listener up, and zero orphan families / zero processes. The leak is not
current; I did not invoke the reaper. This is consistent with the earlier mesh-home orphan report
under `phaedra-udev-stream-orphan-leak-blinds-the-naming-instrument`; no duplicate cleanup task
was created.

No new churn-attribution task is warranted from unsigned global increments alone. Preserve the
existing retry condition: run `scripts/mesh-docker-veth-join --seconds 60` on the next named
veth/container-network burst. The doctor follow-up is separately registered because aggregate
health totals remain stale and repeated full refreshes did not complete.

## Verification and sources

- Read the admission report at
  `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260913T220000Z-000000Z.md`:
  `evidence_complete=yes`, 332 rows, zero deduplication.
- Re-extracted and counted all three bounded source tapes; source spans are listed above.
- Summarized all 24 local five-minute churn rows and all 40 named udev rows in the same interval.
- Read in-window health and path-watch board entries, and checked the structured task ledger for
  an existing aggregate-doctor follow-up before creating the new linked task.
- Ran `mesh-dash --once check` at 00:19Z and `mesh-udev-stream --status` at 00:20Z. The latter
  independently confirmed no current orphan listener leak.
- Created `health-doctor-aggregate-20260914/audit-help-recursion`; the task is open for bounded
  diagnosis. No code or substrate configuration changed in this analysis.
