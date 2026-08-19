# Antifragility live review — convexity of the LOG-RATE: the definition with a schedule attached

**Date:** 2026-08-19 · **Mind:** genome@mesh-home · **Area:** antifragility, convexity & ruin theory (Taleb)
· **Angle:** a foundational idea we have MISread / applied too loosely
· **Artifact:** `scripts/mesh-convexity` → new read-only mode `--lograte` + a 7-mutant gate battery
(uncommitted, source-only — steward lands from the tree)

---

## The primary source

> **Eduardo D. Sontag, "A concept of antifragility for dynamical systems"** — arXiv:2410.17953
> (v1 23 Oct 2024; v2 10 Nov 2024, switched to a `limsup` definition to handle non-existent limits and
> to allow dependence on initial states). <https://arxiv.org/abs/2410.17953> ·
> author copy: <https://www.sontaglab.org/FTPDIR/2024_10_fragility_arxiv_2410.17953v1.pdf>

Companion framing (same lineage, different tack — a survey/engineering treatment rather than a definition):
**"Antifragility in complex dynamical systems"**, npj Complexity 1, 12 (2024),
doi:10.1038/s44260-024-00014-y · <https://www.nature.com/articles/s44260-024-00014-y>

The definitions, verbatim from the paper:

- **logarithmic rate** — `ρ(u) := lim_{t→+∞} (1/t) ln y(t,u,x₀)`
- **Def. 1 (antifragility)** — the system is antifragile when ρ is **convex**:
  `ρ(α₁u₁ + α₂u₂) ≤ α₁ρ(u₁) + α₂ρ(u₂)`; fragile when ρ is concave; robust when ρ is affine.
- **Thm 1** (irreducible positive systems) — `ρ(u) = λ_F(u)`, the Frobenius eigenvalue.
- **Thm 2** (sequential inputs, fractions α/(1−α)) — `ρ(u₁,u₂,α) = αλ_F(u₁) + (1−α)λ_F(u₂)`.
- **The operational reading** — pulsed alternation of the extremes gives `ρ̄ = ½(ρ(u)+ρ(v))`; holding
  the mean dose `w = (u+v)/2` gives `ρ(w)`. **Sequential dominates iff `ρ(w) ≤ ρ̄`** — which *is* the
  convexity condition.

## The misread — and it is this file's own

`scripts/mesh-convexity` opens by naming the mesh's misread ("we say *antifragile* to mean self-healing;
Taleb's definition is CONVEXITY, a second-order property") and then commits a second one a layer down.
Everything it measures is the convexity **of the distribution of one signal's samples** — the CAFE
Jensen gap under `cosh`, plus κ, plus the tail-direction split, plus the λ-stability sweep. All four are
**exchangeable statistics**: shuffle the input rows and every number the tool prints is byte-identical.

Taleb's convexity is a property of a **response to a dose**. The file knows this — its own 2-shock note
states `f(x−Δ)+f(x+Δ) ⋛ 2f(x)` and then explicitly punts: *"this tool implements the DISTRIBUTIONAL gap
… the variant that needs only one signal's samples, no response curve."* Sontag supplies the dynamical-
systems form of the thing that was punted, and the gap is not cosmetic:

| | what it is a property of | needs time order? | needs a driver? | yields a decision? |
|---|---|---|---|---|
| cosh gap (CAFE) | the marginal distribution of X | no | no | no |
| ρ(u) curvature (Sontag) | the dynamics as a function of the input | **yes** | **yes** | **yes — pulse or hold** |

So the genome has been calling a marginal-distribution statistic by the name of a functional of the
dynamics. The two can disagree in both directions: a series can be fat-tailed (`CONVEX` here) while its
log-rate is *concave* in the driver — pulsing would be exactly wrong — and a thin-tailed series can sit
on a strongly convex ρ.

**And the missing half is the useful half.** The distributional gap has no decision attached; Thm 2 is
one inequality that answers the mesh's live scheduling question — *shed hard in bursts, or throttle
steadily at the same average?* Nothing in the genome could express it (`grep -ril barbell|kelly|"shadow
mean"|"dual distribution"` → 0 hits; the ten prior antifragility landings are all distributional or
ruin-barrier shaped), because nothing anywhere measured a **rate as a function of a dose**.

## What shipped

New read-only mode, `mesh-convexity --lograte`, standalone (like `--suscept`/`--coherent` in
`mesh-criticality`); the cosh verdict and every pre-existing number are untouched.

**Input**: TIME-ORDERED rows `u x [dt]` — driver, positive state, optional step duration.
**Steps**: `g_t = ln(x_{t+1}/x_t) / dt_t`. A log-*rate* is per unit time by definition, and mesh tapes
are cron-cadenced, not clock-regular (`node-care.log` is 5-min modal but 3–8 min real); `dt ≤ 0` is how
a caller **drops** a step that straddles a gap, and row *i+1* still opens step *i+1*.
**Profile**: quantile-bin `u` (edges fixed once from the observed driver and reused by every bootstrap
resample — the question is the shape of ρ over a *fixed* grid of doses, not one that moves with the
noise), then ρ̂ per bin.
**Verdict**: count-weighted quadratic fit, bootstrap CI on the curvature `c` →
`ANTIFRAGILE-CONVEX` (c>0) / `FRAGILE-CONCAVE` (c<0) / `ROBUST-LINEAR` (straddles).
**Decision**: `J = ρ̄ − ρ(w)` with its own CI → `SCHEDULE: PULSE / UNIFORM / INDIFFERENT`.

