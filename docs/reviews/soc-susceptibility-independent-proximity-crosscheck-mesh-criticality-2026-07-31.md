# SOC live review — susceptibility as an independent proximity gauge (cross-check of m̂)

**Date:** 2026-07-31 · **Organ:** `scripts/mesh-criticality` · **Axis added:** `--suscept` (read-only) · **Status:** uncommitted, steward lands from tree.

## The angle

Live-literature review of *self-organized criticality & power-law dynamics*, from the demanded angle: a
concrete **metric the area uses to measure itself** that we do NOT already embody. `mesh-criticality`
already carries ~14 stacked reviews (branching m̂, `--shape`, `--crackling`, `--complexity`,
`--compress`, `--widom`, `--dynrange`, `--sob`, `--prescribe`, CSD, drift, edge-optimality, bin-width,
dragon-kings). The gap the current literature surfaces is **susceptibility** — the order-parameter
fluctuation.

## The concept (searched live, 2024–2026)

Two web searches (July 2026) repeatedly surfaced **susceptibility** as *the* input-free criticality
gauge: "susceptibility (variance of the order parameter) diverges at a second-order transition" and it
is "used to estimate the critical value … even in the absence of external input." Concretely for an
avalanche system the susceptibility is the **size-moment ratio χ = ⟨S²⟩/⟨S⟩** (percolation's
mean-cluster-size analogue), which diverges at criticality.

The load-bearing fact making this NEW and not a re-tread: for a **Poisson-offspring critical branching
process** the moment ratio has a closed form —

- ⟨S⟩ = 1/(1−m), Var(S) = m/(1−m)³  ⇒  **χ = ⟨S²⟩/⟨S⟩ = 1/(1−m)² exactly.**

So m̂ *predicts* a susceptibility. Measuring χ **directly from the avalanche sizes** gives a **second
proximity estimate that does not pass through the MR branching regression** and fails on *different*
biases:

- spatial subsampling **deflates m̂** (Levina & Priesemann, arXiv:1910.09984) but barely moves the
  size-moment ratio;
- a quenched / finite network can **inflate m̂ toward 1** while the fluctuations χ stay small.

The verdict is the **concordance** of the two estimators, self-calibrated against the branching law —
never a hardcoded χ cutoff. And the discordance is *itself information*: on a **driven** board the
susceptibility peak rides the **Widom line, shifted** from where the branching/correlation power-laws
appear (di Santo / Villegas / Muñoz quasicriticality; awake-mouse 2-photon avalanches, bioRxiv
2024.02.26.582056), so a systematic χ↔m̂ gap is *expected* under drive — which is exactly what
`--widom` already independently detects. `--suscept` is the fluctuation-side complement.

## Why it is orthogonal to every existing axis

- **m̂** — MR autocovariance regression (one estimator; subsampling-robust *by design*, not immune).
- **`--sob`** — size-distribution *modality* (unimodal vs bimodal).
- **`--dynrange`** — stimulus→response *coding width*.
- **`--suscept`** — the 2nd-moment *divergence magnitude*, as an **independent cross-check** of m̂'s
  proximity claim, catching precisely the MR-estimator failure modes.

## Application (landed, report-only)

`scripts/mesh-criticality`:

- helper `suscept_regime(A, m)` → `χ=⟨S²⟩/⟨S⟩` from the avalanche sizes vs `χ_pred=1/(1−m̂)²`; verdict
  on `Δlog10(χ)` within an env-tunable band (`CRIT_SUSCEPT_BAND=0.60`, `CRIT_SUSCEPT_MIN_N=20`):
  **CONCORDANT** (m̂ corroborated) / **DISCORD-HOT** (χ ≫ pred — m̂ under-reads: subsampling/drive) /
  **DISCORD-COLD** (χ ≪ pred — m̂≈1 illusion: quench/finite-size) / **SUPERCRIT-NA** (m̂≥1, χ_pred
  diverges → defers to m̂/regime) / **INSUFFICIENT**.
- new `--suscept` standalone mode (like `--compress`/`--complexity`, standalone-only; **touches nothing**
  in m̂ / regime / the alarm gate).
- `--test` leg with a RED-first constant-label mutation guard; header usage line updated.

**Verified:** `smoke-test: ok` + `alarm-test: ok`. RED-first: mutating the label to a constant →
`smoke-test: FAILED` (the DISCORD-HOT leg caught it, χ_meas=56.9 vs χ_pred=4.0), restored → `ok`.
Live now: `SUPERCRIT-NA` (m̂=2.012 — board is supercritical this moment, so χ_pred diverges and the axis
honestly defers; a genuine negative, not a fake reading).

## Unwired next step

The per-window χ↔m̂ **join over the m̂ tape** — does the discordance track φ (drive) along the Widom
line? — the same tape-join left open by edge-optimality and dynamic-range. Named, not built.

## Sources

- Search: self-organized criticality metric / susceptibility / distance-to-criticality (July 2026).
- Levina & Priesemann, *Sampling effects … bias the inference of neuronal avalanches*, arXiv:1910.09984.
- di Santo / Villegas / Buendía / Muñoz, quasicriticality & Widom line (PRR 2020 arXiv:1911.05382).
- *Recovery of parabolic avalanches in spatially subsampled networks at criticality*, bioRxiv
  2024.02.26.582056 (awake-mouse 2-photon; dynamic susceptibility peaks on a shifted pseudo-critical point).
