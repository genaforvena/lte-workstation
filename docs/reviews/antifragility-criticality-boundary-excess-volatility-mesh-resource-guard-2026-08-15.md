# The criticality boundary and excess volatility — the fragility verdict's moving operating point

**Date:** 2026-08-15 · **Area:** antifragility, convexity & ruin theory (Taleb) · **Angle:** a known critique
**Organ:** `scripts/mesh-resource-guard` — new `node_criticality_classify()` axis (report-only)

## The critique

Every landing in this area so far reads a system's *character* — convexity (`mesh-convexity`), left-tail
direction, damage-response sign, joint-failure amplification, degeneracy (`mesh-sensorium`), Parisian dwell
(`mesh-resource-guard`) — **at the operating point the system happens to occupy**, and treats that point as
given.

> **Martin, Moran, Panja & Bouchaud, "Fragility-Resilience Trade-off and Excess Volatility in Supply Chain
> Networks", arXiv:2601.20450** (submitted 28 Jan 2026, revised 9 Jul 2026)

shows the point is not given. In a production network with non-substitutable inputs and precautionary
inventories there is a **critical boundary** in the space of (shock volatility, buffer): above it the
economy absorbs shocks and fluctuates mildly; below it cascading shortages make system-wide crisis
inevitable. Two results are the critique:

1. **The operating point drifts toward the boundary on its own.** "Because inventories are costly,
   competitive pressure drives firms toward the fragility boundary: a resilience-efficiency trade-off
   emerges, putting the gains from lean supply chains at risk." A "ROBUST" verdict is therefore a statement
   about a point that is *moving*, and moving the wrong way.
2. **Near the boundary the variance diverges, not the mean.** "Close to the threshold, aggregate output
   volatility diverges through network-mediated amplification of purely idiosyncratic shocks" — their
   concrete mechanism for the *small shocks, large business cycles* puzzle. So the announcement of the
   boundary is in the **fluctuation**, and any detector watching the mean path is structurally blind to it.

(They also show supplier **diversification** shifts the threshold and, if abundant enough, removes the
fragile regime entirely — the `mesh-sensorium --degeneracy` direction. Not taken here: one axis per landing.)

## The gap — and it is not academic on this node

Every `node-*` axis in `mesh-resource-guard` reads the mean path:

| axis | reads |
|---|---|
| `node_pressure_classify` | the level |
| `node_accel_classify` | is the drop accelerating (2nd derivative of the level) |
| `node_tau_eta` | time-**TO** the barrier, extrapolating the smoothed rate |
| `node_dwell_classify` | time-**SINCE** crossing (Parisian) |

None reads the **fluctuation amplitude**, and none asks whether that amplitude depends on the level.

Measured cost of that blindness, from this node's own `~/.mesh/resource-guard.log`:

- **467** `NODE-ACCELERATING` posts, **every one** carrying an `ETA-to-zero` (median **220 min**, min 4 min)
- lowest `MemAvailable now` ever printed across all of them: **2508 MB** — zero was never approached

The ETA is an honest *conditional* ("at current rate"). But in a high-variance, level-independent regime the
condition essentially never holds, so the number carries no information about ruin risk — and nothing in the
tool said so. The four axes agreed with each other because they are four readings of the same quantity.

## The axis

`node_criticality_classify()` over a **long** buffer history — deliberately its own file, not the 4-sample
`accel_series` whose size is load-bearing for accel/tau/dwell (the recovery-curvature HELD block names this
same prerequisite and forbids bending it).

- `CV = sd/mean` of the buffer — is it fluctuating at all?
- `A = mean|Δ| below the median level ÷ mean|Δ| above it` — does the swing **grow as the buffer falls**?
  A non-parametric read of "volatility diverges approaching the boundary": no distributional assumption,
  and no need to know where the boundary is.

| condition | verdict | rc |
|---|---|---|
| CV ≥ floor and A ≥ 1.50 | `critical` — excess-volatility precursor, near a criticality boundary | 0 |
| CV ≥ floor and A < 1.50 | `volatile` — swings hard, level-independently; **and τ's drift extrapolation does not apply here** | 2 |
| CV < floor, too few samples, degenerate split | silent | 1 |

