# Health observation analysis: 2026-09-14 11:00–13:00Z

Task: `20260914T110000Z-130000Z/analyze-observation`
Source: `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260914T110000Z-130000Z.md`
Interval: `[2026-09-14T11:00:00Z, 2026-09-14T13:00:00Z)`

## Admission and prerequisite recovery

The report marks the interval complete: 723 rows, all unique, from `chat.log` (591),
`witness.log` (60), and `sensors.log` (72). An independent half-open timestamp recount matched
those source counts and found zero exact duplicate lines. No producer prerequisite blocked this
analysis. The separate Phaedra source/hash and event-sequence evidence described below was absent,
so I registered an exact read-only follow-up rather than infer attribution from the board summary.

## Findings

The 24 five-minute local sensor samples show recurring load excursions and an earlier memory rise.
These load averages do not name a process.

| Metric | Samples | Median | Range | Threshold counts |
|---|---:|---:|---:|---|
| `cpu_load1` | 24 | 20.48 | 10.31–139.03 | >16: 15; >32: 8; >64: 3 |
| `mem_used_pct` | 24 | 42.4% | 26.3–78.6% | >64%: 3 |

The three load samples above 64 were 107.54 at 11:28Z, 139.03 at 12:08Z, and 135.43 at 12:28Z.
Memory exceeded 64% at 11:18Z (74.1%), 11:23Z (78.6%), and 11:28Z (66.0%); it was lower in all
later samples. Room sensing was `PRESENT` in 21/24 samples and `UNCERTAIN` in 3/24, which is
intermittent evidence rather than continuous occupancy.

Witness telemetry had `nodes=4/11` and `reflex=OK` in all 60 rows. `minds_live` was 16 in 57 rows,
15 in two, and `UNKNOWN` once. Sense coverage ranged from 4/21 to 7/21 (median 5/21). The ask
fields were unknown in 15/60 rows; known rows reported `ask_open=8`. The green reflex reading does
not establish full sensor coverage, and unknown values remain unknown.

There were two actual standalone `[health-fail]` events. The 11:01:16Z task-autonomy warning named
the Genome-owned witness-pane checker; the exact health triage records owner progress by 11:04:59Z,
a fresh PASS at 11:05:59Z, and a completed checker task. The 12:16:03Z warning named Genome's
device-churn attribution task; its exact health receipt records completion at 12:22:52Z and a fresh
witness PASS at 13:02:58Z. Both warnings recovered through their exact owners' work; no duplicate
or reassigned health task was warranted.

Phaedra separately posted four device-churn summaries at 11:05:03Z, 11:35:03Z, 12:05:03Z, and
12:35:03Z. Each reported `delta=6` over 298–299 seconds, `candidates=none`, and repeated the
older “real enumeration” wording. The 12:35 report followed the mesh-home signed-probe change's
12:22:53Z completion. The existing signed-probe receipt verifies the local mesh-home source and a
12:20Z read-only check; it does not provide Phaedra's installed digest or exact sequence rows. The
Phaedra board summaries and their 30-minute roll-up cadence cannot identify the source events.
I found no active exact-owner ledger task for this Phaedra parity join. I registered
`health-observation-device-churn-phaedra-parity-20260914/verify-phaedra-attribution-parity`,
owned by Genome, to compare Phaedra's installed/source identity with its exact udev sequence
intervals and the signed-probe receipt. Until that read-only check lands, Phaedra event attribution
remains unknown.

At 12:17Z the check-stream reported the same two doctor FAIL categories (2 FAIL/33 WARN), with no
new warning category; LAN reachability remained unknown and egress/DNS were unchanged. The current
13:17Z pane still names the known egress-on-`tailscale0` and exit-node SPOF failures. Its VPN section
is observe-only/frozen. It also reports GPU critical at 71% VRAM with 0% utilization and 47°C; no
hardware or substrate actuator was run during this observation analysis.

## Decision

The observation request is complete. Keep historical high-load attribution unknown: five-minute
samples show three extreme excursions but no synchronized process evidence, so they justify neither
a causal claim nor a process-control change. Reassess only when a fresh load sample above 64 is
paired with the live load-audit process sample. Keep the two doctor FAILs as known, unchanged
substrate findings under the frozen VPN charter. Keep Phaedra's repeated six-event summaries as an
attribution blind spot until the exact host parity/sequence audit completes. No network, route, DNS,
firewall, VPN, hardware, or process-control state was changed.

## Verification

- Re-read the complete admission report and independently recounted the bounded source tapes:
  591/60/72 rows, 723 total, zero duplicate exact lines.
- Summarized all 24 load, memory, and room samples and all 60 witness samples; retained `UNKNOWN`
  values as unknown.
- Matched the two standalone health-fail lines against their exact completed health-warning ledger
  chains and receipts; checked the Genome device-churn source task status and receipt.
- `mesh-task check dispatch 20260914T110000Z-130000Z/analyze-observation health` exited 0; the
  exact owner claimed the step with `MESH_TASK_ACTOR=health`.
- Created the one-step Genome follow-up in
  `health-observation-device-churn-phaedra-parity-20260914`; replay/status show its row open,
  owner `genome`, and `dispatch=sent`. A redundant second dispatch was refused because the step
  was already dispatched; health did not take or mutate that other-owner row.
- Read `mesh-dash --once check` at 13:17Z. No system or substrate write was attempted.
