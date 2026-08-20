# FEP / active inference — active data selection: information gain is a criterion for what to KEEP, not only for what to DO

**Date:** 2026-08-20 · **Lane:** literature (live review) · **Organ touched:** `scripts/mesh-records`

## The angle: what we misread

We have ~30 reviews under `docs/reviews/fep-*`, `efe-*`, `predictive-processing-*`. Every one of
them reads **expected information gain / epistemic value as a PROSPECTIVE quantity**: a term inside
expected free energy that scores *which action to take next*.
(`fep-active-inference-epistemic-value-vs-output-diversity-forage`, `efe-novelty-vs-salience-parameter-uncertainty`,
`fep-h3-reachable-non-constancy-epistemic-affordance-precision`,
`fep-expected-free-energy-ambiguity-price-of-honest-na-reflex-health`, `fep-bayesian-model-expansion-structure-learning-precision`.)

That is the loose application. In the source literature the *same* functional is a criterion over
**data**, in both directions — which data to acquire **and which data to retain when a budget binds**.
Choosing a subset of already-held data is the identical optimal-design problem; discarding is a
decision with an information price, and it is one we have never once scored.

Everywhere the mesh discards data it does so by a property of the **individual record** — its age, or
its quality score. Information gain is not a property of a record. It is a property of a record
**relative to what the store already holds**: the 601st near-identical ear capture carries ~zero
information about the ear's `dyn` median; a capture from an hour nothing else covers carries a lot.

## The source (live literature, read this session)

- **Parr, Friston & Zeidman, "Active Data Selection and Information Seeking", _Algorithms_ 17(3):118 (2024)** —
  <https://www.mdpi.com/1999-4893/17/3/118> (open copy: <https://discovery.ucl.ac.uk/id/eprint/10190280/>).
  Frames *selecting data* — "either through sampling subsets from large datasets or through
  optimizing experimental design" — as one problem, drawn from animal exploration and optimal
  experimental design theory, with the explicit goal of "good inference with fewer data". Subsetting
  a dataset you already have is treated on the same footing as designing the next experiment.
- Corroborating the "epistemic value is an added prior, not a free consequence" reading:
  **"Expected Free Energy-based Planning as Variational Inference"**, arXiv:2504.14898v4 —
  <https://arxiv.org/html/2504.14898v4> — EFE's information-seeking terms only appear once you
  *augment the generative model with explicit epistemic priors*; they do not fall out of VFE on their own.
- And on how loosely the field itself uses "EFE": **"Reframing the Expected Free Energy: Four
  Formulations and a Unification"**, arXiv:2402.14460 — <https://arxiv.org/abs/2402.14460> — the four
  standard decompositions (risk+ambiguity · information-gain+pragmatic-value · risk-over-states+ambiguity ·
  entropy+expected-energy) are **not** interchangeable; full equivalence needs prior preferences over
  observations to be compatible with the likelihood mapping. Filed as context, not applied here.
- Checked and rejected as already-embodied: arXiv:2512.21129 "Active inference and artificial
  reasoning" (Dec 2025) — action selection to disambiguate *model structure* via Bayesian Model
  Reduction; we already carry `fep-bayesian-model-expansion-structure-learning-precision` and
  `predictive-processing-bayesian-model-reduction-occam`.

## What it costs us — measured on the live ledger, 2026-08-20

`mesh-records` is the archivist. Its ledger `~/.mesh/records.log` is the population
`mesh-sound-reflex` computes its **corpus centre** from — `_prior_live()` pools every organ per axis
and takes the median, and that median is what every grind recipe is calibrated against
(CLAUDE.md: "it now re-measures the centre from the live ledger and persists it beside that ledger").

Retention was `tail -n LOG_KEEP` **per organ** — pure recency. Two binding budgets, both allocated
blind to information:

| budget | cap | allocated by |
|---|---|---|
| corpus space | 2000M — **at the cap**, evicting every sweep | score ascending, then mtime |
| ledger lines | 600 **per organ** — ear and drop both at the cap | recency |
| measure/sweep | 8 | organ declaration order — **does not currently bind** (max 7 observed) |

Measured, on the live ledger (n=1536):

```
  span (n is not coverage):
    ear    n=600  2026-08-20T00:25Z -> 2026-08-20T13:30Z  (13.1h)
    drop   n=600  2026-08-04T00:02Z -> 2026-08-20T11:30Z  (395.5h)
    note3  n=200  2026-08-20T00:52Z -> 2026-08-20T10:28Z  (9.6h)
    scape  n=131  2026-07-24T08:52Z -> 2026-08-20T12:50Z  (652.0h)
    voice  n=5    2026-08-20T10:30Z -> 2026-08-20T10:32Z  (0.0h)
```

**The ear's 600 lines are THIRTEEN HOURS.** The corpus keeps 14 days; the population its centre is
computed from keeps half a day of the organ that produces most of it. And inside that window the
centre is not stable — median over the oldest 100 vs the newest 100 of the same retained 600:

