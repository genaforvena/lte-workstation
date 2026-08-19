# Live-literature review — biosemiotics: the SENOME's ANALOG CONTINUUM (valence resolution) vs the mesh's band-word senses

Date: 2026-08-18 · lane: genome (idea-queue LITERATURE task) · status: implemented, uncommitted (steward lands from the tree)

## Area & angle

Biosemiotics — sign and meaning in living systems — transferred to a distributed sensor mesh, sampled
off the **live** front rather than a reading list. Reproducible enumeration:

```bash
# the journal's 2026 volume (Springer article pages 303 → idp.springer.com for BOTH curl and WebFetch)
curl -s "https://api.openalex.org/works?filter=primary_location.source.issn:1875-1342,from_publication_date:2026-01-01&per-page=60&sort=publication_date:desc&select=display_name,publication_date,doi,abstract_inverted_index,open_access"
curl -s "https://api.crossref.org/journals/1875-1350/works?filter=from-created-date:2026-06-01&sort=created&order=desc"
```

21 *Biosemiotics* items in 2026 (newest 2026-08-14). The fresh, unmined ones are all **paywalled from
this node and from WebFetch** — "Memes as Structural Signals: A Chemical Model of Interpretive
Compatibility" (2026-06-26, doi:10.1007/s12304-026-09653-1) has no abstract in OpenAlex *or* Crossref, and
the OA items' own PDF URLs return a 3 KB bot-challenge page (`link.springer.com/content/pdf/…` → 200,
`file` says HTML). *Sign Systems Studies* 53(3–4) — the other live OA venue — was **already mined this
morning** by `biosemiotics-dialogue-of-constraints-paradigm-of-choice-mesh-organ-2026-08-18.md` (Lacková
Bennett read in full). So the landing was made in a venue this lane had not used: a 2026 OA journal
article in the biosemiotic lineage proper (Uexküll → Kull → Baluška), readable end to end.

Set aside, with the reason:

- *Fungal Aesthetics and Multispecies Semiosis in Visual Art* (2026-06-26, OA) — art-historical; no mechanism.
- *Umwelt-based Analysis of Multispecies Places* (2026-04-15, OA) — a fieldwork protocol for human/other-than-human
  place analysis; the transferable core (consortium of Umwelten) is already `umwelt-degeneracy-inert-axis-2026-07-27.md`'s neighbourhood.
- *What is Food? Towards a Biosemiotic Definition* (2026-06-19, OA-but-walled) — "material substances become
  nutritively relevant only through sign relations that are efficient yet fallible". Genuinely interesting and
  **adjacent to ours**: `biosemiotics-incentive-salience-wanting-vs-liking-needs-2026-08-18.md` covers the
  wanting/liking dissociation on the intake lane. Held for a later pass, not because it is ours.
- *On the Methodological Foundations of Biosemiotics*, *The Hominin-Canine Axis*, *A Semiotic and
  Systems-Theoretic Framework for the Emergence of Consciousness* — no abstract obtainable from any open index
  and no full text; discarded for **source quality, not content** (reading a title is not reading a paper).

## The concept we did NOT embody: the senome is ANALOG, and the analog-ness is load-bearing

Source (live, 2026, read in full):
**Luís Felipe Basso, František Baluška, Gustavo Maia Souza, "Plant agency: from senome and electrome to
plant semiosphere"**, *Frontiers in Plant Physiology* **4** (2026), Sec. Environmental Interactions,
published **2026-05-20**, doi:[10.3389/fphgy.2026.1861112](https://doi.org/10.3389/fphgy.2026.1861112).

A plant has no neural centre, so all of its sense-making has to be done by a **senome** — *"an integrative
information field that unifies the activities of all the cell's sensory proteins"*, the analog interface
between internal state and environment. The paper's load-bearing claim is not that this field exists but
that its being **analog** is what makes interpretation possible at all:

> "This analog nature allows for a **continuum of intensity and significance**, providing the necessary
> **resolution for the emergence of semiotic interpretation** and allowing the cell to perform real-time
> **valence evaluations** of environmental conditions."

and the semiotic threshold is *not* a bin boundary — it is where a perturbation acquires valence:

> "sensory proteins that operate as biological Maxwell's demons … allowing the system to perform
> anti-entropic work oriented toward survival goals. This evaluative process represents the emergence of a
> **semiotic threshold**, where raw physical perturbations are no longer merely 'data' to be transmitted,
> but are integrated as **functional information that carries biological valence**."

**Not already ours.** `senome`, `electrome`, `ephaptic`, `semiosphere`, `semiotic threshold`, `episenome`:
**0 hits each** across `docs/` and `scripts/` (grep, 2026-08-18). The nearest things we hold are all a
different failure:

- `umwelt-degeneracy-inert-axis-2026-07-27.md` — an axis that carries **no** information. Here the axis
  carries information and the **publication** destroys it.
- memory `a-well-gated-producers-vocabulary-flattened-by-its-consumer`, `degraded-collapsed-to-offline-in-fusion-reader`
  — collapse **between labels, at the consumer**. This is collapse **below the labels, at the producer**.
- `max-fold-effaces-the-disjunction` — a fold that loses which member won; not a reading that loses where it sat.
- `mesh-home-state`'s margin/entropy ledger — margin between **rival candidates**. `to_edge` below is
  distance from a reading to **its own band boundary in the metric's own unit**: a different geometry.
- memory `a-band-pinned-only-by-synthetic-edges` / `stress-thermal-bands-calibrated-to-a-dead-regime` — whether
  the edges are in the right place. This is where the reading sits relative to whatever edges exist.
- The practice half-exists: `.dram-bw.state` publishes `level=IDLE|gbps=2.25|window=inst|cov=100`. **28 of this
  node's 98 `~/.mesh/*.state` files are a bare single word** (`.psi.state CALM`, `.cppc.state BOOST`,
  `.cpu-avgfreq.state NOMINAL`, `.household.state ACTIVE`, `.cell-signal.state FAIR`, …). Nothing anywhere
  publishes a **normalized within-band position**.

