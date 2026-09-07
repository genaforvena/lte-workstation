# Context/handoff recovery — 2026-09-07

Ask: `ask:20260907T075841Z`

## Gap found

The board contained the owner-authored `[taking]` claim and a durable manual handoff, but
`~/.mesh/task-context/witness.json` was absent. The task was therefore visible in chat and
recoverable as prose, but not bound to the canonical task identity used by the lifecycle receipt.

## Repair

Created the one-step durable chain `hand-off-recovery` with the immutable ask key and exact owner
`witness`. Taking its step materializes the owner task context; the handoff remains in
`~/.mesh/handoff/witness.md`. The existing handoff writer and Codex lifecycle hooks are unchanged:
`mesh-clear` writes a snapshot before `/clear`, SessionStart restores charter + handoff, and
SessionEnd/drain persists the final receipt.

## Verification

- `mesh-task --test` PASS: canonical ask/task, exact owner, lease/progress, typed block/resume,
  artifact hash, and idempotent closure.
- `mesh-task audit` PASS: all 19 existing chain steps are artifact-backed DONE; no open chain step
  was silently lost.
- `scripts/mesh-handoff --test` PASS: manual round-trip, snapshot no-clobber/cap, clear coupling,
  charter/goal restore, and outage banner.
- `scripts/mesh-codex-lifecycle --test` PASS: durable result, handoff-before-clear, busy deferral,
  idempotent turn count, quiet reset.
- Source/deployed SHA-256 parity PASS for `mesh-task`, `mesh-handoff`, `mesh-codex-context`,
  `mesh-clear`, and `mesh-codex-lifecycle`; `.codex/hooks.json` has SessionStart and SessionEnd.

The repaired task identity and owner context are the durable receipt; the original ask remains
closed by the keyed board `[done] hand-off` line.
