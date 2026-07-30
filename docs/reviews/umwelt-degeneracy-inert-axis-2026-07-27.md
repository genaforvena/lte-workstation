# Live-literature review — biosemiotics: Umwelt degeneracy, and the axis that reads but no longer means

Date: 2026-07-27 · lane: genome (idea-queue LITERATURE task) · status: fix in tree, uncommitted

## Where we had already been (so this doesn't double-count)

Two prior biosemiotics landings:

- **2026-07-12** → `scripts/mesh-interpretant`: semantic information (Kolchinsky & Wolpert 2018;
  Sowinski et al. 2024) — *does a sign have a receiver at all?*
- **2026-07-24** → `docs/reviews/biosemiotics-functional-cycle-closure-2026-07-24.md`: von Uexküll's
  Funktionskreis — *the un-closed return leg of an actuator's effect.*

Both ask whether a sign relation **exists**. Neither asks whether a sign relation that once existed
has quietly **died while every liveness proxy stayed green**. That is this landing.

## The live source

Searched the journal itself rather than a reading list: Crossref's works feed for *Biosemiotics*
(ISSN 1875-1342), sorted by publication date, gives the field's actual last eight weeks
(`api.crossref.org/journals/1875-1342/works?filter=from-pub-date:2025-06-01&sort=published`).

**Landed on:** M. van Walsum, *"Umwelt Degeneracy as the Primary Cause of North Atlantic Pink Salmon
Invasion"*, **Biosemiotics**, published **2026-06-11** — <https://doi.org/10.1007/s12304-026-09646-0>
(six weeks old at review time; abstract via Crossref, argument via the Springer article page).

Also read for context in the same sweep: Kleisner & Stella, *"Ultraviolet 'Umwelten': Exploring
Semantic Organs Beyond the Visible Spectrum"* (2026-06-10, 10.1007/s12304-026-09648-y); Bivolarski,
*"Time and Meaning: On the Role of Biological Rhythms in the Origins of Semiosis"* (2025-09-09,
10.1007/s12304-025-09622-0); Bove, *"What is Food? Towards a Biosemiotic Definition"* (2026-06-19).

## The mechanism: Umwelt degeneracy

Not a failure of the sense organ — a **loss-of-function in the organism's sign relation to its
environment**, which is then **rewarded**. Introduced pink salmon degenerated their natal-stream
homing capacity; the resulting wanderers escaped intraspecific competition (density-dependent
effects dominate salmonid survival), so survival rates and range **rose**. The invasion is caused by
the loss of a discrimination, not by a new capability.

The paper's diagnostic indices — the part that transfers:

- **loss of environmental preference**: post-2017 fish colonise rivers of *all* sizes, where the
  ancestral population preferred a specific discharge range. The behaviour **stopped covarying**
  with the environmental variable it used to be conditioned on.
- **genetic homogeneity across disparate locations** — the same response everywhere.
- **"aimless behaviour"**, unpredictable movement — variety is *not* reduced.

Note the shape carefully: a degenerate Umwelt does **not** look like collapse. Output variety can go
**up**. What dies is the *conditional* relation between output and world.

## What the mesh already has — and why none of it sees this

| instrument | what it detects | why it misses degeneracy |
|---|---|---|
| `mesh-reflex-health`, `mesh-pulse`, `mesh-state-touch` | staleness (`now - mtime > lease`) | a degenerate axis is perfectly fresh |
| `mesh-novelty --diversity` | monoculture / Shannon-evenness collapse of the board's marker repertoire | degeneracy *keeps* variety; it even scores as healthier |
| `mesh-interpretant` | a sign with no receiver | a coarse sign has *more* receivers, not fewer |
| honest-fusion rule (`UNAVAILABLE`) | an **absent/unreachable** axis | this axis is present, fresh, and answering |
| `docs/reviews/correlation-…-spurious-2026-07-25.md` | a correlation that is spurious | the inverse case: a correlation presumed and gone |

So every metric we own is either indifferent to degeneracy or **rewards** it: coverage up, `n/a` rate
down, freshness green, consumer count up. This is the density-dependent fitness benefit, in our own
metric set.

## Measured live on this node

`~/.mesh/home-state.log`, the tape `scripts/mesh-home-state` writes on every evaluation, carries the
verdict **and** its input axes on one line, so the conditional relation is directly computable.
n = 2756 evaluations (2026-07-14 → 2026-07-27), H(verdict) = **0.930 bits**:

| axis | I(verdict; axis) | share of H(verdict) | I(·|hour-band) |
|---|---|---|---|
| `hour` (the wall clock — not a sensor) | 0.436 bits | **47%** | — |
| `ble_named` | 0.041 | 4.4% | 0.085 |
| `room-fresh` | 0.028 | 3.0% | 0.017 |
| `person_ble` | 0.019 | 2.0% | 0.018 |
| `speech` | 0.007 | 0.8% | 0.007 |

Half the verdict's information is the clock. Every *sensed* axis contributes a few percent. And one
axis is a literal constant: **`speech` took the value `0` in 2126 of 2128 observations**
(H = 0.011 bits) — the receptor was read, printed, and scored 2126 times without ever distinguishing
anything. Loss of environmental preference, measured.

