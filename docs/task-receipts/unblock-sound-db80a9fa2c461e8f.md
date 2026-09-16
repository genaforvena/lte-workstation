# Unblock evidence: sound/db80a9fa2c461e8f

Checked at 2026-09-16T11:03:35Z after taking
`unblock/sound/db80a9fa2c461e8f/resolve` as owner `sound`.

## Eligibility and evidence

- `mesh-dash --once sound` at 2026-09-16T11:02:53Z reported grinder and scanner
  `held` by `mesh-load-gate` at load1=50.58; no evaluated grinder/scanner run
  occurred in this observation. The records corpus was 1,155 files with 851
  pending.
- `mesh-load-gate --quiet-hours` returned exit 1, so the required eligible
  window is not available now.
- `mesh-series-stats --claims` at 2026-09-16T11:03Z returned exit 2. The live
  corpus has 2,435 rows (mtime 2026-09-16T11:02:07Z); claim 2 and all claim-3
  axes are `UNKNOWN` because n=2,356 exceeds the ROM domain 2,343, while claim
  1 is `INDISTINGUISHABLE`. This is fresh calibration evidence, not a passing
  gate.
- The existing triage receipt and its findings sidecar pass inspection:
  `docs/task-receipts/sound-claims-gate-backlog-20260916.md` and
  `docs/task-receipts/sound-claims-gate-backlog-20260916.md.findings.json`;
  the sidecar is version 1 with nonempty findings. The required follow-up
  receipt and sidecar do not yet exist.

## Decision

The blocker is valid and remains a typed dependency. No safe in-scope fix can
manufacture the required load-gate-eligible evaluated window, and no ranker,
estimator, or gate retuning is authorized by this task. The exact retry edge is:

`retry when sound-claims-gate-backlog-followup-20260916/verify-after-load-window`
has run during a load-gate-eligible evaluated grinder/scanner window and both
`docs/task-receipts/sound-claims-gate-backlog-followup-20260916.md` and its
`.findings.json` sidecar exist and pass inspection.

The parent corrective task must remain blocked until that event. The follow-up
task remains open and eligible for its owner when the gate permits evaluation.
