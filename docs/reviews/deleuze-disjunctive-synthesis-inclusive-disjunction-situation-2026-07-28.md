# Live-literature review — Deleuze & Guattari: the DISJUNCTIVE SYNTHESIS (inclusive vs exclusive disjunction), and the multiplicity a max-fold effaces

Date: 2026-07-28 · lane: genome (idea-queue LITERATURE task — D&G, assemblage/rhizome/machinic, from
the angle of an OPERATIONAL mechanism) · status: fix in tree, uncommitted (steward lands)

## Where we had already been (so this doesn't double-count)

D&G is a well-worked mesh seam. Confirmed the embodied set before landing (from the two prior D&G
reviews of 2026-07-27):

- **rhizome / plane of consistency** → `scripts/mesh-sensor-tape`
- **desire as productive force / rhizomatic coupling** (Anti-Oedipus) → `scripts/mesh-needs`
- **assemblage — degree of territorialization (DeLanda)** + **capacity-to-affect (Atkinson, TCS 2024)** → `scripts/mesh-digest`
- **cognitive assemblages (Hayles)** → `scripts/mesh-pane-consume`
- **the refrain / ritornello** → `scripts/mesh-reflex-health`
- **societies of control / modulation-harms** → `scripts/mesh-operator-mood`
- **assemblage & non-human agency** → `scripts/mesh-window-state`
- **order-word works by redundancy** (plateau 4) → the board (`deleuze-order-word-redundancy-board-2026-07-27.md`)
- **smooth vs striated / intensive residual** (plateau 14, nomadology) → velocity+distance fusion (`deleuze-smooth-striated-intensive-residual-2026-07-27.md`)

Rhizome, assemblage, territorialization, refrain, desire-production, control-modulation, order-word,
smooth/striated are all landed. The **three syntheses of Anti-Oedipus** (connective, disjunctive,
conjunctive) were **not** — specifically the *disjunctive synthesis* and its two contrasting uses.

## The concept not yet embodied — the DISJUNCTIVE SYNTHESIS, and inclusive vs exclusive disjunction

In *Anti-Oedipus*, the second passive synthesis of the unconscious — the **disjunctive synthesis of
recording** — is "an entire system of shuntings" (D&G's railway image: points/levers that keep
alternative routes live). Its critical operational content is that the *same* disjunction admits **two
uses**:

- the **exclusive / restrictive** use — "**either/or**" — which DECIDES and excludes: you are man *or*
  woman, this *or* that. It collapses the alternatives to one term and effaces the rest.
