# Health warning triage: chat delivery age expiry — 2026-09-14

Task: `health-warning/59865deac652ea57350d/triage`  
Owner: `health`  
Dispatch check: `mesh-task check dispatch health-warning/59865deac652ea57350d/triage health` exited 0; claimed as `MESH_TASK_ACTOR=health`.

## Event and outcome

At 2026-09-14 11:50:06Z, witness sent Haunt an FYI that the independent scorer-amendment review
was FAIL and asked it to update `unblock/haunt/62025d42f9d68198/resolve` with a validator binding,
a mutation regression, and a scoped commit. The message ID is `40b67d96a018fcb7`.

Delivery emitted `[delivery-failed]` at 12:06:07Z. The delivery log and ledger agree: first seen
11:50:06Z, failed at 12:06:10Z, age 958 seconds, attempts 0, target `haunt`, terminal reason
`age-expiry`, failure window `5964625`. The original note was not delivered before the bounded
900-second TTL. The delivery worker only calls `mesh-tell` after the target pane is stable across
its idle check; the recorded zero attempts is consistent with that gate never opening before the
age bound. The retained evidence does not identify why no idle observation occurred.

The exact recovery already existed: `unblock/haunt/62025d42f9d68198/resolve` completed at
12:23:06Z as stale because the blocker had been resolved. Haunt's scorer-binding task completed,
and the independent witness review is PASS at
`docs/task-receipts/witness-confirmatory-v1-scorer-validator-binding-review-20260914.md`.
The scorer-compatibility chain is complete; its receipt records scoring of the unchanged tape.
No prerequisite task needed to be duplicated and the expired FYI must not be retried.

## Live delivery checks

- `scripts/mesh-chat-deliver` and `/home/mesh-home/.local/bin/mesh-chat-deliver` have matching
  SHA-256 `dbab9c4caaf506178bcf83fb0579555b6ec846015e6155dcd1d461fcf32b62ae`.
- `crontab -l` wires the deployed worker every minute.
- `./scripts/mesh-chat-deliver --test` passed; `bash tests/test-mesh-chat-deliver.sh` passed,
  including retry recovery, one terminal failure edge, ACK handling, duplicate suppression, and
  reopening with a fresh message ID.
- The live `mesh-home:haunt` tmux window exists with two non-dead bash panes.

## Disposition

This is one historical, bounded-delivery expiry, not evidence of a current deliverer regression.
The underlying scorer blocker was fixed and independently verified through its exact recovery
chain. No source, substrate, or retry action is warranted. Retain the delivery failure as evidence;
close this health warning with this receipt.
