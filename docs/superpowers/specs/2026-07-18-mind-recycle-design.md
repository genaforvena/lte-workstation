# mesh-mind-recycle — clear-after-every-stop driver (fresh context per turn)

**Date:** 2026-07-18
**Status:** design (approved for planning) · **rev 2026-07-18** — measurement redesign (canary
meter primary, §Measuring) + Huntley/Ralph reconciliation (Stop-hook trigger, meter-before-trigger
sequencing, §Prior art). Operator-driven over TG.
**Owner:** genome
**Decision (2026-07-18):** do NOT adopt the ralph plugin wholesale (it accumulates context, is
bounded-project shaped); DO steal its Stop-hook trigger; keep our handoff+SessionStart-restore as
the freshness mechanism; **build `mesh-clear-loss` (canary meter) FIRST**, run a week in pure
shadow, let the number settle every-stop vs clear-at-done before shipping the driver.

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

## Prior art — Huntley's "Ralph", and why not just the plugin (operator 2026-07-18)

Geoffrey Huntley's **Ralph** is the same thesis, proven: a mind starts fresh each iteration and
carries work through **files**, not a growing window — "Ralph fixed context rot by restarting
Claude in a loop." Two things transfer, one does not:

- **The thesis is validated — we are not reinventing.** Ralph's load-bearing parts map onto ours:
  `fix_plan.md` / `AGENT.md` / `specs/*` ≙ our **`mesh-handoff` durable file + the doctrine files
  (CLAUDE.md) + the genome**. His key lesson is the sharpest correction to *our* framing:
  **reliability is not in the clear, it is in the QUALITY of the artifact re-read every cycle.**
  Ralph works because its files are good; a Ralph with a lossy `fix_plan.md` drifts. That is
  *exactly* what our canary meter measures — is the re-read handoff good enough to survive the
  clear — so the measurement section above is the empirical bridge to Ralph's one hard dependency,
  not a side quest.
- **STEAL the trigger: a Stop hook.** The official `ralph-wiggum` / `ralph-loop` plugins fire on a
  **Stop hook** (`hooks/stop-hook.sh`) that intercepts the mind's exit at end-of-turn. That is the
  native, reliable **busy→idle signal** — cleaner than this spec's original tmux pane-watch, and it
  **dissolves the hardest open reconciliation below** (self-induced-idle suppression): a Stop hook
  fires on a real end-of-turn by construction, so we no longer have to distinguish "the mind's own
  work stopped" from "the idle our `/clear` produced" by hashing panes. Our recycler becomes *a Stop
  hook that runs `mesh-clear --auto` (+ continuation)*, not an external watch loop.
