# RR live-review — the diametric autism↔psychosis model as a two-sided posture on the correlation miner

**Date:** 2026-07-29 · **Area:** relevance realization & the frame problem (Vervaeke) · **Angle:**
cross-domain transfer to a distributed sensor mesh · **Landed:** `scripts/mesh-correlate --posture`
(read-only, no queue write, RED-first `--test`).

## The concept (LIVE literature, not embodied)

**The diametric model of autism↔psychosis as opponent processing in relevance realization.**

> Brett P. Andersen, Mark Miller & John Vervaeke, *"Predictive processing and relevance realization:
> exploring convergent solutions to the frame problem"*, **Phenomenology and the Cognitive Sciences
> 24:359–380 (2025)**, doi:10.1007/s11097-022-09850-6. (Surfaced via web search 2026-07-29; the
> diametric axis originates with Crespi & Badcock, *Behavioral and Brain Sciences* 31:241, 2008, and is
> imported into RR by Andersen/Miller/Vervaeke.)

RR is not a specialized module but **opponent processing** — a dynamic balance between two *opposite*
pathologies of relevance, made concrete by the diametric spectrum:

- **Autism pole** — over-precision / hyper-**particularization**: every input treated as too specific,
  weak central coherence, real structure filtered out as noise → **false negatives**.
- **Psychosis pole** — under-precision / hyper-**compression** = **apophenia**: pattern and meaning seen
  everywhere → **false positives**.

Healthy RR is the *balance* between them; pathology is collapse to **either** pole.

## Why it is not already embodied

The mesh already embodies precision-weighting (`mesh-precision`), the small-world frame limit,
goal-relativity (`mesh-novelty`), the explore↔exploit and efficiency↔resiliency opponent pairs
(`mesh-needs`/`mesh-sensorium --balance`), and the demand-tracking set-point. The
compression↔particularization pair was flagged in the coverage map as *"named but folded — pick a
distinct mechanism"* (`mesh-sensorium --balance` couples tightly to it). The diametric model **is** that
distinct mechanism: it is about **pattern-detection calibration** (false-positive vs false-negative),
not resiliency depth.

Crucially, `scripts/mesh-correlate` — the mesh's actual pattern detector — is a heavily-engineered
**anti-apophenia device**: permutation null, Bonferroni over the pair family, five documented confound
classes, occasion/clock/density gates, an explicit *"default toward silence"* doctrine. **That is the
entire psychosis-pole guard, and nothing measures the other pole.** Over `correlate.log`'s 424-run
history it emitted exactly **one** finding (a clock confound). But a 0-finding run is **ambiguous**
between:

- *"no structure exists"* → correct silence, healthy; and
- *"structure exists but sits below the floor"* → the over-particularization **pathology** (autism
  pole): the accumulated suppression has swung the miner deaf.

**emit-rate and mtime cannot tell these apart.** You must look at the **effect-size distribution the
gates are throwing away.** This is the same shape as the hollow-sense / impasse blind spot
(`mesh-sensorium --impasse`) from the RR frame-*breaking* side — here on the correlation lane.
`mesh-precision` only *name-drops* the diametric model (as the caveat that its own mechanism is "one pole
of the same process"); it never instruments the balance. That instrument was the gap.

## What landed — `mesh-correlate --posture`

A read-only diametric lens that **reuses the LIFT lane's own episode-collapse + episode-lift** (so it
measures the real gauntlet's floor, not a re-derived one — no "two copies rot"). For every cross-family
pair it takes the strongest real co-occurrence lift, then reports where the miner sits:

- **OVER-PARTICULARIZED** (autism pole, rc 3) — the emit floor `MIN_LIFT` sits *above* the data's
  strongest coupling. LIFT-lane silence is **structural**, not absence of structure; 0-finding runs hide
  sub-floor couplings the gate treats as noise (false negatives).
- **APOPHENIC-LEAN** (psychosis pole, rc 4) — a large fraction (≥ `CORR_APO_FRAC`, default 0.30) of
  pairs clear the co-occurrence floor; the false-positive burden rests entirely on the downstream
  confound/Bonferroni guards.
- **BALANCED** (rc 0) — a minority carries floor-clearing structure; neither deaf nor flooded.
- **NO-DATA** (rc 0) — honest n/a; too few episodes to assess.

Report-only: no queue write, no gate change — a mirror the miner holds up to its own posture. It changes
nothing about what emits; it makes the *reason for silence* legible.

### Live read (deployed tape, 1636 rows, 2026-07-29)

```
cross-family pairs: 45 examined (>= 8 episodes), 49 data-starved (frame/coverage limit)
strongest co-occurrence lift observed: 2.40 (emit floor MIN_LIFT=1.80)
pairs clearing the floor: 2/45 (4%)  [p50 lift 1.06, p90 1.50]
VERDICT: BALANCED
```

The lens immediately earns its keep: it shows the LIFT lane's near-silence is **not** the autism-pole
pathology — 2 of 45 pairs *do* carry floor-clearing structure (max lift 2.40 > floor 1.80), so the
downstream confound guards are what decide whether those 2 emit. The 424-run silence is the **guards
adjudicating a small amount of real structure**, not a deaf detector. Before `--posture`, that
distinction was invisible.

## Verification

- `mesh-correlate --test` names **all three poles** with RED-first fixtures: a decorrelated tape reads
  OVER-PARTICULARIZED (rc 3) **plus a falsifier** (lower `MIN_LIFT` below the ceiling → verdict must flip
  off, proving it keys on floor-vs-ceiling, not on sparseness); the fully-correlated tape reads
  APOPHENIC-LEAN (rc 4); one-strong-among-noise reads BALANCED (rc 0).
- RED-first seen live: inverting the `mx < MIN_LIFT` branch made the over-particularized fixture misread
  BALANCED → `--test` FAILED (rc 1); restored → passes.
- Reuses the LIFT lane's collapse/lift inline (single source of the gauntlet's floor).

## Boundaries

Descriptive, not prescriptive — it does not auto-tune `MIN_LIFT` (that is a live gate on the mesh's only
data-driven idea lane; retuning is the operator's call). It reads the **LIFT** lane's co-occurrence floor
specifically; the PRED lane's Bonferroni/power tradeoff is the same diametric axis in a different metric
and is left for a follow-up. Left **uncommitted** in the tree for the steward to land.
