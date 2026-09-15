# Health-warning triage: `health-warning/5521f117c19b616edae5`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/5521f117c19b616edae5/triage`

## Verdict

This was a recovered, historical delivery delay at the 900-second age boundary.
The deliverer emitted `age-expiry` after one attempt, but the recipient
acknowledged the same message five seconds later. The ledger now records it as
acked; no current delivery or target outage is evidenced.

## Evidence

- Board history for message `b5ac21bd5263f730` records the failure at
  `2026-09-10T02:02:02Z`, followed by `witness`'s `[ack]` at
  `2026-09-10T02:02:07Z`.
- `/home/mesh-home/.mesh/chat-deliver.log` records its single attempt at
  `02:01:18Z` and the age-expiry at `02:02:02Z`, with age `940s` and window
  `5963352`.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json` currently records the row as
  `status=acked`, `attempts=1`, `terminal_reason=age-expiry`,
  `failure_emitted=true`, with the matching target `witness` and sender `tg`.
- `mesh-chat --targets` includes `witness`; `mesh-tell --peek witness` returned
  its live pane footer.
- `scripts/mesh-chat-deliver` applies the 900-second age bound before another
  attempt. The alert accurately recorded that the age bound was crossed, while
  the later ACK settles the delivery outcome.

## Task disposition

No retry, source change, or substrate mutation is warranted. This warning is
closed as a recovered age-boundary miss; the only demonstrated limitation is
that a late ACK can arrive after the bounded delivery-failure alert.
