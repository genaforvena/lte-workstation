# Proactive idle task pickup

## Board finding

The live task ledger had 132 unfinished rows. The consumer wake prompt in
`scripts/mesh-pane-consume` told a mind to read its live dashboard and either
act or emit `[idle]`, but did not tell it to inspect the dispatchable task
queue. That made an idle state report a terminal-looking outcome even when
the board still contained work for that mind.

## Change

The wake prompt now requires this order when the dashboard has no safe action:

1. Run `mesh-task queue --dispatch`.
2. Select a row whose exact owner is the receiving mind.
3. Validate it with `mesh-task check dispatch <task-id> <mind>`; only exit 0 is eligible.
4. Claim it with `MESH_TASK_ACTOR=<mind> mesh-task take <chain> <step>` and work it.
5. Post `[idle]` only when no eligible owned task remains.

The prompt explicitly forbids taking another mind's owned row or attempting a
held/non-pending row. The stream
driver remains a prompt-only consumer: it does not parse, claim, or mutate the
task ledger. General routing remains in `mesh-dispatch`/`mesh-mind-control`.

## Verification

- Red-first smoke check: `scripts/mesh-pane-consume --test` failed before the
  prompt change because the proactive queue instruction was absent.
- Current check: `scripts/mesh-pane-consume --test` passes, including assertions
  for `mesh-task queue --dispatch`, owner-scoped `mesh-task take`, and the
  cross-owner prohibition.
- Live delivery: at `2026-09-11T12:20:00Z`, `scripts/mesh-pane-consume health
  --once` returned 0 and logged `health: WOKE mind (health)`. `mesh-tell
  --peek health` then showed the exact queue/check/owner-scoped instruction in
  the live pane while health was `WORKING`; the first health queue row passed
  `mesh-task check dispatch` with exit 0. No `[taking]` receipt had landed by
  the observation cutoff, so task execution remains unclaimed evidence.
