# Health observation analysis: 2026-09-14 01:00–03:00Z

The admission report at `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260914T010000Z-030000Z.md`
reports complete source coverage: 277 chat rows, 60 witness rows, and 72 sensor rows, with no
duplicates. Independent timestamp filtering of the three source tapes reproduced all 409 rows.

The health-relevant findings are:

- At 01:59Z, health reported a comprehensive doctor result of 3 FAIL / 33 WARN. The two known
  egress failures remained (egress on `tailscale0` and an exit-node SPOF); a new smoke-test
  failure was `mesh-series-stats`. This is a historical check result, not a current doctor run.
- The 02:11Z imac-rozalia alert was explicitly a chronic suppression roll-up for recurring SSH
  unreachability, not a new fault. Its separate triage later found the Tailscale peer offline
  with physical cause unknown; see
  [`health-warning-ed23d7b6fc8ee0959c6b-triage-20260914.md`](health-warning-ed23d7b6fc8ee0959c6b-triage-20260914.md).
- Witness reported `reflex=OK` on all 60 samples, but only 3/11 nodes in every sample; `minds_live`
  and `ask_open` were `UNKNOWN` in 9/60 samples, and `senses` covered only 4–7 of 21 sources.
  The green reflex signal therefore did not imply complete live fleet coverage.
- The 24 CPU samples had median load1 15.43 on a 16-core host, range 7.25–134.31; 12 exceeded
  16, four exceeded 32, and one exceeded 64. The 134.31 peak was at 01:53Z; further elevated
  samples were 39.24 at 01:28, 42.26 at 02:18, and 48.88 at 02:33. Memory remained 19.3–32.7%
  (median 22.7%). Room sensing was PRESENT 9, OFFLINE 10, UNCERTAIN 5. A minute-53 scheduled
  workload is a candidate for the peak, but this observation window has no process sample that
  attributes it; the later 03:53 capture proves that a grinder can consume heavy CPU, not that it
  caused the 01:53 peak.
- Chat contained 64 task-ledger records (23.1% of 277 rows) and 50 handoffs (18.1%), reflecting
  substantial coordination traffic during the interval.

Conclusion: the interval records persistent partial fleet visibility, recurring high CPU, and
one additional doctor smoke-test failure. No new substrate action is supported by these tapes;
the attribution of the largest load spike remains a known gap requiring contemporaneous process
sampling.

Verification: source counts, tags, witness fields, and sensor ranges were independently
recomputed from `/home/mesh-home/.mesh/chat.log`, `witness.log`, and `sensors.log` using the exact
half-open interval `[2026-09-14T01:00:00Z, 2026-09-14T03:00:00Z)`.
