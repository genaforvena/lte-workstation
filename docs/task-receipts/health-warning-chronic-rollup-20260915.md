# Health-warning chronic roll-up admission — 2026-09-15

- Task: `health-warning/86e2172e37803c554a2f/triage`
- Board source: `2026-09-15T12:40:05Z witness@mesh-home`
- Scope: prevent changing chronic-suppression measurements from creating fresh urgent triage chains.

## Change

`scripts/mesh-health-warning-task` now recognizes a `[health-fail]` chronic-suppression
roll-up and fingerprints it as `chronic:<subject>:<signature>`. Volatile `gap`, `win`,
`measured n`, `suppressed`, and last-text fields are excluded from identity. The key is
outside the `error:` namespace, so it follows ordinary trace-tier admission/backpressure
instead of the urgent error sweep.

## Verification

- `python3 tests/test-mesh-health-warning-task.py` — PASS; two changing roll-up snapshots
  produced one `create` call.
- `python3 scripts/mesh-health-warning-task --test` — PASS.
- Live board/ledger inspection confirmed the source report and the exact parent chain were
  still open/sent before implementation; no mesh substrate mutation was performed.
