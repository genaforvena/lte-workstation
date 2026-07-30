# Live-literature review — information theory of agency: NOSTALGIA (nonpredictive retained memory) is dissipative — the thermodynamics-of-prediction lens on how DEEP a sense's memory should go

Date: 2026-07-28 · lane: genome (idea-queue LITERATURE task — information theory of agency / empowerment /
predictive information, cross-domain transfer to a distributed sensor mesh) · status: fix in tree,
uncommitted (steward lands)

## Where we had already been (checked before landing, so this doesn't double-count)

Information theory of agency is a heavily-worked mesh seam. The embodied set, confirmed before landing:

- **empowerment — action→future-sensor-state mutual information** (channel capacity of the sensor-actuator
  loop) → `scripts/mesh-algedonic` AGENCY_INFO sidecar.
- **instrumental / multi-agent empowerment** (through other minds; interference channel) →
  `scripts/mesh-mind-control:155`, `:1324`.
- **Maximum Occupancy Principle** (occupy future action-path space) → `scripts/mesh-vitality`.
- **predictive information / excess entropy — PI₁ = -½log₂(1-ρ₁²)** as a STRUCTURE-vs-NOISE discriminator
  the CV is blind to → `scripts/mesh-precision --num` `pred_info` (2026-07-28, same-day sibling).
- **transfer entropy** (directed lagged info flow) → `scripts/mesh-cooscillate`.
- **overwrite control vs hidden-state identification** (Csaky 2026) → review 2026-07-24.
- **assistive empowerment** (maximize the OPERATOR's option-space) → review 2026-07-28.
- **synergy vs redundancy / O-information** (leave-one-axis-out replay: does removing an axis flip the
  verdict?) → `scripts/mesh-algedonic --synergy`, `scripts/mesh-home-state` ∂ᵢΩ gradient. **This already
  embodies the operational core of Partial Information Decomposition** — so plain PID would double-count.

What every embodied piece takes as given: memory is FREE. Each measures *what* a stream predicts or *which*
axis is load-bearing — none asks whether the memory a reflex RETAINS pays its way, or is dead weight.

## The concept not yet embodied — NOSTALGIA (nonpredictive retained information = dissipation)

**Thermodynamics of prediction.** A system that keeps memory about its environment retains information
about the *past*; only the fraction of that memory which predicts the *future* is thermodynamically
useful. The remainder — information about the past that buys no prediction — Still et al. name
**"nostalgia"**, and prove it is not merely useless but *dissipative*: the **instantaneous nonpredictive
information is proportional to the work dissipated**, and lower-bounds total dissipation over a driving
protocol (augmenting Landauer). Their theorem: *any system built to keep memory about its environment and
operate at maximal energetic efficiency must be predictive* — it must minimize its nostalgia.

This is a genuine **cross-domain transfer** (non-equilibrium thermodynamics → agency/information), and it
is the one branch of the info-theory-of-agency literature the mesh had not touched: not *how much* a
stream predicts (excess entropy, which we landed today) but *whether the memory we retain about it is
predictive* — the asymmetry `I(memory; past)` vs `I(memory; future)`.

**Primary source** (found via live web review 2026-07-28, full read):

- **S. Still, D. A. Sivak, A. J. Bell, G. E. Crooks, "Thermodynamics of Prediction"**, *Physical Review
  Letters* **109**, 120604 (2012). doi:10.1103/PhysRevLett.109.120604 · arXiv:1203.3271.
  "The system's state retains information about past environmental fluctuations, and a fraction of this
  information is predictive of future ones. The remaining nonpredictive information reflects model
  complexity that does not improve predictive power … the fundamental equivalence between model
  inefficiency and thermodynamic inefficiency, measured by dissipation." (LIVE seam — the "minimize
  nostalgia" result is continuously extended, e.g. Still's *Information Bottleneck Approach to Predictive
  Inference*, Entropy 16(2):968, 2014, and the ongoing dissipative-adaptation line arXiv:2009.04006.)

