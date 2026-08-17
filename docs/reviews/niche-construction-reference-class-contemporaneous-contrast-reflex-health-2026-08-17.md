# The reference class: a frozen clock with no contemporaneous contrast is not a measurement

**Live review, genome, 2026-08-17.** Area: **niche construction & the extended phenotype**, angle the
task asked for — an **OPERATIONAL mechanism** (not philosophy) we could implement. Landed as a new
report-only clause in `scripts/mesh-reflex-health` (`ow_cohort_clause()`), uncommitted in the tree.

## What we already embodied (checked first)

Eleven prior reviews from this area are on disk (`docs/reviews/`): external immunity/removal
(2026-07-28), the negative inter-scale terminator (2026-07-29), realized-heritability inflation
(2026-07-31), collective social niche construction (2026-08-03), driftability as a counterfactual
baseline (2026-08-10), NC³ mechanism attribution — construction vs choice vs conformance
(2026-08-15), the by-product null (2026-08-16); plus sematectonic-vs-sign stigmergy, pheromone
entropy, and the facilitation cascade already shipped **inside this same file**. Grepped for the
candidate vocabulary before reading anything: `counteractive`, `inceptive`, `relocational`,
`perturbational`, `evolutionary momentum`, `indirect genetic effect`, `extended fitness` —
**zero hits mesh-wide.** The whole COUNTERACTIVE (buffering) branch of NCT is unlanded.

## The source (found live, read)

