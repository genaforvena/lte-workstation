# FEP / active inference — solenoidal flow: the half of the Helmholtz decomposition we never built

**Area:** the free energy principle & active inference (Friston)
**Angle:** an OPERATIONAL mechanism it proposes (not just philosophy) we could implement
**Date:** 2026-08-18 · **Lane:** LITERATURE (live review) · **Organ touched:** `scripts/mesh-ideate` (`illum_pick`)

---

## 1. The mechanism, and where it was found

**Solenoidal flow** — the divergence-free (conservative, rotational) half of the generalised
Helmholtz decomposition of any flow that maintains a non-equilibrium steady state.

> Friston, K., Da Costa, L., Sajid, N., Heins, C., Ueltzhöffer, K., Pavliotis, G.A., Parr, T.
> **"The free energy principle made simpler but not too simple."** *Physics Reports* **1024** (2023) 1–29.
> https://doi.org/10.1016/j.physrep.2023.07.001 — read in full from
> https://discovery.ucl.ac.uk/id/eprint/10175520/1/1-s2.0-S037015732300203X-main.pdf

Equation (6), §3:

```
ṗ(x) = 0  ⇔  f(x) = Q(x)∇ℑ(x)  −  Γ∇ℑ(x) − Λ(x)          ℑ(x) = −ln p(x),  Q = −Qᵀ
                   \___solenoidal___/  \____gradient____/
```

Their gloss, verbatim:

- "The first (conservative) part of the flow is a **solenoidal circulation on the isocontours of the
  steady-state density** (or surprisal). This component **breaks detailed balance** and renders the
  steady-state density a nonequilibrium steady-state density." (§3, after eq. 6)
- "biological behaviour may be characterised by internal solenoidal flows that **do not change
  variational free energy — or surprisal — and yet move on the internal (statistical) manifold** to
  continually update Bayesian beliefs about external states." (p. 18)
- "the **mixing afforded by solenoidal flow can render gradient descent more efficient**" — their
  sugar-in-coffee image: stirring does not push sugar down its own gradient, it makes the gradient
  descent work. (p. 17, refs [112–116])

Those refs are the operational content, and they are not metaphor — they are the non-reversible
sampling literature, with a shared author (Pavliotis) on both sides:

- [113] C.-R. Hwang, S.-Y. Hwang-Ma, S.-J. Sheu, **"Accelerating diffusions"**, *Ann. Appl. Probab.*
  **15**(2) (2005) 1433–1444.
- [114] same authors, **"Accelerating Gaussian diffusions"**, *Ann. Appl. Probab.* **3**(3) (1993) 897–913.
- [115] T. Lelièvre, F. Nier, G.A. Pavliotis, **"Optimal non-reversible linear drift for the convergence
  to equilibrium of a diffusion"**, *J. Stat. Phys.* **152**(2).

Their common result is the one sentence this review turns on: **adding a divergence-free drift leaves
the target measure exactly invariant while reducing mixing time and asymptotic variance.** You get the
tail for free — the mean costs nothing.

**Not already embodied.** `grep -rliE 'solenoidal|helmholtz|detailed balance|non-equilibrium steady|
Bayesian mechanics'` over all 209 files in `docs/reviews/` returns **0**. The ten prior `fep-*` reviews
cover epistemic value, ambiguity, precision allocation, model expansion/reduction, dark-room priors and
the entropy regulariser on action — all of them terms *inside* free energy. None of them is the
decomposition of the **flow**, and none is the conservative term.

## 2. Where it applies: `scripts/mesh-ideate`, `illum_pick()`

This lane's own selector. `illum_pick` chooses the next literature niche from the 18 areas × 6 angles =
108-cell grid. Since 2026-07-28 it implements MAP-Elites illumination: target the **global-minimum
coverage** cell. That is exactly `−Γ∇ℑ` — the gradient term, and only it. Ties were then broken with
`shuf`: an i.i.d. draw, i.e. the **reversible** move that respects detailed balance.

**On this grid the tie is not an edge case, it is the operating regime.** Live archive, 2026-08-18
(`~/.mesh/.ideate-illumination`, 500 emissions at the `ILLUM_MAX` cap, all 108 cells covered):

| coverage in window | 3 | 4 | 5 |
|---|---|---|---|
| cells | 1 | 38 | 69 |

Range 3–5 around a mean of 4.63. The gradient is essentially **flat**; after the single coverage-3 cell
is consumed, a 38-way tie decides the pick. Almost every draw this lane makes is settled by the
tie-break, not by the gradient — which is to say, by the one component the FEP says must not be i.i.d.

## 3. Measurement — including the half that failed