- **Do NOT adopt the plugin wholesale — it does the opposite of what we need.** The plugin's Stop
  hook **blocks exit and re-feeds the SAME prompt into the SAME session — it never clears; context
  ACCUMULATES.** Ralph's freshness comes from Huntley's *outer* `while :; do … claude …; done`
  restarting the process entirely; the in-session plugin trades that away and **reintroduces the
  very context rot we are trying to kill.** It is also built for a **bounded single project driven
  to `DONE`** (`--completion-promise` exact-match + `--max-iterations`), not for **persistent,
  heterogeneous, conversational mesh minds** (many channels, no single DONE, operator conversation
  that must persist across messages). So: take the **Stop-hook trigger shape**, keep **our**
  `/clear`-to-handoff as the freshness mechanism (our SessionStart-restore *is* Ralph's "re-read the
  files each loop", and `/clear` is our per-turn equivalent of his process restart), and keep the
  measurement. Borrow one more idiom: an **explicit completion token** the mind may emit (Ralph's
  `<promise>DONE</promise>`) is a cheaper, more honest `done`-signal than inferring done from the
  scrollback — fold it into the continuation-extract as the first check.

## The model (corrected from an earlier %-triggered draft)

- **Trigger = every stop, delivered by a Stop hook.** The signal is the mind's end-of-turn Stop
  event (Ralph's mechanism, §Prior art), not a tmux pane-watch inferring a busy→idle edge. There is
  **no context-percentage gate** — not 75%, not any threshold. A stop is the trigger. (A pane-watch
  fallback stays specified for engines/edges the Stop hook can't cover, but the hook is primary.)
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
a guard, that idle edge re-triggers the watch → re-clear → forever.

**The Stop-hook trigger (§Prior art) largely dissolves this by construction:** a `/clear` to a
blank pane runs no turn, so it emits **no Stop event** — there is nothing to re-fire on. A
continuation inject *does* drive a real turn whose Stop is correctly judged next (that is the mind
doing the continued work). The guards below therefore matter most for the **pane-watch fallback**
and as defense-in-depth; under the hook, guard 1 is nearly free. Three interlocking guards:

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

0. **`scripts/mesh-clear-loss`** — the MEASUREMENT instrument (ships FIRST; needs no recycler).
   Canary meter (primary, judge-free) + round-trip probe (secondary). `--canary [--task-type T]`
   runs both arms and appends the binary result; `--probe <win>` runs the shadow round-trip;
   `--report` prints `cost(window, task-type) = recycled − control`; `--test` drives the pure
   scoring core + a KNOWN-DROPPED calibration fixture RED-first. Ledger `~/.mesh/clear-loss.log`.
   This is the tool the operator's plan builds and runs for a week *before* the driver's trigger
   is finalized (§Sequencing).
1. **`scripts/mesh-mind-recycle`** — the driver (built AFTER the meter settles the trigger).
   - **Trigger = a Stop hook** (Ralph's mechanism, §Prior art): the recycler's decision runs on the
     mind's end-of-turn Stop event, invoked from the hook — not an external tmux watch loop. A
     `mesh-mind-recycle --pane-watch` fallback loop stays specified for edges the hook can't cover.
   - `mesh-mind-recycle --once <win>` — run the decision for one window a single time (the unit the hook/loop calls; manual/debug lever).
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

## Measuring the cost — canary tasks (primary) + round-trip probe (continuous)

**Shadow mode as first drafted LIES, and this section is the fix (operator 2026-07-18).** The
draft's shadow mode "runs the full decision and logs `would clear — covered`" — but the coverage
gate is *near-tautological* (the handoff is extracted FROM the scrollback, so it almost always
says YES). Logging "covered" therefore measures **~zero** about whether the clear actually
**loses** anything. Shadow mode as spec'd validates the plumbing, not the policy. The real
question — *is clearing lossy, and where* — is a **serialization round-trip** question, and a
round trip can be measured in pure shadow, **without ever clearing a live mind**. Two instruments,
one primary:

### Canary tasks — the PRIMARY meter (judge-free, reality-routed)

Seed a task whose correct completion **requires carrying a mid-turn discovery across the clear
boundary**: plant a constraint the mind can learn **only by doing step 1**, not restated in step
2's prompt and not present in any static doc. Then check, post-boundary, whether the output
**violates** it.

- **Known ground truth, binary outcome.** The constraint is C; `verify(step2_output) → pass|fail`
  is a real predicate encoding C — *reality grades it*, not a coverage classifier grading its own
  extraction. **No judge model anywhere in the scoring path** — this is what makes the canary
  strictly stronger than the probe below, and it dissolves the "a lenient judge fakes near-zero"
  trap (the same trap the coverage gate itself is).
- **Two arms, always both** (the control is mandatory — operator):
  - **recycled arm:** run step 1 → extract the handoff exactly as the recycler would
    (`mesh-clear`'s `_extract_handoff`, verbatim) → **discard step-1 context, restore handoff
    only** → run step 2 → `verify`.
  - **control arm:** identical, **no clear** between step 1 and step 2 (full context retained).
- **The number.** `cost(window, task-type) = failrate_recycled − failrate_control`. The control
  subtracts the baseline a mind flunks *without* any clear (ambiguous task, just-forgot); the
  **difference** is the loss *attributable to the clear*, denominated in **dropped directives** —
  the exact failure class the operator's log audit found by hand (the "/cleared mid-task, lost the
  thread" family in CLAUDE.md). Same reasoner on both arms controls for model capability, so the
  differential is meaningful even when the absolute rate is not.
- **Tacit-discovery axis.** The valuable canaries are those where C is **tacit** — a mind would
  not naturally write it into a handoff. A canary whose C is trivially handoff-able only tests the
  handoff *plumbing* (and whether the mind reflexively captures its own discovery before clearing —
  itself part of the loop); a tacit C measures the true policy cost. Carry a **spread** across this
  axis so the meter reports both the plumbing floor and the tacit ceiling.
- **Sampled, sandboxed.** Canaries dispatch real work with a binary check and **no live side
  effects**; they are *sampled* (periodic), not run every stop. The reasoner is pluggable
  (`MESH_CANARY_MIND_CMD`, default a local scratch context) — a stand-in isolates the
  handoff-serialization loss and runs today; a v2 can route arms to real mind panes for absolute
  fidelity. State the stand-in limit plainly: the differential is the honest number, the absolute
  rate is reasoner-dependent.

### Round-trip probe — the CONTINUOUS secondary signal

Cheap, per-stop, self-reported divergence — the always-on complement to the sampled canary. At a
stop: extract the handoff, spin a **scratch** context restored from it, and put the same K probe
questions to a reference and the scratch — *what are you working on, what's blocked, **what
constraint did you learn this session that isn't written anywhere**, what would you do next.* Diff
the answers; the divergence is the per-clear loss estimate, per window, per task type, gathered for
a week while **nothing is cleared**. The third probe is the killer — it targets exactly what a
handoff structurally cannot hold.

Two guards so the probe does not itself start lying:
- **The diff is a judge model → it can lie soft** (score everything "same" → fake near-zero). It
  needs its own calibration: feed a **known-dropped** fact (present in the reference, absent from
  the handoff) and confirm the diff **flags** the divergence. A gate you have not seen FAIL is not
  a gate — the canary above is the judge-free cross-check that keeps the probe honest.
- **Never touch the live mind.** Probing the live pane adds turns → pollutes the very state being
  measured. Use **two scratch contexts** — one restored from the full scrollback (reference), one
  from the handoff — so the live mind is untouched and the run stays pure shadow.

### Sequencing — meter FIRST, trigger FROM the data

This inverts the draft's order and is the load-bearing consequence: **build the measurement as a
standalone instrument (`mesh-clear-loss`), which needs no recycler at all** — run its canaries with
a manual mid-task clear today. Gather a week of numbers, per window, per task type. The operator's
prediction — **near-zero loss at `done` stops, real loss at mid-task stops** — is then *settled
empirically*, and the driver's trigger (every-stop vs. clear-at-done vs. a task-type-conditioned
policy) **falls out of the number** rather than out of doctrine aesthetics. Only after the meter
speaks do we finalize §"The model"'s trigger and ship the driver.

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

- **Self-induced idle suppression** (guard 1) — **downgraded from load-bearing to defense-in-depth
  by the Stop-hook trigger (§Prior art).** Under the hook a blank post-`/clear` pane runs no turn →
  emits no Stop event, so there is no self-induced re-fire to suppress. It stays a real concern only
  for the **pane-watch fallback**, where the original mechanism still applies (marker written the
  instant `/clear` is sent; the next transition within the cooldown, or matching the post-clear
  content hash, is ignored).
- **Two model calls per stop** (coverage via mesh-clear + continuation) fire on **every** stop of
  every claude mind — more local inference than any existing reflex. They are local (GPU) and
  fire only on real stops, not per poll. The plan may fold coverage+continuation into one
  structured call to halve it; default is reuse-mesh-clear (DRY) and surface the call count in
  `--status` so cost can't creep unseen.
- **Conversational minds** (tg/tg-roz) may lose cross-message flow under clear-every-stop; shadow
  mode is the decision point on whether they stay in scope or get excluded.