## Live measurement (before wiring)

6 days of unbiased 10-minute `sar -r` `kbavail` from `/var/log/sysstat` (n=299, 291 adjacent pairs), fed
through the shipped function:

```
volatile|MemAvailable swings hard but LEVEL-INDEPENDENTLY (A=1.03 < 1.50: mean swing 1138MB below the
median level vs 1105MB above it; CV=0.22 over 299 samples) — no criticality boundary in view; any tau ETA
above extrapolates a drift this regime does not have, so it is a conditional rate, not a forecast
```

Cross-checks on the same data: A=0.92 by median-of-deltas, **0.62** bottom-vs-top quartile. The buffer swings
±4 GiB around 18 GiB and the swing does **not** grow as it falls. This node is **VOLATILE-STABLE** — real
volatility, no criticality signature — which is precisely the qualification the 467 ETAs needed.

The honest negative is what makes the axis worth having: it is not a rubber stamp.

## Verification

`--test`: 6-case battery — `growing-swing` → critical · `level-independent` → volatile ·
`calm-below-cv-floor` → silent · `degenerate-level-split` → silent · `too-few-samples` → silent ·
`empty` → silent; plus long-history push/trim asserted **separate** from the accel series.

Four mutants, each run from a scratch copy, each RED on its own case:

| mutant | case that went red |
|---|---|
| `cv < CVF` → `cv < -1` (CV floor deleted) | `calm-below-cv-floor` |
| `A = ml/mh` → `A = 1.0` (split-half comparison deleted) | `growing-swing` |
| `m < MINN` → `m < 1` (sample floor deleted) | `too-few-samples` |
| `nl==0 \|\| nh==0` → `0` (degenerate-split guard deleted) | `degenerate-level-split` |

**Trap paid, twice, in mirror image.** The first `calm` fixture used two *identical* level regimes, so it was
rejected by the degenerate-split guard, not the CV floor — the CV-floor mutant stayed green. Separating the
two cases, the *new* degenerate fixture then had an amplitude *below* the CV floor, so it was swallowed
there instead and the degenerate mutant stayed green. Two silent paths shadowing each other, each fixture
passing through the wrong branch. Both now carry the amplitude/level that forces the intended guard, and the
comment in the source says why the numbers are what they are.

## Also fixed (found by the new code path)

`accel_series()`/`long_series()` used `tr '\n' ' ' < "$FILE" 2>/dev/null`. The `2>/dev/null` guards *tr's*
stderr; it does **not** silence a failed redirect, which bash reports itself before tr runs. With
`.rg-memhist-long` not yet created, `--status` printed
`scripts/mesh-resource-guard: line 656: ...: No such file or directory` into its output. Both functions now
test the file first — `accel_series` had the same latent bug on any node whose history did not exist yet.

## Posture and boundaries

Report-only, same as `NODE-ACCELERATING` and `NODE-DWELL`: no kill, no defer, no board post. Live reading is
honest `n/a` until the long history fills (~2.1h at the `*/2` cadence); the sar series above is validation,
not the axis's own artifact, and is deliberately **not** seeded into the history — mixing a 10-minute cadence
into a 2-minute one would change what `|Δ|` means.

Distinct from: `node_accel` (mean-path 2nd derivative vs amplitude about the path) · `node_tau_eta` (this
*qualifies* τ, it does not replace it) · `node_dwell` (below-barrier persistence) · `mesh-convexity` (Jensen
gap of a distribution's shape vs level-dependence of dispersion in a time series) · the CSD/thermal lane
(lag-1 autocorrelation on a thermal series).

**Not taken:** the paper's diversification result (threshold shifts with supplier abundance) — that is a
`mesh-sensorium --degeneracy` question, and belongs to its own landing.

## Cite

Martin, Moran, Panja & Bouchaud, *Fragility-Resilience Trade-off and Excess Volatility in Supply Chain
Networks*, arXiv:2601.20450 (28 Jan 2026, rev. 9 Jul 2026). Found via WebSearch 2026-08-15.
