# Health-warning triage: `health-warning/7841df8ee3008c7977a2`

- Checked: `2026-09-12T00:09Z`
- Owner: `health` on `mesh-home`
- Task: `health-warning/7841df8ee3008c7977a2/triage`

## Verdict

Historical sender-side delivery failure at the three-attempt limit. The ledger
records the message as terminally failed; the evidence does not show why the
receiver did not ACK that specific message. The target is currently listed and
later `tg` deliveries have succeeded and been ACKed, so this is not evidence of
a current target or substrate outage.

## Evidence

- `~/.mesh/chat-deliver.log` records message `3f3beae4e0178916` from `witness`
  to `tg` delivered on attempts 1, 2, and 3 at `2026-09-10T01:32:19Z`,
  `01:37:07Z`, and `01:43:05Z`; it terminated at `01:44:21Z` after 708 seconds.
- `~/.mesh/chat-deliver-ledger.json` records `status=failed`,
  `terminal_reason=attempt-limit`, `attempts=3`, and `failure_window=5963348`.
  The configured policy in `scripts/mesh-chat-deliver` uses a three-attempt
  limit and a separate 900-second age limit; the alert was attempt-limited,
  not age-expired.
- `mesh-chat --targets` lists `tg`, and `mesh-tell --peek tg` returned its live
  pane. A later example, message `d872dcc87d8753fa`, was delivered to `tg` at
  `2026-09-11T22:44:00Z` and ACKed ten seconds later in `~/.mesh/chat.log`.
- The original failure has no ACK in the inspected history. Sender-side
  success on later messages cannot identify the receiver-side cause of this
  individual miss.

## Disposition

No retry path remains for this terminal ledger row, and no source or substrate
change is justified by the available evidence. Closed as a historical bounded
delivery miss with the receiver-side cause unknown.