Simulated both tie-breaks on the real 108-cell grid with the real `ILLUM_MAX=500` rolling window,
40 seeds × 3000 draws:

| tie-break | cover all 108 | worst revisit gap | mean gap | sd(window coverage) |
|---|---|---|---|---|
| `shuf` (reversible) | **108 draws** | **379.5** (max 467) | 106.9 | 0.487 |
| circulating (solenoidal) | **108 draws** | **108.0** (max 108) | 108.0 | 0.483 |

**The coupon-collector story I started with is FALSE, and it is recorded here rather than quietly
dropped.** I expected random tie-breaking to cost `k·H(k) ≈ 571` draws to sweep the grid against 108 for
a rotation. It does not: the min-coverage gradient already forces a perfect first sweep, so cold-start
coverage is **identical**. MAP-Elites had already bought that win in July. Had I asserted the 5.3×
without simulating it, this review would have shipped a number that the code refutes.

What survives is sharper for having been narrowed. **The entire difference is in the tail.** Same
stationary distribution (mean gap 107 vs 108 — the invariance property, measured), same coverage spread
(sd 0.487 vs 0.483), and yet the random rule lets a niche go dark for **4.3× the grid period**. At this
lane's measured rate (209 reviews between 2026-07-06 and 2026-08-18 ≈ 5/day) that is a cell unvisited
for **~93 days** against a guaranteed **~22**. Precisely the non-reversible-sampling result: *invariant
measure untouched, variance not.*

### The shape worth keeping

**Every aggregate we hold looks identical under the two rules.** Mean gap, coverage sd, cold-start
coverage — all unchanged; only the worst-case tail moves. A coverage sense that reports the mean is
structurally blind to the starvation it exists to prevent. Sibling of
`an-unmatched-category-leaves-the-denominator-so-the-ratio-inverts` and of the PSI window finding: an
even-looking average can hide a starving tail.

## 4. Shipped

`scripts/mesh-ideate` (genome source, uncommitted — steward lands):

- **`illum_pick`** now ranks cells by `(coverage asc, staleness asc, grid order)` and takes the Nth.
  Among min-coverage cells it takes the **least recently emitted** — a deterministic antisymmetric
  rotation *on the isocontour*. It never leaves the contour (the gradient's choice is fully respected,
  MAP-Elites is preserved exactly, not approximated), visits every tied cell once per cycle, and its
  long-run marginal over the tie is uniform. One `awk` pass over the archive replaces the previous
  108 `grep -c` scans.
- **`gen_literature`** walks the ranking (`illum_pick "$tries"`) instead of re-calling it. This is the
  one thing `shuf` was silently providing: a deterministic pick would return the *same* rejected cell on
  every `recent_has` retry and stall into the relax path. Rank *n* = the next cell along the contour, so
  a rejection now **advances** the circulation.

### Gate, seen RED

New `--test` leg: seed the archive with all 108 cells emitted once in **reverse grid order** (so grid
order cannot fake a pass), leaving every cell tied at coverage 1 with staleness as the only signal. Six
successive picks must come out in exactly the seeded order with no repeat, and `illum_pick 2` must
differ from `illum_pick 1`. Mutants run from a scratch copy:

| mutant | result |
|---|---|
| revert the tie-break to `shuf` (the exact pre-fix code) | RED — "must circulate oldest-first" |
| zero the staleness axis in the awk | RED — same leg |
| ignore the rank argument (always rank 1) | RED — "does not walk the ranking" |

Full suite green after: 20/20 legs including the existing MAP-Elites unique-minimum gate, which still
passes — the gradient term is untouched.

## 5. Held, not shipped

The FEP's stronger claim is that solenoidal flow is what makes a system **itinerant** rather than
fixed-point — "precise particles exhibit solenoidal behaviour such as oscillatory and (quasi) periodic
orbits", the central-pattern-generator reading (p. 17–18). That suggests every argmax selector in the
mesh is a candidate, not just this one. Two were checked and **discarded honestly**:

- `mesh-feed:pick_local` — draws are **without replacement** (the winner is served and leaves the
  backlog), so there is no mixing penalty to remove. The existing `shuf` drift tie-break is right there.
- `mesh-generate:pick_open_idea` — the STUDY-yield argmax is a real pure-gradient selector with a real
  degeneracy (14 of 19 fields tied at exactly `0.333`, ties held by FIFO forever), **but it is currently
  dormant**: 0 open `STUDY(` lines in the queue. Recorded as a latent structural gap, not claimed as a
  live one.

---

**Self-reference, noted:** the cell this review occupies is
`the free energy principle & active inference (Friston)` × `an OPERATIONAL mechanism it proposes` — cell
(3, 5) of the grid whose selector it just repaired.