**A. D. Clark, D. Deffner, K. Laland, J. Odling-Smee & J. Endler — "Niche construction affects the
variability and strength of natural selection."** *The American Naturalist* **195**(1):16–30, Jan
2020. doi:[10.1086/706196](https://doi.org/10.1086/706196). Verbatim abstract read at the
[St Andrews research portal](https://research-portal.st-andrews.ac.uk/en/publications/niche-construction-affects-the-variability-and-strength-of-natura);
open data at [Dryad doi:10.5061/dryad.g66n3h5](https://datadryad.org/dataset/doi:10.5061/dryad.g66n3h5).
Search path: `niche construction ecological inheritance operational model 2026` →
`counteractive niche construction / evolutionary momentum` → the Am Nat paper, then an independent
second fetch for the citation (the first fetch's author list and year needed corroboration — a
summary is a claim, not an artifact).

Organisms that **regulate** their experienced environment — "by constructing components of their
local environments, such as nests, burrows, or pupal cases, or by choosing suitable resources" —
are predicted to produce **(i)** reduced *temporal* variance in selection gradients, **(ii)** reduced
*spatial* variance, and **(iii)** weaker directional selection, **relative to nonconstructed
sources**. Tested over 1,045 temporally replicated + 257 spatially replicated + 1,230 pooled
gradients: *compelling* evidence for (i) and (iii), only *some* evidence for (ii).

## The mechanism we do not embody

**It is not the result — it is the METHOD.** Low variance is uninterpretable in absolute terms. It is
a measurement only against a **contemporaneous, nonconstructed reference class observed over the same
window**. A buffered variable and an unread one are both flat; the paper cannot separate them from
the constructed series alone either, and so it never quotes one. Its entire apparatus is the
**paired contrast** — the nonconstructed arm is what makes the constructed arm publishable.

## Where it bites: the value-frozen axis in `scripts/mesh-reflex-health`

`overwrite_probe()` reports `overwrite:<seconds the content has not moved>` and the line renders
`psi(value-frozen 69298s ≥ 4800s)`. That is **exactly a bare constructed-arm variance with no
reference arm.** It reads as an accusation, but it means opposite things depending on a fact the line
never carried:

- **nothing else moved either** → the frozen clock is a property of the **tick** (quiet node, or a
  degenerate observation), and says nothing about that reflex at all;
- **eleven others moved and this one held** → the freeze is **idiosyncratic** and worth a look.

Same rendering, both times. This is also the blocker the file's own refrain block records as **HELD**
(*"needs a per-reflex expected-variation model"*). Clark et al. dissolve it: the reference class does
not have to be **modelled** per reflex — it is **measured** from the cohort in the same run, at zero
extra cost, since the digests are already computed. Doctrine sibling: *calibrate a derived axis
against the REAL corpus, never an assumed 0..1* — the same instinct, unembodied here.

## Shipped (report-only, an attribution never a verdict)

`ow_cohort_clause() <held> <moved>` publishes `held/valued` for the same tick and **names the
degenerate end instead of inventing a threshold**:

```
· cohort 4/6 held while 2 moved in the same window
· cohort 6/6 held — NO-CONTRAST: no valued artifact moved in the same window, so the frozen clock
  is a property of THIS TICK, not of these reflexes
```

Design constraints, each with a gate:

- **No verdict.** It does not claim buffering vs death — *a shared observable cannot name the
  mechanism*, and Clark et al. only ever compare **groups**, never classify an individual series.
- **No constant.** A threshold here would be a median pinned as a constant, which rots. Only the
  degenerate end (`moved == 0`) is named.
- **Denominator = artifacts with a VALUE AXIS.** 0-byte beats are excluded: they cannot move by
  construction, so counting them pads the reference arm with members incapable of moving.
- **Membership is counted BEFORE each reflex's own ≥floor test.** The reference class asks one
  question of every member — did the bytes move this window. Gating membership per-reflex-cadence
  would make the denominator a different quantity for each member.
- **Inert to both readers of that line**: no `(` anywhere (else `ow_edge_key()` harvests a phantom
  reflex name into the edge identity), and no `(stale` (which `mesh-needs` scrapes off this line).

Not a duplicate of the embodied axes: **not** the facilitation cascade in the same file (ranks a
STALE set by blast radius — this qualifies a FRESH one's provenance); **not** the bridge-interface
split (names *which* component carried the verdict — this supplies the reference class that makes the
environment-owned component's number readable at all); **not** `mesh-forage`'s driftability null
(a *counterfactual* baseline — this is an *observed* contemporaneous cohort).

## Verification

- `bash scripts/mesh-reflex-health --test` → green, baseline **0 FAIL**.
- **Six mutants, each seen RED, each for its own gate** (run from a scratch copy; the three
  `fanin_count` failures that fire for *any* out-of-tree copy are noise and are excluded from these
  counts):

  | mutant | broken | gates red |
  |---|---|---|
  | M1 | always take the no-moved branch (collapse the reference class) | 2 |
  | M2 | count the 0-byte beat in the denominator | 2 |
  | M3 | count held only past each reflex's floor | 1 |
  | M4 | parenthesise the cohort word | 3 |
  | M5 | drop the clause from the rendered line | 2 |
  | M6 | emit a clause when nothing is held | 1 |

  The load-bearing gate: `ow_cohort_clause 3 0` **must not** render the same string as
  `ow_cohort_clause 3 9`. That equality *is* the failure the axis exists to kill.
- **Live artifact** (genome source, `--check`, read-only peek):

  ```
  reflex-health: ok (7 per-run reflex(es) fresh · overwrite-only: imac-wifi(value-frozen 2098s ≥ 960s)
  psi(value-frozen 69298s ≥ 4800s) · cohort 4/6 held while 2 moved in the same window · lan-newdevice(
  beat-only — 0-byte artifact, mtime is the ONLY evidence by construction))
  ```

  First real reading: **2 of 6 valued artifacts moved in that window**, so the two named freezes are
  *not* a quiet-tick artifact — the contrast exists and the number is now readable. (Consistent with
  the independently-verified finding that `psi`'s constancy here is honest calm.)

## Not taken

- **Indirect genetic effects / the extended fitness hypothesis** (Genetics, Apr 2026; the shared-use
  simulation, PMC7886806) — real and live, but the operational content is a quantitative-genetic
  variance decomposition needing a heritability model we have no substrate for. Discarded.
- **Facilitation-cascade / foundation-species weighting** — already shipped in this same file
  (2026-07-09). Not re-landed.
