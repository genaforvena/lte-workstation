# Resource coordination skill amendment — 2026-09-16

## Scope

Owner step: `operator-resource-coordination-skill-20260916/amend-resource-coordination-skill`.

Updated the tracked skill at `.agents/skills/mesh-operator-followthrough/SKILL.md` with the
operator's resource rule: temporary node-local CPU, memory, GPU, VRAM, and resident Ollama
contention is queued/retried internally; mesh-home GPU work uses `mesh-heavy-run` plus the
bounded `mesh-gpu-lease`; only mesh-managed services may be paused and restored; unrelated
external processes and protected consumers are never stopped; failed acquisition restores
state and remains queued.

## Verification

- `python3 /home/mesh-home/.codex/skills/.system/skill-creator/scripts/quick_validate.py
  .agents/skills/mesh-operator-followthrough` → `Skill is valid!` (exit 0).
- The new rule is discoverable by direct read of the tracked skill and is scoped to
  node-local mesh-owned resources; it grants no authority over external processes or nodes.
- Existing single-writer, task ownership, delivery, and charter-boundary instructions remain
  intact; no other skill or substrate path was changed for this amendment.

## Delegation

`genome-resource-skill-audit` was launched for an independent read-only audit. Its report was
not used as evidence until personally inspectable; the validator output and file inspection
above are the proof for this amendment.

## Successor verification — `verify-resource-coordination-skill`

The successor row was dispatch-checked with exit 0 and taken by the exact owner
`MESH_TASK_ACTOR=genome`. Direct inspection found the resource rule discoverable in the tracked
skill and consistent with the existing single-writer boundary: `mesh-heavy-run` delegates GPU
release to the bounded `mesh-gpu-lease`, whose allowlist and restoration behavior are covered by
the focused test; no instruction grants control over unrelated external processes.

Verification run on 2026-09-16:

- `quick_validate.py .agents/skills/mesh-operator-followthrough` -> `Skill is valid!` (0)
- `python3 tests/test-mesh-handoff-workflows.py` -> both checks PASS (0)
- `python3 tests/test-mesh-tg-filter-ask-key.py` -> PASS (0)
- `scripts/mesh-gpu-lease --test` -> PASS (0)
- `scripts/mesh-heavy-run --test` -> smoke-test ok (0)
- `python3 tests/test-mesh-gpu-lease.py` -> PASS (0)
- `python3 -m pytest -q tests/test-mesh-gpu-lease.py` -> not run: pytest is not installed;
  the repository's direct test runner passed instead.

The delegated `resource-coordination-audit` worker was read-only and produced no inspectable
artifact before settlement; its report was not used as evidence. Personally inspected evidence is
this receipt, the skill, the resource scripts, and the test outputs above.
