# Sound claims-gate backlog triage — 2026-09-16

## Disposition

The backlog is safely queued, not proven stalled. The live pane at 2026-09-16T10:21:51Z
reported 851 pending records, a fresh archivist, and grinder/scanner held intentionally by
`mesh-load-gate` at load1=26.80. The next live command at 10:24:28Z reported 854 pending
markers and an `records.log` source of 2436 rows. This is movement in the corpus, not evidence
that grinding completed; the hold is the exact retry edge: recheck after a load-gate-eligible
evaluated grinder/scanner window.

## Independently inspected evidence

- `mesh-dash --once sound` (10:21:51Z): grinder `held`, last real run 15h41m ago; scanner
  `held`; render `idle`; inbox none; 851 pending records; archivist `fresh`; source organs
  present. Renders were source-starved (`ext` 7/7 of the last 7), so no render was started.
- `mesh-series-stats --claims` (10:24:28Z): exit `2`; source `/home/mesh-home/.mesh/records.log`,
  2436 rows, mtime `2026-09-16T10:24:28Z`, ROM `series-stats.rom`.
- Live claim verdicts: claim 2 `UNKNOWN`; all claim-3 axes `UNKNOWN` because n=2358 exceeds
  the ROM domain 2343; claim 1 `INDISTINGUISHABLE`; claim 4 remains an audit diagnostic with
  24 disagreements / 1260 measurable and 761 unknown degenerate rows. The gate is therefore
  failed with exit 2, not passed or silently downgraded.
- `mesh-task status witness-chat-range-review-near-62757-62819-sound-corrective`: 1/1 active,
  exact owner sound, lease through `2026-09-16T10:52:35Z`.
- Existing prior receipt `docs/task-receipts/sound-claims-gate-rederive-20260915.md` was
  inspected. It is complete historical evidence and does not supersede this fresh corpus.

## Decision and next edge

Do not retune the ranker, estimator, or gate from this observation. Keep the parent task typed
blocked until the follow-up task runs after a load-gate-eligible evaluated window. At that point,
rerun both commands above; a fresh gate result and pending-count delta decide whether the queue
advanced. The claims remain UNKNOWN/INDISTINGUISHABLE unless the live corpus fits the ROM or the
measurement contract changes through separately authorized work.

Delegation: `sound-claims-audit` was launched for a read-only independent audit, but its worker
turn returned `Login expired · Please run /login`; it was stopped and contributed no evidence.
All evidence above was personally inspected from the live commands and files.
