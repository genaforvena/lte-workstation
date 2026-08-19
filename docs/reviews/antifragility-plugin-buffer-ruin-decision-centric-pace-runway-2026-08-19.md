# Antifragility / convexity / ruin live review — THE NAIVE PLUG-IN BUFFER IS NOT A δ-CONTROLLED CLAIM

**Date:** 2026-08-19 · **Lane:** LITERATURE (live review), idea-queue · **Landed in:** `scripts/mesh-pace`
(`--runway`, report-only) · **Status:** uncommitted in the tree, steward lands.

## The search (what "live" meant here)

Prior art here is deep — 11 antifragility reviews, `mesh-convexity` (κ, CAFE Jensen gap, Taleb–Douady
left tail, Sontag log-rate — the last landed **today**), `mesh-resource-guard` (Parisian ruin dwell,
generalized drawdown barrier), `mesh-sensorium` (degeneracy vs redundancy). So the sweep went to the
**live arXiv listing** rather than a reading list: `all:antifragility`, `all:"ruin probability"`,
`abs:"tail index" AND abs:estimation`, sorted by submission date, via the arXiv API.

Recorded as checked and **not** landed:

- *Beyond Resilience: Antifragility in Critical Infrastructure Cybersecurity* (arXiv:2607.29550,
  2026-07-31) — its bounded definition is Jensen-gain based, i.e. the axis `mesh-convexity` already is.
- *On the Expected Maximum Deficit and the Optimal Allocation of Reserves* (arXiv:2605.16448) — the
  interesting half is allocation across **multiple** lines; the mesh has one budget, so it would be a
  model with no second line to allocate to.
- Cirillo & Taleb's **maximum-to-sum plot** / shadow moments: genuinely unembodied (no "moment
  existence" instrument anywhere in the genome), but the literature is 2015–2020. Unexplored ≠ live.
  Left as a named opening.

## The concept we did not embody

> **Yf Henkes, Bart P. G. van Parys & Bert Zwart, "Decision-Centric Large Deviations for Data-Driven
> Capital Buffers in Ruin Models", arXiv:2607.17732 (submitted 2026-07-20).**

A ruin model whose law is **unknown**. The decision maker sees a statistic `Q_n` from `n` historical
observations and must choose a buffer `C_n = n·f(c, Q_n)`, where `c = log(1/δ)/n` couples the amount of
data to the tolerated ruin probability `δ`. The classical safe buffer is inversely proportional to the
adjustment coefficient `γ` — the exponential rate at which the ruin probability decays — and when the
law is unknown, `γ` must be **inferred**. Their result, verbatim:

> "We show that the naive plug-in rule fails to achieve the prescribed logarithmic decay exponent `c`,
> illustrating the adverse impact of model uncertainty when making decisions under rare-event
> constraints."

The safe profile `f*` must charge the **statistical cost of having observed an atypical sample**
against the future ruin exponent that decision induces; rules strictly below `f*` are, under mild
conditions, *unsafe*.

## Where the mesh is exactly the naive plug-in — measured

`mesh-pace`'s `runway_state()` (landed 2026-07-31, the mortality-manifold read) estimates the $-burn
from **one interval** — a two-sample difference — and then classifies HEADROOM / APPROACHING /
COMMITTED, a rare-event decision about whether a dispatch HOLD can still bite, **as if that rate were
the truth**. Nothing anywhere accounts for the estimate being an estimate.

Measured on this node's own double-entry ledger — 267 hourly `inference feed` windows in
`~/.mesh/ledger/2026.journal`, 2026-07-24 → 2026-08-19, burn $36.98/h mean, $301/h max:

| statistic of `r = burn(t+1) / burn(t)` | value |
|---|---|
| P(next hour exceeds the plug-in rate) | **0.515** |
| P(next > 2× plug-in) | 0.162 |
| P(next > 5× plug-in) | 0.060 |
| q0.50 / q0.90 / **q0.95** / q0.99 | 1.04 / 3.19 / **5.57** / 179.7 |
| max | 589× |

So a HEADROOM verdict off a point burn is not "safe at δ" for any δ a reader would recognise — it is a
**coin flip whose error is fat-tailed**. That is the plug-in failure the paper proves, in our own data.

## What was built (report-only — nothing gates)

`scripts/mesh-pace`: `runway_ratio()` + `runway_safe()`, rendered by `runway_line()` (so `--runway` and
`--status` both carry it):

