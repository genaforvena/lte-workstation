# The index is an artifact of its own recipe: a specification curve over `mesh-perimeter`'s fusion

**Live review, 2026-08-22 — homeostasis, allostasis & ultrastability (Ashby, Sterling), from the angle
the task asked for: a known CRITIQUE / failure mode of the area.**
Landed in `scripts/mesh-perimeter` (`--multiverse`, read-only; uncommitted — steward lands from the tree).

## What was already ours (checked first, so the review could not re-land)

Sixteen prior landings in this area. The ones that touch allostatic LOAD specifically:

| embodied | where |
|---|---|
| allostatic load as **cumulative regulatory wear** (McEwen & Stellar) | `mesh-stress` (2026-07-06) |
| load as a **multivariate distance** (Mahalanobis Dᴹ), not a per-axis count | `mesh-algedonic` (2026-07-30) |
| **Reactive Scope Model** — wear that MOVES the overload threshold, and `M(t)`, the ceiling that never heals | `mesh-stress` (2026-07-24) |
| allostatic **overload type 1 vs type 2** (energy balance) | `mesh-algedonic` (2026-08-21) |
| settling point vs set point; predictive vs reactive; timescale viability `T_r ≤ T_m < T_e` | `mesh-homeostasis`, `mesh-algedonic` |

Every one of them argues about **what the index should be**. None asks the prior question the critique
literature has now made central: *given that several defensible indices exist, is our verdict a signal
or a choice?* No review in the corpus contains the words "specification curve" or "multiverse".

## The find

