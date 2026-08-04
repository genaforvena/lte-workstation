# Conformal prediction — the distribution-free complement to precision-as-inverse-variance

**Task** genome / board `task:mesh-precision` (a PARTIAL handoff, not a fresh idea-queue pull)
**Landed** 2026-08-04 · `scripts/mesh-precision --conformal` (report-only, uncommitted — steward lands)
**Artifact** this file + 292 inserted lines in `scripts/mesh-precision`, `--test` green (1.45s), 7 new legs,
8 mutants each seen RED

---

## 1. The joint it attacks

The handoff named it and it was already written into the tool's own coverage map. Every mode in
`mesh-precision` is a statement **conditional on a well-specified generative model**:

| mode | what it computes | what it assumes |
|---|---|---|
| `--num` | precision = inverse variance / CV | that σ describes the spread |
| `--bmr` | free energy of reduced vs full model | Normal likelihood, Normal prior |
| `--bme` | evidence for a second hidden mean | same, marginalised over splits |
| `--recover` | can the *shipped* selector recover a known truth | simulates **from** that same model |

`--recover` (landed 2026-08-04, 01:35Z) makes the limit explicit rather than hiding it: it simulates from a
known generative model and inverts with the shipped estimator, so it can price **sample size** and nothing
else. All its figures are best case. Nothing in the file could ask *"and what if the Gaussian is simply
wrong for this tape?"* — the one question inverse-variance precision is structurally unable to answer,
because σ **is** the assumption.

Same shape one level up, in the fusion rule: honest-fusion handles the **SILENT** input (unreachable/stale
→ UNKNOWN, never a faked all-clear). It has no move for the **LOUD** input whose model is wrong — a fresh,
confident, precision-weighted sense whose asserted ±z·σ̂ does not actually contain the truth 1−α of the
time. That input is counted at full weight today.

`grep -rilE 'conformal|nonconformity|coverage guarantee' scripts/ docs/` → **0 hits** before this edit.

## 2. The mechanism

**Split conformal prediction.** Don't assert a band from the fitted model. Split the tape: fit (μ̂, σ̂) on
one part; on the other, compute nonconformity scores `s_i = |x_i − μ̂|` and take the

    k-th smallest score,   k = ⌈(n_cal + 1)(1 − α)⌉

That order statistic is a band with coverage **≥ 1 − α** that holds for **any** underlying distribution and
at **finite n** — no asymptotics, no distributional assumption, and specifically it survives the model being
wrong. Two consequences that matter operationally:

- **The `+1` is the guarantee.** Drop it and the coverage claim is gone (mutant M1 below).
- **A built-in refusal.** When `k > n_cal` the band is `+∞`: below `n_cal = ⌈1/α⌉ − 1` (= 9 at α = 0.10) the
  method **cannot certify at any width** and says so. It refuses rather than guessing — the opposite of a
  silent fallback.

The single precondition is **exchangeability** of the calibration points.

### Sources (read 2026-08-04)

- Vovk, Gammerman & Shafer, *Algorithmic Learning in a Random World*, Springer 2005 — foundational.
- Lei, G'Sell, Rinaldo, Tibshirani & Wasserman, "Distribution-Free Predictive Inference for Regression",
  *JASA* 113(523):1094–1111, 2018.
- Angelopoulos & Bates, "A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty
  Quantification", arXiv:2107.07511 — the ⌈(n+1)(1−α)⌉ rank and its finite-sample floor.
- **LIVE 2026, squarely our topology:** Ritvik Mahajan, Aneesh Raghavan & Karl Henrik Johansson,
  "Finite-Sample Conformal Coverage Recovery via Fusion under Degraded Local Guarantees in Occupancy Map
  Estimation", **arXiv:2607.14906v1, 2026-07-16**. Per-agent guarantees *degrade* because "temporal
  correlation along a robot's trajectory breaks the exchangeability on which conformal calibration relies"
  and each agent "observes only a spatially limited, non-uniform portion of the environment". Neighbours
  then exchange scalar **e-values**, fused under a per-neighbourhood miscoverage budget **β_i := α/d_i** and
  an uncertainty-attenuated operator, to recover the target coverage "regardless of the communication graph
  topology or the underlying sensor noise distribution".
- The handoff's own lead, read and kept as a companion: Zecchin & Simeone, "Conformal Distributed Remote
  Inference in Sensor Networks Under Reliability and Communication Constraints", arXiv:2409.07902 —
  **CD-CRC**: online exponentiated-gradient estimates of per-sensor observation quality + online conformal
  **risk** control on local and global thresholds, with worst-case FNR and communication-overhead
  guarantees.

