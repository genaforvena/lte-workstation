# TG operator intake and ledger coverage

Date: 2026-09-07  
Ask: `ask:tg-operator-ledger-coverage-20260907`

## Contract

Every actionable operator message receives one immutable `ask:<key>`. If the work is larger than
one bounded action, the intake owner writes a TSV decomposition before execution. The parent chain
is created with `mesh-task create <chain> <plan.tsv> <ask-key>`; each step has an exact owner, a
lease, progress evidence, and a closure artifact. A reply, handoff, or reading note is not closure
unless it cites the task and produces or points to the durable artifact.

The same rule applies to autonomous discoveries: literature or autopoiesis may create an idea, but
the implementation must enter the same chain before it becomes long-running work. Short-lived
observations can remain `[fyi]`; once there is an actionable next step, it is a task.

## What is wired now

`scripts/mesh-task` already provides the durable state machine: JSON chain state under
`~/.mesh/task-chains`, `ask` propagation on board events, exact-owner claims, lease/progress/block
states, artifact-hashed `done`, and `audit`. The live TG intake chain is
`tg-operator-intake`, and this request has a separate audit chain
`witness-ledger-coverage-audit` owned by `witness`.

## Remaining wiring / acceptance

The witness audit must inspect the live board, task-chain JSON, handoffs, and autonomous queues;
classify every actionable long-running item as ledgered or bypassed; and leave a dated report with
the exact repair owner and next command. The intake path is accepted only when a synthetic TG ask
creates a chain with the ask key, dispatches one owner, and cannot close without an artifact.

This design deliberately leaves historical uncited messages visible as audit findings rather than
rewriting them into fake task history.
