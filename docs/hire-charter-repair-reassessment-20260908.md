# Charter-repair reassessment — 2026-09-08

- Task: `recreated-rejected-20260908-04-corrected/charter-repair`
- Owner: `hire`
- Reassessment: current and actionable; the earlier rejection is superseded by the current
  safe fixture in `docs/task-receipts/04-current-charter-fixture-20260908.md`.
- Timestamp: `2026-09-08T14:16:23Z`
- Repository revision: `ccc73714108fe68270f51a06d9155a923e546e98`
- `scripts/mesh-charter-watch` SHA-256:
  `627ddc66683468953efbc776b8d01550779affdf0284ace009ce159b2cd98763`

## Current state

The live `wake` charter and repository `charter/wake.md` are byte-identical:
`85356cccebbe5417418eb35c841bd750b24a4077a66db8f9e14fec927a78671e`.
The live `hire` charter and repository `charter/hire.md` are byte-identical:
`5e218b70bc4e557551c1e4d7625d309707b5a894820fdd92e0551fd1bd65c550`.
No node-local charter override was changed.

## Safe verification

Commands run:

```text
rtk bash scripts/mesh-charter-watch --test
rtk bash tests/test-mesh-charter-watch.sh
```

Both exited `0`. The fixture output verified:

```text
missing charter repaired
divergent charter preserved
unchanged divergence coalesced
changed divergence emitted
recovery emitted
run row written
PASS
test-mesh-charter-watch: PASS
```

The run also reported `staffing_rc=0`. This confirms the current charter-repair behavior while
preserving intentional local overrides; no live charter was overwritten.
