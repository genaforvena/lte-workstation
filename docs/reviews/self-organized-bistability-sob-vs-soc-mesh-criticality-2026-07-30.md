# Self-Organized Bistability (SOB) vs Self-Organized Criticality — a size-law modality the m̂ frame never tested

**Date:** 2026-07-30 · **Organ:** `scripts/mesh-criticality` · **Kind:** live literature review → read-only sidecar (landed, uncommitted)

## The foundational idea we applied too loosely

`mesh-criticality`'s entire frame is **SOC**: m̂ = branching ratio, regime = distance to a
**continuous** absorbing-state transition, m̂≈1 = "the healthy edge". That is only **one of two**
known self-organizing endpoints. A system with a slowly-varying / conserved control field can instead
self-organize to the **edge of bistability of a DISCONTINUOUS (first-order) transition** —
**Self-Organized Bistability (SOB)**.

The trap: **SOB also produces scale-invariant power-law avalanches**, so m̂≈1 and a clean power law do
**not** rule it out. What distinguishes them is the **avalanche-SIZE distribution**:

- **SOC** → **unimodal**, heavy-tailed / monotone-decreasing size law (one continuous power law).
- **SOB** → **bimodal**: a power-law **bulk** from the low-activity branch **coexisting** with a
  **separated, recurring bump** of anomalously large, **system-spanning "dragon-king" avalanches**
  from the high-activity branch — plus **hysteresis** between a quiet branch and a burst branch.

## Sources (real, web-searched 2026-07-30)

- Buendía, di Santo, Villegas, Burioni & Muñoz, **"Self-organized bistability and its possible
  relevance for brain dynamics"**, *Phys. Rev. Research* **2**, 013318 (2020), arXiv:1911.05382 —
  defines SOB as the counterpart of SOC "for systems tuning themselves to the edge of bistability of a
  discontinuous phase transition, rather than to the critical point of a continuous one"; bimodal
  avalanche size/duration distributions with dragon-king statistics.
- di Santo, Burioni, Vezzani & Muñoz, **"Self-Organized Bistability Associated with First-Order Phase
  Transitions"**, *Phys. Rev. Lett.* **116**, 240601 (2016), arXiv:1605.05161 — "the model displays a
  bimodal distribution of the avalanches of activity, with a power-law behavior … and a bump of very
  large avalanches due to the high-activity supercritical state" (the DK signature).
- **"Transition from self-organized criticality towards self-organized bistability"**, *Physica A*
  **665**, 130507 (2025) — the **live** continuation: as dissipation/drive varies, a *single* system
  **slides** from SOC (unimodal power law) to SOB (bimodal + DK bump). SOC↔SOB is an **axis the mesh
  can be anywhere along**, not an exotic corner.

## Why it bites here / the misread

The tool reads m̂≈1 as 1-D "distance to a continuous edge" and treats its large events through the
**dragon-king gate** as an **anomaly to alarm on**. But if the board is in an SOB regime, those large
events are **not** an anomaly — they are the **intrinsic signature of a bistable coordinator** (a
quiet-board branch and a burst-board branch it flips between with hysteresis), and "m̂≈1 = healthy
continuous edge" is a **category error**: the power law is the *shadow of bistability*, not a certified
critical point.

**None** of the existing sidecars catch this — each looks at a different object:

| sidecar | object | blind to |
|---|---|---|
| dragon-king gate | topology/identity concentration on a single aggregate m̂ (WHO redispatches) | the SHAPE of the size law |
| `--shape` | the *average* avalanche time-profile (within-avalanche) | the *across-avalanche* size DISTRIBUTION |
| `--crackling` | exponent coherence (assumes a unimodal law) | a second mode |
| `--widom` | the DRIVE (silence fraction φ) | modality of sizes |

The missing read is **bimodality of the avalanche-SIZE distribution**: a power-law bulk **plus** a
separated, **recurring** (≥2, not a lone outlier) upper-tail bump of system-spanning avalanches.

## What landed (`sob_regime()` + `--sob` + `SOB=` field + JSON `sob`)

Read-only; **never touches m̂/regime/alarm** (same restraint as CSD/Shape/Crackling/Widom/dynrange).

- Log-spaced histogram of avalanche sizes → 3-pt smoothed. Detect a **head mode → real trough
  (≤ `dip`·peak) → re-ascending upper bump** in the **upper (system-spanning) size range**, requiring
  **≥`min_dk` (default 2)** large events so a **lone dragon-king is NOT SOB** (that stays the existing
  single-DK gate's job).
- Labels: **BIMODAL-SOB** / **UNIMODAL-SOC** / **INSUFFICIENT** (n < min, or no size spread).
- Magnitudes (`dk_frac`, bulk→bump `gap×`, `modes`) reported; the "how big is a bump" thresholds are
  env-tunable, never a hardcoded *size* cutoff (constant-outlives-its-reader rule). Calibration of
  `dip`/`sep`/`upper`/`min_dk` against the live corpus is the natural next step.

## Verification

- **RED-first `--test`** (case in the smoke test): heavy-tailed monotone sizes → UNIMODAL-SOC;
  power-law bulk + separated recurring large-event cluster (wide gap) → BIMODAL-SOB; a **lone**
  outlier → UNIMODAL-SOC (not SOB); < n_min → INSUFFICIENT; no spread → INSUFFICIENT; plus a
  constant-label guard. Broke the discriminator (`lab` forced to UNIMODAL) → gate went **RED**;
  restored → **GREEN**.
- **Live** (board chat.log, this run): `SOB=UNIMODAL-SOC modes=1 dkfrac=0.06 gap×1.5` over 34
  avalanches — **no bistable bump today**; the near-critical reading is a genuine continuous-edge
  reading, not an SOB shadow. Honest negative — exactly what the discriminator is for.

## Discarded neighbours (one line each)

- Absorbing-state universality / Manna class (Dickman-Muñoz-Vespignani) — descriptive universality
  labelling, not an operational board read distinct from the existing exponent sidecars.
