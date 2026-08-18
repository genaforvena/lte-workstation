# Live-literature review — biosemiotics: EFFICIENCY SENSING — a census count is `n_true × p`, and the mesh never wrote the `p`

Date: 2026-08-17 · lane: genome (idea-queue LITERATURE task — biosemiotics, from the angle of a concrete
METRIC the area uses to measure itself) · status: fix in tree, uncommitted (steward lands)

## Where we had already been (checked in the tree BEFORE landing, so this doesn't double-count)

Biosemiotics is one of the mesh's most-worked seams — 202 reviews in `docs/reviews/`, ten of them
biosemiotic. Everything obvious in the "measure the sign relation" direction is already embodied, and I
checked each by grep before choosing:

- **Semantic information** (Kolchinsky & Wolpert 2018 — scramble a channel, measure the viability cost;
  Sowinski et al. PRX Life 2023 semantic threshold) → `docs/reviews/info-theory-agency-semantic-information-scramble-viability-2026-07-29.md`, `scripts/mesh-interpretant`.
- **Schneider's R_sequence ≈ R_frequency** — and, precisely, the 2026 *Biosemiotics* paper that carries it
  (Nielsen, Vitti-Rodrigues & Emmeche, "Measuring Meaning of Molecular Motifs", 19:205-222, doi
  10.1007/s12304-026-09637-1) — **already landed**, as `mesh-promises --specificity`. Found it by grep
  after picking it; the landing was taken.
- **Umwelt degeneracy / the inert axis**, and with it Kleisner's UV "semantic organs" → `docs/reviews/umwelt-degeneracy-inert-axis-2026-07-27.md`.
- **Code vs interpretant** (Barbieri/Kull, *Biosemiotics* 18(1), 2025) → `biosemiotics-code-vs-interpretant-light-expectedness-2026-07-29.md`.
- **Funktionskreis closure**, **index vs icon**, **code duality**, **interactive sign**, **habituation /
  dishabituation** (`second-order-cyb-algedonic-habituation-alarm-fatigue-2026-07-28.md`), **tunable
  quorum thresholds** (`swarm-tunable-quorum-speed-accuracy-2026-07-28.md`).

Quorum is in the tree as a *threshold* (how many votes before we act). **What is nowhere in the tree —
zero hits across `docs/` and all 676 `scripts/` — is the ambiguity that the quorum literature spent
twenty years on: `diffusion sensing`, `efficiency sensing`, `autoinducer`.** That is the gap.

## The live source

The journal's own feed, not a reading list — Crossref works for *Biosemiotics* (ISSN 1875-1342) sorted by
publication date, which gives the field's actual last months (Aug 2026 back through 2025). The bacterial
lane is live in it: **"Exploring the Patterns of Bacterial Interactions with the Other"**
(*Biosemiotics*, 2025-10-28, doi `10.1007/s12304-025-09629-7`) and **"The Sense of Microbial Harmony as a
Cognitive Biosemiotic Framework for Health and Well-Being"** (2026-05-12, doi
`10.1007/s12304-026-09647-z`). The concrete mechanism those sit on, tracked back to its primary sources:

- R. J. Redfield, **"Is quorum sensing a side effect of diffusion sensing?"**, *Trends in Microbiology*
  10(8):365-370 (2002) — the original charge: the cell may not be counting neighbours at all; it may be
  measuring how fast its own molecules leave.
- B. A. Hense, C. Kuttler, J. Müller, M. Rothballer, A. Hartmann & J.-U. Kreft, **"Does efficiency
  sensing unify diffusion and quorum sensing?"**, *Nature Reviews Microbiology* 5:230-239 (2007) — the
  resolution, and the transferable metric.
  (Found via search; both are the canonical citations the 2020s literature still argues from, e.g.
  *Nature Communications* 14 (2023), "Quorum sensing as a mechanism to harness the wisdom of the crowds".)

## The concept not yet embodied — EFFICIENCY SENSING

