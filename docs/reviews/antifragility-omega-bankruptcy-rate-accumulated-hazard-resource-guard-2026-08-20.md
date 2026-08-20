# LITERATURE (live review) — antifragility / convexity / ruin theory (Taleb area)

**Date:** 2026-08-20 · **Angle:** an OPERATIONAL mechanism (not philosophy) · **Mind:** genome@mesh-home
**Landed in:** `scripts/mesh-resource-guard` → `node_omega_classify()` (uncommitted; steward lands)

## The concept: the OMEGA MODEL (ω-killing / bankruptcy-rate function)

Classical ruin kills the process at the first instant the surplus crosses the barrier. Parisian ruin —
which this guard already implements twice (`node_dwell_classify`, `node_drawdown_classify`) — kills only
after a **continuous** excursion outlasts a grace clock, and that clock **resets to zero the moment the
process recovers**.

The Omega model replaces both with an **accumulated hazard**. The process is allowed to keep operating
below the barrier, but while it is down it accrues bankruptcy intensity at a rate ω(x) that depends on
**how deep** it is, and death comes when the accumulated intensity exhausts an independent exponential
clock:

    τ_bankruptcy = inf{ t > 0 : ∫₀ᵗ ω(U_s) ds > e₁ },   e₁ ~ Exp(1),   ω(x) = 0 above the barrier

The integral runs over the **whole path**. It never resets on recovery — time above the barrier simply
contributes nothing — so what kills is the **total depth-weighted occupation time in the red, summed over
all excursions**, however many times the process climbs out in between. Hence the founding paper's title.

### Where it was found (real sources, read this session)

- **The model and its name:** H.U. Gerber, E.S.W. Shiu & H. Yang, *"The Omega model: from bankruptcy to
  occupation times in the red"*, European Actuarial Journal 2(2):259–272, 2012 —
  <https://link.springer.com/content/pdf/10.1007/s13385-012-0052-6.pdf> · record:
  <https://scholar.xjtlu.edu.cn/en/publications/the-omega-model-from-bankruptcy-to-occupation-times-in-the-red>
  > "we distinguish between ruin (negative surplus) and bankruptcy (going out of business) … the
  > probability of bankruptcy is quantified by a bankruptcy rate function ω(x), where x is the value of
  > the negative surplus."
- **The area is LIVE, and it is the *level-dependent* ω that is being worked on right now:**
  - D. Mata & J.-F. Renaud, *"Optimality of a barrier strategy in a spectrally negative Lévy model with a
    level-dependent intensity of bankruptcy"*, arXiv:2409.13849, **revised 10 Jul 2026** —
    <https://arxiv.org/html/2409.13849> — "the (controlled) process is allowed to spend time under the
    critical level but is then subject to a level-dependent intensity of bankruptcy".
  - A. Bodnariu, N. Engler & N. Rodosthenous, *"Outrunning the Omega Clock: A Singular Control Problem for
    Dividend Optimisation with Ruin and Time-in-Distress Default"*, arXiv:2601.21705, **30 Jan 2026** —
    <https://arxiv.org/pdf/2601.21705> — default when accumulated time-in-distress reaches an exponential
    killing time; explicitly contrasted with deterministic Parisian windows and instantaneous ruin.

Surfaced by WebSearch 2026-08-20 ("ruin theory 2026 Omega model bankruptcy rate function operational").

## Why this is somewhere we have NOT been

The guard's ruin axes were all reviewed into existence from this same area — Parisian dwell (2026-07-29),
generalized drawdown (2026-08-18), criticality boundary (2026-08-15), left-tail direction, κ-preasymptotics.
**All of them are contiguity-gated and depth-blind once crossed.** `node_dwell_classify` and
`node_drawdown_classify` both count only the **trailing run** below the barrier and `break` on the first
sample at or above it; both then treat every below-barrier sample as one unit of the same clock (depth
enters only as a coarse deep/shallow halving of the grace).

So a **sawtooth** — down, up one sample, down again, forever — resets their clock on every tooth and reads
CLEAN no matter how much of the window is spent in the red. That is the mesh's own doctrine failure
*"n-consecutive debounce has an unacceptable sequence"*: a persistence gate keyed on a **run** is defeated
by an interleaving that never lets the run start. **Death by a thousand cuts is exactly the fault the Omega
model was written for, and this guard had no axis that could see it.**

