# mesh-mind-recycle — idle→clear-or-resume driver

**Date:** 2026-07-18
**Status:** design (approved for planning)
**Owner:** genome

## Problem

A mind whose context window fills up must be `/clear`ed, but nothing does this
autonomously. Today the operator notices a full mind and clears it by hand, or a mind
sits idle-and-full doing nothing while its next turn silently costs more (bigger context =
slower, pricier, closer to the wall). The `mesh-clear` gate exists and is safe, but it is
*on-demand* — a mind must choose to run it. There is no reflex that watches minds and clears
them when they are both **idle** and **full**, and — crucially — nothing that lets a mind
with **unfinished work** clear and then *resume that work* instead of waking blank.

This tool is the autonomous **driver** around the existing `mesh-clear` gate: it decides
*when* to clear and *what to inject after*. It never weakens the gate.

## Non-goals

- **Not a replacement for `mesh-clear`.** The irreversible `/clear` still only fires through
  `mesh-clear`'s fail-safe coverage gate. This tool decides timing + continuation, nothing else.
- **Not a compactor.** `/compact` (context-preserving) is a different lever; this is `/clear`
  (context-dropping) driven by fullness, paired with handoff-restore + a resume nudge.
- **Not for opencode minds.** They emit no per-mind fullness breadcrumb (see Scope). Skipped honestly.

## Trigger — event-driven idle-edge watch

One long-lived `mesh-watch <win> --change` per in-scope claude mind, fired on the **idle
edge** (the mind pane lands on the `❯ ` prompt after being busy). This is the
`mesh-watch <win> --change --until '❯ $'` shape already in the toolbox.

- **One action per idle episode.** After acting (or deciding not to), the loop waits for the
  pane to leave idle (go busy) before re-arming. A mind that sits idle for an hour is judged
  **once**, not every poll — no re-fire storm.
- **Supervised + reboot-survivable** like the other liveness loops (`mesh-liveness-loop` /
  user systemd + linger). A dead recycler loop is itself a fault the existing pane/reflex
  watchdogs can surface; it is not a silent single point.
- **Card-gated.** Skips entirely on a node whose `~/.mesh-card` declares no `minds:` (the
  HANDS-OFF rule). A decommissioned node's panes are never even read.

## The decision (per idle edge)

```
idle edge on <win>
  │
  ├─ read ~/.mesh/ctx/<win>  →  pct  (and breadcrumb freshness)
  │     └─ no fresh breadcrumb  →  do nothing (not a claude mind / mind gone). Honest skip.
  │
  ├─ pct < FULL_THRESHOLD (default 75%)  →  do nothing. Not full = not our business.
  │
  └─ FULL:
       ├─ (1) auto-extract a VERBATIM handoff   [mesh-clear --auto extractive path]
       │        · concrete actions + file paths copied from scrollback
       │        · NO model-invented next-step  ← doctrine (c) preserved
       │
       ├─ (2) COVERAGE GATE  [existing tiny-model YES|NO|UNSURE, --think=false, fail-safe]
       │        · not-covered / UNSURE / model-down  →  BLOCK
       │             →  post one [recycle] line to the board, leave the mind untouched.
       │                Never auto-clear on doubt. (Same irreversibility rule as mesh-clear.)
       │
       └─ (3) COVERED  →  send /clear  (or, in shadow mode, LOG the would-clear — see Rollout)
                │
                └─ (4) CONTINUATION-EXTRACT  [separate tiny-model call over the same scrollback]
                        →  { done | next:"<grounded step>" | unsure }
                          ├─ done    →  inject nothing (mind wakes clean; handoff restored for context)
                          ├─ next:X  →  mesh-tell <win> "continue: X"
                          └─ unsure  →  inject nothing. The restored handoff lets the mind self-orient.
                                         Never inject a fabricated task.
```

### The doctrine collision, resolved

The operator chose "let the model extract the next-step." That appears to violate
`mesh-clear` constraint (c) — *the auto-handoff must not invent a next-step* (the
974d864 / 09f7914 "never fabricate the artifact" family: a hallucinated next-step in
**durable** state is worse than none). It is reconciled by splitting into **two artifacts of
different durability**:

| Artifact | Durability | Next-step source | Rule |
|---|---|---|---|
| **Handoff** (`~/.mesh/handoff/<win>.md`, restored into the cleared session by the SessionStart hook) | durable | **none** — strictly extractive/verbatim | doctrine (c) intact |
| **Continuation prompt** (`mesh-tell`, ephemeral, read once against the restored handoff, fully recoverable) | ephemeral | model-extracted, **grounded**; `unsure → no inject` | the mind course-corrects against its restored handoff |

So the model produces the *resume nudge*, never the *durable record*. Both the operator's
choice and the doctrine hold. `unsure → inject nothing` (never a fabricated task) is the
fail-safe on the *recoverable* side, mirroring `coverage UNSURE → block` on the *irreversible* side.

## Fail-safety

- **Clear stays gated.** The only path to `/clear` is coverage=YES over a fresh handoff.
  Everything else blocks + alerts. Auto-clear inherits `mesh-clear`'s exact irreversibility rule.
