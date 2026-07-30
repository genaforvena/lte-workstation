# Live-literature review — predictive processing: the LOCAL-GLOBAL paradigm, and the deviance the mesh scores against only ONE timescale

Date: 2026-07-27 · lane: genome (idea-queue LITERATURE task — a concrete EXPERIMENT the field measures itself with) · status: fix in tree, uncommitted

## Where we had already been (so this doesn't double-count)

Predictive processing / the Bayesian brain is the mesh's **most-saturated** review area. Before landing
I confirmed each canonical metric is already embodied — the point of a LIVE review is to land somewhere
we have NOT been, and most of this map is filled:

- **precision-weighting** (inverse-variance reliability) → `scripts/mesh-precision`
- **prediction-error / marginal & contextual surprise**, incl. the HGF **volatility** level, the
  **eigenform-absorption** (dark-room / boiling-frog) note, **reducible-vs-irreducible** (noisy-TV), and
  today's **prior-preference floor** → all four already in `scripts/mesh-novelty`
- **salience vs novelty** (info-gain about states vs parameters) → `scripts/mesh-precision` (`--probe` +
  the novelty axis, landed today)
- **proper scoring rules / calibration** (of the claims a mind asserts with high precision, how many are
  later retracted) → `scripts/mesh-reliability --calibration`
