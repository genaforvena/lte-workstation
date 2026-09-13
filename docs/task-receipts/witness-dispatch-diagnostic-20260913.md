# Queue dispatch diagnostic — 2026-09-13

The live task `health-warning/4ffcd9cbfa5307a1234e/triage` repeatedly reached
`dispatch=failed`, but the ledger discarded the failing board-helper exit code and
message. That made the queue observable only up to a generic retry instruction.

`scripts/mesh-task` now captures a failed board helper's return code and bounded
stderr/stdout text, and records it inside `dispatch_error` while preserving the
existing durable state-before-retry behavior. Missing executables are reported in
the same field. A new mesh-task self-test forces a helper failure with exit 73 and
`synthetic board refusal`; it first failed because neither detail reached stderr,
then passed after the change.

Focused verification completed:

- `scripts/mesh-task --test`
- `python3 tests/test-mesh-task-blocked-self-unblock.py` — 12 tests
- `python3 tests/test-pane-consume-unowned-candidate.py`
- `scripts/mesh-pane-consume --test` (the existing long-running sleep-based check)
- `git diff --check`

This is committed on `codex/witness-autonomy-reflex-20260913` and must land with
the earlier witness reflex, GPU lease, and ownerless wake-consumer repairs. It does
not rewrite the current live warning: that task is owned by Health and remains
observable as failed dispatch until the deployed code provides its actual cause or
Health settles it.
