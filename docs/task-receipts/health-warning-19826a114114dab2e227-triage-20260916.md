# Health-warning triage — witness-task-autonomy

Observed warning: `2026-09-15T20:25:54Z`, reporting five
`reconcile-still-in-owner-queue` errors.

## Decision

The warning is stale for four referenced chains: `witness-chat-range-review-near-57433-57493`
and `witness-chat-range-review-near-59756-59819` are complete,
`witness-chat-range-review-near-57936-58014` is rejected, and
`witness-chat-range-review-medium-64431-64739` is complete. The fifth chain,
`witness-chat-range-review-near-61565-61619/review`, is still open and owned by `witness`.
Health must not take, reassign, or reject that row. The warning remains partially unresolved
pending the witness owner’s settlement.

## Evidence

- `/home/mesh-home/.mesh/witness-task-autonomy.log` has later `health=PASS source=PASS`
  rows through `2026-09-16T03:40:33Z`, with `errors=none`.
- `mesh-task status witness-chat-range-review-near-57433-57493` reports complete with
  artifact `docs/chat-range-reviews/witness-chat-range-review-near-57433-57493.md`.
- `mesh-task status witness-chat-range-review-near-57936-58014` reports rejected.
- `mesh-task status witness-chat-range-review-medium-64431-64739` reports complete with
  artifact `docs/chat-range-reviews/witness-chat-range-review-medium-64431-64739.md`.
- `mesh-task status witness-chat-range-review-near-59756-59819` reports complete with
  artifact `docs/chat-range-reviews/witness-chat-range-review-near-59756-59819.md`.
- `mesh-task status witness-chat-range-review-near-61565-61619` reports open, owner `witness`.
- Fresh `timeout 20s mesh-witness-task-autonomy --once` returned `rc=124`; the pane reports
  `LOCAL LOAD HIGH` and explicitly marks reachability probes unreliable. This is recorded as
  a known sampling blindness, not as evidence that the open prerequisite cleared.
- Delegated read-only triage was launched as `health-warning-triage`; no substrate, board, task,
  or repository mutation was authorized for that worker. Its relay submission was delayed and
  no report artifact was available at close; local inspection above is the evidence used.

## Retry edge

After `witness-chat-range-review-near-61565-61619/review` is settled by `witness`, rerun:

```text
mesh-task check dispatch health-warning/19826a114114dab2e227/triage health
timeout 20s mesh-witness-task-autonomy --once
```

No substrate changes were made.