## The gap, measured on this node's own corpus

`mesh-cell-signal` reads a real continuum — serving-cell RSRP in dBm — bands it into five words, and
published **only the word**: `.cell-signal.state` was 5 bytes, `FAIR`. Replaying all 176 successful reads in
`~/.mesh/cell-signal.log` (243 lines: 176 reads + 67 honest `unreachable`, unrotated, cron-appended since the
2026-08-15 autowire) through the new `bandpos()`:

| | |
|---|---|
| verdict changes over consecutive successful reads | **64** of 175 pairs |
| …driven by a move of **≤2 dB** | **10** |
| pairs that moved **≥5 dB with no change of word** (max 7 dB) | **9** |
| smallest move that renamed the link | **1 dB** |
| median distance to the nearest threshold (`to_edge`) | **2 dB** |
| reads within 1 dB of flipping the published word | **63 / 176 (35.8%)** |
| reads sitting **exactly on** a threshold | **26 / 176 (14.8%)** |
| joint-modal interior position | **pos=0.00** — the band's own degrading edge (25 reads) |
| most frequent single reading of this sense | **−110 dBm** = the FAIR floor, 1 dB from POOR (19×) |

Two things fall out, and neither is visible in a band word:

1. **The label's sensitivity is unrelated to how far the signal moved.** A 1 dB wobble renames the uplink;
   a 7 dB collapse is silent. The word is maximally twitchy exactly where the continuum is least
   informative (at an edge) and maximally deaf where it moves most (inside a band).
2. **Half of all readings live within 2 dB of a threshold**, so for half the mesh's perceptions of the
   phone's cell link, the published word was a coin-flip away from being a different word — and the mesh's
   single most common perception was "FAIR", at the exact dB where FAIR ends.

This is the senome claim in mesh form: the *resolution* the continuum provides is what lets a reading carry
valence. Band-only publishing keeps the classification and throws away the valence.

## The instrument (implemented): `bandpos()` in `scripts/mesh-cell-signal`

Instrument-first — **the verdict vocabulary and its thresholds are untouched.** Added beside it:

```
pos        0.00 at the band's DEGRADING edge → 0.99 at its improving edge (interior bands only)
to_worse   dB above this band's own floor  (0 = one more dB down renames the link)
to_better  dB up to the next better band's floor
span       band width, dB
open       none | up | down   (which side, if any, has no edge)
to_edge    min over the sides that EXIST — defined in every band, including the open ones
```

Live in all three outputs: `--json` gains `pos/to_worse_db/to_better_db/band_span_db/band_open/to_edge_db`;
`--edge` writes `FAIR|dbm=-110|pos=0.00|to_edge=0|to_worse=0|to_better=10|open=none|ts=…` (**verdict stays
field 1**, `cut -d'|' -f1` — the continuum is appended beside the word, never in place of it; the state file
has **zero readers** in the tool corpus today, checked, so nothing is broken either way); the human/log line
gains `pos=… to_edge=…dB (… above floor, … below next band) at=<ts>` — the log's verdict lines carried **no
timestamp at all**, which is why Δt between the pairs above is unrecoverable, and is fixed going forward.

Design decisions that are doctrine, not taste:

- **One ladder.** The band floors were an `if/elif` chain; `bandpos` would have needed a second copy of the
  same five numbers. They are now one `BAND_FLOORS` table read by both `classify()` and `bandpos()` — an
  enumerated alphabet that is a copy is a copy that rots, and a position computed against edges the verdict
  no longer uses is worse than no position.
- **An open band renders `pos=na`, never 0.0/1.0.** EXCELLENT (≥ −90) and MARGINAL (< −120) have one edge;
  a position needs two. A fabricated 1.0 would read as "at the top edge" for a band that has no top.
  `to_edge` is still defined there (it takes the side that exists) — that is why `to_edge`, not `pos`, is
  the field a fusion consumer should read.
- **No `eval`.** The extraction is `bp_field`, because `METRIC` is a value the phone hands us and an
  `eval`'d assignment is where a writer-controlled value escapes its own record format.
