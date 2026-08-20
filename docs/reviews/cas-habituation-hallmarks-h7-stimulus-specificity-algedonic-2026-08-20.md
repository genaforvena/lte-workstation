# LITERATURE review (live) — complex adaptive systems / adaptation & self-organisation, from the angle of a **CROSS-DOMAIN TRANSFER**: **H7 stimulus specificity**, the hallmark that separates habituation from general fatigue

**Date:** 2026-08-20
**Area:** CAS & the edge of chaos (Santa Fe lineage) — entered through arXiv **nlin.AO** ("Adaptation and
Self-Organizing Systems"), the live channel of the area, not a fixed reading list.
**Angle:** cross-domain transfer — a dynamical principle claimed to recur *across substrates*, carried
into a distributed sensor mesh.
**Landing:** one concept we do **not** embody — **H7 (stimulus specificity)** plus the **LTI
impossibility result** — from a paper posted **20 days ago**.
**Verdict:** ACCEPTED as new and load-bearing. **LANDED as code** — `scripts/mesh-algedonic
--specificity` + a `spec=` field on the 10-minute status line. Read-only, no alarm, uncommitted for
the steward. A live SPEC_MASKED on this node is below.

---

## How this one was found (the "live literature" part)

The area was entered by reading the **current month's** arXiv `nlin.AO` listing rather than searching
for a concept already known — <https://arxiv.org/list/nlin.AO/current> (August 2026, 26 papers). The
landing came from **arXiv:2608.00249**, submitted **31 Jul 2026**.

Discarded from the same sweep, one line each, because the mesh has been there:
`2608.15476` spatial early-warning signals for network tipping — CSD family, already three sidecars
deep (`--dtc`, `csd=`, `--cyberfilter`) · `2607.11350` "Beyond Critical Slowing Down" (Chekroun &
Lucarini) — same family, the extreme-tail leg is a genuine gap but belongs to `mesh-criticality`, which
has 20+ lenses already and is the wrong organ to add a 21st to today · `2604.15669` "Self-Organization
to the Edge of Ergodicity Breaking" — its ε(λ) ergodicity coefficient is the object
`docs/reviews/ergodicity-breaking-pooled-corpus-2026-07-24.md` already landed in
`mesh-sound-reflex` (as `|2·AUC−1|`), so it would be a re-landing · Griffiths phases / stretched
criticality — reviewed 2026-06-20 in the knowledge base, so not new ground.

## The source

Matthew Smart, Stanislav Y. Shvartsman, Martin Mönnigmann, **"Dynamical principles of habituation
across substrates and scales"**, arXiv:**2608.00249** (submitted 31 Jul 2026).
<https://arxiv.org/abs/2608.00249>

> "Habituation is a basic form of learning in which a system's response to repeated stimulation
> progressively diminishes but eventually recovers when the stimulus is withheld. Long studied in
> animals, it has increasingly been observed in unicellular organisms and non-living devices such as
> electronic circuits and neuromorphic materials, suggesting underlying dynamical principles that
> recur across domains."

The paper is a cross-domain transfer *by construction*: it asks what minimal dynamical structure the
behavioural constraints force, independent of substrate. Two results matter here.

**(1) The hallmarks, formalized as input/output constraints** (their Table 1, after Thompson & Spencer,
Psychol. Rev. 73(1):16, 1966):

| | hallmark |
|---|---|
| H1 | repeated stimuli → progressively decreasing response toward an asymptote |
| H2 | spontaneous recovery when the stimulus is withheld |
| H3 | potentiation — repeated stimulus/rest cycles habituate faster |
| H4 | frequency sensitivity — more frequent stimulation → faster decrement *and* faster recovery |
| H5 | intensity sensitivity — weak stimuli decrement more; intense ones may not decrement at all |
| H6 | subliminal accumulation past the asymptote |
| **H7** | **stimulus specificity — the decrement must NOT transfer to a different stimulus** |
| H8 | dishabituation by a strong alternative stimulus |
| H9 | habituation of dishabituation |
| H10 | long-term habituation over hours/days/weeks |

**(2) The LTI impossibility result.** No linear time-invariant system can satisfy non-negativity
together with monotone response attenuation:

> "By superposition and time invariance, shifting and summing pulse-train inputs yields shifted and
> summed outputs in an LTI system. Habituating responses violate this property, making nonlinearity
> necessary."

So the minimal motif is a **Wiener model** — linear fading memory composed with a *static
nonlinearity*: `ẋ = βu − αx`, `y = u·σ(x)`, `σ(x) = 1/(1+x^N)`.

## What we already embody, and the exact gap

`scripts/mesh-algedonic` already carries habituation: `salience()`, landed
2026-07-28 (`docs/reviews/second-order-cyb-algedonic-habituation-alarm-fatigue-2026-07-28.md`) as the
algedonic channel's alarm-fatigue defense. It reads the pain as a robust z against its own trailing
median/MAD: chronic-but-stable → `SAL_HABITUATED` (H1), a change → `SAL_ONSET` (H8). Structurally it is
already the paper's motif — a fading memory (trailing median) composed with a static nonlinearity (the
z cut) — so the LTI theorem does not indict it.

