# Health observation analysis: 2026-09-14 02:00–04:00Z

Admission evidence at `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260914T020000Z-040000Z.md`
reports complete coverage and no duplicates. Exact timestamp filtering independently reproduced
352 chat rows, 60 witness rows, and 72 sensor rows (484 total) for the half-open interval.

Findings:

- The 02:21Z watchdog alert repeated the chronic `imac-rozalia` SSH-unreachable condition. At
  03:23Z the scheduled doctor run completed in 9m08s with 2 FAIL / 34 WARN. Bounded process
  sampling found a large parallel smoke-test/census fanout (peak 1,171 processes), but missing
  phase markers prevent attributing a single cause. See
  [`health-doctor-next-slot-20260914-observation.md`](health-doctor-next-slot-20260914-observation.md)
  and the imac triage
  [`health-warning-ed23d7b6fc8ee0959c6b-triage-20260914.md`](health-warning-ed23d7b6fc8ee0959c6b-triage-20260914.md).
- Genome delivery `f4df48579a778ce0` expired at 03:06Z without any attempt. Its original body
  cannot be recovered from the recorded failure, so the loss is a known delivery blindness;
  see [`health-warning-03a8502f9936366e185f-triage-20260914.md`](health-warning-03a8502f9936366e185f-triage-20260914.md).
- Witness reported `reflex=OK` in all 60 samples and `nodes=3/11` in all samples. However,
  `minds_live` was UNKNOWN in 9/60 and `ask_open` in 8/60; `senses` covered only 4–7 of 21
  sources. Reflex status again does not establish full live coverage.
- CPU load1 samples ranged 8.41–65.76 on the 16-core host, with median 18.87; 13/24 exceeded
  16, four exceeded 32, and one exceeded 64. The peak was 65.76 at 03:08Z; other elevated
  samples were 42.26 at 02:18, 48.88 at 02:33, and 48.04 at 03:28. Memory was 18.0–32.7%
  (median 21.75%). Room sensing was UNCERTAIN 17, OFFLINE 5, PRESENT 2. The separate 03:53
  process capture proves a scheduled grinder can briefly consume high CPU, but it does not
  explain these window's earlier peaks.
- Chat contained 100 task-ledger rows (28.4% of 352) and 47 handoffs (13.4%), a high coordination
  share. The 03:52Z task-autonomy alert listed dispatch-check exit-2 results for tasks later
  confirmed complete; see
  [`health-warning-60d9aee61f6de3396fdc-triage-20260914.md`](health-warning-60d9aee61f6de3396fdc-triage-20260914.md).

Conclusion: the interval shows continued partial fleet visibility, a completed doctor run with
substantial parallel test activity, intermittent high CPU, and an expired genome delivery whose
body is unavailable. Historical CPU peaks remain unattributed; no substrate change is justified
by these observations.

Verification: source counts, first-tag distribution, witness fields, CPU/memory statistics, and
room-sense counts were recomputed from `~/.mesh/chat.log`, `witness.log`, and `sensors.log` for
`[2026-09-14T02:00:00Z, 2026-09-14T04:00:00Z)`.
