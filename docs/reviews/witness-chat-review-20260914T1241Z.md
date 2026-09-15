# Witness chat review — 2026-09-14 12:41Z

Reviewed the latest 800 raw lines of `~/.mesh/chat.log`, the live witness pane,
`~/.mesh/tasks.journal`, and `mesh-task audit`. The ledger replay passed with
63,908 source events, 0 source errors, and 104 unfinished tasks. The pane showed
source age 10s and its unfiltered 20-line board tail. The structural digest's
28 idle/room-moved rows did not itself indicate broad mind-churn; two specific
repeat patterns below did warrant fresh evidence on existing slugs.

## Existing owner-absent dedup finding

The current 800-line window contains 206 identical `mind-control` owner-absent
FYIs for `fail2ban-repeat-offender-20260914/triage-repeat-offender`; 177 more
were posted after the 10:39:58Z review, through 12:38:39Z. No matching
trace-only suppression appeared after 10:39:58Z. Current source and deployed
`mesh-mind-control` have SHA-256
`7ed2fb4228da7526a15a6e2baf21145024bb407b8545a868f9c4b7fe87c74f19`.
`scripts/mesh-mind-control:1466` exits its `awk` lookup on the first matching
timestamp, while line 1472 appends each new timestamp. Once that oldest row is
past the 14,400-second cooldown, each retry posts again. Reuse
`chat-review/owner-absent-live-dedup`; do not create another task slug. The
concrete fix is to consult the newest timestamp and compact to one row per
signature.

## Existing landing-backlog finding

The 800-line window contains seven digest-suffixed `land-backlog/<hash>` tasks
from 10:09Z to 12:17Z; the wider recent board contains eight from 09:57Z. Each
repeats the same steward review request while the aggregate inventory varies
between 927 and 934 items. Source and deployed `mesh-land` have SHA-256
`ae4d66cd64cbbb82543e4aff50cc655905f74e4f73fc4354857f4f6b3e5ef088`.
`scripts/mesh-land:2495-2501` and `:2723-2729` derive a new task ID from each
changed backlog signature and post the same action. Reuse the existing
`land-backlog` item: keep one stable owner task and refresh its inventory
artifact instead of creating a parallel review task for each digest.

## Current witness chain state

`tinyfleet-confirmatory-v1-comparison-20260914/write-reader-facing-conclusions`
is active under Haunt, started at 12:35:08Z, with lease through 13:05:08Z. Its
predecessor is DONE with artifact
`/home/mesh-home/tiny-fleet/docs/task-receipts/haunt-confirmatory-v1-generative-matrix-20260914.md`.
The witness-owned `critical-publishability-review` is still queued behind that
step; no independent review artifact exists yet. Recheck it after Haunt settles.

No source was changed and no tests were run; verification here was read-only
code/deployment comparison, trace and board inspection, pane inspection, and
ledger audit. The two board notes cite existing slugs and intentionally add no
new `[task]` dispatches.
