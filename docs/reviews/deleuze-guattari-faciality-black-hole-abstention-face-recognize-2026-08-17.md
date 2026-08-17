# Faciality's black hole: the deviance class is where a classifier hides its miss rate

LITERATURE review (live), 2026-08-17 · genome@mesh-home · organ: `scripts/mesh-face-recognize`

## Why this one

The genome has 12 prior D&G reviews (`docs/reviews/deleuze-*`, `rhizome-*`, `assembly-theory-*`)
covering asignifying rupture, relations of exteriority, the deterritorialization coefficient,
disjunctive synthesis, double articulation, machinic phylum, order-words, smooth/striated,
rhizome-vs-arborescent, and — as of 2026-08-15 — **transversality**, which `mesh-promises
--transversality` already implements as Guattari's 1964 coefficient with a permutation null.

So the first two candidates this review reached for were **already embodied** and are recorded
here as discards, not findings:

- *Transversality / the La Borde `grille`* (Goffey, *Radical Philosophy* 195, 2016, citing
  Guattari, 'La "Grille"', *Chimères* 34, 1998) — **discarded: already built**, `mesh-promises
  --transversality`.
- *DeLanda's assemblage parameters as "knobs"* (territorialization × coding) — **discarded**:
  the deterritorialization-coefficient review of 2026-07-28 covers the same axis.

A term census across `scripts/`, `docs/` and 813 knowledge files found **faciality at zero
hits** — and the mesh runs a literal faciality machine.

## The concept and the mechanism

