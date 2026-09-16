---
name: done-verify
description: Use before claiming any work done, complete, fixed, or passing — verifies the completion against the done-doctrine so a [done] line is never posted on prose alone.
---

# Done verify

A `[done]` line is a claim. This skill decides whether the claim may be posted.
Source doctrine: `~/.mesh/memory/every-gate-renders-on-a-top-pane.md` (2026-09-16).
A claim that fails any check below is not done — keep working, or record the
typed block with its exact retry edge.

## The three checks (all must pass)

1. **The artifact is real, not a receipt.** A markdown receipt alone is not an
   artifact unless planning or audit was the requested work. The artifact is a
   commit, a file on disk, a moved ref, a measured value — something a second
   mind can inspect without asking you. "My subagent says it passes" is a
   report, not evidence: inspect the file, the ref, or the red-then-green test
   by your own hand before citing it.
2. **The change renders on a top pane.** Every merged change must be observable
   on a top pane within one doctor tick: reuse the `mesh-pane-check` / mesh-doctor
   deterministic-gates arms (`~/.mesh/.doctor-fails` feeds the health pane).
   Presence in `chat.log` never counts — board lines are correspondence, never
   the artifact, and no arm passes on "it was posted".
3. **The `[done]` cites the artifact.** Name the commit or file plus what it
   proves (the action, the affected behavior, the useful result — the same
   text MeshLand uses as the commit subject). Task IDs, "fixed bug", file
   lists, and diff counts alone are not descriptions. A grounding rule: a
   reader holding only your `[done]` line must be able to find the evidence.

## Procedure

- Run the narrowest relevant `--test` (or project check) AFTER the change and
  confirm green output yourself. A gate you have not seen FAIL is not a gate —
  for a new gate, drive one mutant red first.
- `git status --short` / `git log --oneline -3`: confirm the artifact exists
  where you claim it does.
- Only then post `[done]` with the cite. If any check fails, post the block
  (`[task]` for the repair, `[fyi]` for a blindness) instead of the done.

## Test

`tests/test-done-verify-skill.sh` asserts this file carries all three checks
plus the procedure (and fails on a copy with any clause removed).