Sources:
- [Thermodynamics of Prediction — PRL 109, 120604 (2012)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.109.120604)
- [arXiv:1203.3271 — The thermodynamics of prediction](https://arxiv.org/abs/1203.3271)
- [Still 2012, author PDF (threeplusone.com)](https://threeplusone.com/pubs/Still2012.pdf)
- [Information Bottleneck Approach to Predictive Inference — Entropy 16(2):968 (2014)](https://mdpi.com/1099-4300/16/2/968/htm)

## Why it applies to us — the gap the predictive-information axis left open

Today's PI landing on `mesh-precision --num` computes `pred_info` from the **lag-1** autocorrelation, and
its own honesty note flags the limit verbatim: *"PI₁ is a lag-1 (Gaussian) proxy … a signal whose only
structure is at long lag reads NOISE here."* That is not a cosmetic gap — it is exactly the case
thermodynamics-of-prediction speaks to. A **periodic / seasonal** sense (a diurnal light cycle sampled
fast, a room-occupancy rhythm, a grind-corpus beat) can have `ρ₁ ≈ 0` — consecutive samples uncorrelated,
`pred_info` reads **NOISE** — while being *perfectly* predictable from a deeper lag. A consumer that trusts
the lag-1 axis alone down-weights a living seasonal signal as noise; a consumer that keeps a long rolling
window on a genuinely lag-1 (Markov) signal pays storage/compute/staleness for **nostalgia** — retained
past that predicts nothing.

The un-embodied measure closes both: for a stream, scan lags `2..K`, take the best deeper predictive
information, and report how far it **exceeds** lag-1 (`mem_gain` bits) and at what depth (`pred_depth`).
`mem_gain ≈ 0` ⇒ lag-1 already captures it, a longer retained window is **nostalgia** (shrink it);
`mem_gain` large ⇒ **DEEP** memory that pays — retain to `pred_depth`, a lag-1-only view throws predictive
information away.

## What landed (report-only axis, advisory — touches NO verdict or weight)

`scripts/mesh-precision --num` output now also carries `mem_gain_bits`, `pred_depth`, and a
**SHORT | MODERATE | DEEP** `memory` label, keyed on `MESH_PREC_MG_HI`/`MESH_PREC_MG_LO` (defaults
0.5/0.15 bits), on the numeric non-frozen path (JSON field + text clause). Same report-only posture as the
CV / novelty / pred_info / independence / frame_coverage axes already on this file — it never overrides a
verdict or a fusion weight. It answers a distinct question from `pred_info`: not *is the variance
structure?* but *how DEEP must memory go before prediction saturates — and is anything we retain past that
depth dissipative nostalgia?*

**Verification (artifacts, not claims):**

- `mesh-precision --test` — GREEN. New RED-first assertions: a **period-4** tape `12,10,8,10,…` reads
  `pred_info:NOISE` (lag-1 predicts nothing, `-0.00b`) **yet** `memory:DEEP` `pred_depth:2` (`+0.86b`
  from lag-2) — the memory axis catches the exact deep structure the lag-1 PI axis is blind to. A
  monotone ramp `1..12` reads `memory:SHORT` (fully captured at lag-1; a longer window would be
  nostalgia). Broke it live — `MESH_PREC_MG_HI=99 mesh-precision --test` → **FAIL** (nothing can clear the
  DEEP bar → period-4 assertion goes red), then restored (default → `smoke-test: ok`).
- Live render (text + JSON) confirmed on the period-4 fixture and on a real hwmon thermal read
  (`memory:SHORT`, mem_gain 0 — a slow drift is Markov, no deep memory to retain).

## One-line honesty note

`mem_gain` uses the best **single** deeper lag (a biased-autocorrelation Gaussian proxy), not the full
multivariate excess entropy — it detects *whether some deeper lag carries predictability lag-1 misses*,
which is the operational nostalgia flag; it does not quantify total retained-vs-predictive information
exactly, and gates nothing until the steward validates against real sense tapes. It is a companion to
`pred_info`, not a replacement.