- **`bp_field` is hoisted, not inlined.** On this sense the extraction only ever runs on a real phone read —
  i.e. exactly where a `--test` cannot reach it. Hoisting makes the *wiring* assertable, not just the pure
  function behind it.

## Gates — and each one seen RED

`--test` now carries: 6 classify + 2 honest-unknown + 1 registered-parse (pre-existing), **6 bandpos
fixtures**, a **52-value structural sweep**, **7 extractor-wiring assertions**, then the pre-existing
REAL-READ leg (honest exit 2 when the phone is unreachable → `mesh-land` treats 2 as a pass).

The sweep is the gate that cannot be satisfied by the numbers merely being present: for every dBm from
−130 to −79 it steps to the floor `bandpos` reports and asserts the band still holds, steps one dB past it
and asserts the word **changes**, does the mirror at the upper edge, and asserts `to_edge = min(…)` and that
open bands render `na`. It asserts behaviour, never source text.

Mutants run from a scratch copy (`/tmp/…/scratchpad/mut-*`), each verified to have actually applied:

| mutant | result |
|---|---|
| `to_w = m - floor + 1` (off-by-one floor) | **rc=1**, 53 FAIL lines, 43 from the sweep |
| open band renders `pos=0.00` instead of `na` | **rc=1**, 26 FAIL, 23 from the sweep |
| `to_edge` takes `max` instead of `min` | **rc=1**, 30 FAIL, 27 from the sweep |
| `bp_field` drops the `=` from its prefix strip | **rc=1**, 8 FAIL (wiring leg) |

Clean tree, phone back at 23:54Z: `smoke-test: ok (classify:6 + honest-unknown:2 + registered-parse:1 +
bandpos:6 + edge-sweep:52 + extractor-wiring:7 + REAL registered-cell RSRP read)`, **rc=0**. While the phone
was down (23:36→23:54Z) it was `n/a … classify/parse/bandpos logic ok`, **rc=2** — honest, and the bandpos
legs ran green either way.

## First live readings (all three outputs, real phone)

```
cell=POOR (-114dBm rsrq=-8 lte band=7 bars=1 | 2 cells visible) pos=0.60 to_edge=4dB (6dB above floor, 4dB below next band, open=none) at=2026-08-18T23:54:24Z
{"ts":"2026-08-18T23:54:38Z","status":"OK","verdict":"POOR","dbm":-113,…,"pos":0.70,"to_worse_db":7,"to_better_db":3,"band_span_db":10,"band_open":"none","to_edge_db":3}
.cell-signal.state → POOR|dbm=-113|pos=0.70|to_edge=3|to_worse=7|to_better=3|open=none|ts=2026-08-18T23:54:39Z
```

The first live pair already shows the axis doing the work it was built for. Against the pre-patch 23:32:28Z
reading (`FAIR`, −110, `pos=0.00`, `to_edge=0`), the word got **worse** (FAIR→POOR) while the word's own
**reliability got better**: −110 was a coin-flip FAIR sitting exactly on its floor, −113 is a POOR with 3–4 dB
of room on both sides. Those are two independent facts about the same sense and the band word carries only
one of them.

## Honest limits

- The **corpus table** above is replay of 176 real logged readings, not 176 live renders — the log predates
  the patch. The live render is the block above (three outputs, real phone, 23:54Z). Nothing here was
  produced with an injected fixture (an injected fixture bypasses the parser); while the phone was down the
  review said so instead of manufacturing a reading.
- `n=176` is the log **as it stands**, not a fixed population; re-derive rather than quote.
- Δ between "consecutive reads" is between consecutive **successful** reads; 67 unreachable runs interleave
  and the old log lines carried no timestamp, so the real Δt is unknown and unbounded. The 1 dB / 7 dB
  asymmetry is about magnitude, not rate, and does not depend on Δt.
- `classify()` uses one dBm ladder for every RAT (documented in the header since it was written); `pos`
  inherits exactly that approximation — it says where the reading sits in **this** ladder's band, nothing more.
- **The new axis has no consumer yet.** `.cell-signal.state` had zero readers before this change and has zero
  after; publishing the continuum makes the pre-threshold signal *available*, it does not make anything act
  on it. The obvious next step — a fusion reader that notices "three senses are all at `to_edge≤1`
  simultaneously", the systemic approach-to-threshold no single label can show — is **not** in this change
  and is not claimed.
- The generalization is stated, not done: 28 of 98 state files are bare labels. This review instruments
  **one** organ; the population is the follow-on task, per organ, each with its own real corpus.

## Reproduce

```bash
./scripts/mesh-cell-signal --test          # rc 0 with a reachable phone, rc 2 without; bandpos legs run either way
./scripts/mesh-cell-signal --json          # pos / to_edge_db beside the verdict
# the corpus replay behind the table above:
grep -oE '\(-?[0-9]+dBm' ~/.mesh/cell-signal.log | tr -d '(' | sed 's/dBm//' \
  | while read -r m; do bandpos "$m"; done      # after sourcing BAND_FLOORS + bandpos from the script
```
