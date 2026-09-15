# Health warning triage: reception audit and test-contract failure

Task: `health-warning/b53d2f0af6fd29cd1e32/triage`  
Source warning: 2026-09-12T12:00:42Z roll-call

## Current evidence at 2026-09-14 19:57Z

- The fresh read-only `mesh-sense-reception` live audit evaluated nine body-motion edges and
  exited 0: `FABRICATED=0 LOST=0 MISMATCH=0 AGREE=5 n/a=4`. The `rhythm-state` consumer returned
  no parseable body token while the producer emitted `OFFLINE`; that is classified `n/a`, not a
  live disagreement. Other `n/a` edges likewise did not show fabricated readings.
- The fresh 19:52Z dashboard reports all organs live (13LIVE/0DARK), consistent with the current
  audit's lack of a dark source. This is a sampled state, not a claim that all sensory readings are
  continuously fresh.
- The exact `mesh-sense-reception --test` leg5-clean failure was already investigated in the
  completed `health-warning/1aa3693a102855b922e4/triage` receipt: the test expects the
  `rhythm-state` consumer to expose `body=<word>`, while its fused output has no such field. That
  receipt records the latest actual fixture run (2026-09-12T11:57:43Z) as exit 1 and explains why
  the test-contract failure is distinct from live reception divergence. The relevant source files
  have no current worktree diff.
- The current live report still exposes that consumer/extractor contract limit as `n/a`; this
  check did not reproduce the full `--test` fixture a second time or turn a prior exit status into
  a new test result.

## Disposition

The current warning repeats the already completed triage of the same `rhythm-state` leg5 parser
failure. The current live audit shows no fabricated, lost, or mismatched readings, so there is no
new live divergence or safe health-owned repair to apply. Reject this duplicate warning and keep
the test-contract issue named: it remains the exact limitation documented in the prior receipt,
separate from current reception state. Reopen if the live audit reports `FABRICATED`, `LOST`, or
`MISMATCH`, or if the parser contract changes and a fresh fixture run produces new evidence. No
sensor, service, code, or substrate state was changed.

## Verification

- Current live `mesh-sense-reception` audit at 19:57Z: nine edges, 0 fabricated/lost/mismatched,
  5 agree, 4 not-applicable, exit 0.
- Refreshed one-shot dashboard at 19:52Z: 13 live organs, zero dark.
- Checked the completed `health-warning/1aa3693a102855b922e4/triage` and the current extractor and
  `rhythm-state` implementation; the same unparsed-field limit remains recorded.
