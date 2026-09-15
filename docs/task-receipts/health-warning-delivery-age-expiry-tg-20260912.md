# Health triage: chat delivery age expiry to tg

Date: 2026-09-12
Task: `health-warning/8f1249b68a3d9fd2091b/triage`

The reported message `4b71eceec13455e5` was sent by `witness` to `tg` at
2026-09-09T18:01:20Z and reached terminal `age-expiry` at 18:17:31Z, age 942s
against the 900s limit. The durable delivery ledger records `attempts: 0`.
The message was an owner task about the deployed dashboard test failing on the
missing division-of-labour/mesh-forage output.

The target `tg` was publishing board activity during the interval, including a
handoff at 18:02:06Z. Delivery to `tg` succeeded for another message at
18:11:05Z, while this message still ended with zero successful handoffs. This
does not identify a target-wide outage. In `scripts/mesh-chat-deliver`, the
attempt count advances only when `mesh-tell` returns zero, and stdout/stderr
are discarded. The durable evidence cannot distinguish a failed invocation,
an invocation that was skipped, or why the handoff was unsuccessful.

Disposition: investigated; exact cause remains a known visibility gap in
delivery failure reporting. No dashboard or substrate changes were made.

Evidence:

- `/home/mesh-home/.mesh/chat-deliver-ledger.json`, entry `4b71eceec13455e5`
- `/home/mesh-home/.mesh/chat-deliver.log`, lines around 18:11–18:18Z
- `/home/mesh-home/.mesh/chat.log`, lines around 18:01–18:02Z
- `scripts/mesh-chat-deliver`, `one_pass` handoff and failure accounting
