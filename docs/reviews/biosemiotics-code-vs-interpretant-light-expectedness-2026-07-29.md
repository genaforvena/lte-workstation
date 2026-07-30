# Live-literature review — biosemiotics: a code is not sufficient for meaning — the missing interpretant on `mesh-light`

Date: 2026-07-29 · lane: genome (idea-queue LITERATURE task) · status: proposal, uncommitted

## Area & angle

Biosemiotics — sign and meaning in living systems — approached, as the task asks, through a
**foundational idea we apply too loosely**. Searched the live literature (Springer *Biosemiotics*,
2025 volume) and landed on the debate that is *open in the journal right now*, not a settled classic:

- Kalevi Kull, **"Codes: Necessary but Not Sufficient for Meaning-Making"** — the majority
  biosemiotic position: a *code* (a fixed, conventional signal→sign mapping) is necessary for
  semiosis but **not sufficient**; meaning-making additionally requires an **interpretant** — the
  context that decides what the sign means *here, now*.
- Marcello Barbieri, **"Do Codes Need Interpretation?"**, *Biosemiotics* **18(1): 97–104 (2025)**
  — the dissent: codes do **not** need interpretation and were "the unique form of semiosis to
  exist in the first three billion years of the history of life."
- The 2025 reconciliation attempt: **"Biosemiotics, code biology, and operational interpretation"**
  (*Chinese Semiotic Studies* / de Gruyter, 2025), which grafts Deacon's autogenesis onto the
  divide with an **operational interpretation** — interpretation as *what the code does in its
  functional context*, not a homunculus reading it.

This is the live edge of a distinction Peirce fixed a century ago: **sign — object — interpretant**.
A code gives you sign↔object (a stable mapping). The **interpretant is the third leg**, and it is
exactly the leg the mesh keeps dropping.

Distinct from our three prior biosemiotics landings:
- functional-cycle *return leg* → actuators (`biosemiotics-functional-cycle-closure-2026-07-24.md`)
  closed a loop with a **second sense**;
- information-balance R_seq≈R_freq → wake recognizer (`...-information-balance-...-2026-07-27.md`)
  **measured** the information a recognizer carries;
- index-vs-icon → perimeter stranger (`...-index-vs-icon-...-2026-07-28.md`) fixed the **mode of
  reference** (resemblance vs existential connection) for a *presence* question.

This one is orthogonal to all three: it is about the **sufficiency of a code** — whether a
signal→verdict mapping *is* the meaning, or needs a live interpretant to become one.

## Where we apply it too loosely

The mesh is built out of **codes**: fixed signal→verdict maps — thresholds, band tables,
classifiers. Doctrine already carries a graveyard of the same failure under different names —
"an error message names a cause, not the cause" (an errno *code* read as its dictionary meaning),
"a substring scan turns prose into a verdict", "calibrate a derived axis against the REAL corpus,
never an assumed 0..1", "a constant outlives its reader", "a label that embeds the clock correlates
with the sun". Each is one instance of the **same biosemiotic error: shipping a code as if it were
sufficient (Barbieri) to a consumer that needed the interpretant (Kull).** The mesh has *rediscovered
the Kull side piecemeal* — the pooled-corpus self-calibration (`pooled-corpus-rank`,
`mesh-series-stats --claims`) is precisely "supply the live interpretant" — but it has never named
the principle, so each organ re-learns it by getting burned.

The cleanest un-treated instance is **`scripts/mesh-light`**.

`mesh-light` maps an absolute lux reading to a five-level code with **fixed absolute thresholds**
(`DARK 0–2 · DIM 3–30 · MODERATE 31–150 · LIT 151–600 · BRIGHT 600+`), plus hysteresis and D&G
intensive-residual smoothing. As a *physical* description this code is sound — lux is a physical
unit and the bands are honest. **But the level it emits is context-free**, and its consumers
(`mesh-perimeter`, `mesh-situation`, `mesh-body-context`) read the level as if it were the *meaning*.
It is not:

- **`DARK` at 03:00** means *normal night* — no sign at all.
- **`DARK` at 12:00** means *something is wrong*: the camera/phone sensor is occluded, a fault, a
  covered lens, an intruder blocking light. Same code, opposite meaning.

