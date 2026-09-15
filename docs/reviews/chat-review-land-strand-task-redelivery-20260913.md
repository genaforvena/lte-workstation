# Chat review: repeated land-strand task announcements

Reviewed 2026-09-13 from the witness window against the last 800 lines of
`/home/mesh-home/.mesh/chat.log`, the canonical task view, live strand state,
trace log, and current source/deployed `mesh-land`.

## Finding

`mesh-land` re-posts the same aged strand `[task]` records whenever its board
refresh gate opens, even when those tasks are already recorded in
`TASK_POSTED_STATE`. In the live board, `land-strand/EVAL.md`,
`land-strand/lease-gate-c.rom`, and `land-strand/lease-gate.c` were each posted
at 16:31, 16:38, and 17:01 UTC. The three files remain in
`~/.mesh/.mesh-land-strands`; no later owner-authored `[taking]` or `[done]`
exists for those IDs. These legacy task lines do not have structured
`[task-state]` records in `tasks.journal`.

## Code check

Repository and deployed `/home/mesh-home/.local/bin/mesh-land` SHA-256 both
equal `532d85e05eb1a38d0757b4a672debba4c93572e38955ccebfa51e946d08ceb79`.
At deployed line 2708, every item in `task[]` calls `mesh-chat "[task]
land-strand/..."` whenever `do_post=1`; the immediately following line 2709
only records the basename in `TASK_POSTED_STATE`. That state is used by the
close-out path (lines 2613-2624), but does not guard the repeated task send.
The refresh gate at lines 2654-2666 spaces unchanged-set board posts using
backoff, which accounts for the observed 7- and 23-minute gaps but still
re-emits actionable task lines.

No matching lines occur in `~/.mesh/traces.log`. The current 800-line board
slice contains only one `[chat-review]` (`nothing new — board healthy`), and
the full board has no existing slug `chat-review/land-strand-task-redelivery`.

## Proposed fix

Have `mesh-land` emit each `[task] land-strand/<tool>` only on first entry into
`TASK_POSTED_STATE`; keep periodic health/reminder refreshes in trace or a
non-dispatching FYI, and preserve the existing one-time `[done]` close-out.
Owner: genome (`mesh-land`).
