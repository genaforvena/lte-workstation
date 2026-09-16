# pub tamper clock-skew vet — 2026-09-16

## Evidence inspected

- Source: `scripts/mesh-tamper`, lines 98–125. `EVENT_FUTURE_SKEW` defaults to 300 seconds;
  unusable future rows are excluded from latest-event selection and downstream aggregates.
- Fixture coverage in the source verifies +100 seconds is usable, +401 seconds is rejected, the
  latest valid row skips a corrupt future row, and recent counting excludes it.
- `rtk tests/test-mesh-tamper-test-real-read.sh`: PASS.
- `rtk bash -n scripts/mesh-tamper`: PASS.
- `scripts/mesh-tamper --test`: exit 2, `real sensor read hollow, no trustworthy hardware artifact`.
- The source and evidence document are uncommitted in this worktree; no commit is claimed.

## Disposition

The implementation claim is supported by deterministic fixtures and syntax verification. The
hardware path remains unmeasured on this node, so the draft says that explicitly and does not claim
a live tamper event or deployed reliability.

Delegation decision: no subagent was launched. This was a tightly coupled public-voice vet of one
artifact, and the charter keeps drafting, provenance judgment, and outward-facing wording in pub.

