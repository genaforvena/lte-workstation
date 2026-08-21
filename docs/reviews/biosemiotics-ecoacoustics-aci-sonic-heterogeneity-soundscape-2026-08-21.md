# Live-literature review — biosemiotics / ecoacoustics: the Acoustic Complexity Index, and the axis that says "nothing here is articulated"

Date: 2026-08-21 · lane: genome (idea-queue LITERATURE task) · status: fix in tree, uncommitted

## Area & angle

Biosemiotics — sign and meaning in living systems — taken, as the task demands, through a **concrete
metric the field uses to measure itself**, not through its philosophy. The sub-field that actually
publishes numbers every month is **ecoacoustics**, the wing of biosemiotics that reads a habitat's
sound as a sign system (Farina's ecoacoustic codes; Kull's "ecosystems are made of semiosic bonds:
consortia, umwelten, biophony and ecological codes"). Its instrument is a small family of *acoustic
indices* computed straight off an FFT matrix, and the oldest and most-used of them was re-founded in
the live literature last year.

## Where we had already been (so this doesn't double-count)

Twelve prior biosemiotics landings in `docs/reviews/`: functional-cycle closure, Umwelt degeneracy,
index-vs-icon, code duality, code-vs-interpretant, information balance (Rsequence≈Rfrequency),
interactive-sign liveness, interpretant temporal self-reference, senome band collapse, efficiency
sensing, incentive salience, dialogue of constraints. Semantic information (Kolchinsky & Wolpert)
already sits in `scripts/mesh-interpretant`.

**None of them is acoustic.** The mesh has a large ear (`mesh-overhear`, `mesh-records`,
`mesh-soundscape`, `mesh-sound-reflex`, `mesh-room-music`) and it has never once been pointed at the
literature whose entire subject matter is *how to measure a soundscape*. `grep -ril
'ecoacoust|biophony|anthrophony|NDSI|acoustic complexity index' docs/ scripts/` returns nothing in
this sense before today. That is the unvisited ground.

## The find

**Farina, A. (2025). "The acoustic complexity index (ACI): theoretical foundations, applied
perspectives and semantics." *Oikos* 2025:e10760, doi:10.1111/oik.10760**
(Wiley/Nordic Society Oikos; successor and re-foundation of Pieretti, Farina & Morri 2011,
*Ecological Indicators* 11:868-873, the original ACI paper. Preprint: Authorea
10.22541/au.172329086.60641286.) Found by sweeping the live *Biosemiotics* (Springer) 2026 volumes
and the ecosemiotics/ecoacoustics thread that runs out of them.

**ACI**, in one line: for each frequency bin of an FFT matrix, sum the absolute amplitude difference
between **adjacent time steps**, and normalise by the amplitudes themselves (a Canberra metric). Sum
or average over bins. `ACItf` differences along time; `ACIft` along frequency.

Its founding premise is a **sign criterion, not an energy one**, and that is why it belongs to this
literature rather than to DSP: *biotic sound is intensity-MODULATED, machine noise holds a nearly
CONSTANT intensity.* The index therefore reads whether sound is **articulated** — and is deliberately
blind to how loud it is. Farina 2025 also renames it: **"sonic heterogeneity index"**, on the grounds
that what it measures is variability and evenness, not complexity.

## Why we do not already embody it

`scripts/mesh-soundscape` is the mesh's one measure tract. Its five axes — `dyn` (rms std/mean),
`act` (onset strength), `rich` (spectral contrast), `tone` (flatness), `move` (centroid std) — are
**all broadband energy-shape statistics over the whole spectrum**. Not one of them can distinguish
*continuous* sound from *articulated* sound, and CLAUDE.md already carries the two consequences:

- `dyn` "is the heaviest term — one transient pins it", so the ranker aims at clicks; and
- the beat detector "**hallucinates** beats and cannot report 'no rhythm'".

That second one is the exact hole ACI fills: an index that reaches a floor on continuous material,
with no beat tracking involved at all, can say *"this is a hum"* — a sentence the current organ has
no way to form.

## What measuring it on our own corpus actually taught (three traps)

The naive implementation was written first and then falsified against 2265 archived records
(`~/.mesh/records/`: 1286 ear, 918 operator drops, 61 picked soundscapes). Each trap is a way this
index returns a **confident number to a question you did not ask**.

**1. An empty bin is maximally heterogeneous.** The per-bin normalisation *erases amplitude*, so a
bin holding nothing but numerical/resampler noise counts exactly as much as the bin carrying the
voice — and it returns the index's **ceiling**, because noise differs maximally from itself frame to
frame. Measured: this node's ear records are **16 kHz** sources that librosa loads at 22050, so
everything above 8 kHz is resampler ringing. That dead band carries **0.005 % of the energy and reads
ACI 0.97-0.99**, dragging the unguarded full-band number to **0.50** where the material's own band
reads **0.31**. The 44.1 kHz soundscape captures, whose material really does reach up there, read
0.32 full / 0.31 in-band. So the entire apparent finding "the ear hears a more heterogeneous room
than the scanner does" was **the resampler**, not the room.

The same trap lives one level down, *inside* any band: a synthetic 220 Hz tone reads **0.54** on its
own silent neighbour bins, and **0.013** once they are excluded — 0.013 being the honest reading of a
steady tone.

**And the fix is not the one the literature prescribes.** Ecoacoustics conventionally cuts below
2 kHz (birds above, traffic below) — a **habitat constant**, and it does not transfer indoors, where
the signal we care about *is* the 200-2000 Hz voice band. Measured both ways: with a per-bin energy
floor in place, restricting to 200-8000 Hz moves real records by **≤0.008** (0.4858 vs 0.4866) — the
band is **inert**, so it is not shipped. The floor is not inert: the same hum fixture reads **0.0130
with it and 0.4741 without**, 36×. *Transfer the mechanism (do not measure bins with no energy), not
the constant (2 kHz).*

**2. The time step IS the index.** At FFT-frame resolution (23 ms) ACI is a **constant** on this
corpus — ambient ear **0.316**, picked soundscapes **0.320**, the operator's own music drops
**0.304**: three material classes that cannot be told apart. Clumping the spectra into coarser time
steps first — Farina's own stated prerequisite, usually filed as a preprocessing detail — is what
turns it into a measurement. At 0.5 s the same three read **0.535 / 0.403 / 0.279**, and a synthetic
steady hum reads **0.065**. This is CLAUDE.md's *sample-is-not-the-interval* at the spectral-
differencing scale: the clump does not tune the index, it **names the timescale the claim is about**,
so it is published in the reading beside the value (`aciclump=0.50`).

**3. It is non-monotonic, so it must never enter `score`.** Farina 2025 is explicit: ACI is low when
nothing sounds **and** low when much sounds over a continuous background; it is high only in between.
Our corpus reproduces it exactly — dense continuous music (**0.267**) sits *below* a sparse room
(**0.486-0.559**) and far above a hum (**0.013**). A ranker keyed on it selects the **middle** of its
range. This is the same family as CLAUDE.md's "check what your ranker SELECTS FOR", in its inverted-U
form, and it is the reason the axis is published but kept **out of the score formula**.

## The landing

`scripts/mesh-soundscape` (uncommitted; the genome source, not the deployed copy):

- `_aci(seg)` — ACItf over **clumped** magnitudes with a **per-bin energy floor** and Farina's
  zero-pair exclusion. Returns `(value|None, n_clumps)`; `None` where fewer than 3 clumps exist,
  because **0.0 is the honest reading of a steady tone** and a thin clip must never wear it.
- `--measure` gains `aci=` (the picked window) and `faci=` (the whole file) — the same
  best-moment-vs-this-material pair the existing `f*` axes answer — plus `aciclump=`, `acifloor=`
  and `acin=`, so a consumer can never read one timescale's claim as another's.
- Knobs: `SS_ACI_CLUMP` (0.5 s), `SS_ACI_BINFLOOR` (0.01 of the loudest bin's mean).
- `--scan` is untouched: no new cost on the 10-minute reflex, and the `WINNER` line stays 6 fields.

Live on real records the axis has range where it had none: hum **0.013** · operator music **0.267** ·
room ambient **0.486** · sparse room events **0.559** · synthetic articulated bursts **0.927**.

## Gates (five claims, each seen RED)

Every threshold in `--test` is a **separation between two fixtures measured in the same run**, never
an absolute constant, so a node with different ffmpeg/librosa versions still gets an honest verdict.

1. **the floor is reached** — a steady hum must read < 0.10.
2. **the floor is load-bearing** — with `SS_ACI_BINFLOOR=0` the same fixture must read ≥5× higher.
3. **articulation separates** — burst fixture minus hum > 0.50.
4. **the clump is load-bearing** — at 23 ms the separation must SHRINK by >0.10 (0.914 → 0.462).
5. **non-monotonicity held** — the `dense` fixture is the **most active of the three on our own `act`
   axis** (0.874 vs 0.387, itself asserted so the gate cannot go vacuous) and must still read *below*
   the sparse articulated one. Red the moment anyone "improves" `aci` into another activity measure.
6. **thin is na, never 0** — a 1.2 s clip renders `aci=na acin=2`.

**Five mutants, each run from a scratch copy of the patched script, control green:**

| mutant | verdict | reds at |
|---|---|---|
| M1 per-bin floor deleted (`_keep = _bm >= 0.0`) | FAIL | (1) `steady hum reads aci=0.4741 — a continuous source must reach the floor` |
| M2 default floor set to 0 | FAIL | (1) same, 0.4741 |
| M3 clump hardcoded to one frame (`k = 1`) | FAIL | (3) `articulated (0.4783) vs hum (0.0164) do not separate` |
| M4 thin clip returns `0.0` instead of `None` | FAIL | (6) `a 1.2s clip returned aci=0.0000 instead of na` |
| M5 `aci` replaced by the activity axis | FAIL | (2) `disabling the per-bin floor barely moved the hum reading (0.0055 vs 0.0055)` |
| control (unmutated) | **ok** | — |

Two of them red at an **earlier** gate than the one written for them — CLAUDE.md's *a red gate hides
every gate after it* — so both were checked against their intended gate by the numbers the run
printed: M3's frame-resolution separation is 0.462 against the default's 0.914, which is exactly what
gate (4) compares (and under M3 the two sides become identical, so it reds); M5's `dense` fixture
reads 0.874 against `artic` 0.387, an inversion gate (5) rejects.


## Honest negatives

- **Band-limiting is inert here and was dropped.** It was in the first implementation, justified by
  trap 1, and the per-bin floor turned out to subsume it (≤0.008 on real records). Shipping both
  would have been a gate that cannot fail standing next to one that can.
- **The axis does not separate the scanner's picks from raw ambient.** Band-limited, frame-resolution
  ACI reads 0.316 (ear) vs 0.320 (scape) — and even at 0.5 s clumps the ear/scape difference is
  confounded by duration (ear records are 1.4-3 s = 3-6 clumps; small-n). No claim is made that `aci`
  validates the picker.
- **The beatless split is NOT demonstrated on live material, and the one sweep that looked like it
  points the other way.** 28 real records measured through the patched tool: the ones the grinder
  calls beatless (`beats<=2`, n=7) mean **aci 0.564**, the beated ones (n=15) mean **0.379** — the
  *opposite* of "beatless because hum". It is confounded and no conclusion is drawn from it: every
  beatless record in this corpus is a 1.4-3 s ear chunk (3 clumps, or `na` at <1.5 s) and every
  beated one is a 5 s scape capture, so that comparison is organ-and-duration, not rhythm. The
  hum-vs-articulated separation is established on **synthetic fixtures only** (0.013 vs 0.927). The
  proposal below is therefore a proposal, not a measured result.
- **`ACIft` (differencing along frequency) is not implemented.** Farina treats the pair as
  complementary signatures; only the temporal one is landed.
- **Nothing consumes it yet.** `mesh-records`' ledger line (`scripts/mesh-records:145`) is a fixed
  `printf` and does not carry `aci`, so `mesh-sound-reflex` cannot read it from `records.log`.
  Extending that line touches **13 readers** (`grep -rln 'records\.log' scripts/`) and is a format
  change with its own sweep — deliberately left to the steward rather than smuggled in here
  (memory: `a-format-fix-must-sweep-every-reader`).

## The one-line proposal that follows

Once the ledger carries it: `mesh-sound-reflex` can finally tell **"beatless because it is a steady
hum"** (low `aci`) from **"beatless because the detector failed"** (high `aci`, no beats) — the
distinction CLAUDE.md records the beat detector as structurally unable to make, and the reason the
grind lane's beatless verdict has never been trustworthy.

## Sources

- Farina, A. (2025). *The acoustic complexity index (ACI): theoretical foundations, applied
  perspectives and semantics.* Oikos 2025:e10760. https://doi.org/10.1111/oik.10760
- Pieretti, N., Farina, A., Morri, D. (2011). *A new methodology to infer the singing activity of an
  avian community: The Acoustic Complexity Index (ACI).* Ecological Indicators 11(3):868-873.
- Kull, K. (2010). *Ecosystems are made of semiosic bonds: consortia, umwelten, biophony and
  ecological codes.* Biosemiotics 3:347-357.
- Farina, A. et al. *On the semantics of ecoacoustic codes.* BioSystems (2023), and *Ecoacoustics and
  Multispecies Semiosis*, Biosemiotics (2021) 14:141-165 — the biosemiotic frame the index sits in.
- Springer *Biosemiotics*, vol. 19 (2026), incl. the special collection *Empirical Approaches and
  Theoretical Modelling in Biosemiotics across the Natural Sciences* — the live-literature entry point.
