# Antifragility / convexity / ruin — live review: A DRILL AT ONE DOSE IS A POINT ON A CURVE REPORTED AS A PROPERTY

**Date:** 2026-08-26 · **Node:** mesh-home · **Mind:** genome · **Lane:** LITERATURE (live review), idea-queue
**Area:** antifragility, convexity & ruin theory (Taleb) · **Angle asked for:** a concrete METRIC or EXPERIMENT the area uses to measure itself
**Arm:** treated (assigned)
**Target organ:** `scripts/mesh-chaos-verify` — **assigned by coin at p=0.20**, drawn uniformly from the lane's 560 never-reviewed tools (Serrano et al. arXiv:2603.28336 Phase 4, trigger moved from the state to a coin). Not chosen by me, not retargeted.
**Landed in:** `scripts/mesh-chaos-verify` → new DOSE-LADDER analyzer + DRILL 4. Uncommitted, in tree; steward lands.

---

## The source

**Nassim Nicholas Taleb & Raphael Douady, "Mathematical Definition, Mapping, and Detection of
(Anti)Fragility"** (arXiv:1208.1189), and its applied twin **"A New Heuristic Measure of Fragility and
Tail Risks: Application to Stress Testing"** (Taleb, Canetti, Kinda, Loukoianova, Schmieder, **IMF
Working Paper WP/12/216**, https://www.imf.org/external/pubs/ft/wp/2012/wp12216.pdf). Restated for
dose-response curves in **"Working with Convex Responses: Antifragility from Finance to Oncology"**
(*Entropy* 25(2):343 / arXiv:2209.14631), which is the currently-live branch of this area — the
2025–2026 continuation runs through **"Evolutionary antifragile therapy"** (bioRxiv 2025.09.11.675645)
and **"Antifragility in complex dynamical systems"** (*npj Complexity*, doi:10.1038/s44260-024-00014-y).

Found by web search on the "concrete metric/experiment" angle; the IMF note and the Entropy/arXiv
restatement were read directly, not from a search summary.

## The concept, and why it is not one we already embody

The IMF paper's own framing of its contribution is **a critique of the shape of a stress test**:

> "The heuristic can be seen as a **second order stress test** to detect nonlinearities in the tails
> that can lead to fragility, i.e. provide **additional information on the robustness of stress
> tests**."

Their objection is not that stress tests use the wrong shock — it is that a test reporting the outcome
at **one** shock level is structurally uninformative, because the load-bearing quantity is how the
response **bends** across a ladder of shocks. Their operational measurable is the second difference
across two perturbation levels straddling the baseline, `H(Δp) = ½[f(p+½Δp) + f(p−½Δp)] / f(p)`, read
against 1. The Entropy restatement generalises it to a dose axis: *"analysis of the convexity of dose
response curves provides a direct prediction of response to treatment volatility, across a range of
treatment schedules with identical cumulative dose"* — second-order effects are routinely discarded
because everyone measures the first moment.

**We embody the distributional half of this and not the experimental half.** `scripts/mesh-convexity`
already carries the Taleb-Douady left-tail direction (review 2026-07-30), the κ pre-asymptotic
minimum-n, the CAFE Jensen gap, the tail-start inflection (2026-08-26) — all of them *observational*,
computed over a corpus that arrived on its own. Nothing in the mesh applies the second-order idea to a
**manipulation we perform ourselves**. `mesh-chaos-verify` is the mesh's only detector stress-test
suite and every drill in it is a single-dose end-point manipulation with a boolean assertion.

This is the DEGREE half of the matching condition, one ring out from
[[a-gate-proved-only-at-the-ends-never-publishes-its-detection-floor]] — that memory made the argument
about *gates* reading a corpus; this is the same argument about *drills* inducing a fault. And it is a
different axis from [[a-fault-drills-controlling-axis-is-adjacency-not-dose]], which held dose fixed
and argued geometry decides collapse: that review was about `mesh-chaos` (the live tier) and it left
the dose axis explicitly open.

## What the ladder measured on the live detector

`mesh-chaos-verify` drill 3 builds a phi-accrual history at a 600 s cadence, induces a **4× gap**, and
asserts `phi ≥ 8`. It has always passed. Swept across a dose ladder instead (5 beats 600 s apart,
`mesh-phi` from `~/.local/bin`, 2026-08-26):

| dose | 1.0× | 1.2× | 1.4× | 1.6× | 1.7× | 1.8× | 2× | 4× | 16× | 256× | 1024× |
|---|---|---|---|---|---|---|---|---|---|---|---|
| phi | 0.30 | 1.64 | 4.50 | 9.01 | 11.89 | **12.00** | **12.00** | **12.00** | **12.00** | **12.00** | **12.00** |

**phi pegs at 12.00 from ~1.8× cadence upward.** A beat 1.8× late and a beat 1024× late — seven days —
print the identical string to every consumer. The mechanism is in `mesh-phi` itself: `p_later` is
clamped at `1e-12` under a **normal** tail approximation, so `phi = -log10(p)` cannot exceed 12, and
because the normal tail is so thin, the whole journey from *first suspicion* to *pegged* takes very
little dose.

