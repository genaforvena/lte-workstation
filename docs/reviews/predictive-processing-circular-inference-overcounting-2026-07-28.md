# Live-literature review — predictive processing: CIRCULAR INFERENCE, and the corroboration the mesh sums without checking it is independent

Date: 2026-07-28 · lane: genome (idea-queue LITERATURE task — a concrete METRIC the field measures itself with) · status: fix in tree, uncommitted

## Where we had already been (so this doesn't double-count)

Predictive processing / the Bayesian brain is the mesh's **most-saturated** review area. Before landing I
confirmed the canonical single-sense and single-timescale metrics are already embodied:

- **precision-weighting** (inverse-variance reliability) → `scripts/mesh-precision`
- **prediction-error / marginal & contextual surprise**, HGF **volatility**, **eigenform-absorption**
  (dark-room), **reducible-vs-irreducible** (noisy-TV), **prior-preference floor**, and the **LOCAL-GLOBAL
  two-timescale** deviance axis → `scripts/mesh-novelty`
  (`docs/reviews/predictive-processing-local-global-two-timescale-2026-07-27.md`)
- **salience vs novelty** (info-gain about states vs parameters) → `scripts/mesh-precision` (novelty axis)
  + `scripts/mesh-interruptibility --probe` (`docs/reviews/efe-novelty-vs-salience-...-2026-07-27.md`)
- **proper scoring / calibration** → `scripts/mesh-reliability --calibration`
- **omission as prediction-error** → `scripts/mesh-pulse`, `scripts/mesh-reflex-health`, `mesh-ambient-clock`
- **efference-copy / reafference-vs-exafference** (self-caused signal cancellation) → `scripts/mesh-audio-active`,
  consumed by `scripts/mesh-room-sense` — checked; the AUDIO self-caused lane is already done, so it is **not**
  this landing.
- **Markov blanket**, **good regulator**, **allostasis / CSD / FROZEN variance-collapse** → their own organs.

Every one of these measures a **single** sense, or one event at one/two timescales. The un-embodied thing is
at the **fusion** step: when the mesh combines several senses, it never asks whether they are **independent**.

## The mechanism not yet embodied — CIRCULAR INFERENCE (overcounting of reverberated messages)

The field's **third** account of Bayesian computation in the brain — alongside sampling and predictive
coding — is **circular inference** (Jardri & Denève). In hierarchical belief propagation, top-down and
bottom-up messages are *integrated*; to keep inference correct the system must **"subtract repeated
messages"** — discount any piece of evidence that has already been counted as it loops (reverberates) back
up the hierarchy (ascending loops) or down (descending loops). When that control fails, a **single**
observation reverberates and is counted as if it were **many independent** observations → pathological
**over-confidence**. This is the leading computational model of hallucination/delusion in schizophrenia.

The field's concrete **metric** is the **loop gain / overcounting factor**: climbing (α_c) and descending
(α_d) loop gains fitted to choice data, where α > 1 means redundant messages are being overcounted. Its
correct-Bayes counterpart is the **effective number of INDEPENDENT sources** — far below the raw count when
the sources share an upstream cause.

### Live sources (read 2026-07-28, current lit — not a fixed list)

- **"The myth of the Bayesian brain"** — PubMed **40569419** (2025). Names circular inference a **third
  framework** (with sampling & predictive coding) whose defining control mechanism is to **"subtract repeated
  messages"** so redundant information does not corrupt inference; notes it may be mediated by inhibitory
  connections balanced against excitation. <https://pubmed.ncbi.nlm.nih.gov/40569419/>
- **Safavi, Chalk et al., "Perceptual multistability: a window for a multi-facet understanding of psychiatric
  disorders"** — arXiv:**2506.18176** (2025-06-24). Circular inference as **redundant message-passing between
  hierarchical levels**, applied to bistable perception. <https://arxiv.org/abs/2506.18176>
- Foundational: **Jardri & Denève, "Circular inferences in schizophrenia", Brain 136:3227 (2013)**;
  **"Circular inference: mistaken belief, misplaced trust", Curr. Opin. Behav. Sci. (2016)**; **Leptourgos et
  al., "Circular inference in bistable perception" (2020)**.

## The gap in the mesh, measured against the tools themselves

`mesh-precision` embodies precision-weighting: it grades how **reliable** each sense is (inverse variance).
But honest-fusion then **sums the reliable senses as independent votes**. The clearest instance is
`scripts/mesh-home-state`'s additive combiner (`score[state] += n`, argmaxed at line ~485/1041): it counts
`ble_named` (raw BLE device count), the **`mesh-arrivals` present-roster**, and **`room-sense`** as separate
corroborating axes — yet `ble_named` and the arrivals roster **both derive from the same BLE scans of the
same phones**. Correlated senses summed as independent = **overcounting reverberated messages** = circular
inference: an apparent 3-way corroboration that is really **~1 source seen three ways**, inflating the
winning-state margin. The file's own `off_manifold` shadow instrument computes the vote-vector entropy/margin
**as if the votes were independent** — precisely the assumption circular inference says to check.

