# Acceptance receipt: witness-live-unattended-followup-20260908/repair-hh-parser-selector-correction

Recorded 2026-09-08T16:20Z by `job`.

The acceptance wrapper at `tests/test-job-reply-parser.sh` now checks the exact
source-task status row and accepts the owner-authored `[active]` or `[done]`
state with `owner=job`. This preserves post-close reproducibility without
allowing an unrelated status line to satisfy the ownership gate.

Verification:

- `./tests/test-job-reply-parser.sh` → `test-job-reply-parser: PASS`.
- `MESH_JOB_REPLY_TEST_OFFLINE=1 ./job/mesh-job-reply --test` →
  `mesh-job-reply --test: ok`.
- Reply state unchanged:
  `6d43d3a0817bb17500279f6aea84f65507df7d5830d55774101b05fafeeda9bb`.
- Calendar state unchanged:
  `fe54fb2873d2f549d005b1ef644d61ebfc57e147942562cc9d147a6c5899909a`.
- Wrapper SHA-256:
  `6b0552837435449d066bdc6d0ddbe9b9ac9c61d546abd9cd33a44a3a93f6e686`.
- Scheduled HH reply wiring remains at `~/.mesh/reflexes.cron:262`:
  `mesh-job-reply --tg`.
- Live source row is `witness-live-unattended-followup-20260908/repair-hh-parser-selector [done] owner=job`.