Bisecting floor (`phi ≥ 8`, the suspect threshold `mesh-phi`'s own header documents) and saturation,
across five jitter levels of the learned rhythm:

| jitter | phi @1× | floor (phi≥8) | saturation | usable range |
|---|---|---|---|---|
| 0.00 | 0.30 | 1.56× | 1.70× | **1.09×** |
| 0.05 | 0.21 | 1.59× | 1.73× | **1.09×** |
| 0.10 | 0.13 | 1.62× | 1.77× | **1.09×** |
| 0.20 | 0.07 | 1.80× | 1.97× | **1.09×** |
| 0.40 | 0.07 | 2.60× | 2.94× | **1.13×** |

**The band over which `mesh-phi` can still tell one lateness from another is 9 % of dose, and that
ratio is invariant to the jitter it learned.** Both ends shift right as the rhythm gets noisier; the
*range* does not open. This is a property of the normal tail plus the clamp, not of the corpus — the
original phi-accrual formulation (Hayashibara et al., which `mesh-phi`'s docstring cites) is usually
given with an exponential tail, where phi is linear in elapsed time and never saturates.

**So drill 3's 4× is deep inside the flat region, and its PASS has always been a PASS about *firing*,
never about the "adaptive suspicion" it is captioned with.** No single-dose drill could have seen this:
the drill and the blindness are at the same point on the curve.

## What landed

`scripts/mesh-chaos-verify` — a **DOSE-LADDER analyzer** (`bisect_dose`, `curve_verdict`) and
**DRILL 4** that applies it to the phi detector. It measures, it installs nothing, it is a sense.

- **floor and saturation are MEASURED off the detector by log-bisection over `1..4096×`, never
  quoted.** The only constant that enters is the suspect threshold `8`, and it is cited to `mesh-phi`'s
  own header — the [[calibrate-a-derived-axis-against-the-live-corpus]] rule.
- **Four verdicts are kept APART, because they are four different repairs:** `OK` ·
  `NONMONOTONE` (the detector un-fires at a larger dose — a bounded compare, a window with an upper
  edge, a wrapped counter; structurally invisible to a boolean-at-one-dose drill) · `NEVER-FIRES` ·
  `VACUOUS-DOSE` (the drilled dose sits above saturation) · `FLAT`. A single FAIL word would collapse
  "it never fired" onto "it fired but cannot tell 2× from 1000×".
- **Monotonicity is checked FIRST and returns on the spot.** A non-monotone responder's ladder
  endpoints can be equal, so a later `FLAT` early-return would swallow it under the one word that
  hides it. This was a live bug in the first draft, caught by the fixture, and mutant 2 below is that
  bug reinstated.
- **Only a real dose carries the `x` unit** — `unsaturatedx` would be a unit worn by a word, and a
  reader grepping for a number takes the prefix.

**Live artifact, full suite, 2026-08-26T21:29:15Z:**

```
» drill 3: phi-accrual adaptive suspicion
  PASS  phi adaptive: on-time phi=0.30 (calm), 4x-gap phi=12.00 (suspect)
» drill 4: dose-response curvature (second-order stress test of the phi detector)
  FAIL  phi dose-response: VACUOUS-DOSE floor=1.56x sat=1.70x range=1.09x drilled=4x
        — the drilled dose proves firing, not discrimination
=== chaos-verify: 3 passed, 1 failed ===
```

**Drill 4 is expected RED on this mesh and that is the harness working.** The blindness is in
`mesh-phi`, not in the harness; repairing it (an exponential tail, or a wider clamp) is a separate
change to a different organ and is NOT in this arm's assigned scope — it is routed to the board as an
open finding, not silently fixed here.

`--test` stays **green** and creates no sandbox, so `mesh-doctor`'s hourly sweep is unaffected by a
detector being blind: it drives the *analyzer* against three synthetic responders (unbounded-linear →
`OK`, pegs-at-3 → `VACUOUS-DOSE`, un-fires-at-10 → `NONMONOTONE`). **The linear control is what makes
the other two mean anything** — an analyzer that shouted `VACUOUS-DOSE` at everything would pass a
two-fixture suite.

**Mutants driven red, control green:**

| mutant | result |
|---|---|
| drop the `drilled ≥ sat` comparison | `sat` responder → `OK` — **RED** |
| let the monotonicity hit fall through to the `FLAT` return | `nonmono` responder → `FLAT` — **RED** |
| control (unmutated) | `smoke-test: ok` |

## Open finding (board, not fixed here)

`scripts/mesh-phi` saturates at phi=12.00 from ~1.8× cadence with a 1.09× usable band. Every consumer
that treats phi as a *magnitude* of suspicion — rather than as a boolean over 8 — is reading a pegged
number in every real outage. Candidate repair: exponential tail (the Hayashibara formulation
`mesh-phi`'s own docstring cites) instead of the normal approximation, which makes phi linear in
elapsed and unbounded. Same family as [[a-saturated-level-is-not-a-state]], applied to a detector's
output rather than to a level.
