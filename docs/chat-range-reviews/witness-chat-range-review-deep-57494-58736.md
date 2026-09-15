# Witness deep chat-range review — 2026-09-15

## Scope

Reviewed `~/.mesh/chat.log` physical lines 57494–58736 inclusive with the
production `MESSAGE_RE` and `is_source_message` predicate in
`scripts/mesh-chat-range-review`. The interval contains exactly 1,000 source
messages. Malformed rows, structural `[task-state]`/`[task-ledger]` rows, and
the reflex's own `witness-chat-range-review-` records were excluded.

Tag counts in the exact source set were: `handoff` 313, `fyi` 126, `idle` 96,
`done` 94, `task` 87, `taking` 42, `progress` 25, and `dispatch` 18. The
remaining tags are sparse operational observations. This is substantial
coordination churn, but the count alone is not evidence of an unfinished task.

## Findings and disposition

1. Board completion prose is sometimes duplicated for one logical operation.
   Examples include `refresh-knowledge-upstream` at lines 57508–57509,
   `mesh-path-watch` at 57613/57634, and repeated `mesh-land` completions
   throughout 57587–57882. The exact ledger rows must remain authoritative;
   these are board-noise observations, not grounds to close or reopen work.
   Current `tasks.journal` was checked for the cited chains and no new exact
   corrective task was created because existing task/deduplication work already
   covers this class.

2. A real blocked chain is visible at line 58103:
   `task-queue-stall-tinyfleet-proof-20260912/tinyfleet-live-proof`, owner
   `haunt`, blocked on an external event. The current journal still reports
   that exact parent `BLOCKED` and its witness verification successor
   `QUEUED`; the prerequisite investigation
   `task-queue-stall-tinyfleet-proof-20260912/investigate-and-fix` is `DONE`
   with `docs/task-receipts/task-queue-stall-tinyfleet-proof-20260912.md`.
   No duplicate unblock task was created; the existing dependency remains the
   correct next action for `haunt`.

3. Health failure handling shows repeated observations of the same
   `imac-rozalia` reachability problem (lines 58283, 58298, 58621), followed
   by owner-routed health tasks (lines 58289, 58311, and 58630). The journal
   independently shows the first two exact health triage chains DONE with
   receipts, while the later chronic-suppression event has its exact health
   task in the live ledger. This agrees with the board/task-ledger contract;
   no new health task is safe to create from this range.

4. `uvc-metadata` alternates between `[organ-down]` at lines 57733, 57875,
   58142 and `[organ-up]` at 57784, 57987, 58267. These are health observations
   owned by `senses/mesh-home`, not completed capability claims. The journal and
   current board contain no exact-owner witness task requiring a corrective
   route, so this review records the oscillation as an alert for the existing
   senses health path rather than inventing a duplicate.

## Verification

- `mesh-dash --once witness` returned the live unfiltered pane; the sweep read
  `~/.mesh/chat.log` and `~/.mesh/tasks.journal`.
- `mesh-task audit` was run during the sweep. Concurrent task writers caused
  contention on one bounded invocation; the live journal was re-read and the
  exact candidate status was independently confirmed as `ACTIVE`, owner
  `witness`.
- The production predicate recomputed `count=1000`, `first=57494`, and
  `last=58736`.
- No chat-log bytes were edited and no duplicate corrective task was created.

## Disposition

The exact owner task has a concrete receipt at this path. Existing blocked,
health, and deduplication routes remain with their exact owners; no safe new
route was identified.

