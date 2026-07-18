# Crash-proof mind recovery — treat `/clear` as a crash

**Operator ask (2026-07-18):** "make sure we indeed treat `/clear` as a crash and easily
recover without losing work" — refined: **"no context death nor bloat it should be."** Scope
decision: **full crash-proof** — recovery must lose at most one cadence of work on ANY context
death: `/clear`, `/compact`, OOM, `kill -9`, engine death, **reboot**.

## The twin invariant: no death, no bloat

Context has two failure modes and they pull AGAINST each other:
- **death** — a `/clear`/crash loses the working thread (what we've been building).
- **bloat** — context grows until it degrades, the very thing `/clear` exists to relieve.

The cure for bloat is to clear aggressively (every idle edge, `mesh-mind-recycle`). The risk
of clearing aggressively is death. **So the crash-proof recovery below is not a side project —
it is the ENABLER that makes aggressive anti-bloat clearing safe.** Without durable recovery,
aggressive clearing loses work (why aggressive-clear was blocked — minds 7d ~84% + handoff-
capture); with it, the mind can clear at every idle edge and never lose the thread. Both halves
must hold at once:
1. **anti-death** — P1/P2 make any death recoverable (below).
2. **anti-bloat** — P3 (`mesh-mind-recycle`) clears at every busy→idle edge, gated by
   `mesh-clear`, so context never accumulates past a working set.
3. **the recovery artifacts must not themselves bloat** — the restored SessionStart context is
   a TERSE bounded handoff (a state summary, capped), never a raw scrollback dump; a wake that
   re-injects a wall of transcript just re-bloats the fresh context and defeats the recycle.
   `refs/wip/<win>` is a single moving ref (not an accumulating history); handoff files are
   overwrite-one-file, not append.

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
- **Bounded (anti-bloat):** the snapshot is a TERSE state summary with a hard size cap (a few
  lines: what-done / next / key paths+refs) — NEVER the raw scrollback. The restore re-injects
  it into a fresh session; a fat handoff re-bloats the context the recycle just relieved. Gate
  asserts the emitted `additionalContext` stays under the cap even from a huge scrollback.
- **RED-first gate:** scrollback with work-state + NO manual handoff → `--snapshot` writes a
  handoff drawn from the scrollback → `--restore` carries it. A fresher manual handoff is NOT
  overwritten. Coverage still fails on a deliberately-uncovering snapshot. Output stays under
  the size cap even when the scrollback is 100× it.

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
**No context death and no context bloat:** no death — graceful or violent — loses more than one
cadence of work, no recovery step depends on the dying mind cooperating first, AND the mind
clears at every idle edge so context never bloats — with the recovery bounded (terse handoff,
single WIP ref) so it never re-bloats what the clear relieved. Death and bloat are one problem;
recovery is what lets us clear aggressively without losing the thread.