- the inflation is **not a tuned constant** — it is the mesh's own empirical exceedance ratio at δ: the
  (1−δ) **upper** quantile of `r` over the ledger's hourly windows (live: **5.57×**, n=266);
- `safe_burn = burn × factor`, the class recomputed at that rate, and a disagreement **named**:
  `PLUG-IN-OPTIMISTIC: the point-burn class (HEADROOM) is one the safe rate does not support`;
- the paper's coupling is printed, not implied: `c = log(1/δ)/n` appears in the line, so the reader can
  see the claim is only as strong as the data behind it;
- honest degradation: no ledger, or fewer than `MIN_R` ratios, renders the safe leg **n/a** *and says*
  `the class above is a PLUG-IN estimate, NOT a δ-controlled claim`. A missing journal must never
  quietly become factor 1.00, which would print agreement it never had.

**Live rendering on mesh-home at 21:17:35Z** (the real `--runway`, not a fixture):

```
budget-runway: spent=$337.8025 cap=$900 burn=$63.6988/h eta=8.8h class=HEADROOM — cap 8.8h off ...
  plug-in-risk: safe=APPROACHING at $354.8023/h (plug-in burn × 5.57x, the δ=0.05 exceedance ratio
  of this ledger, n=266, c=log(1/δ)/n=0.0113) eta=1.6h — PLUG-IN-OPTIMISTIC: the point-burn class
  (HEADROOM) is one the safe rate does not support
```

The plug-in says the cap is 8.8 hours away — comfortably beyond the 5h window, so *rolling relief keeps
spend under it*. At the rate this ledger's own history says is exceeded 5% of the time, it is 1.6 hours
away, i.e. inside the window and avertable only if a HOLD is placed. Same moment, same data, two
different budget portraits — and until now only the optimistic one existed.

## A defect the live run caught (and the fix)

The first live rendering read `class=HEADROOM` with `no projection to inflate in class=HEADROOM`.
Cause: `runway_safe()` called `runway_state()` a **second** time, and `runway_state` *persists a sample
on every live call* — so the second call consumed the baseline the first had just written and came back
UNKNOWN. A probe that mutates what it measures. `runway_safe` now takes the plug-in state from its
caller and only reads it when invoked bare.

## Gates (each seen RED first, from scratch copies)

Fixture: a synthetic ledger with a **known** ratio distribution — 38 ratios of 1.0 and 3 of 10.0
(n=41), where the δ=0.05 upper quantile is 10.00 and the **mean is 1.66**, so a mean-based inflation is
distinguishable from a quantile one.

| leg | asserts | mutant | seen |
|---|---|---|---|
| 1 | the factor is the δ upper quantile (`10.00 41`) | factor pinned to `1.00` | RED |
| 1 | ″ | quantile → mean (`1.66`) | RED |
| 2 | a HEADROOM plug-in (eta 20000s) reclassifies to `safe=APPROACHING` and is named PLUG-IN-OPTIMISTIC | the disagreement clause deleted | RED |
| 3 | below `MIN_R` ratios → `n-a 4`, count named | the MIN_R gate dropped (`2.00 4`) | RED |
| 4 | no ledger → says "NOT a δ-controlled claim", prints **no** safe class | missing journal → silent `1.00` | RED |

Control: unmutated copy `smoke-test: ok`.

## Held (deliberately not built)

The **decision** half. The paper's `f*` is a buffer *rule*; here the safe class is reported and nothing
in `eff_gap`, the gate, or dispatch reads it. Pacing behaviour stays the operator's call (the same
posture as `--burden` and `--runway` itself), and a governor that tightened on a 5.57× inflated rate
would be a materially different spend policy — argued separately, on evidence this axis has yet to
accumulate.

## Sources

- Henkes, van Parys & Zwart, *Decision-Centric Large Deviations for Data-Driven Capital Buffers in Ruin Models*, arXiv:2607.17732, 2026-07-20 — https://arxiv.org/abs/2607.17732
- Flowerday, Papa & Flowerday, *Beyond Resilience: Antifragility in Critical Infrastructure Cybersecurity*, arXiv:2607.29550, 2026-07-31 (checked, not landed)
- Lefevre & Zuyderhoff, *On the Expected Maximum Deficit and the Optimal Allocation of Reserves*, arXiv:2605.16448, 2026-05-15 (checked, not landed)
- Cirillo & Taleb, *On the shadow moments of apparently infinite-mean phenomena*, arXiv:1510.06731 — https://arxiv.org/pdf/1510.06731 (the maximum-to-sum / moment-existence opening, still unembodied)
