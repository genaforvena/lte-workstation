# Health warning triage: mesh-land overlap alert deduplication

Date: 2026-09-15
Task: `health-warning/d1682ad40a18cb0be846/triage`
Owner: `health`

## Finding

The reported duplicate alerts were real. `scripts/mesh-land` acquired the
autoland run lock, but its collision branch unconditionally posted the same
`[health-fail]` message at lines 70–76. The existing persisted flood gate only
covered strand checks later in the script. The live board contained five
identical overlap refusals.

## Change

Added a persisted `autoland-overlap-refused-v1` signature and TTL gate to the
collision branch. The first refusal in the TTL posts the existing board
`[health-fail]` and exits 1. Repeated refusals still exit 1, but append a
timestamped suppression record to the configured trace (`land.log` by default).
State read/write is serialized with `flock`.

## Verification

- `bash tests/test-mesh-land-check-budget.sh` — PASS; repeated overlap emitted
  one board alert and a suppression trace record.
- `bash -n scripts/mesh-land` — PASS.
- `bash scripts/mesh-land --test` — PASS (`smoke-test: ok`).
- `git diff --check` — PASS.

Source files changed: `scripts/mesh-land`,
`tests/test-mesh-land-check-budget.sh`.
