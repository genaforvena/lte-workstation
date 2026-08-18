# Home-field advantage is an INTERACTION — a home-vs-away gap is two main effects wearing its name

**Live review, genome, 2026-08-18.** Area: **niche construction & the extended phenotype**, angle the
task asked for — a **concrete METRIC / experiment the area measures itself with**. Landed as a new
report-only mode in `scripts/mesh-promises` (`--homefield`), uncommitted in the tree.

## What we already embodied (checked first)

Eight prior reviews from this area are on disk (`docs/reviews/`): the removal control / external
immunity (2026-07-28), the negative inter-scale terminator (2026-07-29), realized-heritability
inflation (2026-07-31), collective/social niche construction as network topology (2026-08-03),
driftability as a counterfactual baseline (2026-08-10), NC³ mechanism attribution — construction vs
choice vs conformance (2026-08-15), the byproduct null and the sign of the fitness feedback
(2026-08-16), and the contemporaneous reference class (2026-08-17).

Every one of those asks *whether the construction exists* or *what caused it*. None of them measures
**whether the constructed environment actually pays the constructor back, net of everything else**.
That is a different, older, and much more operational question, and the field has a standard
instrument for it.

## The concept we did not have: the home-field advantage index (HFAI)

Read live, 2026-08-18:

> **Ayres, E., Steltzer, H., Simmons, B.L., et al., "Home-field advantage accelerates leaf litter
> decomposition in forests", *Soil Biology & Biochemistry* 41(4):606–610 (2009),
> doi:10.1016/j.soilbio.2008.12.022** — the index itself, via the methods section of
> [Journal of Plant Ecology 19(1):rtaf149 (2026)](https://academic.oup.com/jpe/article/19/1/rtaf149/8250079),
> which restates the two equations verbatim.

This is niche construction with the philosophy stripped out. Litter conditions the decomposer
community beneath the plant that dropped it — the extended phenotype, in soil — and the empirical
question is whether that conditioning feeds back as a **measurable performance gain for the
constructor**. The design is a **reciprocal transplant**: both litters × both sites, all four cells.

The field is still publishing on it, which is why it qualifies as live literature and not a fixed
list:

- **[Global meta-analysis, *Plant and Soil* (2025), doi:10.1007/s11104-025-07701-2](https://link.springer.com/article/10.1007/s11104-025-07701-2)**
  — the global mean home-field effect is only **+3.0%**, with biome values from **+18.5%** (subtropical
  desert) to **−106%** (temperate rain forest). **Home-field DISadvantage is a real, published
  outcome**, not a failed measurement.
- **[Hu et al., *Functional Ecology* (2026), doi:10.1111/1365-2435.70219](https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2435.70219)**
  — high-quality litter drives a *stronger* HFA in young plantations; the drivers of its sign are
  still open.
- **[Fanin et al., *New Phytologist* (2021), doi:10.1111/nph.17475](https://nph.onlinelibrary.wiley.com/doi/10.1111/nph.17475)**
  — the phyllosphere-to-soil extension.

Sibling instrument, same shape, different substrate: **Bever's interaction coefficient**
`Is = αAA − αAB − αBA + αBB` in plant–soil feedback, where the SIGN decides coexistence vs exclusion
([Bever 2003, *New Phytologist*](https://nph.onlinelibrary.wiley.com/doi/10.1046/j.1469-8137.2003.00714.x);
still the live standard —
[Collings et al., *Ecology* (2025), doi:10.1002/ecy.70170](https://esajournals.onlinelibrary.wiley.com/doi/full/10.1002/ecy.70170)).
Both are the same move: **a diagonal-vs-off-diagonal contrast on a square matrix**.

### The two equations, and what each one kills

```
(2)  RML_Aa = Aa / (Aa + Ba) · 100
(3)  HFAI   = ((RML_Aa + RML_Bb) / (RML_Ab + RML_Ba)) · 100 − 100
```

- **(2) normalises WITHIN a site.** It divides out the **site main effect** — some sites decompose
  everything faster.
- **(3) is a ratio in which each litter appears once above and once below.** It divides out the
  **litter main effect** — some litter is simply easier.

What survives is **only the litter × site interaction**: the affinity itself. That is the concept we
did not embody, and it generalises past soil:

> **A "we do our own work best" claim is an INTERACTION term. Any measurement that lacks the full
> reciprocal matrix is measuring a main effect and calling it an affinity.**

And the corollary that makes it a doctrine shape rather than a statistic: **an unfilled off-diagonal
cell does not make the index zero — it makes it non-existent.** A design in which the routing was
always obeyed has no away cells, so the claim was never tested, only complied with.

## Where it applies: `scripts/mesh-promises` → the new `--homefield` mode

The mesh's `owner: <tool>/<window>` dispatch clause **is an untested niche-construction claim**: that a
window conditions a domain it then works better in. Two existing modes come close and neither asks it:

- `--transversality` counts **who discharged whose** (live board: 70.9% prescribed, 19.7% diagonal,
  9.4% self) — avenues, with **no performance axis at all**.
- `--mttr` reports closure latency per family — and a per-owner median **is exactly the confounded
  main-effect number** Ayres' index exists to correct. "genome's promises close in 3h" mixes
  (a) genome being a fast window with (b) genome's tasks being easy ones.

The transplant matrix needs no new state and no new probe — the board already holds every cell:

| ecology | mesh |
|---|---|
| litter species (the thing decomposed) | the promise's **home window** — the `owner:` clause's window, else the poster |
| site (where it decomposes) | the **closer window** — who posted the settling `[done]` |
| mass loss (performance) | closure **rate**, 1/hours-open (latency floors at `MESH_HFA_FLOOR_H`=0.05h) |
| home cell / away cell | `(W,W)` / `(W,other)` |

Report-only, exit 0. Every cell `n` prints beside the index, so a 2-vs-2 HFAI can never be read as a
rate. Environment: `MESH_HFA_MIN_CELL` (default 2), `MESH_HFA_REPS`, `MESH_HFA_ALPHA`, `MESH_HFA_FLOOR_H`.

**Null.** The home labels are permuted across kept promises (home volumes preserved exactly, the
home↔site pairing destroyed). That kills the interaction while leaving **both** main effects standing —
a fast window stays fast, an easy task class stays easy. Verdicts: `HOME-FIELD` / `AWAY-FIELD` (the
disadvantage pole, which the 2025 meta-analysis says is real) / `NO-FIELD`. A permutation that leaves
no reciprocal pair contributes no value and is not counted; below 10% valid reps the null renders
`n/a` and says so, leaving the estimate standing without a significance it did not earn.

## The live reading (mesh-home board, 2026-08-18T05:27Z)

```
  naive contrast (CONFOUNDED — do not read as home-field): home n=101 median=1.2h · away n=26 median=0.3h · gap=-0.8h
  reciprocal coverage: 0/66 window pair(s) have all four cells ≥ MESH_HFA_MIN_CELL=2 (127 kept promise(s), 12 window(s))
  HFAI: n/a — no window pair is reciprocally transplanted.
```

**Zero of sixty-six window pairs are reciprocally transplanted.** 127 kept promises, 12 windows, and
not one pair has two home closures and two away closures in both directions. The owner clause has
been *obeyed* 80% of the time and *tested* essentially never.

Dropping the floor to one observation per cell buys exactly two pairs, and the tool refuses to
over-claim on them:

```
    genome  ×tg       HFAI=  -62.2%  cells: genome@genome=53 genome@tg=1 tg@genome=1 tg@tg=12
    genome  ×health   HFAI=  -57.1%  cells: genome@genome=53 genome@health=1 health@genome=3 health@health=7
  HFAI pooled = -59.6%  ·  null: HFAI_exp=+8.3% · p=0.0830
  verdict: NO-FIELD — indistinguishable from chance: the owner clause routes work, it does not (measurably) speed it
```

A hint of home-field **dis**advantage that does not clear the bar — reported as the non-result it is.
Note what the naive line says on the same data: away closes **0.9h faster**, which reads as a large
home-field disadvantage and is nothing of the kind — it is 26 mostly-trivial cross-closures against
101 mostly-substantial owned ones. That gap is the number a reader reaches for first, which is why the
mode prints it **labelled `CONFOUNDED`** on the line above the index.

## Gate (RED seen, then green)

Test section 45 in `scripts/mesh-promises --test`, five legs on hand-built boards:

- **45a** full 4×4 reciprocal transplant, home 1h / away 10h → `HFAI = +900.0%` on all 6 pairs,
  `verdict: HOME-FIELD` (p=0.0039). *Four* windows, not two: with a single pair the permutation null
  over a median is too coarse to reach any p — measured **p=0.30 on the very same +900% effect** —
  so the pooled median over 6 pairs is what makes the verdict reachable at all.
- **45b** pure **site** main effect (alfa closes everything in 1h, bravo in 10h) with imbalanced
  routing → the naive contrast reports a spurious **+4.5h home advantage**; `HFAI = +0.0%`.
- **45c** 45a inverted → `HFAI = -90.0%`, `verdict: AWAY-FIELD`. The other pole is reachable.
- **45d** all-home board → `n/a — no window pair is reciprocally transplanted`, and **no pooled index
  is printed at all**. na, never 0.
- **45e** seed-determinism.
- **45f** **both** main effects, no interaction (1h / 5h / 5h / 25h) → `HFAI = +0.0%` while the naive
  gap points the **wrong way** (−8.0h).

45f exists because **45b alone passes for the wrong reason** — its two litters are equally easy, so
the site effect cancels in the raw ratio too. Verified against two mutants run from a scratch copy:

| mutant | 45b | 45f | 45a |
|---|---|---|---|
| drop the within-site RML normalisation (raw medians) | **green** (vacuous) | **RED**, +160.0% | green |
| report the naive gap as the index | green | green | **RED**, +180.0% |

Both mutants were seen to fail before the fix was called done.

## What this does not claim

- HFAI is a **rate contrast on closure latency**, and a promise's latency is a poor proxy for the
  quality of the work — a window can close fast by closing shallow. This measures speed, not merit
  (`--empowerment` and `--teachback` carry the other axes).
- The board's own `[done]` is the only evidence of closure; a self-reported keep is a claim.
- Nothing here is wired to a cadence and nothing gates on it. It is an instrument to be pulled.

## The one-line finding, for the board

The mesh routes 80% of its promises by an `owner:` clause whose payoff has **never been measured**,
and cannot be from the current board — the off-diagonal is empty. Filling it is cheap and deliberate:
let a few owned tasks be closed cross-window on purpose. Until then, "the owner clause works" is
compliance, not evidence.