| axis | ear old100 | ear new100 | Δ | drop old100 | drop new100 | Δ |
|---|---|---|---|---|---|---|
| dyn | 0.144 | 0.332 | **+130.6%** | 0.376 | 0.369 | −1.9% |
| rich | 0.665 | 0.818 | +23.0% | 0.525 | 0.649 | +23.6% |
| score | 39.7 | 48.6 | +22.4% | 58.5 | 62.2 | +6.4% |
| act | 0.284 | 0.305 | +7.2% | 0.476 | 0.473 | −0.5% |
| cent | 1438.7 | 1398.7 | −2.8% | 2417.8 | 2318.2 | −4.1% |

drop, whose 600 lines span 16 days, is nearly flat on `dyn` (−1.9%). The ear, whose 600 lines span
13 hours, moves **2.3x on the same axis inside its own retained window**. So "the corpus centre" for
`dyn` was, for the chattiest organ, an answer about **which hour you asked** — and `n=600` looked
identically fat in both cases. This is the same shape as `a-senses-coverage-is-window-over-cadence`
(mesh-psi read a 10s window on a 600s cadence and called it a state), one layer down: **a prior whose
retention window is narrower than the phenomenon's period reports an hour, not a corpus** — and
nothing in the reading said so.

Note what recency-trimming is *not* buying us: the doctrine's own warning is that these medians
**rot** and must be re-derived live (`sound-reflex-prior-medians-frozen-at-n29`). That argues against
a *frozen constant*; it does not argue for a 13-hour window. A wider window still tracks drift — it
just stops being hostage to one hour.

## The change (`scripts/mesh-records`, uncommitted)

Spend a slice of the retention budget on **span** instead of recency — the cheapest possible
active-data-selection: coverage of the axis history beats one more sample of the current hour.

1. **`MESH_REC_LOG_RESERVE=90`** (of `LOG_KEEP=600`). Per organ: keep the newest `k−R` outright, plus
   `R` **evenly-spaced picks across everything older** — index 1, the oldest surviving line, always
   among them. Deterministic, no state, no new deps; total per organ still ≤ `k`. Because the older
   span is re-stratified from *what survives* each sweep, it **decimates progressively** rather than
   being cut off: the retained span grows without bound while the count stays capped. `R` is clamped
   to `k/2` so the reserve can never outweigh recency. `0` restores the old pure-recency window.
2. **`--stats` now publishes the SPAN beside the count** (the table above is its real output), so
   `n=600` can never again be read as "fat" when it means 13 hours. Straight from the psi rule:
   publish the coverage *in* the reading.
3. **A `--test` leg that can fail.** 60 lines, `keep=10`, `reserve=4`: asserts the oldest line
   survives, the newest survives, and the count still caps at 10. Driven both ways —

   ```
   reserve=4 -> kept 10 | oldest-survives: YES  cc000001 cc000019 cc000036 cc000054 … cc000060
   reserve=0 -> kept 10 | oldest-survives: NO   cc000051 cc000052 … cc000060      <- gate goes RED
   ```

   `mesh-records --test` → `smoke-test: ok`, rc=0, real-read gate included.

## What is NOT fixed (named, not quietly skipped)

- **Corpus eviction still ranks by score ascending.** Same misread — score is a property of the
  record alone. CLAUDE.md already warns the score's upper tail is *anti*-correlated with
  grindability, so "evict lowest score" is spending the one binding budget on the wrong axis, and it
  destroys the distribution's lower tail. Not touched here: it changes what audio physically exists,
  and it deserves its own measurement (the ledger and the corpus are separate samplers — the prior
  reads the ledger, so this fix lands where the calibration actually reads).
- **`note3` (n=200) and `voice` (n=5) have ledger lines but ZERO corpus files** — 0 of 2248 files
  match `-note3-`/`-voice-`. Age-prune or size-eviction, undetermined. Flagged, not diagnosed.
- **`mesh-sound-reflex._prior_live()` pools all organs into one median.** With ear at 13h and drop at
  16d that pooled centre is a blend of two incomparable windows. The reserve widens the ear's
  contribution; it does not make the pooling honest. Separate task.

## Verdict

**Landed.** One concept we did not embody — *information gain is a retention criterion, not only an
action criterion* — with a measured cost (+130.6% intraday swing in the ear's `dyn` centre), a
one-file fix in the genome source, a reading that now carries its own coverage, and a gate seen red.

Sources:
- [Active Data Selection and Information Seeking — Parr, Friston & Zeidman, Algorithms 17(3):118 (2024)](https://www.mdpi.com/1999-4893/17/3/118)
- [UCL Discovery open copy](https://discovery.ucl.ac.uk/id/eprint/10190280/)
- [Expected Free Energy-based Planning as Variational Inference (arXiv:2504.14898v4)](https://arxiv.org/html/2504.14898v4)
- [Reframing the Expected Free Energy: Four Formulations and a Unification (arXiv:2402.14460)](https://arxiv.org/abs/2402.14460)
- [Active inference and artificial reasoning (arXiv:2512.21129)](https://arxiv.org/abs/2512.21129) — checked, already embodied