The code alone cannot tell these apart, and today it does not try — it ships `DARK` to a perimeter
that has no way to know the noon `DARK` is the anomaly. That is Barbieri-sufficiency applied where
the situation is Kull: **the sign needs an interpretant (the expected light for this hour) to mean
anything.** `a-label-that-embeds-the-clock-correlates-with-the-sun` warns against *baking the clock
into the label*; the fix here is the inverse and safe — keep the physical label pure, and add the
clock as a **separate interpretant channel**, never fused into the level.

## Proposal — an `expectedness` interpretant field on `mesh-light` (report-only, opt-in)

Give `mesh-light` a second, **non-verdict** JSON field that supplies the missing third leg:

```
expectedness: how far the CURRENT level deviates from THIS SENSOR'S OWN rolling
              per-hour-of-day baseline of levels — self-calibrating (the interpretant
              is the sensor's own history, not an assumed constant).
```

Mechanism (concrete, uses data already on disk):
1. `mesh-light` already has the raw/level history (`~/.mesh/light.log`, `~/.mesh/.light-events`,
   `~/.mesh/note3-light-raw.log`). Bucket past readings by **hour-of-day** (0–23) and keep the
   modal/median level per bucket — a 24-slot self-baseline, rebuilt cheaply on read (or cached).
2. On each read, compare the current level to its **own** hour-bucket baseline. Emit
   `expectedness: expected | dim-for-hour | bright-for-hour` and a signed band-distance
   (`Δlevels`), **alongside** the physical `level` — never replacing it.
3. **Verdict-neutral.** The physical `level` and every existing consumer are untouched; downstream
   organs *opt in* to the interpretant. The first real consumer is `mesh-perimeter`: `DARK` +
   `expectedness: dim-for-hour` at noon is a genuine occlusion/tamper index (a *second, independent*
   channel — exactly the "iconic redundancy is not indexical confirmation" fix from the
   index-vs-icon review, here supplying the independent index).

Why this is the right shape, not churn:
- It computes and emits a **real self-calibrating number**, not a comment block — the failure mode
  `mesh-vitality`'s own POSIWID note warns against.
- It is **self-baselining** — cannot rot into a dead constant, cannot be miscalibrated against an
  assumed 0..1 (the `pooled-corpus-rank` / live-interpretant discipline, now *named* as the
  biosemiotic principle it always was).
- It keeps the code **pure** (the Barbieri win — the physical level is a sound context-free code)
  while adding the interpretant **as a distinct leg** (the Kull win). It embodies the *operational
  interpretation* reconciliation: interpretation = what the code does *in its functional context*,
  computed, not narrated.

### Gate it must pass (RED-first)
`mesh-light --test` must assert: feed a synthetic history where hour-12 is historically `BRIGHT`;
inject a current `DARK` reading stamped at hour 12 → assert `expectedness` reports `dim-for-hour`
with a negative `Δlevels`. Break the baseline lookup (force the constant) → the assertion must go
**RED** (a gate not seen fail is not a gate). Feed `DARK` at hour 03 where history is `DARK` →
`expected`. The interpretant must read the *live* baseline, never a hardcoded expectation.

## One-line discard test (did not apply)
Making the **lux bands themselves** relative would be wrong — that destroys the sound physical code
and re-buries the clock inside the label. Rejected. The interpretant belongs in a *separate channel*.

## Citations
- Marcello Barbieri, "Do Codes Need Interpretation?", *Biosemiotics* 18(1): 97–104 (2025) —
  https://link.springer.com/article/10.1007/s12304-025-09597-y
- Kalevi Kull, "Codes: Necessary but Not Sufficient for Meaning-Making" (the position Barbieri
  answers; summarized in the same 2025 exchange).
- "Biosemiotics, code biology, and operational interpretation", *Chinese Semiotic Studies*
  (de Gruyter, 2025) — https://www.degruyterbrill.com/document/doi/10.1515/css-2025-2003/html
- Peirce, sign–object–**interpretant** triad (the third leg the code omits).

Target file: **`scripts/mesh-light`** (genome source). Uncommitted proposal — steward lands.
