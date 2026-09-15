# Receipt: idempotent mesh-land board output

Implemented `post_board_once` in `scripts/mesh-land`. Board emissions now use a persisted,
flock-serialized artifact-signature gate with a one-hour TTL: the first `[done]`, `[strand]`, or
`[health-fail]` post is emitted, while repeats are recorded in `land.log` and do not wake the board.
Overlap alerts retain their existing independent alert state and now share the same duplicate-safe
board emission path.

Verification:

- `bash -n scripts/mesh-land tests/test-mesh-land-idempotent-output.sh`
- `git diff --check`
- `bash tests/test-mesh-land-idempotent-output.sh` — PASS, including cross-kind duplicate suppression
- `bash tests/test-mesh-land-check-budget.sh` — PASS, including overlap alert trace behavior
- `bash scripts/mesh-land --test` — PASS (`smoke-test: ok`)
