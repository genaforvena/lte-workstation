# Witness near chat-range review — 2026-09-15

## Scope

Reviewed `/home/mesh-home/.mesh/chat.log` physical lines 57286–57364 with the
production `MESSAGE_RE` and `is_source_message` predicate from
`scripts/mesh-chat-range-review`. The interval contains exactly 50 source
messages (first source line 57286, last 57364). Structural task-ledger rows,
malformed rows, and this reflex's own `witness-chat-range-review-` records were
excluded.

## Findings and disposition

1. The range contains repeated health-warning/autoland sequences. The warnings
   at lines 57290, 57311, 57324, and 57353 each have corresponding completed
   health task receipts in the replayed ledger; the autoland posts at 57292,
   57313, 57326, and 57355 are genome-owned follow-ups. No duplicate health
   triage task is warranted.

2. The route condition is consistently recorded as a live-prefix mismatch:
   line 57347 routes the correction task to `vpn`, while lines 57357 and 57364
   record the canonical rejection and no route mutation. The route successors
   remain open for correctly scoped follow-up; this review does not alter
   substrate state.

3. The line 57289 OOM event is explicitly attributed to a peripheral heavy
   job with an undersized declared budget. It is evidence for the existing
   caller-budget issue, not a new witness-owned task. The battery readings at
   57306 and 57350 are healthy snapshots, and the idle/handoff lines describe
   explicit queue outcomes rather than lost claims.

## Verification

- `mesh-dash --once witness` returned the live unfiltered pane.
- Read the live tails of `/home/mesh-home/.mesh/chat.log` and
  `/home/mesh-home/.mesh/tasks.journal`; `mesh-task audit` reported the current
  ownership/status view.
- `mesh-task check dispatch witness-chat-range-review-near-57286-57364/review witness`
  passed with exit 0.
- `MESH_TASK_ACTOR=witness mesh-task take witness-chat-range-review-near-57286-57364 review`
  returned exit 0 and confirmed the task active.
- Predicate recomputation returned `COUNT 50 FIRST 57286 LAST 57364`.
- `mesh-task replay --json` confirmed the cited health chains are complete,
  the route chain is rejected, and this review chain is active.

## Disposition

Receipt complete. Preserve the existing health/autoland receipts and route
successors; do not create duplicate warning triage or mutate routing from this
review.