**Patel, P. C. (2026). "Biomarker Panel Selection Explains Heterogeneity in Allostatic Load–Mortality
Risk: A Specification-Curve Analysis." *medRxiv* 2026.05.06.26352579.
doi:[10.64898/2026.05.06.26352579](https://www.medrxiv.org/content/10.64898/2026.05.06.26352579v1.full)**
— posted 2026-05-06, three months old. Found by live web search 2026-08-22; the standing form of the
same complaint is [Measuring allostatic load: approaches and limitations to algorithm creation](https://www.sciencedirect.com/science/article/abs/pii/S002239992200335X)
(*J Psychosom Res*) and the [2025 systematic review](https://www.frontiersin.org/articles/10.3389/fpsyt.2025.1590547/full)
that still reports "no consensus on the specific components required for the formulation of the AL index".

The critique, in the paper's own words:

> "published studies use at least 18 distinct calculation methods across 26 biomarkers, raising a
> fundamental question: **does this association reflect a stable biological signal or an artifact of
> investigator choice?**"

And the answer is not a better index. It is a method:

> "**Multiverse specification-curve analysis replaces a single set of investigator choices with a
> systematic enumeration of all defensible analytical alternatives.**"

Patel crosses 5 biomarker panels × 3 scoring methods × 5 covariate configurations × 3 outcomes × 2
cohorts = **450 specifications**, and the headline is the transferable part:

> "**Biomarker panel composition explained 46% of between-specification variance, compared with 4% for
> covariate adjustment.** … biomarker panel selection — not covariate adjustment — is the primary
> target for field-wide standardization."

That is the mechanism we did not embody: **enumerate the defensible recipes, publish the DISTRIBUTION
of verdicts, and attribute the disagreement to the choice that drove it.**

## Why `mesh-perimeter`

`mesh-perimeter` is an allostatic-load index in everything but name and nobody had noticed: a
hand-picked **panel** of axes (OUTSIDE / NETWORK / PHYSICAL, the last one itself a hand-picked bundle
of five sub-senses) reduced by one hand-picked **scoring rule** (`fuse_posture`: worst reachable axis,
non-compensatory max) under one **coverage configuration** (`ROBUST_PARTIAL`, default 0) into a single
CALM/NOTICE/ALERT band that the cron reflex posts to the board. It has no prior landing from this area
and it emits a verdict a human acts on.

## Measured on the live corpus

`~/.mesh/perimeter.log`, 576 durable edge lines, replayed across 7 panels × 3 rules × 2 coverage
configs = **42 specifications** (`mesh-perimeter --multiverse`, 2026-08-22):

```
n=576 specs=42 (panel 7 x rule 3 x partial 2)
shipped: panel=ONP rule=worst partial=off -> elevated=6.1% of edges
shipped-bands: CALM=534 NOTICE=12 ALERT=23 CANNOT-ASSESS=7
spec-curve elevated%: min=0.2 p50=4.7 max=56.2
agreement-with-shipped%: min=44.3 p50=69.1 max=98.4
  drop-O: 1.6% of edges change verdict
  drop-N: 4.5% of edges change verdict
  drop-P: 25.5% of edges change verdict
attribution: panel=58% (d=0.325)  rule=3% (d=0.017)  partial=39% (d=0.217)
```

Three things fall out, and the first reproduces Patel's headline on our own data:

1. **Panel 58%, rule 3%.** Which senses are IN the fusion moves the verdict ~19× more than how they
   are combined. Every argument this mesh has had about fusion rules (worst-axis vs count vs mean) was
   arguing about the 3%. Patel found 46% vs 4%; we find 58% vs 3% — same structure, independently.
2. **The shipped alert rate is a coin-flip's distance from arbitrary.** 6.1% of edges elevated, in a
   defensible space that runs 0.2% → 56.2%, with a median alternative agreeing with us on only 69% of
   edges. The band is not wrong; it is *contingent*, and nothing said so before today.
3. **PHYSICAL is a coverage axis, not a severity axis — and it is the load-bearing one.** It supplied
   an elevated severity on **1 of 576** edges, yet dropping it changes **25.5%** of verdicts, because
   on 145 edges it is the *only reachable axis* and without it the read collapses to CANNOT-ASSESS.
   Five sub-senses (presence, motion-attribution, stranger-watch, powerbtn, soundscape) are wired into
   an axis whose actual contribution to this organ is *keeping it assessable at all*. That is worth
   knowing before anyone prunes it for being quiet.

`ROBUST_PARTIAL` (39%) is the second-largest lever and it is off by default — a one-env-var flip that
would reshape a quarter of the verdicts, currently invisible.

## What landed

`scripts/mesh-perimeter --multiverse` — read-only, raises no probe, touches no state, and **does not
change the shipped verdict**. The point is to publish how contingent the verdict is, not to pick a
different one. It reports the band tally, the spec curve, leave-one-out over the panel, and the factor
attribution (mean pairwise disagreement between specs differing in exactly one factor — deliberately
*not* called an R²).

Coverage is stated **in the reading**, not only here: the log is written by `--edge`, so this is a
specification curve over *transitions*, never over time. An alternative spec that would have fired
where the shipped one sat still is invisible, which biases every alternative downward. Below 30 edges
the attribution renders `na (n=… < 30)` rather than a number off five rows.

## Verification

`--test` drives it against a fixture log (30 edges where only PHYSICAL is reachable + 10 where NETWORK
is the sole ALERT) and asserts n/specs, the band tally, the shipped rate, the full spec-curve triple,
all three leave-one-out values, the exact attribution, the n-floor `na` path, and the coverage caveat.

Driven red four ways, each restored to green:

| mutation | result |
|---|---|
| `if rule == 'worst':` → `if False:` (shipped rule silently replaced by the mean rule) | `FAIL … missing 'shipped-bands: CALM=30 NOTICE=0 ALERT=10 CANNOT-ASSESS=0'` |
| `if partial and v == 'CALM'` disabled (coverage config inert) | `FAIL … missing 'spec-curve elevated%: min=0.0 p50=25.0 max=100.0'` |
| `if n < 30:` → `if n < 1:` (attribute variance below the floor) | `FAIL: --multiverse attributed variance below its own n floor` |
| `max(reach)` → `min(reach)` (fusion inverted) | `FAIL … missing 'elevated=25.0%'` |

The first two mutations **survived** the first version of this gate — an elevated-rate assertion cannot
see a rule that downgrades every ALERT to a NOTICE, since both count as elevated. That is why the tool
now emits `shipped-bands:` as its own line: the fix to the blind gate is a fix to the *reading*.

## Sources

- [Patel 2026, medRxiv 2026.05.06.26352579](https://www.medrxiv.org/content/10.64898/2026.05.06.26352579v1.full)
- [Measuring allostatic load: approaches and limitations to algorithm creation](https://www.sciencedirect.com/science/article/abs/pii/S002239992200335X)
- [Allostatic load index across the psychosis spectrum: systematic review & meta-analysis (PMC12260679)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12260679/)
- [Retrospective operationalization of allostatic load in patients with cancer: a systematic review](https://www.sciencedirect.com/science/article/abs/pii/S030645302400129X)
