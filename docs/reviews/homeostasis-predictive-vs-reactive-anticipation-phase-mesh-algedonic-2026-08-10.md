# Predictive vs reactive homeostasis — the anticipation PHASE of the corrective stream

**Live review** · area: homeostasis / allostasis / ultrastability, from the METRIC angle · 2026-08-10 ·
organ: `scripts/mesh-algedonic` (`anticipation_index()` + `--anticipate`) · READ-ONLY, on-demand.

## The concept we did not embody

Every homeostasis read in the mesh is **phase-blind**. `allostatic_load()` is a mean over a window,
`viability_csd()` a variance + lag-1 AC, `joint_dysregulation()` a Mahalanobis distance at an instant,
`constrained_disorder()` a variability-collapse ratio, `agency_info()` a mutual information over intervals
that pools everything into one action column, and `mesh-pace --burden` reads which branch of a
control-burden loop the spend governor is on. Not one of them can ask the question that *defines*
allostasis as against homeostasis: **does corrective effort arrive BEFORE the challenge, or after it?**

Moore-Ede's split — *predictive* (feedforward, initiated in anticipation of a predictably timed challenge)
vs *reactive* (feedback, corrective after the deviation) homeostasis — is the oldest operational form of
that question. The live literature restates it with an explicit criterion and an explicit measurement:

> "Such an anticipatory response is effective for minimizing the overall error when the error at A [the
> deviation deliberately incurred in advance] is less than the reduction in error at B [the challenge]."
> — Yoshida, Sprekeler & Gutkin, *Linking Homeostasis to Reinforcement Learning: Internal State Control of
> Motivated Behavior*, arXiv:2507.04998 (2025-07-07), Fig 2b caption.

Their Fig 2c measures it the only way an observer can **without a counterfactual**: the probability of the
corrective action in the **cue** state versus in the **challenge** state (predictive shivering — the agent
learns to raise internal temperature at the CS, before the thermal challenge arrives).

That "cue-state vs challenge-state probability" is a metric the mesh can compute on its own tape, and had
no instance of. The coverage memory lists *anticipatory/predictive setpoint (Sterling)* as still-open gap
(3), noting it as "a harder actuator-side move" — this lands its **measurement half**, which is what any
future actuator needs first: evidence, not assertion, about which regime we are in.

## What was built

`anticipation_index()` in `scripts/mesh-algedonic`, exposed as `--anticipate` (never in the 10-min row,
never escalating, no row-format change):

- **onset** — a `pain` step ≥ `ANT_RISE` (0.10) arriving out of `ANT_QUIET` (3) intervals with no comparable
  rise: a viability excursion *begins*, i.e. the challenge a predictive regulator would have pre-empted.
- **lead** — corrective actions in `[onset − L, onset)`, the cue side (`L = ANT_LEAD_S`, 3600s).
- **lag** — corrective actions in `(onset, onset + L]`, the challenge side.
- action vocabulary is **the same regex `agency_info()` uses** (`[done|homeostasis|resource-guard|
  mesh-stress|therm-hot|therm-cool|alert]` on the board) — one definition per organ, not a second private
  one that could drift from it.
- peri-onset windows are kept **disjoint** (`≥2L` apart) and must fit inside the span where *both* streams
  exist, so no action is double-counted and no onset is scored against a window the tape cannot cover.

**Test statistic is the raw count difference `D = lead − lag`, not the normalized AI.** Under a shift most
actions fall outside every peri-onset window, so a null draw's AI is a ratio of single digits and its
distribution runs to ±1 — a band wide enough to swallow any real effect. AI is reported as effect size only.
(Built the naive way first: with AI as the statistic, a fixture with *every* action on the cue side reads
UNPHASED. Mutant M3 below re-creates that.)

**Null = 200 CIRCULAR SHIFTS of the action stream, never a shuffle.** Board action is bursty and diurnal and
onsets sit in busy hours; a shuffle destroys exactly the autocorrelation that makes peri-onset density look
impressive, and would manufacture a phase claim out of it. (Same reasoning as `mesh-load-gate --coupling`;
cf. `cooscillate-parametric-p-ignores-autocorrelation`.)

Verdicts: `ANT_ANTICIPATORY` / `ANT_REACTIVE` / `ANT_UNPHASED` / `ANT_INSUFFICIENT` / `ANT_UNKNOWN` (the last
two exit 2 — honest n/a, never an interpolated phase).

