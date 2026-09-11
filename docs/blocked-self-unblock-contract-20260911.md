# Blocked self-unblock contract

Date: 2026-09-11  
Task: `blocked-self-unblock-followthrough-20260911/make-every-block-actionable`

## Contract

Every `BLOCKED` transition with an owner materializes exactly one resolver chain owned by that
same owner, regardless of blocker class (`operator-input`, `external-event`, `dependency`,
`capability`, or `safety`). The resolver is an actionable task: it must be taken by the exact
owner, diagnose the blocker, create or implement the narrowest safe in-scope prerequisite/fix,
and finish with an artifact-backed result. Parking or rejection requires evidence that authority or
external state is irreducible.

The resolver identity is the exact parent/blocker epoch:

```text
owner | parent chain | parent step | block epoch | blocked timestamp |
blocker type | needs | retry event
```

The parent chain and monotonically increasing `block_epoch` prevent same-text blockers on
different parents, or a new block after an old resolver became terminal, from aliasing. A repeated
observation of the same epoch is idempotent and does not create a paid loop. A resolver result
containing `unblock=cleared event=<event>` resumes only the one blocked parent whose exact identity
it carries; all other parents remain blocked. A terminal resolver without that marker leaves its
parent blocked and does not itself recur for the same epoch.

Resume removes transient blocker fields from the active step. Readers also guard their output by
step status, so historical rows resumed or completed before this contract do not render
`blocker=`/`retry=` as if they were currently blocked.

`mesh-task unblock-sweep` accepts no owner and discovers every blocked owner from the canonical
task ledger. The scheduled `mesh-task-unblock-sweep` reflex invokes that dynamic form, so adding a
new owner cannot silently remove its blocked rows from recovery. The optional owner argument remains
available for targeted repair and compatibility.

## Verification acceptance

- New standalone regression coverage exercises every blocker class, same-text parent separation,
  terminal-resolver epoch replacement, exact-parent clearing, owner-independent idempotent sweep,
  legacy-parent migration, and stale metadata suppression on terminal rows.
- `mesh-task --test` remains green and the source/deployed copies have matching SHA-256 values.
- The sweep reflex `--test` passes and its dynamic no-owner invocation is present in the live
  reflex wiring.
- One live migration sweep is run after deployment; its output is retained in the implementation
  receipt, including the no-new-task/idempotent result when applicable.