A bacterium reads one scalar: the local concentration of its own autoinducer. That scalar is
**density × transport**. It rises when there are more neighbours, and it rises identically when the
neighbours are unchanged but the medium confines the molecule (a biofilm, a pore, a small volume). The
cell **cannot** separate the two from one signal, and the field's answer is not a better estimator — it
is a change of claim. Efficiency sensing says the cell never publishes a population count at all: it
reads the pair as *"is secreting this costly molecule going to pay off here?"* and that question is
answered correctly by the confounded scalar. The confound is not noise; for that interpretant it **is**
the content.

That is the biosemiotic bite, and it is why this is a sign relation and not a sensor bug: the same
physical reading means two different things to two different interpretants, and only one of them is the
one the organism actually holds. Where the receiver DOES need the two apart, biology pays for a second
channel — autoinducers with different diffusivity and half-life, read jointly.

**The mesh transfers this exactly.** Every RF census the mesh runs publishes a COUNT and the count is
`n_true × p`, where `p` is the per-tick probability that a present device is actually detected — and `p`
is nowhere in the mesh's vocabulary.

## The organ, and what its own log says

`scripts/mesh-bt-census` — the BR/EDR inquiry census, cron-wired `11-59/19`, `--edge`. Its radio guard is
already careful and already all-or-nothing: adapter DOWN ⇒ honest exit 2, *"cannot distinguish
no-devices from radio-off"*. The binary case is covered. **The graded case has no term at all**: a radio
that is UP but dim yields a smaller `n`, and the tool mints `DEPARTED` for the difference. On this node
that is not hypothetical — `p` rides the combo wifi+BT chip that carries the sole uplink and is
documented in `CLAUDE.local.md` to fault, with the BT half named there as the untested suspect.

`p` is recoverable the way the biology recovers it: from a source whose emission is known constant. A
device that does not leave the room cannot depart for one census tick and come back. Replaying
`~/.mesh/bt-census.log` — 264 censuses, 2026-07-15 → 2026-08-17, 157 ARRIVED / 156 DEPARTED:

| device | CoD | absence episodes | one tick (≤28 min) | median absence |
|---|---|---|---|---|
| `E7:4D:F9:65:B0:65` | `0x240404` A/V Headset | 18 | **15 (83%)** | 19 min |
| `EC:C1:AB:D1:A7:EF` | `0x380424` A/V Set-top-box | 20 | **15 (75%)** | 19 min |
| `5C:49:7D:92:1E:58` | — | 52 | 13 (25%) | 90 min |
| `D4:8A:3B:1A:82:A1` | — | 14 | 3 (21%) | 14.3 h |
| `84:C8:A0:16:04:8A` | — | 14 | 2 (14%) | 34.0 h |
| `F0:A3:B2:DF:EB:83` | — | 14 | **0 (0%)** | 31.8 h |

The split is not subtle: the two bolted-down A/V devices leave for exactly one tick and come back; the
phones leave for half a day. **52 of 141 absence episodes mesh-wide are one tick long.** Estimated over
the anchors' 3196 tick-opportunities, **p̂ = 0.991** — about **30 DEPARTED/ARRIVED pairs in a month that
no device performed**, each published to `bt-census.log` where the presence/arrivals fusion reads them.

Note what p̂ is and is not: it is measured on the loudest, nearest, most reliably-discoverable devices,
so it is an **upper bound**. A fainter device's `p` is strictly worse and stays unobserved — which is
the efficiency-sensing point restated, not a caveat that dissolves it.

## The change (uncommitted, in tree)

`scripts/mesh-bt-census`:

1. **`--efficiency`** — report-only, pure log replay (no radio, no adapter, no network). Recovers the
   anchor set from the log's own absence-duration structure (never a hand-listed MAC — a pinned address
   ages out the moment the headset is replaced, and then `p` is estimated from a device that IS gone)
   and prints `p`, the anchor count, the mesh-wide one-tick fraction, and the anchors it used. Live now:
   `EFFICIENCY p=0.9906 anchors=2 one-tick=52/141 anchor-ticks=3196 anchors=[E7:4D:F9:65:B0:65,EC:C1:AB:D1:A7:EF]`
