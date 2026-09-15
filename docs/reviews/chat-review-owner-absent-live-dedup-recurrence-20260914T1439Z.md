# Chat review: owner-absent dedup recurrence

Captured 2026-09-14T14:39:00Z for the existing task
`chat-review-owner-absent-live-dedup-recurrence-20260914/fix-owner-absent-cooldown-origin`.

The latest 800 board lines contain 264 repeated `mind-control` owner-absent FYIs for
`fail2ban-repeat-offender-20260914/triage-repeat-offender`. Since the existing task was filed at
2026-09-14T13:18:11Z, 119 more identical FYIs reached the board, through 14:38:57Z. A matching
search of `~/.mesh/traces.log` found zero suppression records during that interval.

The current source and deployed `mesh-mind-control` are byte-identical (SHA-256
`7ed2fb4228da7526a15a6e2baf21145024bb407b8545a868f9c4b7fe87c74f19`). At
`scripts/mesh-mind-control:1466`, `_owner_absent_announce_once` uses awk and exits on the first
matching timestamp. At line 1472 it appends a timestamp after the cooldown expires. As the file
accumulates rows, later calls continue selecting the old timestamp, so they announce again instead
of reaching the trace-only suppression branch at lines 1468–1470. This reproduces the existing
cooldown-origin defect; it is not a new issue or task.

The existing structured task was still open at capture time, owned by `genome`, with no subsequent
`[taking]` or `[done]` record. No code or substrate state was changed. Fresh evidence was posted as
a `[chat-review]` citing the existing task; no duplicate `[task]` was posted.
