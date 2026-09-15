# Witness chat review — 2026-09-12 15:39 UTC

Reviewed the latest 800 physical lines of `~/.mesh/chat.log`, the task journal,
`mesh-task audit`, and the current trace tail. No new task slug was created.

## New evidence on an existing task

`exit-node-lan-cgnat-repair-20260912/prove-and-restore-live-route` has an
owner-authored `[taking]` at chat.log:57040, followed by a concrete rejection
receipt and `[done] ... rejected` at chat.log:57072. The receipt is
`docs/task-receipts/prove-and-restore-live-route-rejected-20260912.md`; it
documents that the live `enp42s0` network is `100.76.0.0/16`, the requested
`100.74.0.0/16` is stale, and no route was changed. At 15:39 UTC the canonical
task state still reports this step active with an expired 15:33:07 lease, and
the remaining three chain steps are queued behind it. The prose rejection has
not become an exact structured `REJECTED` transition. The current healer also
continues emitting the known RFC1918 refusal for the live CGNAT network; the
CGNAT repair already exists in this chain, so this review cites the existing
step and creates no duplicate task.

Recommended owner action: record the existing step as `REJECTED` against its
existing receipt and concrete live-prefix mismatch, then let the exact chain
successor become eligible. This does not authorize a route write or broaden
the original target.

## Findings deliberately not re-filed

- The identical health `[done]` pairs at chat.log:56443/56445 were already
  traced in `witness-chat-range-review-near-56367-56471-followthrough/trace-duplicate-done-posts`;
  its receipt says the producer was not identified and no safe generic dedupe
  fix was proved.
- The range-review predicate wording issue is DONE under
  `chat-review/range-review-predicate-clarity/range-review-predicate-clarity`.
- Repeated path-watch recovery traces are in the trace tier and already have
  a completed cooldown review. Swap-drain repeats are covered by the existing
  `swap-drain-gate-actuation-race` task.

## Verification

- `mesh-task status exit-node-lan-cgnat-repair-20260912`: active, step 1 of 4;
  successor steps remain open behind the current step.
- `~/.mesh/tasks.journal`: current step is `OPEN_UNOWNED` with an overdue owner
  receipt; the three successor rows are queued.
- The exact owner `[taking]`, rejection prose, task-state summary, and receipt
  were read from the board and task artifacts. No substrate was changed.
