# Chat review: blocker-class-aware unblock routing

Implemented the fix for `chat-review/operator-input-unblock-misroutes/fix`.

`scripts/mesh-task` now keeps `operator-input` and `external-event` blockers parked. It emits an
event-indexed `[fyi]` trace naming the retry event and does not create or dispatch an
`unblock/<owner>/.../resolve` chain. Owner-resolvable blocker classes, including `dependency`,
retain the existing idempotent resolver behavior.

Verification performed on 2026-09-09:

- `python3 -m unittest tests/test-mesh-task-no-expiry.py` — 11 tests passed.
- `python3 scripts/mesh-task --test` — smoke test passed.
- All Python `test-mesh-task-*.py` tests — passed (including 14 task-log tests, 11 no-expiry tests,
  import, optional-owner, and origin-envelope tests).
- Task shell checks through `tests/test-mesh-task-identity.sh` were inspected; the identity check
  passed independently. The batch stopped at that check without a failure diagnostic from the
  script, so no broader shell-suite pass is claimed.

The source and regression test remain in the working tree for the genome landing steward; unrelated
pre-existing dirty files were not touched.
