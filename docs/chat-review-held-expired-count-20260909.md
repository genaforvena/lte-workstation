# Chat-review receipt: HELD_EXPIRED witness visibility

Task: `chat-review-held-expired-count-20260909/held-expired-count`

The requested behavior is landed in commit `9f055053`: `scripts/mesh-dash`
counts `HELD_EXPIRED` as unfinished and includes it in the first 20 witness
rows, preserving its `retry=` reason. The focused fixture in
`tests/test-mesh-witness-task-queue-fit.sh` covers the count, row visibility,
retry text, and exclusion of terminal rows.

Verification on 2026-09-09:

- `bash tests/test-mesh-witness-task-queue-fit.sh` — PASS.
- `mesh-task audit` — live audit emits `HELD_EXPIRED` rows with
  `retry=next fresh health warning`.
- `mesh-dash --once witness` — `373 total · 136 unfinished · 31 rejected ·
  206 done`; the claimed row is rendered as `RUNNING`.
- Direct `/home/mesh-home/.mesh/tasks.journal` count — `373 total`, `136
  unfinished`, `31 rejected`, `206 done`; 14 `HELD_EXPIRED` rows.
- Source/deployed `mesh-dash` SHA-256 parity —
  `bd87e6ec9c10b75342145264938071ddf5e70bf0e2316a1b7ff2c9d7e3bf4ef6`.

No source edit was needed in this receipt turn; the already-landed artifact
and regression satisfy the exact task.