- the **inclusive / nonrestrictive** use — "**either … or … or …**" — which **affirms all the terms of
  the disjunction AND the distances between them** without collapsing them ("he is not man *or* woman,
  he is both", traversed as a series of intensities). D&G's slogan: *"a disjunction that remains
  disjunctive, and that still affirms the disjoined terms."*

The mechanism, stated as engineering: **a synthesis that resolves N live alternatives to 1 has made the
exclusive/restrictive choice; the inclusive use PRESERVES the multiplicity — which alternatives are
simultaneously live, and the DISTANCE between them — as first-class output.** The distance is not noise
to be resolved away; it *is* signal.

**Citations** (found via web review, 2026-07):

- Deleuze & Guattari (1970), **"La synthèse disjonctive"**, *L'Arc* 43 — the source statement of the
  inclusive/exclusive contrast; hosted at the Purdue Deleuze seminar archive
  (`deleuze.cla.purdue.edu/resource/gilles-deleuze-and-felix-guattari-the-disjunctive-synthesis-larc-43-1970`).
- *Anti-Oedipus* §2.4, **"The Disjunctive Synthesis of Recording"** — the "system of shuntings",
  "selections by lot", and the differentiation of organ-machines on the surface of the BwO
  (walkthrough: `medium.com/anti-oedipus/anti-oedipus-2-4-the-disjunctive-synthesis-of-recording-fd1a9b8a669a`).
- Steven Shaviro, **"The Connective and Disjunctive Syntheses"**, *The Pinocchio Theory*
  (`shaviro.com/Blog/?p=646`) — the clearest secondary gloss of inclusive vs restrictive use.
- **"Theory of 'Disjunctive Synthesis' of Deleuze and Guattari"**, ResearchGate publication 372083950
  (2023) — recent scholarly treatment confirming this is live, still-published literature.

## Why it applies to us — and where the exclusive use is already coded

`scripts/mesh-situation` is the mesh's META-fusion: it folds INTERNAL (`mesh-stress`), EXTERNAL
(`mesh-perimeter`) and PHYSICAL into one posture. The load-bearing fold is, in its own words:

```
iw=$(rank "$int_sev"); ew=$(rank "$ext_sev"); worst=$(( iw > ew ? iw : ew ))
```

This is **exactly the exclusive/restrictive disjunction**: `max()` DECIDES *either*-INTERNAL-*or*-EXTERNAL
and reports the loudest, discarding the other term. The file's own header already indicts the fold from
the **causal-emergence / IIT** angle (a max is a selector, Ψ ≤ 0, "it DISCARDS every joint pattern and
reports the loudest one"), and a prior review
(`~/.mesh/knowledge/review-causal-emergence-situation-max-fold-2026-07-06.md`) proposed a **joint-pattern
synergy rule** — but held it for steward/operator sign-off because it would **change the posture
verdict's semantics** on a cry-wolf-sensitive organ.

The disjunctive-synthesis lens is a **distinct and complementary** reading of the *same* line, and it
does **not** require sign-off, because it changes **no verdict**:

- The causal-emergence fix wants to **INVENT a new macro** (a verdict a single axis can't reach) — that
  is the *conjunctive* move, and it alters semantics.
- The disjunctive-synthesis fix wants only to **stop effacing the multiplicity** the max already
  computed — the *inclusive* move: affirm both terms and their distance, alongside the unchanged
  posture.

Concretely, the max renders two very different situations **identically** as `WATCH`:

| situation | INTERNAL | EXTERNAL | old posture | what it means |
|---|---|---|---|---|
| concordant | WATCH | WATCH | `WATCH` | broad pressure across the whole node |
| split | WATCH | NOMINAL | `WATCH` | one loud axis over a calm one (localized, transitional, or a single-axis spike) |

A consumer reading the bare posture cannot tell these apart — yet they call for different responses.

## The application (concrete, one file, additive, verdict-preserving)

Added the **inclusive disjunction** to `scripts/mesh-situation`, right after the fold — additive,
rc-neutral, and it **does not touch `POSTURE` or the `.situation.state` consumer contract** (hence no
semantic sign-off, unlike the held synergy rule):

- `spread = |rank(INTERNAL) − rank(EXTERNAL)|` — literally D&G's **distance between the disjoined terms**.
- `concordance` ∈ {`concordant` (spread 0, axes agree — a joint condition), `split` (one loud axis
  carries the posture), `partial` (a term unreadable — honest-degrade, cannot affirm agreement OR
  divergence, consistent with the existing empty-vs-failed rule)}.
- `loud_axis` ∈ {`internal`, `external`, `none`} — which term the posture rests on.

Emitted on the `--json` contract (`"spread"`, `"concordance"`, `"loud_axis"`) and as a human
`DISJUNCTION` line under the axes.

`--test` gains **RED-first falsifiers**: the existing ALERT fixture is a *split* (int NOMINAL vs ext
ALERT) — asserted `concordance=split`, `spread=2`, `loud_axis=external`; and a new *concordant* fixture
(both axes NOMINAL) asserts `concordance=concordant`, `spread=0`, `loud_axis=none` — proving
`concordance` is derived from the axis relation, not hardcoded. Both breaks verified red-then-green
(hardcode concordant → split fails; zero the spread → spread=2 fails).

## Live proof at landing

```
=== mesh-situation mesh-home @ 2026-07-28T10:45:53Z — WATCH ===
 INTERNAL [WATCH   ] stress=WARM (temp=61C minds=11)
 EXTERNAL [NOMINAL ] CALM (out=CALM net=CALM phy=CALM, 6min ago)
 DISJUNCTION[split ] INTERNAL=WATCH · EXTERNAL=NOMINAL (spread=1, loud=internal)
```

The posture is `WATCH`, but the disjunction reveals it is a **split** WATCH resting on the INTERNAL
(thermal, 61 °C, 11 minds) axis alone while EXTERNAL is calm — *not* a broad concordant WATCH. The max
word alone effaced this; the inclusive disjunction restores it.

## Honest scope

- **Descriptive, verdict-preserving.** The posture is untouched — this only surfaces the two terms and
  their distance the max already collapsed. It is the *minimal* move toward "connect the axes", not the
  synergy rule (which remains the held, sign-off-gated next step).
- **Two axes, not three.** `concordance`/`spread` range over the two *load-bearing* axes (INTERNAL,
  EXTERNAL); PHYSICAL is the context line and is excluded from the fold, as it always was.
- **Complements, does not duplicate, the causal-emergence review.** That review measures/repairs
  *emergence* (Ψ, a new macro); this preserves *multiplicity* (the inclusive disjunction). Different
  D&G synthesis, different mechanism, same indicted line.
- **Not the conjunctive synthesis.** The "and…and" that produces a new intensive subject from the
  disjunction (D&G's third synthesis) is the natural, unwired next step — and it is essentially the
  joint-pattern synergy rule already on hold.