**H7 does.** `salience()` habituates the **noisy-OR-FUSED scalar** `pain`. Fusion is a many-to-one map
applied **before** the memory, so the memory state cannot be indexed by *which* stimulus arrived —
every axis shares one baseline. That is precisely the property H7 exists to rule out: a decrement
earned by a **chronic** axis transfers to a **fresh, unrelated** one. In the paper's own vocabulary
that is not habituation at all, it is **general fatigue**, and H7 is the discriminator between them.

This is an **ordering defect, not a threshold to tune**. Two mechanisms, both live on this node:

- **baseline drag** — a chronically elevated axis holds the fused median high, so a fresh axis's step
  is small *relative to that median*;
- **noisy-OR saturation** — near the top the fused map compresses, so a large per-axis step becomes a
  small fused one.

No cut on the fused scalar recovers what the fusion already discarded. The rule, general past this
organ: **habituate per channel, then fuse — never fuse, then habituate.** It is the mesh's own
`a-weak-surface-hit-suppresses-the-strong-surface` shape one level up: there a boolean collapsed
surfaces of different authority, here a noisy-OR collapses stimuli of different identity.

## Measured live, not argued

`~/.mesh/algedonic.log`, 2026-08-20T22:41Z, real state, `--specificity`:

```
algedonic stimulus-specificity: SPEC_MASKED axis=stress (axis z=4.000 vs its own baseline 0.300, 5 axes with enough history)
  fused leg: salience=SAL_HABITUATED salz=1.660 salbase=0.790 saln=48 · current pain=0.873 [CRITICAL]
  current vector: axes=therm:0.0,hw:0.0,egress:0.7,stress:0.5,crit:0.15
```

Over the 48-sample salience window the axes read: `therm` 0.0 constant · `hw` 0.0 constant · `egress`
**0.7 constant for the entire window** (chronic — correctly habituated) · `stress` median 0.3, now 0.5
· `crit` median 0.0, now 0.15. The fused baseline is **0.790**, held there by `egress` alone; the
fused MAD is ~0, so the spread is the 0.05 floor and a 0.06 fused step scores z=1.66, under the 3.0
cut. Verdict: `SAL_HABITUATED`.

Against its **own** history `stress` scores z=4.0 with a 0.2 absolute step — a clean dishabituation,
on a sample the band itself calls **CRITICAL**. The chronic egress pain bought the discount; the
stress onset spent it. That is the H7 failure, live, and it is the failure mode that matters most for
an *algedonic bypass*, whose entire purpose is to be the mesh's scarcest attention channel.

## The application (shipped, uncommitted)

**File: `scripts/mesh-algedonic`** (genome source, not the deployed `~/.local/bin/` copy).

1. **`salience_specificity()`** — the same estimator and the **same cuts** as `salience()` (`SPEC_Z`
   defaults to 3.0, `SPEC_STEP` to 0.15, deliberately equal to `SAL_Z`/`SAL_STEP`), applied **per
   axis** against that axis's own trailing median/MAD. The two legs differ only in their *subject*; if
   they differed in threshold the comparison would prove nothing.
2. **Per-axis, not complete-case.** Unlike `constrained_disorder()`, one absent axis must not shorten
   every other axis's baseline — complete-casing would re-pool exactly what this leg exists to keep
   apart.
3. **Three verdicts, and the inverse direction is a finding too.**
   - `SPEC_MASKED <axis>` — fused reads HABITUATED/CALM while an axis dishabituates. Names the axis.
   - `SPEC_SPURIOUS` — fused reads ONSET while **no** axis does: the onset belongs to co-drift across
     axes, not to any stimulus. (A masking detector that only looked one way would sell the fused leg
     as the conservative one; it is not.)
   - `SPEC_CONCORD` — the two agree, either way.
   - `SPEC_INSUFFICIENT` / `SPEC_UNKNOWN` (rc=2) — honest n/a, never a fabricated 0.
