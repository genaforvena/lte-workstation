# Witness medium chat-range review — 2026-09-15

## Scope

Reviewed `/home/mesh-home/.mesh/chat.log` physical lines 57494–57816 with the
production `MESSAGE_RE` and `is_source_message` predicate from
`scripts/mesh-chat-range-review`. The interval contains exactly 250 source
messages (first source line 57494, last 57816). Structural task-ledger/task-state
rows, malformed rows, and this reflex's own `witness-chat-range-review-` rows
were excluded.

## Findings and disposition

1. The range continues the route/health warning stream and high coordination
   volume seen in the prior reviewed slices. Repeated health triages are
   fingerprinted into exact owner tasks and receipts; no duplicate warning task
   was opened. The current audit still reports `chain_steps=1570`, with live
   findings increasing to 96 as new checks arrive.

2. The concrete workflow discrepancy is task-production backpressure. The
   range contains repeated witness/autonomy and owner-queue activity, while the
   live board later reports `health-fail witness-task-autonomy` with
   `checks=113` and errors naming review rows still in the owner queue. This is
   consistent with a producer outrunning a single active witness consumer, not
   with missing ownership: the current dash shows many exact witness-owned
   review rows and zero `RUNNING` rows before dispatch. The board records the
   bounded producer fix `MESH_CHAT_REVIEW_MAX_PENDING=10` and its focused tests
   as already applied. No new corrective task was created; the existing queue
   and the exact witness review claimed this turn are the safe recovery path.

3. Repeated handoffs, claims, completions, and idles were checked against the
   task journal. They are high-volume coordination records, but exact replay
   distinguishes completed work from queued/blocked rows and rejected
   duplicates. No duplicate claim or source/task-ledger disagreement requiring
   a new owner route was found in this slice.

## Verification

- `rtk mesh-dash --once witness` returned the live unfiltered pane.
- Read the live tails of `/home/mesh-home/.mesh/chat.log` and
  `/home/mesh-home/.mesh/tasks.journal`; `rtk mesh-task audit` returned the
  current `FAIL` result and findings count.
- `rtk mesh-task queue --dispatch --owner witness` returned this exact row;
  `rtk mesh-task check dispatch witness-chat-range-review-medium-57494-57816/review
  witness` passed, and the owner-authored take claimed it.
- Predicate recomputation returned `COUNT 250 FIRST 57494 LAST 57816`.
- `rtk mesh-task replay --json` was used to distinguish existing completed,
  queued, blocked, and rejected rows; no duplicate task was created.

## Disposition

Receipt complete. Preserve the pending-limit fix and existing owner-routed
queue; do not replay already completed warnings or create duplicate reviews.
