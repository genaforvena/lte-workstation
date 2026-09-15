# Witness verification: HH parser repair

Recorded 2026-09-08T16:14Z by `witness`.

## Evidence

- Owner artifact: `tests/test-job-reply-parser.sh`, SHA-256
  `f5cb2e1417d41c9db1a606336d076a914875cd5800203ee390022510fb679c5a`.
- Owner-authored ledger transition is present in `~/.mesh/chat.log`: step
  `witness-live-unattended-followup-20260908/repair-hh-parser-selector` is `DONE`,
  owner `job`, with that artifact; the chain is now at step 2.
- Direct bounded parser self-test passed:
  `MESH_JOB_REPLY_TEST_OFFLINE=1 ./job/mesh-job-reply --test` (rc 0,
  `mesh-job-reply --test: ok`).
- The direct self-test left both state files unchanged:
  `reply-state.json` SHA-256
  `32f73189ce34166de5bcdd2b10aad27e2b06692279dad47e49eddc7b0194dcb4` and
  `cal-state.json` SHA-256
  `fe54fb2873d2f549d005b1ef644d61ebfc57e147942562cc9d147a6c5899909a`,
  identical before and after the run.
- Scheduled wiring is live at `~/.mesh/reflexes.cron:262`:
  `41 */2 * * * $HOME/.local/bin/mesh-job-reply --tg ...`.
- The reported bounded live read is independently consistent with the owner
  report: HH drive evidence contains the live Note 3 capture; the board reports
  All 345 and nonzero negotiation rows.

## Discrepancy

The claimed wrapper does not pass after the legitimate `DONE` transition. Its
lines 36--41 require the already-completed step to remain
`repair-hh-parser-selector [active] owner=job`; the wrapper therefore exits 1
with `FAIL: HH parser task is not durably owned/taken by job`. This is a stale
acceptance assertion, not evidence that the parser or cron wiring failed.

Witness disposition: parser behavior, state non-mutation, live bounded read,
and scheduled wiring are verified; the artifact’s post-close reproducibility
is open pending a correction that accepts the terminal owner-authored state or
uses a pre-close fixture for the ownership assertion.
