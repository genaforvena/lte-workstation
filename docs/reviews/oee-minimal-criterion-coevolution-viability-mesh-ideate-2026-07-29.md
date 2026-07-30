# Minimal Criterion Coevolution — the fitness dual of illumination for the review-area population

**Area:** artificial life & open-ended evolution · **Angle:** an OPERATIONAL mechanism it proposes (not just philosophy) we could implement
**Date:** 2026-07-29 · **Landed in:** `scripts/mesh-ideate` (`viability_tally`, report-only) · **Status:** SHIPPED (detection) + HELD (selection/spawn)

## The concept

**Minimal Criterion Coevolution (MCC)** — Jonathan C. Brant & Kenneth O. Stanley, *"Minimal Criterion
Coevolution: a new approach to open-ended search"*, GECCO 2017
([ACM 10.1145/3071178.3071186](https://dl.acm.org/doi/10.1145/3071178.3071186); thesis
[stars.library.ucf.edu/etd2020/21](https://stars.library.ucf.edu/etd2020/21)). Still the reference
OEE-without-archive mechanism — current per the 2025 **awesome-open-ended** survey
([github.com/jennyzzt/awesome-open-ended](https://github.com/jennyzzt/awesome-open-ended)) and the
*"Benchmarking open-endedness in minimal criterion coevolution"* follow-up (GECCO 2019).

The mechanism: open-ended divergence needs **neither an objective nor a novelty archive / behaviour
descriptor**. It falls out of **two coevolving populations**, where an individual is eligible to
reproduce *only when it satisfies a pass/fail **minimal criterion** defined by its interaction with the
other population*. In Brant & Stanley's maze/agent world: a maze is viable iff **some-but-not-all**
agents solve it (neither trivial nor impossible); an agent is viable iff it solves ≥1 maze. Their thesis
is that unconstrained novelty / illumination **wanders into functionless regions**, and the coevolving
minimal criterion is exactly what keeps the search *functional* without an objective.

## Why it is not already embodied

The mesh's literature lane (`mesh-ideate`) already embodies **MAP-Elites illumination** (landed
2026-07-28): `illum_pick()` draws the **darkest** (least-covered) cell of the 108-cell AREAS×ANGLES grid.
That is pure **divergence** — coverage with **no fitness term**. It will keep re-drawing an *exhausted*
area (one the mesh's capability-set has fully absorbed) purely because its grid-cell is under-covered,
spending review turns that come back "already embodied." That is precisely the *"illumination without a
minimal criterion wanders into the functionless"* failure MCC fixes.

The mesh already has **both MCC populations, and they already coevolve**:

- **Population A = the review-AREAS** (the "mazes" — problems to review).
- **Population B = the mesh's embodied-capability set** (the "agents" — what it can already absorb).
- **The minimal criterion** is the *"novel AND learnable"* test the LITERATURE directive states and
  `mesh-vitality` already reads on the measurement side (Hughes et al., ICML 2024): an area is **viable**
  iff it still yields a mechanism the mesh does **not** already embody — i.e. a review that **lands** (a
  `docs/reviews/` artifact).
- **The coevolutionary ratchet:** every landing *adds* an embodied mechanism, raising the bar for
  "not-already-embodied," so a once-fertile area **exhausts** as the capability set absorbs it. The
  growing embodied-set is the parasite that turns old mazes trivial, forcing the area population toward
  ever-newer niches.

What was missing: nothing reads that **fitness/viability** dimension. It is distinct from everything
embodied — not MAP-Elites illumination (coverage, no fitness), not novelty-search sparseness
(behaviour-distance, no productivity signal), not the repellent (verdict-keyed dead-end mute). It is the
**positive dual of the RR-impasse detector** (`mesh-ideate`, the sparseness block), which counts *in-frame
non-progress* from `$SPLOG` — a *negative* "retire this frame" signal. MCC needs the **positive fitness
count** — *which areas are still landing* — the exact "outcome count the mesh already produces"
(`docs/reviews/` landings) that the RR-impasse block named but did not read.

## What shipped (detection — report-only)

`viability_tally()` in `scripts/mesh-ideate` reads the **landing artifacts** (`docs/reviews/*.md` — one
file per productive review, its filename carrying an area-prefix and a `-YYYY-MM-DD` stamp), buckets them
by area via `VIABILITY_MAP`, and over `VIABILITY_WINDOW_D` (30d) logs **one** measured line to `$SPLOG`:

```
MCC-VIABILITY (30d, ... Brant & Stanley 2017): FERTILE(...): <areas that landed within window> | DORMANT(...): <areas with no recent landing>
```

- **Report-only** — the measurement is the artifact; it never blocks emission (called at the top of
  `gen_literature`).
- **Honest n/a** — an absent landing corpus logs `MCC-VIABILITY n/a`, never a faked all-fertile.
- **Falsifiable `--test`** — a *recent* landing must read FERTILE; an *ancient-only* landing must read
  DORMANT. Breaking the `>= cutoff` recency test flips the ancient case to fertile → the gate goes red
  (verified: `sed 's/\$0 >= c/1==1/'` → `smoke-test: FAIL`).

Live read (2026-07-29): all 18 areas FERTILE within 30d — honest for a review-heavy window; DORMANT
detection is proven by the falsifier, and shows its value at the tail as review activity in an area dries
up.

## What is HELD (behavioral — steward/operator-gated)

The **selection** side — Brant & Stanley's actual move: bias `illum_pick()` toward **viable** areas (a
minimal-criterion filter on the illumination draw). And the **generative** half the RR-impasse block called
*"the non-computable reframe (Jaeger 2024)"*: MCC shows new problems need **not** be externally minted — a
DORMANT area is retired and a VIABLE one **spawns a variant** (mutate its angle), a coevolving population
under the minimal criterion with no external creativity.

**Why HELD:** biasing the draw is a generation-**behaviour** change (steward's, not a report), and a
dormant read must be **real, not a flap** — an area can read dormant merely because its recent reviews
happened to find it already-embodied (the honest-flap caveat every gate here carries). Detection ships;
the selection/spawn stays open for the steward. Its noise ceiling is also honest: several `VIABILITY_MAP`
regexes soft-overlap (e.g. `criticality` matches both edge-of-chaos and SOC), so the partition is a
**soft** viability signal, adequate for a report but to be tightened before it drives selection.

## One-line summary

Named MCC (Brant & Stanley, GECCO 2017), the OEE-without-archive mechanism; landed its **detection** half
as `viability_tally` — the fitness dual of the mesh's coverage-only MAP-Elites illumination and the
positive dual of its RR-impasse detector — and left the coevolutionary **selection/spawn** as a named,
no-longer-"non-computable" HELD for the steward.