### Why the constant axis was invisible — and it is worse than a dead sensor

`mesh-home-state` already had an honest-n/a branch for this axis (`speech=UNAVAILABLE (transcript
source stale/absent — not evidence of silence)`, added after phaedra's false-`ASLEEP`, 2026-07-08).
It fired **2 times in 2756**. The gate it hangs on is the transcript file's mtime:

- `scripts/mesh-transcribe:18` — `CHUNK=…; mkdir -p "$MESH"; touch "$LOG"` — runs in the **prologue,
  before argument dispatch**. `--test`, `--tail`, *any* invocation re-stamps the file. mesh-doctor
  runs every tool's `--test` hourly.
- Live right now: `~/.mesh/transcript.log` is **0 bytes**, mtime **minutes old**. The consumer reads
  that as "a live transcription pipeline across a quiet stretch" and scores `speech=0 (silent)` as
  positive evidence for `QUIET_NIGHT`/`ASLEEP` — *and* `speech_reachable` satisfies the `sensed`
  predicate (`scripts/mesh-home-state:942`), the guard that is supposed to render a senseless node
  honest-`UNKNOWN`.
- Deeper: `mesh-transcribe` writes `14:37:42Z  <text>` (time-only, `date -u +%H:%M:%SZ`) while the
  reader calls `datetime.fromisoformat("14:37:42+00:00")` → `ValueError`, swallowed by
  `except (ValueError, IndexError): pass`. **The axis could not have been non-zero even with a
  working mic.** The sign relation is dead at both ends; the mtime says alive.

This is the mesh's own silent-fallback doctrine one level up. `mesh-state-touch`'s convention —
*mtime = ran-live, content = the value* — is right for a change-gated reflex writing its own state.
It is **wrong as a liveness proof for a value axis someone else consumes**: there, mtime proves a
touch, not a transcription.

### One near-miss, recorded

`~/.mesh/room-sense.log` first looked like a textbook case (138/138 lines `PRESENT … confidence=high`
against wildly varying inputs). It is not: `scripts/mesh-room-sense:1289-1295` emits that line only
on a confirmed edge **and** only when `verdict=PRESENT && confidence=high` (`MISHA_CONFIRMED_ONLY`).
The uniformity is the filter, not the sense. A verdict-filtered log cannot answer a question about
covariance — checking the writer before believing the tape is the whole discipline here.

## The fix — one file: `scripts/mesh-home-state` (in tree, uncommitted)

**Liveness of a value axis is proven by a value the reader can actually read**, never by the file's
timestamp: `fresh` **and** non-empty **and** ≥1 parseable line. The two dead modes now say what they
are, distinctly from stale/absent:

- `speech=UNAVAILABLE (transcript source INERT (mtime-fresh but the pipeline has never written a
  line — a bare touch is not a transcription) — not evidence of silence)`
- `speech=UNAVAILABLE (transcript source UNPARSEABLE (N line(s), none carry a dated timestamp —
  writer/reader format break) — not evidence of silence)`

Live effect on this node right now: the speech axis reports `INERT` instead of contributing 2126
counterfeit votes for silence, and no longer props up `sensed`.

Four fixtures added to `--test`, each seen **RED** against its own mutant before being made green:

| fixture | asserts | mutant that made it fail |
|---|---|---|
| (a) touched-but-empty | not "silent"; names `INERT`; still honest n/a `exit 2` | restore mtime-only gate → node broadcast `ASLEEP` at 17h local on zero evidence |
| (b) unparseable (real time-only format) | not "silent"; names the format break | mark unparseable reachable → `speech=0 (silent)`, `ASLEEP` |
| (c) dated recent line | words actually scored (`speech=16 words`) | — parse-path guard |
| (d) live pipeline, quiet stretch | a live axis **can still say** `speech=0 (silent)` | blanket-mute → every silence became `UNAVAILABLE`, node went `UNKNOWN` |

(d) exists because (c) could not catch the blanket-mute mutant — the `UNAVAILABLE` branch is only
reachable when `speech_words == 0`. Both edges of the gate needed their own fixture.

## Honest scope — what this does NOT do

- **The producer's format break is exposed, not repaired.** Fixing `mesh-transcribe`'s time-only
  stamp is a second file, and a "assume today" repair in the reader would resurrect yesterday's words
  as fresh speech — strictly worse than a loud `UNPARSEABLE`. Flagged for the senses lane.
- **No general degeneracy audit was built.** The natural next instrument is per-axis
  I(verdict; axis | clock) over a sense's own tape, flagging axes that have gone inert — the numbers
  in this review were computed ad-hoc. Proposed, not landed; and it needs a tape that is *not*
  verdict-filtered (see the room-sense near-miss), which most senses do not write.
- **One node, one log, one window.** The MI figures are this corpus's current answer, not constants —
  the claim is the gate, per the doctrine on re-derived figures.

## The transferable sentence

An organ can keep every receptor, stay fresh, stay well-connected, and lose the sign relation
entirely — and in a mesh that scores coverage and freshness, that loss is not penalised but
**rewarded**. Absence we already model. **Inertness we did not**: a value axis is alive only if it
can be seen to distinguish something.