**Correction to the handoff's organ pick.** It proposed `mesh-situation` or `mesh-presence-fuse`.
`mesh-situation`'s fold is a `max()` over categorical postures (its own header documents that it is
provably non-emergent) — there is no numeric band there to price, so a conformal set would have to be
invented rather than measured. The misspecification joint lives where the parametric claim is *made*:
`mesh-precision`. Putting the distribution-free complement next to the parametric one, over the same tape
reader, is what makes the comparison an artifact instead of an analogy. `mesh-presence-fuse` is not
discarded — it is named below as the **next** step, for the half of the paper this edit does not implement.

## 3. What shipped

`mesh-precision --conformal <file|-> [--alpha A] [--field N] [--win M] [--seed S] [--split F]`,
report-only, no state written, no verdict or weight anywhere else changed.

Two splits answer two different questions, and **the pair is the discriminator**:

| split | condition | question | reading |
|---|---|---|---|
| **IID** (seeded shuffle) | exchangeable — the guarantee actually holds | is the Gaussian **shape** right for this tape's marginal? | ρ_iid = distribution-free half-width ÷ parametric half-width |
| **FORWARD** (chronological) | *not* exchangeable by construction | does a band fitted on the past cover the present? | ρ_fwd — descriptive, **not** a guarantee |

Verdicts:

- **CALIBRATED** — the two bands agree; the Gaussian assumption is earning its keep here.
- **OPTIMISTIC** (ρ_iid ≥ 1.25) — shape misspecified; the sense is over-trusted and **ρ_iid is the widening
  factor**. This is the "calibrated way to widen a LOUD input" the handoff asked for.
- **CONSERVATIVE** (ρ_iid ≤ 0.80) — parametric band is *wider*; the sense is **under**-trusted.
- **NON-EXCHANGEABLE** (ρ_fwd/ρ_iid ≥ 1.25) — the tape drifts, so conformal's **own** precondition fails.
  The honest report is that the guarantee is degraded, not a shuffled number quietly presented as one.
  This is Mahajan et al.'s degradation, diagnosed locally.
- **UNCERTIFIABLE** — `n_cal < ⌈1/α⌉ − 1`. No band, and it says the parametric band's coverage is
  **UNCHECKED, not confirmed**.
- **UNKNOWN** — unreadable/too-short tape. Renders a `verdict` field with no band, never a blank row
  (`[[a-discarded-exit-code-renders-na-as-a-blank-row]]`).

Knobs: `MESH_PREC_CONF_HI` / `_LO` / `_DRIFT`. `--json` carries both splits' σ̂, both bands, both empirical
coverages, `score_r1` (lag-1 autocorrelation of the scores in time order — supporting evidence only), the
`frame_coverage` self-description every other mode carries, and an explicit `guarantee` string naming the
marginal-not-conditional limit.

## 4. Live reads at landing (mesh-home, all report-only)

| tape | n | verdict | number |
|---|---|---|---|
| `therm.log` `max=`°C | 1877 | **NON-EXCHANGEABLE** | ρ_fwd 1.58 vs ρ_iid 0.98 |
| `wifi-quality.log` `signal=` dBm | 1900 | **CONSERVATIVE** | ×3.04 too wide; empirical coverage 0.995 vs nominal 0.900 |
| `nvme-temp.log` °C | 36 | **NON-EXCHANGEABLE** | ρ_fwd 1.57 vs ρ_iid 1.01 |
| `therm.log` `load=` | 1877 | CALIBRATED | ρ_iid 0.97 |
| `wifi-quality.log` `link=` | 1900 | CALIBRATED | ρ_iid 0.91 |
| `records.log` `dyn=` | 529 | CALIBRATED | ρ_iid 0.95 |

Two findings worth the landing:

1. **The thermal band is fitted to a dead regime, and now that is a computed verdict.** A band fitted on the
   older half of `therm.log` is 58% too narrow for the newer half, while the *shuffled* split reads 0.98 —
   i.e. the Gaussian shape is fine and the **history** is stale. `[[stress-thermal-bands-calibrated-to-a-dead-regime]]`
   records exactly this as an incident previously caught by a human. It is now mechanical.
2. **The wifi RSSI sense is under-trusted by 3×, not over-trusted.** σ̂ is inflated by rare deauth excursions
   (`[[mesh-home-sole-path-deauths-every-14min]]`), so the parametric band covers 99.5% where 90% was asked
   for. A precision-weighted fusion is discounting a sense that is *tighter* than its σ suggests. This is the
   direction nobody looks for, and it is why the axis is a measurement rather than an alarm.

