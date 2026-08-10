# Niche construction — DRIFTABILITY: the variance channel, and the null the J-gate never had

**Live review, genome, 2026-08-10.** Area: **niche construction & the extended phenotype**, angle the
task asked for — a **known CRITIQUE / failure mode of the area**, found by live web search, landed
somewhere the mesh has not been. Landed as a new read-only axis in `scripts/mesh-forage`
(`drift_null()` / `drift_verdict()`), rc-neutral, uncommitted in the tree.

## The source (found live, read)

**Fábregas-Tejeda, Alejandro & Ramsey, Grant — "Driftability and niche construction."**
*Synthese* **204**:162 (2024). doi:[10.1007/s11229-024-04815-5](https://doi.org/10.1007/s11229-024-04815-5)
— open access. Search path: `niche construction theory critique … counterfactual baseline` →
[Springer landing page](https://link.springer.com/article/10.1007/s11229-024-04815-5) (auth redirect) →
[PhilArchive record](https://philarchive.org/rec/FBRDAN) → Version-of-Record PDF read from KU Leuven
Lirias, <https://lirias.kuleuven.be/retrieve/793149>. Companion term paper:
Ramsey, G. "Driftability", *Synthese* **190**(17):3909–3928 (2013).

### The critique it makes

Niche construction theory's traditional definition requires the constructing organism to alter
**selection pressures** — that is what makes construction *evolutionarily* consequential rather than
merely a description of organisms making messes. Fábregas-Tejeda & Ramsey argue this is too narrow:

> "changes in selection pressures is not the only way organisms can influence the evolutionary futures
> of their population" … "organismic activities that modify drift probabilities should count as niche
> construction, **even if selection pressures remain unaltered**."

Drift probability, on their account, is the joint product of **two** factors:

1. **effective population size** — the number of rolls, and
2. **driftability** — "individual variance in possible reproductive outcomes" (Ramsey's 2013 term).

Their dice image carries the whole mechanism. Two six-sided dice, sides `{0,10,20,30,40,50}` and
`{22,23,24,26,27,28}`, have the **same expectation** (25) and radically different variance:

> "Roll each of those dice 1,000 times and the cumulative total for each will be close to 25,000. But
> roll each die once and only the low variance die will likely be close to 25."

Hence the asymmetry that matters operationally:

> "with very large population sizes, differences in driftability can make little difference. Conversely,
> with low population sizes, driftability values can take the upper hand in determining drift outcomes."

**The failure mode, stated generally:** a detector keyed on the **mean / share** is structurally blind
to construction that changes only the **variance** of outcomes — and at small effective sample size the
variance channel is the one that dominates.

## Why this is not already embodied

`mesh-forage` carries nine stacked axes (pheromone entropy, no-entry repellent, response-threshold,
ant-mill, sematectonic grounding, terminator/inter-scale, asignifying rupture, forager-drive, social
topology) plus a HELD heritability-inflation note. **Every one of them — and the headline verdict
itself — is a point estimate over counts in one window, read as if it were a fact about the colony.**
`grep -niE "variance|stddev|drift|chance|null|binom|multinom|poisson" scripts/mesh-forage` returned no
statistical machinery of any kind before this landing.

The concrete defect that follows:

- `classify()` fires **STAGNATING** at `J < 0.50` or `dom >= 0.60`, and `MIN_MARKS` is **8**. It will
  therefore call a colony of *equal-propensity* lanes "funneling into one trail" off **eight dice
  rolls**, with no notion of how much of that skew chance alone produces.
- The **inverse** error is just as live and had never been named: at N=4 across 4 lanes a perfect
  `J=1.0000` reads BALANCED, although chance alone lands four deposits on four distinct lanes only
  ~9% of the time. J is biased in **both** directions at small N, and every consumer reads it raw.

The mapping to the paper is exact: a lane's expected deposit rate is its **fitness**; the number of
`[done]` deposits in the window is the number of **rolls** (effective population size); a lane's
burstiness — six marks in one hour then nothing for ten, versus one an hour — is its **driftability**.

## What landed

`drift_null()` (reads the board on stdin) + `drift_verdict()`, wired into `run()`, JSON, and the text
renderer. Additive and read-only: it never touches `J`, `regime`, or `rc`.

1. **Candidate pool K** = the dice that could have been rolled: a real mind lane (the `LANES` roster)
   that was **alive** in the window (posted any well-formed board line), plus any lane that actually
   deposited (a forager by demonstration, e.g. the steward `land`). A decommissioned lane must not
   inflate the null; neither must a reflex identity that posts notices but never forages. Reading the
   raw poster set instead gave K=69 on the live board — an obviously wrong null.
2. **The band**: simulate `N_eff` deposits falling **uniformly** across K, `DRIFT_SIMS=2000` times,
   recompute J on each draw with the same `k<=1 => J=0` convention, take the **[5th, 95th] percentile**.
   Fixed seed (`DRIFT_SEED=20260810`) — a null that moves run-to-run is not a null; verified identical
   across repeated runs.
3. **Driftability enters as the design effect**, not as a second verdict — exactly as the paper
   composes the two factors into one drift probability. A uniform multinomial has per-bin Fano
   `Dbase = 1 - 1/B` *by construction*, so the baseline is 0.83 at B=6, **not 1**. Then
   `N_eff = N / max(1, Dbar/Dbase)`, floored at 2 and capped at N. A 300-mark burst that carries three
   rolls' worth of independent evidence cannot certify anything — and `DRIFT_FLOOR` is applied to
   **N_eff**, not to the raw deposit count, for that reason.
4. **Verdicts**: `SELECTIVE` (J below band — the skew exceeds drift, the regime verdict is EARNED) ·
   `DRIFT-CONSISTENT` (J inside the band — the evenness, high *or* low, is what equal-propensity lanes
   produce by chance at this N_eff; the regime label is not evidence) · `OVER-EVEN` (J above the band —
   something is enforcing balance) · `INSUFFICIENT` (honest n/a).

### Honest scope (written into the header, not just here)

- The null is **parametric** (equal-rate multinomial), **not** a label permutation. Permuting lane
  labels against deposits destroys the very association J is built from, so the shuffled distribution
  would exceed the observed value and the test would report the opposite of the truth — the trap
  measured on `mesh-promises --flow` (p=0.997 on a textbook-positive fixture).
- The comparison is **not matched-N**: the observed J is measured at raw N while the band is drawn at
  N_eff, and J's small-sample bias pushes the band **down**. That makes `SELECTIVE` harder to reach,
  never easier — the conservative direction for an axis whose job is to stop a gate over-claiming.
  `MESH_FORAGE_DRIFT_DEFLATE=0` draws the band at raw N for a steward who wants the uncorrected read.
- Fano conflates temporal burstiness with lane concentration. It is a **modulator of confidence**,
  reported, never verdicted on alone.

## Gate (RED-first, all seen fail)

`mesh-forage --test`: **PASS** (whole suite; the five new blocks below plus the nine pre-existing axes).

| check | result |
|---|---|
| SOLO(J=0) vs EVEN(J=1) at identical N=12, K=4 | `SELECTIVE` vs `OVER-EVEN` — the band discriminates the two extremes, so the verdict is not a constant |
| RED-first: `DRIFT_BREAK=1` neuters the band to [0,1] | SOLO flips `SELECTIVE` → `DRIFT-CONSISTENT` — the band, not the label, decides |
| the inverse trap: perfect `J=1.0000` at N=4, K=4 | `DRIFT-CONSISTENT` — asserted, since chance reaches it ~9% of draws |
| N_eff deflation live: same lane marginal, BURST vs SPREAD in time | burst **3** vs spread **8** rolls off the same raw N=8 |
| below the effective-roll floor | `driftability: n/a` (honest, never a faked verdict) |

**Mutant, seen red then restored green:** forcing `infl = 1` (killing the design-effect correction)
→ `FAIL: bursty deposits must carry FEWER independent rolls … the driftability channel is inert`;
restored → PASS. The first version of the deflation fixture *also* failed, for a real reason worth
recording: Fano reads **concentration into bins, not which bins** — two deposits in two different bins
have the same variance however far apart those bins are, so a "burst" spread over two adjacent bins is
statistically identical to one spread over the whole window. The burst fixture must put both deposits
in **one** bin.

## Live reading (this node, 2026-08-10)

```
forage: SKEWED  J=0.5087  dominant=genome 0.4569  marks=313/400h across 10 lanes
  driftability: SELECTIVE   J=0.5087 vs chance band [0.8982, 0.9756]
                N=313 deposits -> N_eff=10 rolls over K=9 candidate lanes
                (Fano=25.0914, 2000 equal-rate draws)
  -> driftability is HIGH: Fano=25.0914 vs the 6-bin multinomial baseline 0.83 — deposits arrive in
     bursts, so 313 marks carry only ~10 rolls' worth of independent evidence.
```

Two things worth stating plainly. First, the SKEWED verdict at 400h **survives** the correction —
J=0.5087 sits below the band even after driftability deflated 313 marks to 10 effective rolls, so that
particular reading is earned. Second, the deflation factor is **25x**: the board's deposits are wildly
bursty (silence for a day, then a flood), which is precisely the regime in which the paper says
driftability "takes the upper hand". At the default 12h window the node currently reads
`driftability: n/a (1 deposit … N_eff=1 < 8)` — an honest defer on a quiet board, and the correct
answer where the old gate would have been willing to render a regime off 8 marks.

## Unwired next

The observed J is compared against a band drawn at a different N. The rigorous version resamples the
observed deposits to raw-N-matched draws under an equal-rate null **with** the observed per-lane
burstiness (a Dirichlet-multinomial / block bootstrap over bins), which would drop the conservatism
caveat entirely. Left unwired: it needs a calibration decision the steward owns, and the conservative
form is already correct in direction.

## Files

- `scripts/mesh-forage` — header axis block, six `MESH_FORAGE_DRIFT_*` knobs, `drift_null()`,
  `drift_verdict()`, `run()` wiring, 6 new JSON fields (`drift_verdict`, `drift_candidate_lanes`,
  `drift_J_lo`, `drift_J_hi`, `driftability_fano`, `drift_effective_N`, `drift_sims`), text renderer,
  5 `--test` blocks. +276/-2. Uncommitted — steward lands from the tree.
