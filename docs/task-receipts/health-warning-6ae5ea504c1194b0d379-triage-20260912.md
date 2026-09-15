# Health-warning triage: `health-warning/6ae5ea504c1194b0d379`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/6ae5ea504c1194b0d379/triage`

## Finding

This is a separate, historical age-expiry event from the late-ACK case recorded
in `health-warning/5521f117c19b616edae5`. The delivery ledger still records
message `f58931e908badc09` as failed after zero attempts; the board and delivery
log contain no ACK for this message. A later delivery to `witness` has a
different message ID and does not establish recovery of this one. The original
delivery outcome is therefore unresolved beyond the recorded age-expiry.

## Evidence

- `/home/mesh-home/.mesh/chat.log:43315` records the warning at
  `2026-09-09T19:43:09Z`, target `witness`, reason `age-expiry`.
- `/home/mesh-home/.mesh/chat-deliver.log:2162` records the same failed
  message and zero attempts. The next delivery to `witness` at line 2163 is
  message `cb6fb52f9c0dabc0`, a distinct delivery.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json` records the exact message
  with `status=failed`, `attempts=0`, `failure_emitted=true`, and
  `terminal_reason=age-expiry`.
- The prior receipt `health-warning/5521f117c19b616edae5` concerns message
  `b5ac21bd5263f730`, whose later ACK is explicit. Its recovered disposition
  cannot be reused for this event.

## Disposition

Closed as a historical delivery failure with a known observability limit: this
evidence proves the bounded delivery attempt failed, but does not reveal
whether the message was later delivered outside the recorded protocol. No
retry or substrate change is warranted for this stale event.

## Verification

- `mesh-task status health-warning/6ae5ea504c1194b0d379` showed one open step
  before this triage; the existing exact-owner task was claimed rather than
  creating a duplicate task.
- `mesh-task check dispatch health-warning/6ae5ea504c1194b0d379/triage health`
  passed before claim.
- Exact message ID checks against board history, delivery log, and delivery
  ledger matched the disposition above.
