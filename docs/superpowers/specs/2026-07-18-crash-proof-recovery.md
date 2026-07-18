# Crash-proof mind recovery — treat `/clear` as a crash

**Operator ask (2026-07-18):** "make sure we indeed treat `/clear` as a crash and easily
recover without losing work." Scope decision: **full crash-proof** — recovery must lose at
most one cadence of work on ANY context death: `/clear`, `/compact`, OOM, `kill -9`, engine
death, **reboot**.

## Why the current machinery is not enough

The graceful path exists and is tested green:
- `mesh-handoff <win> "<state>"` → durable `~/.mesh/handoff/<win>.md` + one `[handoff]` board line.
- SessionStart hook (`startup|clear|compact`) → `mesh-handoff --restore` cats it back.
- `mesh-clear` fail-safe gate: refuses unless handoff is FRESH (<`MESH_CLEAR_FRESH_SECS`,
  900s) + coverage-confirmed (gemma4:e2b) + no `running|done-undelivered` bg-manifest job.
- `bg-manifest` (`mesh-bg-register`/`mesh-bg-done`) + `grind-durable-delivery`: background
  jobs deliver themselves from the DETACHED child, never from mind context.

**Two holes break the crash promise:**

1. **The gate is not enforced.** A bare `/clear` (mind- or operator-typed) skips `mesh-clear`
   entirely. `mesh-mind-recycle` (the driver that would route every idle-edge clear through
   the gate) is spec'd (`2026-07-18-mind-recycle-design.md`) but **not built**.

2. **Recovery depends on the mind writing a handoff FIRST — a real crash never does.** OOM /
   `kill -9` / engine death / reboot mid-work writes no handoff → `--restore` finds nothing →
   the mind wakes blind, uncommitted work lost. The whole design assumes a *graceful* exit.
   "Treat it as a crash" means: **do not depend on the pre-clear write.**

## The four prongs

### P1 — `mesh-wip-commit`: the only reboot-durable substrate  ·  owner genome
A reflex (cadence ~`*/5`) that, per active mind window with a **dirty** worktree, snapshots
uncommitted work into git so a reboot cannot lose it.
- **Non-invasive:** MUST NOT touch HEAD / current branch / index / staging. Use plumbing —
  `git stash create` stored at `refs/wip/<window>`, or a `commit-tree` on `refs/wip/<window>`.
  A mind's normal `git add`/`commit`/`mesh-land` flow must see an unchanged working tree.
- **Recoverable:** a documented verb (`mesh-wip-commit --restore <win>` / show) reconstructs
  the change; the wake context (P2 handoff) names the ref so the reincarnated mind knows to look.
- **RED-first gate:** dirty a tracked file → run reflex → assert `refs/wip/<win>` carries the
  change AND HEAD/branch/index are untouched. Clean worktree → NO ref update (no empty churn).
  Break each half, watch it go red, restore.

### P2 — `mesh-handoff --snapshot`: continuous, cooperation-free handoff  ·  owner genome
A mode that auto-derives a handoff from the window's pane scrollback (verbatim extract, like
`mesh-clear --auto` — **never invents a next-step**) + a one-line git-status/`refs/wip` summary,
refreshing `~/.mesh/handoff/<win>.md` on a cadence. A crash-not-reboot then has a ≤cadence-old
thread to restore.
- **Never clobber a FRESHER manual handoff** — a mind's explicit handoff is richer; snapshot
  only writes if it is newer than the last write, or writes an `auto:`-marked tier the restore
  merges under the manual one.
- **Interaction constraint (call out in the gate):** a continuously-fresh handoff makes
  `mesh-clear`'s FRESHNESS check always pass — so the COVERAGE gate (gemma4:e2b handoff-vs-
  scrollback) becomes the sole real barrier. Verify coverage still discriminates against an
  auto-snapshot (it asserts the handoff COVERS the scrollback; a shallow auto extract must
  still be able to FAIL coverage). If it can't, the snapshot has defeated the gate.
- **RED-first gate:** scrollback with work-state + NO manual handoff → `--snapshot` writes a
  handoff drawn from the scrollback → `--restore` carries it. A fresher manual handoff is NOT
  overwritten. Coverage still fails on a deliberately-uncovering snapshot.

### P3 — build `mesh-mind-recycle`: enforce the gate on every clear  ·  owner genome
Build the spec'd driver: clear on every busy→idle edge, gated by `mesh-clear`; loop-prevention
(real-stop-only + content-hash + cooldown, first-class + tested); shadow-first rollout. This
makes routing through the gate the norm so a bare `/clear` stops being the common path.
- **RED-first gate:** per the existing recycle spec — plus assert an idle edge with an UNSAFE
  gate (no/ stale/uncovered handoff, or a `running` bg job) does NOT clear.

### P4 — the live crash drill: verify, do not claim  ·  owner pub (this mind)
In a SHADOW/test window (never a live mind), actually kill a mind mid-work (`kill -9` the
engine) with a dirty worktree + unwritten manual handoff, then reincarnate and assert it
recovers its thread from P1+P2 artifacts alone. The artifact for "treat `/clear` as a crash"
is a real recovered session, not a green `--test`. Repeat per death mode (/clear, engine kill,
simulated reboot = fresh session + clean tmpfs handoff dir but intact `.git`).

## Order
P1 + P2 are independent (both genome) and can build in parallel; P3 depends on nothing new but
should land after P1/P2 so the enforced clears already benefit from continuous durability. P4
drills each prong as it lands, then the whole chain end-to-end.

## The one-line invariant
**No context death — graceful or violent — loses more than one cadence of work, and no
recovery step depends on the dying mind having cooperated first.**
