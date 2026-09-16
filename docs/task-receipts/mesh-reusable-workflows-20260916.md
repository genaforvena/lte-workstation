# Reusable mesh workflows adoption receipt — 2026-09-16

## Result

Adopted three bounded, reusable repository workflow skills for window turns,
operator follow-through, and stalled-task recovery. The skills are discoverable
from every restored charter through `scripts/mesh-handoff`; they do not add
scheduled mind turns and preserve event-only `tg`/`tg-roz` behavior.

## Evidence

- Evidence-ranked design and selection are recorded in
  `docs/task-plans/mesh-reusable-workflows-20260916.md`.
- `tests/test-mesh-handoff-workflows.py` passes, proving every charter restores
  all three skill pointers, node-local charter text retains precedence, and a
  missing genome reports `workflow UNAVAILABLE`.
- A live `bash scripts/mesh-handoff --restore` pass also found all three
  workflow pointers and the living-procedure guidance.
- The parent source receipts were independently rehashed and found on
  `origin/main`: health
  `71b00bb290268771987603966c38333d8b66c2e833e1c7f7e364d2cbf3173136`, VPN
  `aed4aafdcd6c233d5ae841d1911d3b59d82dab6d40a486cde08699fc4ab23ac2`.

## Deployment boundary

These are repository instruction artifacts consumed by the restore hook, not
`~/.local/bin` executables. The verified deployment/wiring path is the
repository `.agents/skills/*/SKILL.md` tree referenced by
`MESH_WORKFLOW_SKILLS`; missing files are reported explicitly by restore.

## Scope note

No private chat content, routing, substrate, or external delivery was changed.
