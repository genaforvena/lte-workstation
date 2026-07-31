# Homeostasis → Network Physiology: Time Delay Stability (TDS) — the lagged-coupling gap (mesh-algedonic)

**Date:** 2026-07-31 · **Lane:** genome literature live-review (feed auto-task) · **Organ named:** `scripts/mesh-algedonic`

## Area & what the mesh already embodies

Homeostasis / allostasis / ultrastability is deeply embodied here ([[homeostasis-review-coverage]]):
allostatic load (`mesh-algedonic` `allostatic_load()`, `mesh-stress`), **multivariate** allostatic load as
Mahalanobis distance (`joint_dysregulation()`), critical slowing down (`viability_csd()`), the Constrained
Disorder lower border (`constrained_disorder()`), requisite variety (`mesh-vitality channel_variety`),
Ashby ultrastability trials-to-stable-field (`mesh-homeostasis`), reactive scope (`mesh-stress`).

Every coupling-aware measure we have reads coupling at **one instant or one lag-direction**:
- `joint_dysregulation()` uses the axis covariance Σ — that is **zero-lag** linear coupling.
- `mesh-cooscillate` uses transfer entropy — directed info flow, but a **single** signal pair (Δ-RSSI).

Neither asks the question at the centre of the **Network Physiology** programme: *is the coupling between
two subsystems **stable over time**, and does the network of couplings **reorganise** at a state transition?*

## The concept we do NOT embody — Time Delay Stability (TDS)

**Time Delay Stability** (Bashan, Bartsch, Kantelhardt, Havlin & Ivanov, *Network physiology reveals
relations between network topology and physiological function*, Nature Communications 3:702, 2012; and the
ongoing Network Physiology programme, Ivanov, *Frontiers in Network Physiology*, 2021–2026) is the field's
signature **link-strength metric**, and it is neither a correlation nor a transfer entropy:

1. Slide overlapping short windows over two normalised signals.
2. In each window, compute the **cross-correlation** and take the **time lag τ = argmax|C(τ)|** — the delay
   at which one system's bursts most consistently precede the other's.
3. A link is **stable** across the consecutive windows where τ stays **constant** (within a small tolerance,
   typically ±1 time-step). Bursts of activation in one system consistently followed at a *fixed* delay =
   a real, stable interaction.
4. **%TDS** = the fraction of the record for which the pair is stable = **link strength**. Stronger coupling
   → longer stretches of constant delay → higher %TDS.

The load-bearing empirical finding: **physiologic state transitions (wake↔sleep, rest↔stress) appear as a
REORGANISATION of the TDS network — links form and dissolve — even when the individual signals' means and
variances barely move.** The information is in the *stability of the lag structure between* subsystems, a
quantity invisible to any per-signal statistic and to zero-lag covariance.

## Why this is a genuine gap, not a re-tread

`mesh-algedonic` already logs the multivariate essential-variable vector each run (`axes=` =
therm/hw/egress/stress/crit). `joint_dysregulation()` reads that vector's **Σ** — the **zero-lag** geometry —
and flags off-manifold *configurations*. It is structurally blind to **lagged** structure: two axes can be
strongly coupled at a stable 2-step delay (therm rise → stress rise 2 windows later) and contribute **zero**
to the zero-lag Σ, so joint_dysregulation sees them as independent. And when that stable delay **breaks** —
the subsystems decouple — nothing in the current stack notices: pain may be flat, each axis in-range, each
axis's CSD/CDP quiet, Σ unchanged. TDS is exactly the missing view: the **network topology of stable lags**,
whose *reorganisation* is an early warning of a regime change one order of coupling above what CSD (per-axis)
and Mahalanobis (zero-lag) can see. Same "the discard pile is another sense's signal" shape as CDP surfacing
the axes joint_dysregulation drops — here it is the *lags* the covariance drops.

## The concrete application — `scripts/mesh-algedonic`

Propose a report-only `tds_network()` / `--tds`, sibling to `joint_dysregulation()`:

- Read the last-N `axes=` vectors from the window; for each axis-pair, slide short windows, take τ = argmax
  of the windowed cross-correlation, and compute **%TDS** (fraction of consecutive windows with τ constant
  within ±1 step).
- Emit per-pair `%TDS` and a network summary; flag **`TDS_DECOUPLING`** when a pair whose %TDS was high in
  the prior half **collapses** in the recent half (a stable lag-link dissolving — the reorganisation signal),
  and **`TDS_REWIRING`** when the set of strong links (%TDS ≥ threshold) turns over between halves.
- Self-calibrated (own prior-half %TDS as the reference, no hardcoded coupling strength), honest
  `TDS_INSUFFICIENT` below a minimum window/pair count, guarded by a **shuffled-window surrogate null**
  (reuse the algedonic/cooscillate null idiom — %TDS has a chance floor that must be cleared;
  [[surrogate-null-cooscillation]], [[a-rule-asserted-at-one-call-site-is-not-asserted]]).

**Not implemented this turn — held on data sufficiency (honest).** TDS needs a reasonably long multi-channel
series with *burst* structure and consistent sampling cadence; the `axes=` vector is a slow, coarsely-sampled
essential-variable stream, so a naive per-window %TDS risks the sparse-N hollow-proxy trap that kept
`tail_first()` HELD ([[homeostasis-review-coverage]]). The honest first step is to confirm the axes log has
the cadence/length TDS requires (or lengthen the retained window) **before** shipping a `--tds` that would
otherwise emit confident network verdicts from 5-sample cross-correlations. The proposal names the file, the
sibling function, the estimator, the flags, and the null so it lands directly once the cadence is verified.

## Discarded alternatives (one line each)

- **Anticipatory/predictive allostatic setpoint** (Sterling, *Allostasis: A model of predictive regulation*,
  PMID 21684297) — **discarded here**: already a HELD open gap in the coverage map, and it is an *actuator*
  move (shifting a defended setpoint from a forecast), which stays held on the substrate/actuator boundary —
  not a measurement landing.

## Status

Review is the artifact (concept + grounded target + held-implementation rationale + discard). No tool edited
this turn — shipping `--tds` onto an unverified-cadence log would be the hollow-proxy anti-pattern this lane
exists to catch. Uncommitted in tree (this doc). Steward lands.

## Cite

- Bashan, Bartsch, Kantelhardt, Havlin & Ivanov, *Network physiology reveals relations between network
  topology and physiological function*, Nature Communications 3:702 (2012) — origin of TDS / %TDS link strength.
- Ivanov, *The New Frontier of Network Physiology: From Integrated Organ Network Interactions to Emergent
  Physiologic States*, Frontiers in Network Physiology (2021–2026, ongoing).
- Sterling, *Allostasis: A model of predictive regulation*, Physiology & Behavior (2012), PMID 21684297 —
  the discarded (actuator-side, held) alternative.