Nothing in the mesh measures the **independence** of a fused set: `mesh-precision` grades one sense at a
time; the honest-fusion rule (`mesh-situation`/`mesh-sensorium`/`mesh-home-state`) is *fresh→count,
stale→UNKNOWN* with **no discount for shared upstream cause**.

## The fix — one file: `scripts/mesh-precision` (in tree, uncommitted)

A report-only **`--independence`** mode. Given ≥2 aligned sense tapes it computes:

- **ρ̄** = mean absolute pairwise (Pearson) correlation of the aligned series;
- **n_eff** = `n / (1 + (n−1)·ρ̄)` — the Kish equicorrelation **effective number of independent sources**;
- **overcount** = `n / n_eff` (= `1 + (n−1)·ρ̄`): 1.0 = fully independent, `n` = fully circular;
- a **CIRCULAR / PARTIAL-REDUNDANCY / INDEPENDENT** band on ρ̄ (env-tunable `MESH_PREC_INDEP_HI`/`_LO`,
  defaults 0.70/0.30) — advisory only; the continuous n_eff/overcount is the primary output.

This is the field's **"subtract repeated messages"** control turned into a **measurement**: a fusion consumer
reading "4 senses agree" can ask how many are actually independent before trusting the margin. Live:

```
identical tapes:   CIRCULAR    — mean|r|=1.00 → n_eff=1.00 (overcount ×2.00)   [2 senses seen once]
scrambled tapes:   INDEPENDENT — mean|r|=0.05 → n_eff=1.91 (overcount ×1.05)   [genuine corroboration]
3-way (a,b,c):     PARTIAL-REDUNDANCY — mean|r|=0.37 → n_eff=1.73 (overcount ×1.73)
```

**Scope discipline** — identical to the file's `novelty`/`frame_coverage` axes: it touches **no** verdict or
weight downstream. ρ̄ is a genuine 0..1 axis (not an assumed-0..1 saturation trap — cf. the tone-median
family); the band is a tunable convenience, and the wiring of the discount **into** `mesh-home-state`'s vote
combiner is deferred to the steward, exactly like the sibling HELD behavioural fixes. Distinct from
precision-weighting (reliability of ONE sense), from the EFE novelty axis (info-gain about a sense's own
reliability parameter), and from honest-fusion's real-read/mtime gates (which catch EMPTY/STALE/FROZEN, never
REDUNDANT-BUT-FRESH).

## Gate (RED-first verified)

`mesh-precision --test` gains cases driving the **real** `--independence` path: two **identical** tapes must
read `CIRCULAR` **and `n_eff≈1.0`** (not 2 — the whole point); **scrambled/uncorrelated** tapes must read
`INDEPENDENT`; **anti-correlated** tapes are still redundant (`|r|=1`) → `CIRCULAR`; a **single** tape →
`UNKNOWN` (no independence with one source). Falsified live: replacing the discount with `n_eff = n` (no
subtraction of repeated messages) makes the identical case report `n_eff=2.0` → the gate goes **red**
(`rc=1`, seen); restoring it goes green. Run with `bash scripts/mesh-precision --test` (it is a **bash**
script — unlike `mesh-novelty`, do not invoke it via `python3`).

## Why not discarded

Discardable only if a mesh tool already discounted correlated evidence when fusing — none does:
`mesh-precision` grades one sense, and honest-fusion sums fresh senses with no shared-cause discount, so a set
of senses reverberating one upstream signal reads as strong multi-way corroboration. Circular inference is a
first-class, currently-published (2025 "myth of the Bayesian brain"; arXiv 2025-06) account of Bayesian
computation with a concrete overcounting metric, and the fix is cheap, report-only, and fits the file's
existing precision-weighting charter (reliability of a sense) with its missing complement (independence of a
set).

## Sources

- "The myth of the Bayesian brain" — PubMed 40569419 (2025) — <https://pubmed.ncbi.nlm.nih.gov/40569419/>
- Safavi, Chalk et al. — "Perceptual multistability: a window ... psychiatric disorders", arXiv:2506.18176
  (2025-06-24) — <https://arxiv.org/abs/2506.18176>
- Jardri & Denève — "Circular inferences in schizophrenia", Brain 136:3227 (2013)
- Jardri & Denève — "Circular inference: mistaken belief, misplaced trust", Curr. Opin. Behav. Sci. (2016)
- Leptourgos et al. — "Circular inference in bistable perception" (2020)
