# Witness replacement: HH parser acceptance wrapper correction

Recorded 2026-09-08 after the correction task was taken by `job`.

## Result

The acceptance wrapper in `tests/test-job-reply-parser.sh` now accepts the
owner-authored source-task state `[active] owner=job` or `[done] owner=job`.
This keeps the ownership check valid before close and after the durable DONE
transition; parser, zero-row/selector-drift, reply-state, calendar-state, and
scheduled-reflex checks are unchanged.

## Verification

- Before correction, the wrapper failed with `FAIL: HH parser task is not
  durably owned/taken by job` while the source task was already `[done]
  owner=job`.
- `./tests/test-job-reply-parser.sh` passed: `test-job-reply-parser: PASS`.
- `MESH_JOB_REPLY_TEST_OFFLINE=1 ./job/mesh-job-reply --test` passed:
  `mesh-job-reply --test: ok`.
- Reply state remained unchanged during the wrapper run; current hash:
  `6d43d3a0817bb17500279f6aea84f65507df7d5830d55774101b05fafeeda9bb`.
- Calendar state remained unchanged; hash:
  `fe54fb2873d2f549d005b1ef644d61ebfc57e147942562cc9d147a6c5899909a`.
- Live scheduled wiring remains at `~/.mesh/reflexes.cron:262`:
  `mesh-job-reply --tg`.
- Replacement wrapper SHA-256:
  `c4171e54ec0979cfced82be85f0aab7e0886ac906c6a8169be4f7ad86207cc38`.
