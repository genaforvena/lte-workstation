# Swarm intelligence & stigmergy — live review: influence is a DIRECTED quantity, and its scale is EXTRACTED

**Date:** 2026-08-19 · **Mind:** genome · **Area:** swarm intelligence & stigmergy
**Angle the task asked for:** the concrete METRIC the area measures itself with — here, the
information-theoretic measurement of *who influences whom* in a moving collective.
**Landed:** `scripts/mesh-leadlag` — a NET DIRECTED ASYMMETRY gate + a sweep-edge (railed delay) flag.
Uncommitted in the tree; steward lands.

---

## The source (live, read, cited)

**Udoy S. Basak, Sulimon Sattari, Iacopo Hachen, Iain D. Couzin, Liang Li — "Decoding Spatial and
Temporal Influence in Collective Behavior Using Information Theory."** In *Swarm Intelligence: 15th
International Conference, **ANTS 2026***, Darmstadt, Germany, 8–10 June 2026. LNCS **16515**,
ch. 8, **pp. 95–108** (title / authors / DOI / pages independently confirmed via ouci.dntb.gov.ua).
doi:[10.1007/978-3-032-26123-6_8](https://doi.org/10.1007/978-3-032-26123-6_8) · published 2026-05-22 ·
**Best Paper Award, ANTS 2026**
([announcement](https://www.exc.uni-konstanz.de/collective-behaviour/news-and-events/news/details/konstanz-collective-behaviour-research-takes-centre-stage-at-ants-2026-and-wins-best-paper/),
Cluster of Excellence Collective Behaviour, Konstanz · [proceedings](https://ants2026.org/) ·
[Springer volume](https://link.springer.com/book/10.1007/978-3-032-26123-6), 21 full + 21 short papers
from 93 submissions).

Found by live web search (not a fixed list): the ANTS 2026 proceedings are two months old at the time
of this review, and this is the volume's prize paper.

## The metric

The paper's method is that **the two scale parameters of social influence are MEASURED, never
assumed**:

- **time-delayed mutual information**, swept over the delay, extracts the **optimal temporal
  influence delay** — the τ at which one individual's state most reduces uncertainty about
  another's future;
- **distance-constrained transfer entropy**, swept over the distance cutoff, extracts the **spatial
  influence range** — the radius within which social information actually transfers.

The operative word is transfer *entropy*: a **directed** quantity. Direction in this framework is
established by netting X→Y against Y→X — not by taking the largest number in one direction's sweep.

## What the mesh already embodies (checked, skipped)

This lane is well travelled, so the check came first:

- `swarm-stigmergy-pheromone-entropy-foraging-evenness` (2026-07-27), `swarm-no-entry-repellent`
  (2026-07-27), `swarm-density-adaptive-evaporation` (2026-07-28), `swarm-tunable-quorum-speed-accuracy`
  (2026-07-28), `swarm-cross-inhibition-value-sensitive-dispatch` (2026-07-28),
  `swarm-response-threshold-division-of-labour` (2026-07-28), `swarm-ant-mill-positive-feedback-trap`
  (2026-07-28), `swarm-sematectonic-vs-sign-based-stigmergy` (2026-07-29),
  `swarm-interaction-rate-closed-loop-forager-drive` (2026-07-30),
  `swarm-collective-gradient-margin-vantage-fusion` (2026-07-30),
  `swarm-fundamental-diagram-retrograde-capacity-promises` (2026-08-04) — which already closed the
  *marginal-gain / retrograde-scaling* angle, so ANTS-adjacent
  [arXiv:2512.23431](https://arxiv.org/abs/2512.23431) (scalability-aware swarm allocation) was
  **discarded as already embodied**.
- On the measurement side: `mesh-leadlag` already sweeps lags {1,2,3,4,6,8} bins with a persistence
  baseline and a global-max permutation null; `mesh-cooscillate` does same-time co-oscillation and
  names transfer entropy in its header as a gap; `mesh-closure` runs Granger LLR over the *static*
  dependency graph; `mesh-dnb` cites CNM-GC/CNM-TE as literature.

So the delay sweep is embodied. **The DIRECTION test is not, anywhere in the genome.**

## The gap (a real defect, not a decoration)

`mesh-leadlag`'s statistic is

```
eff(X→Y, k) = |corr(ΔX_t, ΔY_{t+k})| − |corr(ΔY_t, ΔY_{t+k})|
```

It is directed *by construction*, so it always names a leader — **including for a pair that has
none.** A pair whose cross-correlation function is symmetric about zero lag (one driver reaching a
channel by two paths, multipath, a shared schedule offset both ways, mutual coupling) satisfies

```
eff(X→Y, k) ≈ eff(Y→X, k)
```

and neither existing guard sees it: `|r|` is high, and the persistence baseline is ~0 because a
white-driven channel does not predict its own future. Worse, the scan iterates **ordered** pairs and
de-dupes per **directed** key — so both directions can be emitted as two separate findings.

## The landing — `scripts/mesh-leadlag` (uncommitted)

1. **Net directed lead.** `scan()` now evaluates every ordered pair once and nets each direction
   against its own reverse at the same lag: `net = eff(X→Y,k) − eff(Y→X,k)`. `net` is the statistic
   the global-max permutation null is computed on and the one candidates are gated on
   (`LEADLAG_ASYM`, default 0.10). A symmetric pair nets ~0 and is now honest-empty instead of a
   fabricated leader. Cost: **zero extra work** — both orders were already being evaluated; the
   reverse leg is a dict lookup. Reverse not evaluable → `eff_rev = 0` (no counter-evidence,
   deliberately permissive).
2. **The emitted idea reports the decomposition** — `net directed lead 0.65 = fwd 0.83 − reverse
   0.18` — so a reader can see how one-way the lead actually is, rather than one number that hides it.
3. **Sweep-edge flag** (same paper's "extract the delay" point): if the winning lag is the largest
   swept, the profile has not peaked inside the window, so the text says the delay is a **LOWER
   BOUND, not a measurement**, instead of quoting the edge as the answer
   (`a-railed-axis-is-a-perfectly-formed-integer`).

## The artifact (seen red, then green)

New `--test` leg plants two pairs in one log: `Lead1 → Lead2` (genuinely one-way) and
`MutualP ↔ MutualQ` (one white driver W reaches MutualQ 2 bins **early and** 2 bins **late**;
MutualP sees it now). It asserts **both** directions — that the fixture is a real trap with the gate
disabled, and that the trap is gone with it on.

With the gate deliberately broken (`if net<ASYM` → `if False`), the pre-fix behaviour is exactly the
predicted one — two contradictory findings from one leaderless pair, both clearing every older guard:

```
0.0303  leadlag:MutualP:MutualQ  ... MutualP movement PREDICTS MutualQ movement ~10 min later
        (r=0.72 at lag 2 bins; net directed lead 0.00 = fwd 0.62 − reverse 0.61; beats MutualQ
        self-prediction r=0.11; 117 aligned Δ-steps; perm p=0.005)
-0.0303 leadlag:MutualQ:MutualP  ... MutualQ movement PREDICTS MutualP movement ~10 min later
        (r=0.73 at lag 2 bins; net directed lead -0.00 = fwd 0.61 − reverse 0.62; ...)
smoke-test: FAIL
```

Restored, the whole suite is green and the genuine `Lead1 → Lead2` still survives:

```
smoke-test: ok (recovered WatchA→LampB @10min lag; wifi APX→APY; cross-node iMac-SHARED→local-SHARED
@10min lag; noise rejected by permutation; 1 finding; directed seed; floor-gate holds)
```

## Honest limits

- **No live symmetric pair is quoted, because there is none to quote right now**: `mesh-leadlag --dry`
  on the real tapes is honest-empty at 18:00Z and 18:06Z today (nothing clears the permutation null),
  so the change is verified against planted fixtures only. The claim that the RF tapes *produce*
  symmetric pairs rests on `mesh-cooscillate`'s existing `[common-mode]` class, not on a leadlag
  observation — stated as the inference it is.
- **This is correlation-based netting, not transfer entropy.** The paper's estimator is
  information-theoretic and catches nonlinear coupling that Pearson cannot; the net-asymmetry *shape*
  is what landed, at the cost of a linear estimator. A binned-TE leg on the winning pair is the
  obvious follow-on and is **not** claimed here.
- The paper's second half — *distance-constrained* TE for the spatial influence **range** — is
  **discarded for now**: the mesh's channels have no metric embedding (RSSI is a proximity proxy, not
  a distance), so a distance sweep would be a fabricated axis. It becomes real if channels are ever
  keyed by node position.
