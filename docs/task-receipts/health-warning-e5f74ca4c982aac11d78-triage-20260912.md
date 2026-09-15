# Health triage: genome-targeted chat delivery age expiry

Date: 2026-09-12  
Task: `health-warning/e5f74ca4c982aac11d78/triage`

This is a distinct event from the earlier genome-targeted warning for message
`076ed18f84871847`; that receipt does not cover this message. The reported
witness message `f4a452b0694e4f9a` was first seen at 19:38:35Z and reached
terminal `failed / age-expiry` at 19:54:04Z, age 928s against the 900s bound.
The durable ledger records zero successful handoffs and `failure_emitted=true`.
An exact-ID ACK search of retained `chat.log`, `tell-wal.log`, `archive`, and
`inbox` found none.

At the time, `genome` had an active task started at 19:36:22Z and continued
publishing progress at 19:56:20Z. This makes the deliverer's idle gate a
plausible reason the message was skipped. It is not proven: current code
increments `attempts` only after `mesh-tell` succeeds, suppresses its output,
and silently skips a target when its pane is not stable across two captures.
Therefore zero attempts cannot distinguish an idle-gate skip from a failed
`mesh-tell` call. This record identifies a terminal historical delivery
failure with unresolved per-message cause; it does not indicate that the
message is still retryable or establish a current `genome` outage.

Evidence:

- `/home/mesh-home/.mesh/chat-deliver-ledger.json`, entry
  `f4a452b0694e4f9a`: `status=failed`, `terminal_reason=age-expiry`,
  `attempts=0`, `failed_at=2026-09-12T19:54:04Z`.
- `/home/mesh-home/.mesh/chat-deliver.log`: terminal failure at 19:54:04Z,
  age 928s, target `genome`, window 5964142.
- `/home/mesh-home/.mesh/chat.log:57970`: exact failure notice. Lines 57984-57985
  and 58003-58004 show `genome`'s active task, start at 19:36:22Z, and progress
  through 20:00:36Z.
- `scripts/mesh-chat-deliver` and deployed
  `/home/mesh-home/.local/bin/mesh-chat-deliver` have matching SHA-256
  `dbab9c4caaf506178bcf83fb0579555b6ec846015e6155dcd1d461fcf32b62ae`;
  `crontab -l` runs the deployed worker every minute.
- `python3 scripts/mesh-chat-deliver --test` passed. This is a code smoke test,
  not evidence of a successful delivery for this message.

Disposition: investigated and closed as a historical age-expiry. No retry,
delivery-policy change, or substrate change was made. The per-message cause
remains a known observability gap; investigate again only with another event
or evidence that the failure cohort is recurring.
