# Witness chat review — 2026-09-09 15:37Z

## Finding

`scripts/mesh-task` treats every blocked step as owner-resolvable. At lines 695–732,
`ensure_unblock_task` hashes the owner/blocker and immediately saves and dispatches an
`unblock/<owner>/.../resolve` chain without branching on `blocker_type`. The live board
then showed `unblock/haunt/2516948d7a4ec4e4/resolve` for an `operator-input` dictionary
blocker and `unblock/haunt/d777001dbb8844aa/resolve` for an operator-directed dependency
(2026-09-09T15:29:57–15:29:58Z). These tasks route an unavailable external decision back
to the same worker and consume dispatch capacity without changing the prerequisite.

## Proposed fix

Keep `operator-input` and `external-event` rows parked and emit only an event-indexed
reminder/trace entry; materialize an owner resolver only for blocker classes that the
owner can actually satisfy. Preserve idempotency and add a test proving that an
operator-input block does not dispatch an unblock worker task, while a resolvable
dependency still does.

## Verification

- `mesh-task audit` and `tasks.journal` were read before review.
- Last 800 unfiltered `/home/mesh-home/.mesh/chat.log` lines were reviewed.
- Existing `[chat-review]` slugs were searched; no prior review targets this
  blocker-class routing defect.
- Source was inspected with `nl -ba scripts/mesh-task | sed -n '680,760p'`.
