# Live-literature review — Deleuze & Guattari: the DETERRITORIALIZATION COEFFICIENT, and the RECAPTURE that separates a RELATIVE surge from an ABSOLUTE line of flight

Date: 2026-07-28 · lane: genome (idea-queue LITERATURE task — D&G, assemblage/rhizome/machinic, from
the angle of a concrete METRIC the field uses to measure itself) · status: fix in tree, uncommitted (steward lands)

## Where we had already been (so this doesn't double-count)

D&G is a well-worked mesh seam. Confirmed the embodied set before landing (from the four prior D&G reviews):

- **rhizome / plane of consistency** → `scripts/mesh-sensor-tape`
- **desire as productive force / rhizomatic coupling** (Anti-Oedipus) → `scripts/mesh-needs`
- **assemblage — degree of territorialization (DeLanda)** + **capacity-to-affect (Atkinson, TCS 2024)** → `scripts/mesh-digest`
- **cognitive assemblages (Hayles)** → `scripts/mesh-pane-consume`
- **the refrain / ritornello** → `scripts/mesh-reflex-health`
- **societies of control / modulation-harms** → `scripts/mesh-operator-mood`
- **assemblage & non-human agency** → `scripts/mesh-window-state`
- **order-word works by redundancy** (plateau 4) → the board (`deleuze-order-word-redundancy-board-2026-07-27.md`)
- **smooth vs striated / intensive residual** (plateau 14) → velocity+distance fusion (`deleuze-smooth-striated-intensive-residual-2026-07-27.md`)
- **disjunctive synthesis / inclusive-vs-exclusive disjunction** → `scripts/mesh-situation` (`deleuze-disjunctive-synthesis-inclusive-disjunction-situation-2026-07-28.md`)

Rhizome, assemblage, territorialization, refrain, desire-production, control-modulation, order-word,
smooth/striated, the three syntheses — all landed. **Territorialization is landed as a STATIC degree**
(DeLanda's coefficient in `mesh-digest`); what is **not** embodied is the field's own measure of a
*movement*: the **coefficient of deterritorialization**, and its **relative-vs-absolute** cut.

## The concept not yet embodied — RECAPTURE distinguishes relative from absolute deterritorialization

D&G's key operational claim about escape: **every deterritorialization (an element escaping its coded
territory) is coupled with a RETERRITORIALIZING edge**, and the *same* magnitude of escape has two
uses, told apart not by how big it is but by whether it is **recaptured**:

- **RELATIVE (negative) deterritorialization** — the assemblage "only changes in relation to a given
  form of stability that it **maintains over time**": the escape is **recaptured**, it snaps back. ATP:
  relative D. is "**stratic or interstratic**".
- **ABSOLUTE (positive) deterritorialization — a LINE OF FLIGHT** — "one **leaves all assemblages
  behind**... entering another plane": the prior organisation is destroyed and **not recaptured**. ATP:
  absolute D. "concern[s] the **plane of consistency and its destratification**."

Stated as engineering: **a surge is a line of flight ONLY if it is not pulled back. Magnitude alone
(a big surprise) does not tell you which — PERSISTENCE past the reterritorializing edge does.** The
measurable form has a name in Guattari: the **"coefficient of transversality"**, a group's tunable
degree of openness-to-escape.

**Citations** (found via web review + primary-source extraction, 2026-07):

- **Deleuze & Guattari, *A Thousand Plateaus*** — ATP p.359 (leaving all assemblages behind / entering
  another plane) and ATP p.62 (relative = stratic/interstratic; absolute = plane of consistency +
  destratification; "absolute deterritorialization becomes relative only after stratification occurs").
  (upenn hosted scan: `web.english.upenn.edu/~cavitch/pdf-library/Deleuze_and_Guattari_A_Thousand_Plateaus.pdf`.)
- **Edward Thornton, "On Lines of Flight: A Study of Deleuze and Guattari's Concept"**, Royal Holloway
  PhD thesis 2018, pp.196-197 — the cleanest secondary statement of the relative/absolute = recapture
  distinction, and (pp.~127) Guattari's **coefficient of transversality** as a tunable, measurable
  quantity. (`pure.royalholloway.ac.uk/ws/portalfiles/portal/30911200/2018thorntonephd.pdf`.)
