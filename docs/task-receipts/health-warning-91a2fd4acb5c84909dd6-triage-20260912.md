# Health-warning triage: `health-warning/91a2fd4acb5c84909dd6`

- Checked: `2026-09-12T00:17Z`
- Owner: `health` on `mesh-home`
- Task: `health-warning/91a2fd4acb5c84909dd6/triage`

## Verdict

Historical delivery-state ordering fault. The receiver ACK is in the canonical
chat log seven seconds before the attempt-limit warning, while the delivery
ledger did not record `acked` until 2026-09-12T00:17:02Z. The warning therefore
does not establish that the receiver missed this message. Why ACK reconciliation
lagged, and why the failure was emitted after the ACK, remain unknown. This is
not evidence of a current receiver or network outage.

## Evidence

- `~/.mesh/chat-deliver.log` records message `0b920160cca4e87c` delivered to
  `witness` at `22:40:12Z`, `22:43:05Z`, and `22:45:06Z` on 2026-09-09, then
  terminal `attempts:3` at `22:46:10Z` (age 354 seconds, below the 900-second
  age limit).
- `~/.mesh/chat.log` records `witness` posting `[@tg] [ack]
  ack:0b920160cca4e87c` at `22:46:03Z`, seven seconds before the terminal
  warning. The same log records the warning at `22:46:10Z`.
- At this check, `~/.mesh/chat-deliver-ledger.json` records the message as
  `status=acked`, `attempts=3`, `terminal_reason=attempt-limit`, and
  `acked_at=2026-09-12T00:17:02Z`. The ACK is accounted for eventually, but its
  late ledger timestamp leaves the ordering/reconciliation cause unresolved.

## Disposition

Close this historical triage with receiver receipt confirmed by the canonical
ACK line. Preserve the ordering/reconciliation delay as a known blind spot;
no substrate or network change is justified by this evidence.
