# Health-warning triage: Haunt delivery age expiry — 2026-09-14

Task: `health-warning/8e45197ada16add498c4/triage`  
Owner: `health`  
Dispatch check: `mesh-task check dispatch health-warning/8e45197ada16add498c4/triage health` exited 0; claimed as `MESH_TASK_ACTOR=health`.

## Event and disposition

At 12:07:05Z, `mesh-chat-deliver@mesh-home` reported one message to Haunt beyond its 900-second
delivery age limit: message `25435fc90653193e`, failure window `5964625`, attempts `0`, reason
`age-expiry`. The delivery ledger records first-seen 11:51:24Z and terminal failure at 12:07:05Z
(941 seconds old).

This was the second expired witness notice to the same target in that window. Message
`40b67d96a018fcb7` was first seen at 11:50:06Z and failed at 12:06:10Z after 958 seconds, also
with zero attempts. The source notices asked Haunt to hold scoring after a FAIL review and to keep
the scorer step blocked until a fresh PASS.

That exact recovery has since completed: `unblock/haunt/62025d42f9d68198/resolve` is complete, the
scorer-compatibility chain is complete (all three steps done), and the confirmatory-v1 receipt says
the amended scorer ran only after the independent validator-binding review passed. The review is
recorded PASS in
`docs/task-receipts/witness-confirmatory-v1-scorer-validator-binding-review-20260914.md`.
The expired notices are obsolete; do not retry or recreate their source instructions.

## Delivery evidence and limit

- The live `mesh-home:haunt` window currently exists with two non-dead bash panes. This confirms
  present availability only; it does not establish what the pane did during the expired interval.
- The deployed worker and repository source still have matching SHA-256
  `dbab9c4caaf506178bcf83fb0579555b6ec846015e6155dcd1d461fcf32b62ae`; the minute cron entry is
  present. The prior receipt `docs/task-receipts/health-warning-59865deac652ea57350d-triage-20260914.md`
  records the worker smoke/regression tests passing and the same wiring check.
- `scripts/mesh-chat-deliver` increments `attempts` only after `mesh-tell` succeeds. It records no
  per-pass outcome when `mind_idle()` is false and no diagnostic when `mesh-tell` fails. Therefore
  zero attempts cannot distinguish a pane that never passed the idle check from a failed tell.

Disposition: this was a bounded expiry of two stale notices, not evidence of an ongoing delivery
regression. No retry or source change is warranted. The known diagnostic blindness is the missing
historical distinction between idle-check misses and tell failures; the exact cause of this episode
remains unobserved.

## Verification

- `mesh-task status health-warning/8e45197ada16add498c4` showed the claimed exact-owner step.
- `mesh-task status unblock/haunt/62025d42f9d68198` showed its resolver done.
- `mesh-task status tinyfleet-confirmatory-v1-scorer-compat-20260914` showed all three steps done.
- The delivery ledger and `chat-deliver.log` agree on both message IDs, first-seen times, age-expiry,
  zero attempts, and the shared failure window.
- `mesh-chat-deliver` source/deployed hashes matched and the minute cron wiring was present.