2. **`MISS-SUSPECT`** — a new, purely additive log line emitted **beside** a `DEPARTED` when the
   departing device is an anchor, i.e. when `p` says it cannot leave. The departure and the reason to
   doubt it arrive together, or nobody reads both.
3. The census tick is **read from the file's own `# reflex-cadence:` header**, not copied as a second
   `19` that rots the moment the cadence is retuned.
4. An unmeasurable channel renders **`na` + exit 2**, never `p=1.0`. A fabricated unity would make a
   dark radio publish itself as a perfect one — the silent-fallback shape.

**Report-only on purpose** (instrument-before-actuator, the discipline `mesh-promises --specificity`
already follows in this genome). Suppressing an anchor's `DEPARTED` until a second consecutive miss
trades a false departure for a delayed real one, and that trade wants live `MISS-SUSPECT` counts first.
That is the steward's call, not this landing's.

## Gates — seen RED, then GREEN

`--test` grows 17 → **23 assertions** (`ok`, incl. the pre-existing live-inquiry leg; hci0 `UP RUNNING`
and the uplink healthy at the time, so the live leg was one extra inquiry on a cadence that already runs
one every 19 min). Every new gate was broken from a scratch copy and watched fail:

| mutant | result |
|---|---|
| cadence hardcoded 7 min instead of read from the header | **RED** — 3 assertions |
| `na` branch replaced by a fabricated `p=1.0000` | **RED** — "eff no-anchor must exit 2 with no stdout claim" |
| the `MISS-SUSPECT` emit line alone removed (test left intact) | **RED** — 1/23 |
| `MISS-SUSPECT` fired for every device instead of anchors | **RED** — "mobile departure must NOT be flagged" |

(The first attempt at the last-but-one mutant deleted the *assertion* along with the emit — `sed
'/MISS-SUSPECT/d'` matches both — and came back green with 21 assertions instead of 23. That is the
mutant-can-go-green-for-the-wrong-reason trap; the assertion count is what exposed it.)

## Discarded on the way (recorded so the next mind doesn't re-derive it)

**Kleisner & Stella's calibrated cross-band imaging → `scripts/mesh-cam-light`.** The UV-Umwelten paper
(*Biosemiotics*, 2026-06-10, doi `10.1007/s12304-026-09648-y`) argues that a signal read outside a
calibration standard measures your instrument, not the world. `mesh-cam-light` classifies **absolute**
mean grayscale into DARK…BRIGHT off a frame that `mesh-cam-watch` deliberately captures with
`fswebcam -S 8`, *"frames to skip for exposure"* — i.e. after auto-exposure has converged. The
hypothesis was that the vocab therefore measures the camera's AGC target. **Measured and falsified**:
903 frames in `~/.mesh/cam-events.log` track the diurnal cycle cleanly (median mean-luma 155 at 12:00
UTC, 18 at 00:00 UTC), and `v4l2-ctl --list-ctrls` shows this device exposes **no** exposure or gain
controls at all. The camera is effectively fixed-exposure; the calibration critique does not bite here.
Also checked and rejected as already-landed: Schneider R_seq/R_freq (`mesh-promises --specificity`),
habituation/dishabituation, semantic organs, umwelt degeneracy.

## The doctrine line this earns

**A count is a claim about a population only if the detection probability is written next to it.**
`n=<devices>` from any scanning sense is `n_true × p`, and an all-or-nothing radio guard (up ⇒ trust the
count, down ⇒ n/a) covers only the case where `p` is 0. Recover `p` from the sources you know do not
move, publish the pair, and let a departure that `p` cannot distinguish from a miss say so in its own
line. Siblings with the same shape and no `p` term today: `scripts/mesh-ble-proximity`,
`scripts/mesh-wifiscan`, `scripts/mesh-mdns-census`, `scripts/mesh-lan-presence` — flagged, not fixed
(a fix scoped to the measured lane leaves its siblings broken; each needs its own anchor set measured,
not this one's number copied).
