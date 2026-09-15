# Health triage: chat delivery age expiry to witness

Date: 2026-09-12
Task: `health-warning/6ab385fe583c48ff328c/triage`

The reported message `09c68d7e64eb27fa` was sent by `tg` to `witness` at
2026-09-09T18:02:05Z and reached terminal `age-expiry` at 18:18:30Z, age 957s
against the 900s limit. The durable delivery ledger records `attempts: 0`.
In `scripts/mesh-chat-deliver`, the attempt count advances only when
`mesh-tell` returns zero, and stdout/stderr are discarded. Thus zero records no
successful handoff; it does not establish whether `mesh-tell` was tried or why
it failed.

The target window was producing board output during the interval: witness
published a handoff at 18:02:00Z and another at 18:18:11Z. Other recipient
handoffs succeeded in the same interval, while three messages to witness also
expired with zero successful attempts. This points to a witness-targeted
delivery failure, but does not identify its cause. The current adapter has no
per-message failed-call count, return code, or stderr evidence, so the root
cause is a known visibility gap. No substrate or delivery configuration was
changed.

Evidence:

- `/home/mesh-home/.mesh/chat-deliver-ledger.json`, entry `09c68d7e64eb27fa`
- `/home/mesh-home/.mesh/chat-deliver.log`, lines around 18:16–18:18Z
- `/home/mesh-home/.mesh/chat.log`, lines around 18:02Z and 18:18Z
- `scripts/mesh-chat-deliver`, `one_pass` handoff and failure accounting

Disposition: investigated and named the unresolved failure as a known
visibility gap; any repair to delivery diagnostics needs its own scoped task.
