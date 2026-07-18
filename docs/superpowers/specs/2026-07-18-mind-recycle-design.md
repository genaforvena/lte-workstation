# mesh-mind-recycle — clear-after-every-stop driver (fresh context per turn)

**Date:** 2026-07-18
**Status:** design (approved for planning)
**Owner:** genome

## Problem

Minds accumulate context across turns until someone clears them by hand. The operator wants
the opposite discipline: **a mind starts every turn fresh.** After each stop (the agent
finishes a turn and lands idle), the mind is cleared — carrying its work forward not through a
long context window but through the durable handoff (restored by the SessionStart hook) plus,
when work remains, an injected continuation prompt. The mind never grows a big window; it
re-derives from a small, current handoff each turn.

`mesh-clear` already exists as the *safe* `/clear` (a fail-safe tiny-model gate that refuses to
clear when the thread would be lost). It is **on-demand** — a mind must choose to run it.
Nothing watches minds and clears them after each stop. This tool is that autonomous **driver**;
it never weakens the gate.

## The model (corrected from an earlier %-triggered draft)

- **Trigger = every stop.** The watch fires on each busy→idle edge of a mind pane. There is
  **no context-percentage gate** — not 75%, not any threshold. A stop is the trigger.
- **Always clear, safety-gated only.** Every real stop attempts a clear. The *only* thing that
  prevents one is `mesh-clear`'s safety gate (the handoff doesn't cover the work / extraction
  failed / model down) → **BLOCK + alert, leave the mind**. There is no "leave it alone because
  it's small" outcome.
- **Branch = the resume nudge, not whether to clear.** Both branches clear:
  - **done, nothing left** → `/clear`, mind wakes blank (its handoff restored for context).
  - **unfinished work** → `/clear` **and** inject a continuation prompt so it resumes.

```
busy→idle edge on <win>   (a REAL stop — not the idle our own /clear produced; see Loop-prevention)
  │
  ├─ (A) continuation-extract   [tiny-model over scrollback, BEFORE clear] → { done | next:"<grounded>" | unsure }
  │
  ├─ (B) mesh-clear <win> --auto  [reused wholesale: extract VERBATIM handoff → coverage gate → /clear]
  │        · covered      → /clear happens
  │        · not covered / UNSURE / model-down / extraction-empty → BLOCK: post one [recycle] line, leave mind
  │
  └─ (C) if cleared:
           ├─ continuation = next:X  → mesh-tell <win> "continue: X"
           ├─ continuation = done    → inject nothing (wake blank)
           └─ continuation = unsure  → inject nothing (restored handoff lets the mind self-orient)
```

In **shadow mode** (`MESH_RECYCLE_LIVE=0`, the ship default) step B is `mesh-clear --auto
--dry-run` and step C is a log line — no `/clear`, no inject reaches the pane.

## Why "always clear" is safe here

The auto-extracted handoff is derived FROM the scrollback, so the coverage gate is *near-
tautological* — it will almost always say YES. That is fine: its real remaining job in this
path is to **catch a failed/empty extraction** (empty handoff → coverage NO/UNSURE → BLOCK),
so a mind whose work couldn't be captured is never cleared. The thread is carried by the
restored handoff + continuation regardless; the gate is the floor that stops a clear when even
the handoff would be lossy. This is a weaker guarantee than mesh-clear gives a *mind-written*
handoff, and the spec says so plainly — shadow mode is where we watch it hold.

## The doctrine collision, resolved (unchanged from the first draft — still load-bearing)