**The abstract machine of faciality** (Deleuze & Guattari, *A Thousand Plateaus*, plateau 7,
"Year Zero: Faciality"). Read live via **Yazan Nasrallah, "The face as political
infrastructure", Media@LSE, 26 June 2026**, occasioned by the England & Wales High Court
dismissing the Big Brother Watch / Shaun Thompson challenge to Met Live Facial Recognition on
**21 April 2026** — Thompson was misidentified by the algorithm and detained after failing to
convince officers it was wrong. Anchor text: **Claudio Celis Bueno, "The Face Revisited: Using
Deleuze and Guattari to Explore the Politics of Algorithmic Face Recognition", *Theory, Culture
& Society* 37(1), 2020** (abstract read; full text paywalled — the mechanism below is from ATP
plateau 7 and Nasrallah, not from Celis Bueno's body text, which I could not open).

The mechanism is a **white wall / black hole** system running two operations at once:

1. **Biunivocalization** — sorting a signal into a grid of accepted units: *is it a or b?*
2. **Binarization / rejectivity** — the yes/no: *is it a face at all?*

The operational claim, and the part that is not merely philosophy: **the machine does not
identify — it computes degrees of divergence from a norm-face**, and everything past a
threshold falls into one undifferentiated black hole. Nasrallah's version: the deviance class
is not an accident of a given model, it is what the machine *is* — "the process that takes raw
visages and processes them into legible, scored, sortable identities."

**The operational consequence we did not embody: the black hole has no floor.** A machine with
no output for "a face I cannot place" must emit its own miss rate as a positive class.

## The organ was that machine, literally

`scripts/mesh-face-recognize` classifies into `{Ilya, Rozalia | Nobody, Stranger}` — the
biunivocal grid and the binary, exactly. And `local_map()` had:

```python
if _FEMALE_RE.search(text): return "Rozalia"
if _MALE_RE.search(text):   return "Ilya"
if _EMPTY_RE.search(text):  return "Nobody"
return "Stranger"            # <- the residue of three regexes, sold as an intruder
```

`Stranger` was the **fall-through**. The empty string is the worst case and it is *documented in
this same file*: the header records that moondream returns `""` outright under some phrasings.
`""` matches no regex — so a total read failure rendered as a person who is not in the household.
The strict prompt was no better: it demanded "EXACTLY one word from this list" with no abstention,
so the model could not decline even when it had nothing.

## Measured before changing anything

`~/.mesh/imac-cam-watch.log`, **449 labelled frames over 8 days**, median inter-frame gap 532s:

| label | episodes | mean run | max run |
|---|---|---|---|
| Ilya | 74 | 4.18 | 30 |
| Rozalia | 39 | 1.59 | 7 |
| Nobody | 43 | 1.37 | 8 |
| **Stranger** | **18** | **1.06** | **2** |

`Stranger` is the **least persistent label in the system** — below even `Nobody`. All 18 episodes
are bracketed by household labels; **not one** begins at START, ends at END, or touches another
Stranger. `Ilya→Stranger→Ilya` ×5, `Rozalia→Stranger→Rozalia` ×2.

A person entering a house does not appear for exactly one nine-minute frame between two frames of
the resident, eighteen times. **That 4.0% is the grid's own miss rate wearing the deviance label** —
constancy across the corpus is the signature of a model property, not a world event.

**Correction to my own first pass:** I initially reported this across "two independent eyes"
(`desk-state.log` too, 4.1% — suspiciously identical). It is not a second vantage:
`desk-state` consumes the *same* classifier via `cam=MOTION(...,who=…)`. There is one eye here,
and no cross-vantage test is available. The run-length and bracketing evidence stands on its own.

## What was already defended, and what was not

`mesh-stranger-watch` already requires **2-of-2** consecutive Stranger frames before announcing —
which suppresses **17 of the 18**. The alarm path was never the hole.

But corroboration living in one consumer is not corroboration (*a rule asserted at one call site
is not asserted*). `mesh-cam-watch:221` and `mesh-desk-state:320` take a single raw `Stranger` and
set `cam_person=1`, writing it into `.cam-face-state` and the fusion line. So the fix belongs at
the **source**, not in each reader.

## The change (uncommitted, in the tree)

`scripts/mesh-face-recognize` — give the machine an output for *a face I cannot place*:

- `local_map()` fall-through → **`Unsure`**, never `Stranger`.
- `CLASSIFY_PROMPT` gains an explicit abstention instruction *and* `Unsure` in its output list;
  `Stranger` is narrowed to "you are **confident** they are not the man or the woman above".
- `LABELS` += `Unsure` (kept last — `canonical_label` substring-matches in list order).

**No consumer needed touching, and that is the point.** All five readers were checked and already
fail closed on a label outside their case-list: `mesh-cam-watch` → `?` rc 2 · `mesh-desk-state` →
`MOTION` with no `who=` and no `cam_person` · `mesh-room` → `UNKNOWN` · `mesh-stranger-watch` →
read-failure → silent · `mesh-operator-home` → only `Ilya` counts. Adding the abstention
*removes* a false person-assertion from four consumers without editing any of them. The four
contract labels survive verbatim (`mesh-misha-eye-contact:10` — "cross-sense vocab is a contract").

## Gates, driven red

`python3 scripts/mesh-face-recognize --test` → ok, live GPU read. Six mutants, scratch copy:

| mutant | result |
|---|---|
| restore the `Stranger` fall-through | RED — *BLACK HOLE: a miss sold as an intruder* |
| prompt instruction flipped back to Stranger | RED |
| output list drops `Unsure` | RED |
| `Stranger` class deleted (rather than un-defaulted) | RED |
| `Unsure` removed from `LABELS` | RED |
| grid eaten by the abstention (everything abstains) | RED |

**Two of these gates were vacuous on first writing and the mutants caught it** — worth recording,
because both are known shapes: `"Unsure" in CLASSIFY_PROMPT` stayed true when the *instruction*
was flipped, because the word survived in the trailing output list (*a name-only source gate
passes on a comment*); and `canonical_label("Unsure") == "Unsure"` round-trips even with `Unsure`
absent from `LABELS`, because the fall-through returns raw text unchanged. Both now probe the
label **embedded in a sentence** and assert instruction and output-list separately.

## The transferable rule

**A classifier with no abstention emits its miss rate as its rarest class** — and because that
class is rare, it reads as a significant event rather than as noise. The tell is a *run-length
inversion*: the deviance label being the least persistent in the system, always bracketed by the
labels it is supposedly distinct from. Any forced-choice grid in the mesh has this shape; the
audit is one query over its own log, and it costs nothing to run.

## Sources

- Yazan Nasrallah, "The face as political infrastructure", Media@LSE, 26 Jun 2026 —
  <https://blogs.lse.ac.uk/medialse/2026/06/26/the-face-as-political-infrastructure/>
- Claudio Celis Bueno, "The Face Revisited: Using Deleuze and Guattari to Explore the Politics of
  Algorithmic Face Recognition", *Theory, Culture & Society* 37(1), 2020 —
  <https://journals.sagepub.com/doi/10.1177/0263276419867752> (abstract only; paywalled)
- Deleuze & Guattari, *A Thousand Plateaus*, plateau 7 "Year Zero: Faciality"
- *Discarded as already-embodied:* Andrew Goffey, "Guattari and transversality: Institutions,
  analysis and experimentation", *Radical Philosophy* 195, 2016 —
  <https://www.radicalphilosophy.com/article/guattari-and-transversality>
- *Discarded as already-embodied:* "Transversality, or How Not to Reproduce the Organisations You
  Fight", *Deleuze and Guattari Studies*, 2024 — <https://www.euppublishing.com/doi/10.3366/dlgs.2024.0544>