- **"Drawing Out Deleuze and Guattari's Assemblage: New Insights for Geography"**, *Deleuze and
  Guattari Studies* 18(3), 2024 (`euppublishing.com/doi/10.3366/dlgs.2024.0568`) and **"Territorialisation,
  Deterritorialisation and Power in Democratic Assemblages"**, *Theoria* 72(183), 2025
  (`berghahnjournals.com/view/journals/theoria/72/183/th7218302.xml`) — confirm this is LIVE,
  continuously-published literature applying the de/reterritorialization pair as an analytic measure.

## Why it applies to us — the gap in `scripts/mesh-novelty`

`mesh-novelty` scores the board's event stream for surprise and is used as a **spend gate** ("wake on
HIGH novelty, stay silent on routine"). Every axis it already carries scores a surge's **magnitude or
timescale at one moment**: marginal surprisal (rarity NOW), `--conditional` (contextual residual NOW),
`--levels` (short-vs-long deviance NOW). **None asks the D&G question: did the surge STAY, or did the
board's distribution RETERRITORIALIZE back to its prior shape?**

A one-shot spike that snaps back — a flapping sense, a burst that self-resolves — is a **RELATIVE**
deterritorialization: low wake value. Yet it reads MAX bits and can wake an expensive mind. The
recapture read separates it from an **ABSOLUTE** line of flight (a genuine new regime the board did not
return from). This is **distinct** from the two HELD blocks already in `analyse()`:

- **eigenform-absorption** is the SAME type's surprise *falling* as it accretes across baselines (a
  false negative; HELD because separating real regime-change from pathological accretion "needs a
  reference the loop does not author").
- **This is the COMPLEMENT that IS self-authored** — the reference is simply **time-forward recapture**,
  observable on the board with a lag, no oracle. It does not judge whether an absolute shift is *good*
  (that stays the steward's, like the siblings); it only measures relative-vs-absolute.

## What landed (report-only instrument, opt-in — does NOT touch the wake gate)

`scripts/mesh-novelty --territory` (and `--territory --json`). It splits the recent window into an
EARLY half F and a LATE half S; for each type whose early frequency **escaped** above the long baseline
`p(t)` by ≥ `MESH_NOVELTY_ESCAPE_MIN` (default 0.1), it computes the **deterritorialization coefficient**

    κ = clamp( (late_freq − base) / (early_escape) , 0, 1 )

κ→0 = the late half returned toward baseline → **recaptured → RELATIVE** (a blip);
κ→1 = the elevated rate held or rose → not recaptured → **ABSOLUTE** (a line of flight).

Report-only, same instrument-first discipline as `--levels`/`--diversity` (changing the default `fmt()`
output silently breaks the tools that grep it; the wake wiring is the steward's after validation).

**Verification (artifacts, not claims):**

- `mesh-novelty --test` — GREEN. New RED-first assertion: two types both surge in the early half
  (identical early surprise) but `[flight]` persists into the late half → **ABSOLUTE** while `[blip]`
  vanishes → **RELATIVE**; magnitude cannot tell them apart, only recapture can. Broke it live —
  `MESH_NOVELTY_ESCAPE_MIN=1.0 mesh-novelty --test` → **FAIL rc=1** (no surge clears the floor →
  territory empties) — then restored (default → `smoke-test: ok`).
- Live board read: `[fyi]` surged early (0.6 vs baseline 0.24) and was recaptured late (0.1) →
  **RELATIVE, κ=0.0** — a real recaptured blip, correctly NOT flagged as a line of flight.
- Regression: default report + `--levels` + `--diversity` unchanged.

## One-line honesty note

The recapture read needs the excursion to sit inside the window (early/late split), so a line of flight
still forming at the very tip reads as ongoing escape until a later half exists to test recapture — by
design it measures *completed* movements, and pairs with `--levels` REGIME-ONSET (which catches the
onset before absorption). It gates nothing until the steward validates against board history.
