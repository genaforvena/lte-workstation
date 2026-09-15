# Current charter fixture — charter-repair reassessment

- Task: `hire-ledger-correction-prereqs-20260908/04-current-charter-fixture`
- Scope: safe verification fixture for charter repair; intentional local overrides remain untouched.
- Code revision inspected: `a626f4228e0b24b6cb0129ff412545a98dedfeef`
- Source charter: `charter/wake.md`
- Live charter: `/home/mesh-home/.mesh/charter/wake.md`
- Source/live SHA-256: `85356cccebbe5417418eb35c841bd750b24a4077a66db8f9e14fec927a78671e`

## Current state

The live `wake` charter is present and byte-identical to the repository charter. The current
charter still declares the finnegans-fake distillation lane, the `wake)` data pane, and the
required `[fyi]`, `[done]`, and `[idle]` board obligations. No local override was changed.

## Safe fixture

The existing `scripts/mesh-charter-watch --test` fixture was rerun against the current code.
It exercises all relevant reassessment paths:

- missing charter is repaired from the repository;
- divergent local charter is preserved;
- unchanged divergence is coalesced;
- changed divergence emits a new finding;
- recovery emits a finding; and
- every run writes an evidence row.

Evidence:

```text
attention mesh-charter-watch: blocked=1 repaired=0 staffing_rc=0
missing charter repaired
divergent charter preserved
unchanged divergence coalesced
changed divergence emitted
recovery emitted
run row written
PASS
test-mesh-charter-watch: PASS
```

Commands:

```text
rtk bash scripts/mesh-charter-watch --test
rtk bash tests/test-mesh-charter-watch.sh
```

Both exited `0`. This is a safe fixture for the charter-repair reassessment; it does not justify
overwriting a current intentional local divergence.