Second, depth: Parisian says a barely-below dip and a near-zero collapse are the same tick of the same
clock. ω makes the rate a **convex function of the deficit** — which is the convexity the antifragility
program actually asks for: twice as deep is 2^p times as lethal, not twice as long.

## The concrete application — `scripts/mesh-resource-guard`, `node_omega_classify()`

Over the LONG MemAvailable history (n=64 × 120s ≈ 2.1h), with the **same barrier fold** as its sibling
(max(generalized-drawdown level ξ(peak), absolute barrier), naming the binding one):

    f_i = (B - U_i)/B                       # deficit as a fraction of the barrier
    H   = Σ_i (f_i / FREF)^p · Δt / d0      # accumulated hazard — NEVER reset on recovery
    P(bankruptcy over the window) = 1 - e^(-H)

**Calibration is anchored to its own sibling, and the anchor is named:** at deficit fraction `FREF`
sustained continuously, hazard accrues at exactly one clock per `d0` — so Omega and Parisian fire together
on the excursion Parisian was built for, and diverge only where Parisian is structurally blind (intermittent,
or deeper/shallower than the reference). Defaults `FREF=0.5` (the same half-barrier depth the siblings call
"deep"), `p=2` (convex), `d0=RG_DWELL_CLOCK_S=300`.

Verdicts (report-only, same posture as every sibling — no kill, no defer, no board post):
`ruin` H≥1 (rc 0) · `hazard` H≥0.35 (rc 2) · `clean` (rc 1, incl. H=0) · `n/a` (rc 3, never clean).

**Honest limits, published in the reading itself:** H is a hazard over the **observed window only** (never
"since boot"), computed as a rectangle-rule quadrature at the sampling interval — an excursion shorter than
one interval is invisible to it exactly as to every other axis here. The reading prints
`n=…, ~…m window, …s quadrature` so the narrow claim cannot be read as the wide one. There is **no
persistence floor by design** — a run-length floor would re-impose the very contiguity gate this axis
removes; the consequence (a lone sample can reach H≥1 only at deficit ≥0.79) is asserted in the gates.

## Artifacts

**Live reading on mesh-home, first run** — and it already says something its siblings could not:

    NODE-DRAWDOWN (draw-down Parisian ruin): … below the drawdown level for 1200s … SUSTAINED
    node-omega: accruing: H=0.85 (P=57%, floor 0.35) over 5 excursion(s), 6720s in the red,
      longest single 2400s; deepest 24% below the barrier; peak 29970MB over n=64 (~128m window,
      120s quadrature), xi=peak-25%=22477MB, abs=3201MB, binding=drawdown, omega=(deficit/0.50B)^2 per 300s

The Parisian axis sees the **current 1200s run**. Omega sees that **6720s of a 7680s window** — 87% of it —
has been in the red across **5 separate excursions**. Same node, same barrier, same moment: one axis reports
an episode, the other reports that the episode is the node's normal condition.

**Gates (`--test`, 11 assertions), all seen RED before green** — three mutants run from a scratch copy:

| mutant | what it breaks | gate that killed it |
|---|---|---|
| `H=0` on recovery | re-imposes the Parisian contiguity gate | sawtooth-ruin, Parisian-invisible marker, contiguity-independence, convexity ratio, hazard tier (5 gates) |
| `p=1` (linear ω) | drops the convexity | depth-weighting, convexity ratio (H ratio 2.0, needs 4.0) |
| `H += const` per red sample | drops the depth weighting entirely | depth-weighting, convexity ratio (ratio 1.0) |

The load-bearing gate is the **both-ways CONTROL**: the sawtooth fixture must read `ruin` under Omega while
**both** `node_drawdown_classify` and `node_dwell_classify` read CLEAN (rc 1) on the identical series — if
they ever agree, this axis is decoration. Its twin leg asserts the **contiguous** version of the same 6
samples is ruin under drawdown too, so Omega is a superset and not a sawtooth-only gimmick.

## Not discarded — the one thing deliberately left out

`--alert` board escalation. One hazard reading needs trend before it can gate, exactly as its siblings do;
the axis ships read-only in `--status` first.
