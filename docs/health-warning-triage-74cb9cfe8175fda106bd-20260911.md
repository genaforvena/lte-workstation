# Health-warning reconciliation: `health-warning/74cb9cfe8175fda106bd`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/74cb9cfe8175fda106bd/triage`

## Live-task verification

The task was the exact live queue head ahead of `health-warning/915a3ef9522ed7288174`:
priority 54, owner `health`, status `open`, dispatch `sent`. The exact command
`mesh-task check dispatch health-warning/74cb9cfe8175fda106bd/triage health`
returned exit 0. It was then claimed with the required owner identity:

```text
MESH_TASK_ACTOR=health mesh-task take health-warning/74cb9cfe8175fda106bd triage
```

## Distinct historical message evidence

The warning remains in `/home/mesh-home/.mesh/chat.log` at
`2026-09-11T18:35:30Z`:

```text
mesh-home/mesh-chat-deliver@mesh-home :: [@haunt] [delivery-failed] target:haunt
window:5963839 count:1 msg:983a38face3fb2f6 attempts:983a38face3fb2f6=0
reason:983a38face3fb2f6=age-expiry age-limit:900s
```

This is distinct from the preceding VPN message `32b0247b056842eb`: the ledger
records sender `haunt`, target `haunt`, message `983a38face3fb2f6`, first seen
`2026-09-11T18:19:55Z`, zero attempts, and terminal failure at
`2026-09-11T18:35:30Z` in failure window `5963839`.

The original message at `2026-09-11T18:19:55Z` was haunt's targeted completion:
`C06-V immutable-training-runs PASS`, with an isolated 4/4 test result, mutation
red/restore-green check, and receipt `docs/task-receipts/C06-verification.md`.
The message was therefore a stale delivery of an already-completed C06-V result,
not a new unresolved Haunt obligation.

## Current delivery-state verification

The current deployed `/home/mesh-home/.local/bin/mesh-chat-deliver` retains the
bounded delivery contract (`MAX_ATTEMPTS=3`, `MAX_AGE=900`): a message with zero
attempts that reaches the age bound is terminally classified `age-expiry`, and a
failure notification is emitted once. The direct smoke test passed:

```text
mesh-chat-deliver --test
mesh-chat-deliver: smoke-test ok (stable message id, terminal controls, bounded ledger contract)
exit=0
```

`haunt` remains a valid target and its tmux window is live. The failure is thus a
historical bounded-delivery expiry, not an absent target and not evidence of a
current deliverer regression.

## Disposition

No retry or source/substrate change is warranted. Retrying this message would
duplicate a completed C06-V result. The warning is settled as superseded stale
delivery evidence while preserving its distinct message ID, sender, timestamp,
attempt count, failure window, and terminal reason above.

Verification artifacts inspected: canonical task queue/state, exact eligibility
check, task claim, original board message, delivery log, delivery ledger, current
deployed deliverer source and smoke test, current Haunt target/window presence,
and the C06-V completion evidence named by the original message.
