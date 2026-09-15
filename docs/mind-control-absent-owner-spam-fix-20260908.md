# Mind-control absent-owner spam fix — 2026-09-08

## Root cause

`scripts/mesh-mind-control:1237` posted a board `[fyi]` every time
`mesh-dispatch` retried an explicit-owner task whose window was absent. The
dispatcher correctly returned rc=3 and kept the task open, but the notification
side effect had no deduplication. The live task
`witness-live-unattended-followup-20260908/repair-parked-autostash-strand`
generated repeated posts roughly every minute.

## Change

Added `_owner_absent_announce_once()` and routed the absent-owner branch through
it. It keys state by the normalized task summary, stores the last notification
epoch in `~/.mesh/.owner-absent-announced`, and suppresses repeats for the
default 14,400 seconds. Suppressed retries are sent to `mesh-trace`; dispatch
still returns rc=3, so the task remains open and is rechecked.

## Verification

- Regression first ran red: the new test observed a second absent-owner `[fyi]`.
- `bash scripts/mesh-mind-control --test` then passed: `9 classifier + 8 picker +
  27 owner-routing + 3 owner-route-wrapper + 3 dispatch-echo + 1 human-owned-
  announce + 3 owner-hold-announce + 5 darwinian-fitness + 4 phaedra-thermal-
  prefer + 6 dispatch-remote-phaedra + 16 dispatch-ack-gate + 3 noack-board-
  dedup + 3 ack-load-window + 3 cross-node-dedup + 3 gossip-lag-presync + 5
  same-target-dedup + 10 resume-resurface + 23 orphan-owner-finding-detector +
  4 dispatch-flag-injection-guard + 3 owner-honesty + 13 row-table + 10
  dispatch-gate + 7 structural-bias assertions`.
- The deployed `/home/mesh-home/.local/bin/mesh-mind-control` resolves to
  `scripts/mesh-mind-control`.
- Live state at 18:04:23Z recorded one notification in
  `~/.mesh/.owner-absent-announced`; no further matching board `[fyi]` appeared
  through 18:04:43Z, while `~/.mesh/dispatch.log` continued to record rc=3
  retryable holds.

## Remaining task state

The original land-owned task remains `OPEN_UNOWNED` as required by exact-owner
discipline. This fix does not close it or infer completion; it only stops the
notification loop while preserving retry and ownership semantics.
