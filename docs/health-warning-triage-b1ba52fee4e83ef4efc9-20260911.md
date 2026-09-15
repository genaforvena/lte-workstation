# Health warning triage: b1ba52fee4e83ef4efc9

Date: 2026-09-11

## Verdict

Historical, terminal delivery failure; no current code or substrate repair is warranted.

## Evidence

- Source event: `2026-09-11T14:28:02Z`, `genome -> witness`, message
  `3449e008576e14d4`, failure `age-expiry`, age `904s`, window `5963789`.
- The live delivery ledger records the exact message as `status=failed`,
  `attempts=0`, `terminal_reason=age-expiry`, and `failure_emitted=true`.
- The current `mesh-chat-deliver` implementation preserves this distinction: it
  emits `age-expiry` when the 900-second age bound is crossed and writes the
  terminal state once; it does not retry an already failed record.
- Both `health` and `witness` windows currently exist. Later delivery log entries
  show successful deliveries to `witness`, including message
  `89a7604a8c408a22` at `2026-09-11T20:39:06Z`; this disproves a continuing
  target/session outage.
- `rtk bash tests/test-mesh-chat-deliver.sh` passed, including bounded retry,
  one failure edge, terminal acknowledgement, duplicate suppression, and fresh-ID
  reopening coverage.

## Disposition

The warning is known historical blindness/expiry evidence, not an active delivery
incident. Preserve the ledger record and do not rewrite it or alter substrate state.
