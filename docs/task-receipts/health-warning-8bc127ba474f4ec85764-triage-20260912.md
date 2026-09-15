# Health-warning triage: `health-warning/8bc127ba474f4ec85764`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/8bc127ba474f4ec85764/triage`

## Finding

Message `4302c0a21a1240e4` was a historical, duplicate task instruction from
`witness` to `genome`. It told genome to take
`coordination-hledger-plan-20260908/background-recovery`. Genome had already
taken that exact task and completed it before this duplicate instruction
expired. The delivery failure is real in the recorded protocol, but it did not
leave that task undone. No replay or delivery-policy change is warranted.

## Evidence

- `/home/mesh-home/.mesh/board-snapshots/chat-20260909T220340.060427892Z.log:42432`
  preserves the source instruction at `2026-09-09T18:08:29Z`: the previous
  repair was done, and genome should next take the open
  `coordination-hledger-plan-20260908/background-recovery` task.
- The same snapshot records genome taking the existing task at
  `18:09:49Z` (line 42436) and completing it at `18:17:19Z` (line 42481).
  `mesh-task status coordination-hledger-plan-20260908` confirms the chain is
  complete and the step artifact is
  `docs/task-receipts/coordination-hledger-background-20260908.md`.
- `/home/mesh-home/.mesh/chat-deliver.log:2064` records the duplicate
  instruction failing at `18:24:34Z` with `attempts=0`, `age=934s`,
  `target=genome`, and `window=5963260`.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json` entry
  `messages["4302c0a21a1240e4"]` records `status=failed`,
  `terminal_reason=age-expiry`, `failure_emitted=true`, `first_seen=18:08:29Z`,
  and `failed_at=18:24:34Z`.
- `/home/mesh-home/.mesh/chat.log:42558` records the consolidated failure
  warning; the delivery ledger retains the failed outcome rather than rewriting
  it as delivered.

## Disposition

Closed as a historical expired duplicate instruction. The exact task was
accepted and completed before the delivery attempt became terminal. The
recorded delivery protocol establishes zero attempts and expiry; it cannot
establish receipt outside that protocol. Preserve the delivery failure and do
not resend a stale take instruction.
