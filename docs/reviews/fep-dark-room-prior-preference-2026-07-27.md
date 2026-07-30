# Live-literature review — active inference CRITIQUE: the dark-room problem, and the wake-gate that goes blind to a chronic alarm

Date: 2026-07-27 · lane: genome (idea-queue LITERATURE task — critique/failure-mode angle) · status: fix in tree, uncommitted

## Where we had already been (so this doesn't double-count)

The mesh has landed the major FEP/active-inference **critiques** already:

- **Emperor's-New-Markov-Blankets** / Pearl-vs-Friston reification → `scripts/mesh-perimeter`
- **small-world / frame-problem** limit of relevance-realization → `scripts/mesh-precision`
  (Jaeger et al. 2024, Parvizi-Wayne 2025)
- **noisy-TV / curiosity-trap** (reducible vs irreducible surprise) → `scripts/mesh-novelty`
  (Schmidhuber; Mavor-Parker et al. 2022), reviewed 2026-06-21

The one canonical FEP failure mode still un-landed is its **most-cited**: the **dark-room problem**.

## The failure mode — the DARK ROOM

If a system minimises **surprise**, why not seek the most predictable environment possible — a dark,
silent, unchanging room — and stay there? A pure surprise-minimiser *prefers* predictable input, so it
goes **blind to a condition once that condition becomes predictable.**

`mesh-novelty` **is** a surprise-minimiser used as a spend gate: "wake expensive minds on HIGH novelty,
stay silent on routine." Its own `analyse()` header already documents the dark-room in local form — the
**boiling-frog / eigenform absorption** note: a persistent `[health-fail]`/`[incident]` recurs, accretes
into the baseline `base`, its `p(t)` rises, its surprisal `-log P` **falls**, and it **stops waking
minds** precisely because it is now chronic. That fix was left **HELD** because "a real regime change
looks identical to a pathological accretion at the signal level — separating them needs a reference the
loop does **not** author."

Measured live on this node's scratch fixture: a chronic `[health-fail]` (every other line) scores
**1.0 bits** of marginal surprise and is **not** a new type. A surprise-only gate (`--threshold 4`,
`mean_bits ≥ 6` for a routine spike) never fires on it. The alarm is real, ongoing, and invisible.

## The mechanism — PRIOR PREFERENCES (the FEP's own resolution)

The FEP answer to the dark room is that agents do **not** minimise raw surprise; they minimise surprise
relative to **preferred observations** — goal priors, the "C" vector — outcomes they act to obtain, and
to keep observing, **even when unsurprising.** Crucially those preferences are **design-specified, not
learned from the agent's own sensory history** — which is exactly the "reference the loop does not
author" the HELD note needed. Prior preferences therefore **unblock** the absorption failure for the
critical **subset** (a curated must-attend tag set), while the general regime-change-vs-accretion problem
stays correctly HELD.

### Live sources (read 2026-07-27, current lit — not a fixed list)

- **Karl Friston, Christopher Thornton, Andy Clark, "Free-energy minimization and the dark-room
  problem", Frontiers in Psychology 3:130 (2012)** —
  <https://www.frontiersin.org/articles/10.3389/fpsyg.2012.00130>. The canonical statement of the
  objection and the prior-preference resolution ("agents … come to expect, and actively seek, their
  preferred exchanges with the world").
- **Filippo Torresan, Ryota Kanai, Manuel Baltieri, "Prior preferences in active inference agents: soft,
  hard, and goal shaping", arXiv:2512.03293 (Dec 2025)** — the *current* treatment of **how** to specify
  these preferences: **hard (sharp) priors are brittle, soft/shaped priors are robust.** This is why the
  floor below re-asserts on a cadence (a shaped preference) rather than a hard always-fire.
- The mesh already accepts a must-attend floor on a different organ — the **"by-name poke must-answer"**
  rule on the room voice. Same principle; this extends it to the novelty spend-gate.

## The fix — one file: `scripts/mesh-novelty` (in tree, uncommitted)

A **PRIOR-PREFERENCE FLOOR**. A design-specified must-attend tag set
(`MESH_NOVELTY_PREF_TAGS`, default `incident health-fail gap`) is:

1. surfaced by `analyse()` as `pref_hits` **whatever its surprisal** (kept separate from
   `mean_bits`/`scored` — the surprise **measurement stays pure**, no silent inflation);
2. shown by `fmt()` **even on a "routine" window** — the header reads `routine · must-attend present`
   and lists the must-attend section;
3. fired into the `--threshold` wake gate **regardless of `mean_bits`**, deduped by **time**
   (re-assert every `MESH_NOVELTY_PREF_REFRESH`, default 1 h) — so a chronic critical condition is
   **never permanently absorbed** (the boiling-frog failure) **nor spammed** each cron cycle. This is a
   *shaped* preference, per Torresan et al. 2025, not a brittle hard always-fire.

Scope discipline: this touches **only** the design-specified subset. The general
regime-change-vs-accretion absorption problem in `analyse()` stays **HELD** — this does not claim to
solve it.

## Gate (RED-first verified)

`mesh-novelty --test` gains a case: a chronic `[health-fail]` stream is **absorbed** (asserted:
`hf_bits < 4.0` **and** not a new type — proving the dark-room failure is real) yet **still lands in
`pref_hits`**. Falsified via the knob: `MESH_NOVELTY_PREF_TAGS=""` empties the set →
`absorbed=True pref_hits=[]` → the assertion goes **red**; the default goes green. Live: `--threshold 4`
on the chronic fixture fires `must-attend [health-fail] … attended regardless of surprise` at
**1.0 b**, and an immediate re-run is silent (cadence dedup). `--edge`/`--test` unregressed.

## Why not discarded

Discardable only if a surprise-gated attention mechanism already had a must-attend floor it could not
absorb — it did not: `mesh-novelty`'s own header names the absorption failure as HELD for lack of a
non-self-authored reference, and prior preferences are exactly that reference. The mesh's other
continuous-threshold reflexes (`mesh-stress`, `mesh-algedonic`) are already soft/hysteretic/adaptive, so
the *hard-vs-soft prior* angle discards there; the **dark-room proper** had no home, and now does.

## Sources

- Friston, Thornton & Clark — Frontiers in Psychology 3:130 (2012) —
  <https://www.frontiersin.org/articles/10.3389/fpsyg.2012.00130>
- Torresan, Kanai & Baltieri — arXiv:2512.03293 (Dec 2025)
