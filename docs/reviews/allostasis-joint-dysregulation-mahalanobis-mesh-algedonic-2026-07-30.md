# Allostatic load as a MULTIVARIATE statistical distance (Mahalanobis Dᴹ), not a per-axis count

**Date:** 2026-07-30 · **Organ:** `scripts/mesh-algedonic` · **Kind:** live literature review → read-only sidecar (landed, uncommitted)

## The recent result (2023-2026) we did not embody

The classic allostatic-load index (McEwen & Seeman) — and `mesh-algedonic`'s `allostatic_load()` —
score cumulative burden by **counting** how many essential-variable axes sit past a threshold
(`high=N/n`) and averaging the NOISY-OR-fused scalar `pain`. Both **collapse the multi-axis vector to a
magnitude** and are therefore **blind to the correlation structure** between axes: a configuration where
every axis is individually in-range but the **joint combination** is one the system never occupies
(broken inter-axis coupling) scores **low** on a count, yet is exactly the early-dysregulation signature.

The field's fix — developed over a decade and, crucially, **cross-population validated in 2024** — is to
measure dysregulation as the **Mahalanobis distance Dᴹ** of the current vector from the joint
distribution of a healthy reference: a statistical distance that **accounts for the correlations among
variables**, so an *off-manifold* combination reads far even when each coordinate is normal.

## Sources (real, web-searched 2026-07-30)

- Cohen, Milot et al., **"A novel statistical approach shows evidence for multi-system physiological
  dysregulation during aging"**, *Mech. Ageing Dev.* (2013) — the original Dᴹ dysregulation index (a
  statistical distance accounting for correlations among biomarkers).
- Li, Milot et al., **"Physiological Dysregulation Proceeds and Predicts Health Outcomes Similarly in
  Chinese and Western Populations"**, *J. Gerontol. A Biol. Sci. Med. Sci.* **79**(1), glad146 (2024) —
  the **recent** cross-population validation: Dᴹ predicts outcomes similarly across very different
  populations, evidence the joint-distance measure captures something real and portable.
- **"Integrating allostasis and emerging technologies to study complex diseases"** (2025 synthesis,
  ResearchGate 397306338) — folds Dᴹ-across-channels into a deployable allostatic-load measure and
  discusses calibration-variance robustness for field data.

## Why it bites here / what was missing

`mesh-algedonic` already logs the multivariate vector — the `axes=` field
(`therm:0.0,hw:0.0,egress:0.0,stress:0.3,crit:?`, each in [0,1]). But **every** existing moment reads the
**fused scalar `pain`**, never the joint vector's covariance:

| sidecar | moment of the SCALAR `pain` |
|---|---|
| `allostatic_load()` | LEVEL (count past threshold + rolling mean) |
| `viability_csd()` | 2nd MOMENT (variance + lag-1 AC early-warning) |
| `salience()` | DEVIATION vs habituated baseline |

**None** read the **joint-configuration** moment — how aberrant the *combination* of axes is given their
learned correlations. That is the blind spot Dᴹ fills.

## What landed (`joint_dysregulation()` + `--dysreg` mode + `dysreg=`/`dm=`/`dmq=` row fields)

Read-only, advisory; **never escalates** (mirrors every existing sidecar; the substrate/actuator side
stays untouched, per the homeostasis-coverage safe-landing rule).

- Parses the `axes=` history into complete-case vectors over the axes **known in the current sample**,
  computes the window's mean + covariance, **ridge-regularizes** Σ (so a collinear covariance still
  inverts — Gauss-Jordan, pure-python, k≤5), and reports the **Mahalanobis distance** of the current
  vector.
- **Degeneracy-honest:** constant axes (variance below floor) are **dropped** (no covariance signal,
  would singularize Σ); a joint measure needs **≥2** surviving axes else `DYSREG_INSUFFICIENT`; empty/
  unreachable → `DYSREG_UNKNOWN`.
- **Self-calibrated:** flags `DYSREG_ABERRANT` when the current Dᴹ exceeds a **quantile of the window's
  own Dᴹ cloud** (default 0.90), **never a hardcoded distance cutoff** (the constant-outlives-its-reader
  rule). All thresholds env-tunable.

## Verification

- **RED-first `--test`:** two axes move together (a correlated diagonal cloud); a third is constant and
  **must be dropped**. A sample on the manifold (a=b=0.5) reads `DYSREG_TYPICAL` (Dᴹ=0.00, q=0.11); an
  **off-manifold** sample (a=0.4, b=0.6) — both mid-range per-axis, and *near the centroid in raw
  distance* — reads `DYSREG_ABERRANT` (Dᴹ=5.16, q=1.00). **Only the covariance flags it:** breaking Σ to
  identity (Euclidean) makes the aberrant sample read `DYSREG_TYPICAL` and the gate goes **RED**;
  restored → **GREEN**. Plus INSUFFICIENT (<2 axes / too-few rows) and UNKNOWN (empty) cases.
- **Live** (board `algedonic.log`, this run): `dysreg=DYSREG_ABERRANT dm=0.298 dmq=0.917 dmk=2 dmn=144` —
  the current stress-elevated joint config sits at the 91.7th percentile of its own recent Dᴹ cloud
  (2 axes with variance survived; self-calibrated). An honest upper-tail flag the per-axis `high=3/144`
  count did not raise — exactly the value-add.

## Discarded neighbours (one line each)

- Sterling anticipatory/feedforward setpoint (predictive homeostasis, PMID 21684297) — actuator-side
  (needs a predictor that MOVES a setpoint); already noted as a HELD gap, not a read-only measurement.
- "Love the noise" variability-as-information (arXiv:2508.12791) — already embodied in `viability_csd()`.
