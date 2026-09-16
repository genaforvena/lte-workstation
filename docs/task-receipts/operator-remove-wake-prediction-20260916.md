# Remove mandatory wake prediction prompt — 2026-09-16

Task: `operator-remove-wake-prediction-20260916/remove-pane-wake-prediction-prompt`
Ask key: `ask:tg-796515a700e3cf7fbeb4b340`

The requested prompt change is present in `scripts/mesh-pane-consume` at HEAD
`74fb4e6f`: generated `wake_msg` no longer appends the mandatory
`mesh-wake-expect` prediction ritual. The explicit expectation gate and
`mesh-wake-expect` integration remain available in the consumer implementation;
only the generated final instruction was removed.

Verification evidence for this recovery:

- `bash -n scripts/mesh-pane-consume` passed.
- Source assertion found the autonomy instruction and the opt-in wording, and
  found no `Last: PREDICT your pane`, `mesh-wake-expect $ch`, or mandatory
  `mesh-wake-expect senses` suffix in the generated prompt.
- `scripts/mesh-pane-consume --test` was started with a 180-second bound, but
  the live test process did not produce output and was stopped during this
  recovery; this is recorded as an environment/test-run limitation, not a
  passing result.
- Existing focused evidence in
  `docs/task-receipts/operator-autonomous-revisable-mind-20260916.md` records
  the same smoke test as passing before this ledger claim stalled.

No corrective finding was identified; the adjacent findings manifest records
the non-actionable verification limitation and its reason.

Recovery note: at 2026-09-16T06:47Z the canonical `mesh-task progress`, `done`,
and `status` commands remained blocked behind concurrent task-ledger writers;
the observed retry edge is: retry the exact ledger transition when the current
task-ledger writers release the shared state, then settle this step and re-read
the successor dispatch row. No code prerequisite is needed because the source
change is already landed.