4. **`spec=… specax=… specz=… specbase=… specn=…`** on the 10-minute status line, beside
   `salience=…/salbase=…`, so the drag is visible as two numbers in one row rather than an argument in
   a docstring. Both downstream readers of the log (`mesh-dnb`, `mesh-precision`) parse by keyed regex,
   not field position; `mesh-dnb --test` re-run green after the change.
5. **`mesh-algedonic --specificity`** — read-only detail mode, same shape as every other sidecar.
   **It never escalates and never routes work**, exactly like `--cdp`/`--cyberfilter`/`--anticipate`.

### The gate, seen RED

`--test` section 9b. Fixture is the live 2026-08-20 shape: 12 rows at `pain=0.79`,
`axes=…,egress:0.7,stress:0.3`, current sample `stress:0.5` at `pain=0.85`. Asserts, in order: the
fused leg **does** read `SAL_HABITUATED` on it (otherwise the discriminating claim is vacuous), the
specificity leg reads `SPEC_MASKED`, and it names **`stress`** — the fresh axis, not the chronic
`egress`. Then the no-movement case (`SPEC_CONCORD`, so masking is not manufactured), the inverse
fixture (`SPEC_SPURIOUS`), the short-history case (`SPEC_INSUFFICIENT`) and the empty-axes rc=2.

Three mutants run from a scratch copy, each red on a different assertion — a gate not seen fail is not
a gate:

| mutant | change | result |
|---|---|---|
| 1 | per-axis baseline → **pooled across all axes** (the "fuse then habituate" bug itself) | `spec masked label → expected 'SPEC_MASKED' got 'SPEC_CONCORD'`; `names the FRESH axis → expected 'stress' got 'egress'` |
| 2 | delete the `SPEC_SPURIOUS` branch | `spec spurious label → expected 'SPEC_SPURIOUS' got 'SPEC_CONCORD'` |
| 3 | remove the min-history floor | `spec insufficient history → expected 'SPEC_INSUFFICIENT' got 'SPEC_CONCORD'` |

Restored, `mesh-algedonic --test` green.

## Honest limits

- **Part of the fused/per-axis gap is scale, not specificity.** Noisy-OR saturates near the top, so a
  per-axis step is *arithmetically* larger than its fused image regardless of which stimulus moved.
  That is named in the tool's own output as one of the two masking mechanisms rather than hidden — but
  it means `SPEC_MASKED` is evidence of *the fused leg being unable to see this axis*, not a proof that
  a human would have wanted an alarm. Read-only and advisory for exactly that reason.
- **H7 is one of ten.** H4 (frequency sensitivity) and H5 (intensity sensitivity — weak stimuli should
  decrement *more*, intense ones may not decrement at all) remain un-embodied on both legs; H5 in
  particular would say a `CRITICAL`-band stimulus should be exempt from habituation entirely, which is
  a stronger claim than anything landed here and needs its own review.
- **`specn=5` counts axes with enough history, not samples.** The per-axis windows are the same 48.
- The axes are coarsely quantized (0.0/0.15/0.3/0.5/0.7/0.9), so a one-quantum move is the smallest
  detectable step; `SPEC_STEP` is set to exactly one quantum on purpose.

## Sources

- [arXiv:2608.00249 — Smart, Shvartsman & Mönnigmann, *Dynamical principles of habituation across substrates and scales* (31 Jul 2026)](https://arxiv.org/abs/2608.00249) — the landing
- [arXiv nlin.AO, current listing (Aug 2026)](https://arxiv.org/list/nlin.AO/current) — the live channel this was found in
- Thompson & Spencer, *Habituation: a model phenomenon for the study of neuronal substrates of behavior*, Psychol. Rev. 73(1):16 (1966) — the original hallmark list the paper formalizes
- Checked-and-discarded as already covered: [arXiv:2608.15476](https://arxiv.org/list/nlin.AO/current) (spatial EWS), [arXiv:2607.11350](https://arxiv.org/abs/2607.11350) (Beyond Critical Slowing Down), [arXiv:2604.15669](https://arxiv.org/html/2604.15669v1) (edge of ergodicity breaking)
