# Task-flow priority observation

Date: 2026-09-12 (UTC)  
Window: `tg`

## Operator request

Make reliable task intake, dispatch, and completion the mesh's critical priority, add observability, and name an observer (operator suggested `business`).

## Live state observed

- Existing chain `task-queue-stall-tinyfleet-proof-20260912` already has priority `0` on all three steps. Its scopes are: `genome` investigates and fixes queue/dispatch/taking stalls; `haunt` proves one real Tiny Fleet task proceeds through owner-authored `taking`/progress to `DONE` or records a concrete blocker; `witness` independently verifies transitions and artifacts.
- The first step has remained `open` and owner-directed to `genome` since 17:31:22Z. The board records re-dispatches at 18:21:50Z and 18:54:04Z, with no `taking` transition in the observed history through 19:18Z.
- At 19:18Z, `mesh-dispatch --status` showed nine idle workers and one open task, still directed to `genome`. The genome pane showed active work on `tg-scripts-layout-migration-20260912/core-primitive-slices`. This is evidence of a task waiting behind its exact owner's active work; it does not establish a queue parser defect by itself.
- Task state refresh is wired through a five-minute `mesh-task-watch` listener on `~/.mesh/chat.log` invoking `mesh-task-journal`. The live crontab also has a five-minute `mesh-dispatch` cadence and a board-write `mesh-fsnotify` trigger for dispatch.

## Verification

- `mesh-task status task-queue-stall-tinyfleet-proof-20260912` — three priority-0 steps, first open and assigned to genome.
- `mesh-task queue --dispatch` — one eligible owner-directed step: genome's `investigate-and-fix`.
- `mesh-dispatch --status` — nine idle workers; the single open task is still routed to genome.
- `mesh-task-watch --test` — PASS (a chat.log write triggers task replay).
- `crontab -l` — task journal event refresh and five-minute dispatcher/reflex wiring present.

## Observer routing and unresolved work

There is no live `business` target in `mesh-chat --targets`. `witness` is already the independent verifier on the existing chain and is the available observability route. The chain is already at priority 0; the immediate visible wait is at owner capacity/claim, not a task that is missing from the ledger. Keep the queue/fix task open until its owner records a structured terminal transition and retain the independent live-task proof and verification steps.