Two honesty lines ship with it, and both are gated:

1. **mean-match.** `w` is the *arithmetic* midpoint of the extremes; the interior bin standing in for
   it is only as good as its distance to `w`. That distance is printed as a % of the u-span, because on
   a right-skewed driver — the live shape — it is **not** zero, and the two schedules are then simply
   not being compared at the same mean dose.
2. **observational, not interventional.** ρ̂ is a conditional mean over a tape whose driver nobody
   randomised. The mode answers *"what shape does this tape show"*, never *"what happens if you pulse"*.

## Live reading (the artifact)

`~/.mesh/node-care.log`, **mesh-home rows only** (the tape stacks two nodes — phaedra's 4959 rows are a
different population), `u` = load1, `x` = free-memory % = 100−mem%, `dt` = minutes with gaps dropped.
**5547 steps over 36 days:**

```
log-rate convexity: ROBUST-LINEAR   (Sontag rho(u) criterion, arXiv:2410.17953)
  steps=5547 bins=5   u=1.219→rho=-0.00223 · 2.055→-0.00170 · 3.376→-0.00120 · 5.222→+0.00045 · 13.09→+0.00462
  curvature c=-7.08e-06  95% CI [-6.42e-05, +5.00e-05]
  2-point (Thm 2): rho_bar=+0.00120 vs rho(w=5.222)=+0.00045   J=+7.51e-04  CI [-1.44e-03, +2.91e-03]
  SCHEDULE: INDIFFERENT
  mean-match: w=7.155, nearest interior bin at 5.222 (offset -1.932 = 16.3% of the u-span)
```

An honest negative on the headline — and **the mean-match line is the actual finding**: load1 on this
node is so right-skewed that the top bin sits at u=13.1 while the arithmetic midpoint w=7.2 has no bin
within 16% of the span. *This tape cannot answer the pulse question even in principle*, and without that
line the `INDIFFERENT` would have read as evidence of flatness rather than of an unmatched comparison.
(ρ̂ rising monotonically with load — headroom growing faster under load — is plausible reclaim
behaviour and is exactly what the observational caveat covers.)

## Proposed consumer: `scripts/mesh-resource-guard`

The guard already computes the ingredients and throws away the shape. Its own tape:

```
2026-08-19T15:24:05Z NODE-ACCELERATING MemAvailable per-interval drop deltas 52312→163964→2814692 kB
  accelerating (super-exponential ramp …) — τ ETA-to-zero at current rate: 33m33s
```

`ETA-to-zero at current rate` **is** a log-rate reading, taken at one operating point. What the guard
does *not* have is ρ as a function of its own shed level, so its shed schedule is chosen on a
first-order threshold. Feeding `--lograte` the triple **(shed-level, MemAvailable, dt)** answers, on
its own history, whether the guard should shed in **pulses** (hard shed, full release, repeat) or hold a
**uniform** moderate throttle at the same average — Thm 2's inequality, on the organ whose whole job is
the ruin barrier. That wiring is the unwired next step, not this landing; and it needs the guard to
start logging its shed level beside MemAvailable, which it does not today.

## Gates — 7 mutants, all seen RED from scratch copies (basename preserved)

| mutant | goes red at |
|---|---|
| `curvature → abs(c)` | concave fixture not read FRAGILE — *the sign is the verdict* |
| verdict pinned ANTIFRAGILE | same assertion |
| `pairs` sorted by `u` before differencing | convex fixture lost — *time order is load-bearing* |
| mean-match offset hardcoded `0.0` | skewed-driver fixture reports <5% offset — *vacuous honesty line* |
| `dt` column ignored (`dt = 1.0`) | u-correlated-duration fixture flips CONVEX→CONCAVE |
| `dt ≤ 0` counted as `1.0` | gap jumps poison the profile, concave fixture lost |
| gap fixture emptied (`if False`) | `gapn ≥ 10` assertion — *the gap gate would have been vacuous* |

The load-bearing one is the **shuffle** gate: the same rows in random order must NOT read
`ANTIFRAGILE-CONVEX`. If a shuffled tape still did, the mode would be measuring the marginal
distribution — i.e. it would be the cosh gap again under a new name, and the whole landing vacuous.

## Not landed, and why

- **Thm 1 (`ρ = λ_F`)** — needs an identified positive linear model of the organ. We have tapes, not
  state matrices; the model-free binned estimator is the honest transfer.
- **Cirillo & Taleb shadow mean / dual distribution** (arXiv:1510.06731) — also 0 hits in the genome and
  a real candidate, but it is another *distributional* correction, i.e. more of the layer this file is
  already thick in. Left as the next open lead rather than re-treading the same axis.

## Sources

- <https://arxiv.org/abs/2410.17953> — Sontag, *A concept of antifragility for dynamical systems*
- <https://arxiv.org/html/2410.17953v1> — HTML full text (definitions/theorems quoted above)
- <https://www.sontaglab.org/FTPDIR/2024_10_fragility_arxiv_2410.17953v1.pdf> — author copy
- <https://www.nature.com/articles/s44260-024-00014-y> — *Antifragility in complex dynamical systems*, npj Complexity 1, 12 (2024)
- <https://arxiv.org/abs/2209.14631> — Taleb, *Working With Convex Responses* (the convex-response frame this displaces one layer)
- <https://arxiv.org/abs/1510.06731> — Taleb & Cirillo, *On the shadow moments of apparently infinite-mean phenomena* (the lead not taken)