Discriminating in **both** directions on real tapes is the anti-hollow check
(`[[hollow-render-is-not-degenerate-material]]`, and the χ-crypticity axis that was built and **discarded**
on 07-30 for failing exactly this).

## 5. Gates — RED-first, 7 legs, 8 mutants each seen red

Fixtures are **deterministic** (an exact Gaussian quantile grid under a fixed coprime-stride permutation —
no RNG), so a leg that goes red went red for its own reason.

| # | leg | asserts | solo killer (verified RED) |
|---|---|---|---|
| 1 | stationary exact-Gaussian tape → **CALIBRATED** | the axis does not flag noise | M2: `z := 1.0` |
| 2 | 15%-spike bursty tape → **OPTIMISTIC** | shape misspecification is detected | M4: `MESH_PREC_CONF_HI=99` |
| 3 | 2% far-outlier tape → **CONSERVATIVE** | the **opposite** direction from the same instinct | M5: `MESH_PREC_CONF_LO=0` |
| 4 | level-shift tape → **NON-EXCHANGEABLE** | the precondition is checked, not assumed | M7: `MESH_PREC_CONF_DRIFT=99` |
| 5a | n_cal=8 → **UNCERTIFIABLE**; n_cal=9 → not | the floor lifts (a permanent refusal asserts nothing) | M8: `n_cal_min := 0` |
| 5b | forward band = 1000 on a hand-built tape | the **rank** `⌈(n_cal+1)(1−α)⌉` itself | M1: drop the `+1` |
| 6 | absent tape → `verdict:UNKNOWN`, **no** band field | honest n/a, never a blank row | M6: revert to bare `exit 2` |

**Legs 2 and 3 are each other's red.** They come from the same instinct — "outliers break the Gaussian
band" — and land on **opposite** verdicts. Spike *frequency*, not spike *size*, decides which: 15% spikes
push the held-out 90th percentile past z·σ̂ (OPTIMISTIC), 2% far outliers inflate σ̂ instead (CONSERVATIVE).
An axis that could only ever say "over-confident" would be an alarm, not a measurement.

**Leg 5a did not test the rank.** The finite-sample floor is a separate constant (`⌈1/α⌉−1`), so M1 —
dropping the `+1` that *is* the coverage guarantee — passed leg 5a silently on the first draft. Leg 5b was
added for it: a chronological, RNG-free tape whose forward-split band is 1000 with the `+1` and 9 without.
Recorded because the first draft looked complete and was not.

**Mutant honesty.** M3 (make the forward split interleaved rather than chronological) kills legs 4 **and**
5b. That is correct rather than sloppy — leg 5b reads the forward band by design — and both legs have their
own solo killer (M7, M1), so neither rests on M3.

## 6. Weakest joint, stated

The guarantee conformal gives is **marginal** — averaged over the calibration draw and over query points —
**not conditional** on the point you are about to judge. A band with 90% overall coverage can systematically
miss one regime. That is the ceiling of the method, not of this implementation, and it is why
NON-EXCHANGEABLE is a verdict rather than a footnote.

Secondary: the drift discriminator compares two *ratios*, so a tape that drifts **and** is shape-misspecified
in the same direction reads NON-EXCHANGEABLE and the shape finding is folded into it. NON-EXCHANGEABLE is
the louder fault (the guarantee itself is void), so the ordering is deliberate — but it is a known
false-negative for OPTIMISTIC.

## 7. Not taken — the named next step

Mahajan et al.'s actual contribution is **coverage RECOVERY by fusion**: neighbours exchange scalar e-values
and fuse them under β_i = α/d_i to rebuild the target coverage from degraded local guarantees. This edit
implements the **diagnosis** (per-tape, single vantage) and not the recovery, because recovery needs ≥2
vantages on **one** quantity. The mesh has exactly one such pair: `scripts/mesh-presence-fuse` (BLE RSSI for
the same device from this node and from `ds`). That is the honest next task, and it is a design change to an
operator-facing organ, not a baton edit — held for the steward. Naming it here so it is a queued step rather
than a leaked implication.

## 8. Files

- `scripts/mesh-precision` — `--conformal` mode + literature header + 7 `--test` legs (+292 lines).
- `docs/reviews/predictive-processing-conformal-distribution-free-coverage-precision-2026-08-04.md` — this file.

Uncommitted in the tree; steward lands.