## Live reading on mesh-home (2026-08-10)

```
algedonic anticipation phase: ANT_UNPHASED — lead−lag D=-13 actions vs circular-shift null ±16.0
  (AI=-0.086 effect size; lead=69 lag=82 around 21 onsets)
  peri-onset action rate 3.286/h vs whole-window baseline 1.321/h · window ±3600s around each onset
```

The mesh's corrective stream carries **no anticipatory phase** — and the reactive tilt does not clear the
null either. Effort *is* 2.5× denser around onsets than baseline, but the shift null reproduces most of that
density from the action stream's own burstiness, and it lands on neither side. Stable across
`L ∈ {30m, 60m, 120m}` and `ANT_RISE ∈ {0.10, 0.15, 0.20}` (16–24 onsets, AI ∈ [−0.13, +0.02] against a null
band that always contains it).

Read plainly: **on the evidence, this organ's regulation is not feedforward.** That is the honest state of
gap (3), and the number now exists to compare against if an anticipatory actuator is ever built.

## Two limits stated in the tool itself

1. **Reverse causation.** Board action can *cause* load and hence pain. Peri-onset elevation is therefore not
   evidence of regulation, and a lead would not be proof of prediction. This is a phase reading with a null,
   never a causal claim.
2. **Periodicity makes the null conservative.** Against a strictly periodic disturbance a shift by one period
   reproduces the observed phase, so the null contains the effect and no phase can be called. Where onsets are
   cron-locked, the bar is too high — never too low. (Found the hard way: the first fixture had perfectly
   periodic onsets and the true-positive case read UNPHASED. The shipped fixture uses irregular spacing.)

## RED-first verification

Suite: 1.79s (inside `mesh-doctor`'s 12s per-tool gate). Fixtures hold onset times and action **count** fixed
and vary only *where* the actions sit relative to onset, so the fixture can only pass on the phase.

| mutant (run from a scratch copy, not the live file) | result |
|---|---|
| M1 — verdict's lead/lag sides swapped | **red** (cue fixture → ANT_REACTIVE) |
| M2 — circular-shift null removed (band forced to 0) | **red** (sideless fixture → ANT_REACTIVE) |
| M3 — normalized AI used as the statistic instead of D | **red** (cue fixture → ANT_UNPHASED) |
| M4 — min-onset floor removed | **red** (thin tape → ANT_ANTICIPATORY instead of INSUFFICIENT) |
| unmutated control | green |

M2 **survived the first version** of the fixture: the "even" case placed one action on each side, so `D = 0`
exactly and a zero band could not change the verdict — a fixture that can only produce a zero statistic
cannot tell a working null from a missing one (*a gate you have not seen fail is not a gate*). The shipped
fixture uses deterministic LCG offsets across the window, leaving a small **chance** imbalance: sideless, but
nonzero. It goes red without the null.

## Sources

- Yoshida, Sprekeler & Gutkin, "Linking Homeostasis to Reinforcement Learning: Internal State Control of
  Motivated Behavior", arXiv:2507.04998 (2025-07-07) — HRRL; drive `d(H)`, reward as drive reduction, Fig 2b
  the A<B anticipatory-benefit criterion, Fig 2c the cue-vs-challenge action-probability measurement.
- Moore-Ede, "Physiology of the circadian timing system: predictive versus reactive homeostasis",
  Am J Physiol 250(5):R737 (1986).
- Sterling, "Allostasis: a model of predictive regulation", Physiol Behav 106(1):5 (2012), PMID 21684297.

## Not landed (checked, discarded in one line each)

- **Ziegler, "When Regulation Has Memory: Hysteresis and Control Burden in Artificial Agency",
  arXiv:2606.30975 (2026-06-29)** — already embodied: `mesh-pace burden_state()` / `--burden` cites it.
- **HRRL drive function `d(H) = (Σ|h*−h|ⁿ)^{m/n}` as an alternative to the noisy-OR fusion** — a real
  divergence (noisy-OR *saturates* at the top where HRRL's `m>n>1` drive is *super-additive*, so the mesh
  cannot rank two critical states), but it is a change to the fused `pain` every other sidecar reads, i.e. a
  fusion-behaviour change, not a read-only instrument. HELD, noted here as the next candidate.