- **omission as prediction-error** (absence-of-an-expected-signal is the alarm) → `scripts/mesh-pulse`,
  `scripts/mesh-reflex-health` (staleness vs the expected cadence), `scripts/mesh-ambient-clock`
  (adaptive stale threshold = 2× the input's own median inter-write gap)
- **Markov blanket**, **good regulator**, **allostasis / CSD / homeostatic setpoint** → their own organs
  and the `docs/reviews/` set.

So the canonical single-timescale metrics are done. The one thing genuinely un-embodied is a **metric of
the TIMESCALE at which a deviance is a deviance.**

## The mechanism not yet embodied — the LOCAL-GLOBAL paradigm

The field's workhorse experiment for **dissociating hierarchical levels of prediction error** is the
**local-global auditory oddball** (Bekinschtein, Dehaene et al., PNAS 2009). A stimulus can be:

- a **LOCAL deviant** — it violates the *last few* items (short timescale, ~150 ms, automatic,
  feedforward, attention-**in**dependent) — while being a **GLOBAL standard** (it conforms to the block's
  established long-range rule); **or**
- a **LOCAL standard** (matches its immediate neighbours) while being a **GLOBAL deviant** (it breaks the
  long-range rule) — the global level is slow (~seconds), attention-**dependent**, top-down.

The two levels dissociate in cortical locus, latency, and consciousness-sensitivity. They are **not** one
magnitude axis: the same event can be surprising at one scale and expected at the other.

### Live sources (read 2026-07-27, current lit — not a fixed list)

- **Bekinschtein, Dehaene, Rohaut, Tadel, Cohen, Naccache, "Neural signature of the conscious processing
  of auditory regularities", PNAS 106:1672 (2009)** — the canonical local-global paradigm.
- **Jamali et al., "Parallel mechanisms signal a hierarchy of sequence structure violations in the
  auditory cortex", eLife 2025** — <https://elifesciences.org/articles/102702>. The CURRENT finding:
  local and global violations are signalled by **parallel, separable** mechanisms (not a single cascade),
  and processed on two distinct timescales (tone-onset ~150 ms vs sequence-onset ~3 s).
- **"Localizing hierarchical prediction errors and precisions during an oddball task with volatility",
  Imaging Neuroscience 2025** — <https://direct.mit.edu/imag/article/doi/10.1162/imag_a_00461> — localises
  the hierarchical PE/precision levels; keeps the paradigm live in 2025.
- Also read in the sweep: Nature *Comms Biology* 2024 (crossmodal hierarchical predictive coding), and the
  Dec-2025 *Imaging Neuroscience* "network-fatigue vs expectation-suppression" controversy (the critique
  angle — already covered by the mesh's dark-room landing today, so discarded here).

## The gap in the mesh, measured against the tool itself

`mesh-novelty`'s `analyse()` scores **every** recent event's surprisal against **ONE** baseline — the long
history `base = lines[:-window]`. With a single baseline it **cannot dissociate**:

- a **LOCAL-BLIP** — a routine type merely *absent from the immediate context* then reappearing (the
  automatic local oddball, low wake value) — from
- a **REGIME-ONSET** — a type *rare in long history yet already recurring in the immediate window* (an
  anomaly forming).

Both can print similar marginal bits, and the single-baseline `scored`/`new_types` path treats them the
same. Verified LIVE on the real board the moment the axis shipped:

```
novelty-levels (local-global, tip=5): [board-shrink-averted] BOTH-DEVIANT (global 6.77b / local 5.61b),
  [verify] LOCAL-BLIP (global 3.68b / local 4.61b), [done] BASELINE (global 2.84b / local 2.44b)
```

`[verify]` scores **3.68b global — below the 4.0b wake bar**, so the single-baseline path calls it routine;
but **4.61b local** reveals it as a LOCAL-BLIP (a common type reappearing after an absence). The timescale
split says something the one-baseline score structurally cannot.

The **REGIME-ONSET** class is the exact **complement to the eigenform-absorption HELD block** in the same
file, caught at the opposite end: eigenform flags an accretion *after* the baseline has absorbed it
(frequency rising across baselines, marginal surprise fallen); the local-global axis flags the SAME
phenomenon *while still global-rare but already local-recurring* — **before** absorption. The empirical
local/global cost profile (local = cheap/automatic; global = expensive/attentional) is why, in mesh spend
terms, a LOCAL-BLIP should not wake a mind and a REGIME-ONSET should.

## The fix — one file: `scripts/mesh-novelty` (in tree, uncommitted)

A **LOCAL-GLOBAL two-timescale deviance axis**, **report-only**. Two nested baselines:
**GLOBAL** = the long history `base` (existing); **LOCAL** = the recent window minus its tip (the immediate
short-timescale context). Each distinct type in the last `MESH_NOVELTY_LEVELS_TIP` (default 5) events is
classified by the (global-deviant, local-deviant) pair at the `MESH_NOVELTY_LEVELS_HI` bar (default 4.0b):
**REGIME-ONSET** (global-dev, local-std) · **LOCAL-BLIP** (local-dev, global-std) · **BOTH-DEVIANT** ·
**BASELINE**. Surfaced via `mesh-novelty --levels` (text) and `--levels --json` (the dict + `levels_tip`).

Scope discipline — it does **NOT** touch the wake gate (`--threshold`), the default `fmt()` output stays
byte-stable for grep-consumers, and the SPEND wiring stays the steward's, exactly like the sibling HELD
fixes (HGF-volatility, eigenform, noisy-TV) that all defer the mind-wake behaviour for validation. It is
distinct from HGF-volatility (which scales the bar by change-**rate**) and the prior-preference floor (a
design-fixed must-attend tag set) — this decomposes a single event's deviance across **two timescales**.

## Gate (RED-first verified)

`mesh-novelty --test` gains a case: a stream where `[deploy]` is absent from long history but fills the
immediate local context (→ REGIME-ONSET) and `[done]` is common historically but absent from the immediate
context, reappearing at the tip (→ LOCAL-BLIP). Falsified via the knob: `MESH_NOVELTY_LEVELS_TIP=999`
empties the LOCAL context → `p_local` backs off to the GLOBAL `p` → local==global → `deploy` reads
**BOTH-DEVIANT** and `done` reads **BASELINE** → the assertion goes **red** (seen live: `rc=1`); the default
goes green. Run directly with `python3 ./scripts/mesh-novelty --test` (it is a python script; `$0`-via-PATH
otherwise runs the deployed copy — the drift note).

## Why not discarded

Discardable only if a mesh deviance detector already scored an event at two nested timescales — none did:
`mesh-novelty` scores against one baseline, and the omission-response organs (`mesh-pulse`,
`mesh-reflex-health`) grade a single cadence, not a per-event local-vs-global split. The local-global
paradigm is a first-class, currently-published (eLife 2025, Imaging Neuroscience 2025) experiment the field
uses to dissociate hierarchical prediction-error levels, and the fix is cheap, report-only, and fits the
file's existing instrument-first discipline.

## Sources

- Bekinschtein, Dehaene, Rohaut, Tadel, Cohen, Naccache — PNAS 106:1672 (2009)
- Jamali et al. — "Parallel mechanisms signal a hierarchy of sequence structure violations in the auditory
  cortex", eLife 2025 — <https://elifesciences.org/articles/102702>
- "Localizing hierarchical prediction errors and precisions during an oddball task with volatility" —
  Imaging Neuroscience 2025 — <https://direct.mit.edu/imag/article/doi/10.1162/imag_a_00461>