- **Two independent fail-safes, one per direction of risk:**
  - irreversible (`/clear`): coverage `NO|UNSURE|model-down` → **block**.
  - recoverable (inject): continuation `unsure` → **no inject**.
- **Model-down = no-op**, not a false green. No ollama / timeout / unparseable → both calls
  degrade to the blocking/no-inject side.

## Scope & rollout (operator-chosen)

- **All claude minds** (`MESH_RECYCLE_WINDOWS` default = every window with a **fresh**
  `~/.mesh/ctx/<win>` breadcrumb — the self-adjusting "which minds have a fullness signal"
  detector; today: minds genome models health discover room chat tg-roz tg pub vpn).
  Conversational minds (`tg`, `tg-roz`) are **included**, but the coverage gate is their guard:
  a mind idle mid-conversation with the operator is rarely "covered" by a handoff, so it blocks.
- **Shadow mode first** (`MESH_RECYCLE_LIVE=0`, the default at ship). The recycler runs the
  FULL decision and logs `[recycle] <win>: would clear+inject "<next>" (pct N, covered)` to the
  board — but sends **no** `/clear` and **no** inject. Watch it judge real minds (especially
  tg/tg-roz) for ~a day; flip `MESH_RECYCLE_LIVE=1` once its verdicts read right. This is the
  verification principle applied to an irreversible action: see the gate act correctly before
  trusting it with the irreversible step.
- **Opencode minds skipped** (no breadcrumb → no fullness signal → honest no-op).

## Configuration (env)

| Var | Default | Meaning |
|---|---|---|
| `MESH_RECYCLE_LIVE` | `0` | `0` = shadow (log verdicts only); `1` = send real `/clear` + inject |
| `MESH_RECYCLE_WINDOWS` | *(fresh-breadcrumb windows)* | which windows to watch |
| `MESH_RECYCLE_FULL_PCT` | `75` | pct at/above which an idle mind is "full" |
| `MESH_RECYCLE_CTX_FRESH_SECS` | `600` | a `~/.mesh/ctx/<win>` breadcrumb older than this = mind gone → skip |
| (inherits) | | `MESH_CLEAR_*` (model, timeout, freshness budget) via the `mesh-clear` calls |

## Components

1. **`scripts/mesh-mind-recycle`** — the driver. Subcommands:
   - `mesh-mind-recycle` — start/ensure the per-window watch loops (idempotent; the supervised entrypoint).
   - `mesh-mind-recycle --once <win>` — run the decision for one window a single time (the unit the loop calls; also the manual/debug lever).
   - `mesh-mind-recycle --status` — per-window: pct, idle?, last verdict, live/shadow.
   - `mesh-mind-recycle --test` — RED-first gate over the pure decision core + the artifact split (see Testing).
2. **`_recycle_decision`** — the pure function (no tmux/model): given
   `(have_fresh_ctx, pct, full_pct, coverage, continuation)` → one of
   `SKIP:no-ctx | SKIP:not-full | BLOCK:not-covered | CLEAR:no-inject | CLEAR:inject`.
   This is what `--test` drives through every branch, RED-first.
3. **Reuse, do not fork:** the handoff extraction + coverage gate are `mesh-clear`'s existing
   `_extract_handoff` / `_classify_coverage` (invoked via `mesh-clear --auto`), so there is one
   coverage model and one extractive path, not a second copy that rots.

## Testing (verification principle)

- **Pure core, RED-first** (`--test`): every `_recycle_decision` branch, and each gate watched
  to FAIL when broken — `SKIP:not-full` at 74% vs decide at 75%; `BLOCK:not-covered` on
  coverage=UNSURE (fail-safe); `CLEAR:no-inject` on continuation=done; `CLEAR:inject` on
  continuation=next; **`unsure → no-inject`** (never a fabricated task).
- **Artifact split asserted:** a test drives the auto-handoff path and asserts the **durable
  handoff contains NO model-invented next-step** (only extractive bullets), while the
  **continuation** carries the model's next-step — i.e. the doctrine-(c) boundary is a gate you
  can watch fail.
- **Shadow ≠ live is a gate:** with `MESH_RECYCLE_LIVE=0`, `--once` on a covered fixture emits
  the `would clear` log line and sends **no** tmux keys (assert no `/clear` reached the pane);
  with `=1` on the same fixture it sends `/clear`. A shadow that silently clears is the failure
  this asserts against.
- **Model-down degrades safe:** ollama absent → both calls degrade (block / no-inject), tool
  exits without touching any mind.
- Exit 2 (honest n/a) on a node with no session / no minds card — reachable-but-absent is not a
  false green.

## Open reconciliations (call out, don't silently resolve)

- **`--change` idle-edge vs a mind that never went busy.** The loop must arm only on a
  busy→idle *transition*, not on a mind already sitting idle at startup (else it judges a mind
  the instant the loop boots). First observation seeds state; only a real transition fires.
- **Cost of two model calls per full+idle event.** Coverage + continuation are two local
  (ollama, GPU) calls. They fire only on the rare idle+full edge, not per poll — acceptable,
  but `--status` should surface the call count so it can't creep.