The operator chose "let the model extract the next-step," which appears to violate `mesh-clear`
constraint (c): *the auto-handoff must not invent a next-step* (the 974d864 / 09f7914 "never
fabricate the durable artifact" family). Reconciled by splitting into two artifacts of
different durability:

| Artifact | Durability | Next-step source | Rule |
|---|---|---|---|
| **Handoff** (`~/.mesh/handoff/<win>.md`, restored into the cleared session) | durable | **none** — strictly extractive/verbatim (mesh-clear's `_extract_handoff`) | doctrine (c) intact |
| **Continuation prompt** (`mesh-tell`, ephemeral, read once against the restored handoff, recoverable) | ephemeral | model-extracted, grounded; **`unsure → no inject`** | mind course-corrects against its restored handoff |

The model produces the *resume nudge*, never the *durable record*.

## Loop-prevention (now first-class, because "always clear" creates the loop)

A done mind cleared to blank sits idle. The `/clear` itself drives the pane busy→idle. Without
a guard, that idle edge re-triggers the watch → re-clear → forever. Three interlocking guards:

1. **Real-stop only.** Arm on a genuine busy→idle *transition* that follows *the mind's own
   work*, never on a pane already idle at loop startup, and never on the idle produced by our
   own `/clear` (the recycler knows it just sent one; it suppresses the next N seconds /
   the next transition it caused).
2. **Content-hash gate (à la `mesh-pane-watch`).** Record a hash of the mind pane at the last
   action. Skip if the current idle-state content has not meaningfully changed since — a mind
   sitting blank after a clear has the same (near-empty) content, so it is judged **once** and
   left until real work changes the pane.
3. **Per-window cooldown** (`MESH_RECYCLE_COOLDOWN_SECS`, default 60) as a backstop against any
   rapid re-fire the first two miss.

A mind dispatched real work changes the pane substantially → new hash → next stop is judged.
A mind that stays blank is never re-cleared. This trio is the piece the plan must nail; it is
tested (see Testing), not left to hope.

## Fail-safety

- **Clear stays gated.** Only a covered `mesh-clear` pass clears. `NO | UNSURE | model-down |
  empty-extraction` → block + alert. Auto-clear inherits mesh-clear's irreversibility rule.
- **Two fail-safes, one per direction of risk:** irreversible (`/clear`) — coverage not-YES →
  block; recoverable (inject) — continuation `unsure` → no inject.
- **Model-down = no-op**, never a false green: no ollama / timeout / unparse → block + no inject.

## Scope & rollout (operator-chosen)

- **All claude minds.** `MESH_RECYCLE_WINDOWS` default = every window with a **fresh**
  `~/.mesh/ctx/<win>` breadcrumb (the self-adjusting "this is a claude mind" detector — the
  breadcrumb's *presence*, not its pct; today: minds genome models health discover room chat
  tg-roz tg pub vpn). Conversational minds (`tg`, `tg-roz`) are **included** per operator choice.
- **Conversational-mind risk, stated:** clearing `tg`/`tg-roz` after every stop can drop
  conversational flow the operator expects to persist across messages. The coverage gate may
  block a thin conversational extraction, but shadow mode is the real safeguard — this is
  exactly what we watch before flipping live.
- **Shadow mode first** (`MESH_RECYCLE_LIVE=0`, ship default). Full decision runs; it logs
  `[recycle] <win>: would clear (+continue "<next>") — covered` and sends **no** `/clear`, **no**
  inject. Watch it judge real minds ~a day (especially tg/tg-roz), then flip `=1`. Verification
  principle: see the gate act correctly before trusting it with the irreversible step.
  (Note: `mesh-clear --auto --dry-run` still *writes* the durable handoff — harmless, non-
  destructive state — but never sends `/clear`. Shadow suppresses the irreversible act, not the
  save.)
- **Opencode minds skipped** (no breadcrumb → not a claude mind → honest no-op).
- **Card-gated & supervised** like every mind-touching reflex; skips a node declaring no `minds:`.

## Configuration (env)

| Var | Default | Meaning |
|---|---|---|
| `MESH_RECYCLE_LIVE` | `0` | `0` = shadow (log only); `1` = real `/clear` + inject |
| `MESH_RECYCLE_WINDOWS` | *(fresh-breadcrumb claude windows)* | which windows to watch |
| `MESH_RECYCLE_COOLDOWN_SECS` | `60` | min seconds between actions on one window (loop backstop) |
| `MESH_RECYCLE_CTX_FRESH_SECS` | `600` | breadcrumb older than this → mind gone → skip window |
| (inherits) | | `MESH_CLEAR_*` (model, timeouts, freshness budget) via the mesh-clear calls |

There is intentionally **no** `MESH_RECYCLE_FULL_PCT` — fullness is not part of the trigger.

## Components

1. **`scripts/mesh-mind-recycle`** — the driver.
   - `mesh-mind-recycle` — start/ensure the per-window idle-edge watch loops (idempotent, supervised entrypoint).
   - `mesh-mind-recycle --once <win>` — run the decision for one window a single time (the unit the loop calls; manual/debug lever).
   - `mesh-mind-recycle --status` — per-window: idle?, last verdict, last action age, live/shadow, model-call count.
   - `mesh-mind-recycle --test` — RED-first gate over the pure decision core, the loop-prevention guard, and the artifact split.
2. **`_recycle_decision`** — pure function, no tmux/model: given
   `(is_real_stop, changed_since_last, cooldown_ok, clear_verdict, continuation)` →
   `SKIP:not-a-stop | SKIP:unchanged | SKIP:cooldown | BLOCK:not-covered | CLEAR:no-inject | CLEAR:inject`.
   Every branch driven RED-first by `--test`.
3. **Reuse, don't fork.** Handoff extraction + coverage gate are `mesh-clear`'s existing
   `_extract_handoff` / `_classify_coverage`, invoked via `mesh-clear --auto[ --dry-run]`. One
   coverage model, one extractive path — no second copy to rot. Only the continuation-extract
   call + the inject are new here.

## Testing (verification principle)

- **Pure core, RED-first:** every `_recycle_decision` branch, each watched to FAIL when broken —
  including `SKIP:unchanged` (loop-prevention: a blank post-clear pane must NOT re-clear),
  `BLOCK:not-covered` on coverage=UNSURE (fail-safe), `CLEAR:inject` on continuation=next,
  `CLEAR:no-inject` on done, and **`unsure → no-inject`** (never a fabricated task).
- **Loop-prevention is a gate, not a hope:** a fixture where the pane content is unchanged since
  the last action must yield `SKIP:unchanged`; break the hash-compare and watch the test go red
  (it would re-clear forever). A same-window action inside the cooldown yields `SKIP:cooldown`.
- **Artifact split asserted:** drive the auto path; assert the **durable handoff has NO model-
  invented next-step** (extractive bullets only) while the **continuation** carries the model's
  next-step — doctrine (c) boundary is a watchable gate.
- **Shadow ≠ live:** `MESH_RECYCLE_LIVE=0` `--once` on a covered fixture emits `would clear` and
  sends **no** tmux keys (assert no `/clear` reached the pane); `=1` on the same fixture sends
  `/clear`. A shadow that silently clears is what this asserts against.
- **Model-down degrades safe:** ollama absent → block + no inject, no mind touched.
- **Honest n/a:** exit 2 on a node with no session / no minds card — reachable-but-absent is not
  a false green.

## Open reconciliations (call out, don't silently resolve)

- **Self-induced idle suppression** (guard 1) is the subtle one: the recycler must reliably tell
  its own `/clear`'s busy→idle from a real turn's. The plan pins the mechanism (marker written
  the instant `/clear` is sent; the next transition within the cooldown, or matching the post-
  clear content hash, is ignored).
- **Two model calls per stop** (coverage via mesh-clear + continuation) fire on **every** stop of
  every claude mind — more local inference than any existing reflex. They are local (GPU) and
  fire only on real stops, not per poll. The plan may fold coverage+continuation into one
  structured call to halve it; default is reuse-mesh-clear (DRY) and surface the call count in
  `--status` so cost can't creep unseen.
- **Conversational minds** (tg/tg-roz) may lose cross-message flow under clear-every-stop; shadow
  mode is the decision point on whether they stay in scope or get excluded.
