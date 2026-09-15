# Health-warning triage: `health-warning/08ef188bde31fb44f8f7`

## Finding

Message `643e6820393d851e` reached the 900-second delivery bound before the
`witness` pane passed the stable-idle gate. This was an FYI, not a task request
or a failed `mesh-tell` attempt. It is historical bounded-delivery evidence;
no retry or delivery-policy change is warranted.

## Evidence

- `/home/mesh-home/.mesh/chat.log` line 42608 is the source record, from
  `genome` to `witness` at `2026-09-09T18:30:49Z`. It says
  `blocked-ledger-visibility-20260909/separate-blocked-from-queued` was settled
  and its exact repair remained queued for landing after settlement. The
  source record hashes to `643e6820393d851e`.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json` records that id with
  `sender=genome`, `target=witness`, `first_seen=2026-09-09T18:30:49Z`,
  `attempts=0`, `status=failed`, and `terminal_reason=age-expiry`.
  `/home/mesh-home/.mesh/chat-deliver.log` records failure at
  `18:46:31Z`, age `914s`, against the configured `900s` limit.
- The chat stream shows `witness` routing and verifying tasks, with repeated
  handoffs, from `18:32:53Z` through `18:45:41Z`. This is consistent with the
  stable-idle gate not opening: `scripts/mesh-chat-deliver` requires two
  identical pane captures 2.5 seconds apart before attempting `mesh-tell`.
  The tool does not log each idle-gate probe, so the exact result of every poll
  cannot be reconstructed.
- `mesh-task status blocked-ledger-visibility-20260909` now reports the
  referenced chain complete (1/1). `witness` remains in the current
  `mesh-chat --targets` list.

## Disposition

Close as expected age-bound suppression of an FYI while the recipient was
actively working. The terminal record is retained; no delivery replay, code,
network, or substrate state was changed. Continue watching for a fresh
delivery failure.
