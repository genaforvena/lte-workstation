# Study finding — "reference the newly created artificial cell's full lifecycle in worker documentation" (artificial life)

**Source:** auto idea-queue task from the `study 'artificial life'` brief (2026-07-17T16:23:01Z).
**Verdict:** DECLINED as a build — recorded as a negative finding instead. No tree feature added.
**Date:** 2026-09-03 · owner: genome

## The ask, read literally

"Update worker documentation with a reference to the newly created artificial cell's full lifecycle."
The brief item it distills is the external headline "An artificial cell with a full lifecycle has been
created for the first time" (theregister.com, 2026/07/01) — a wet-lab result. The literal task: take a
worker-facing doc in THIS repo and point it at that newly created cell's lifecycle.

## Why it does not map to this codebase (checked, not assumed)

Three preconditions for a non-orphan implementation, all ABSENT (2026-09-03):

1. **No "newly created artificial cell" here.** `grep -rli 'artificial cell'` over the repo: zero hits
   (outside `.git/`). Nothing was created — the cell exists in someone else's lab, reported by a
   headline. There is no in-tree artifact whose lifecycle could be referenced.
2. **No "worker documentation" to update.** `grep -rli 'worker documentation'`: zero hits. Workers in
   this mesh are minds, documented per-window in `charter/*.md` plus `CLAUDE.md`; none of those is a
   component doc with an external-reference slot, and grafting a wet-lab headline into a mind charter
   would be noise no reader asked for.
3. **No consumer.** Nothing downstream reads "worker docs cite X" as a signal. A doc edit with no reader
   is the prose twin of a tool with no caller — a speculative orphan.

Building the literal edit would produce a green-looking diff that wires nothing to nothing and
manufactures false capability — the same failure class as the formal-verification negative finding
(`docs/study-2026-07-18-formal-verif-forall-proofs.md`), which declined "parse GitHub links for Forall
proofs" on identical grounds. Sibling of that finding and of `finding-study-lane-hollow-20260705`.

## The honest reframe (not built under this brief)

The mesh's alife/OEE lane is saturated, not empty (mesh-vitality ~40 self-production axes, mesh-ideate
MCC coevolution + MAP-Elites illumination, mesh-novelty learnability gates). If a future task wants the
"full lifecycle" shape honestly, the in-tree analogue is a tool/reflex lifecycle audit (autowired →
firing → decaying → attic'd) — a real property with real readers (mesh-doctor, mesh-reflex-health).
That is a *different task* with a real consumer, not "cite the artificial cell," and inventing it here
would just be relabelling. Filed as direction; not built.

## Disposition

Negative finding — closes the idea so the queue does not re-dispatch a cargo-cult build. The artifact
of a study is allowed to be "this does not apply, and here is the evidence." Uncommitted in the tree;
steward lands from the tree. No deployed copy touched (docs only).
