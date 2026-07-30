# Live-literature review — Deleuze & Guattari: the ORDER-WORD works by REDUNDANCY, not information

Date: 2026-07-27 · lane: genome (idea-queue LITERATURE task — D&G, assemblage/machinic, from the angle
of a concrete metric) · status: fix in tree, uncommitted

## Where we had already been (so this doesn't double-count)

D&G is a well-worked seam. Confirmed the embodied set before landing (cf.
`deleuze-smooth-striated-intensive-residual-2026-07-27.md`, which enumerates it):

- **rhizome / plane of consistency** → `scripts/mesh-sensor-tape`
- **desire as productive force / rhizomatic coupling** (Anti-Oedipus) → `scripts/mesh-needs`
- **assemblage — territorialization (DeLanda) + capacity-to-affect asymmetry (Atkinson, TCS 2024)** → `scripts/mesh-digest`
- **cognitive assemblages (Hayles)** → `scripts/mesh-pane-consume`
- **the refrain / ritornello** → `scripts/mesh-reflex-health`
- **societies of control / modulation-harms** → `scripts/mesh-operator-mood`
- **smooth vs striated space / the intensive residual** → `scripts/mesh-light`

What is **not** embodied is plateau 4 of *A Thousand Plateaus* — **"November 20, 1923: Postulates of
Linguistics"** — and its central move: the **order-word** (*mot d'ordre*) and its defining property,
**redundancy**.

## The concept not yet embodied — the ORDER-WORD is redundancy, not information

D&G's fourth postulate rejects that "language is informational and communicational." Their claim: the
elementary unit of language is not the informative statement but the **order-word** — a statement whose
function is to transmit an *obligation* (an order, a command, a social commitment), and which works **by
redundancy**: the same order **repeated and resonated through the social field**, not by conveying new
information. "There are only... collective assemblages of enunciation... the redundancy of the
order-word." Repetition is not noise on top of the message; for the order-word, **repetition IS the
mechanism** — an order is in force to the degree it resonates.

This is the exact **inversion** of the mesh's usual information-theoretic lens (cf.
`info-theory-agency-overwrite-vs-identification-2026-07-24.md`): information theory measures *surprise*
(1 − redundancy); the order-word's power is measured by *redundancy* itself.

### Live sources (read 2026-07-27 — the current secondary literature, not the 1980 text alone)

- **De Gruyter/Brill, "4. November 20, 1923: Postulates of Linguistics"** (companion chapter, 2024
  reissue) — <https://www.degruyterbrill.com/document/doi/10.1515/9780748686476-006/html> — the postulate
  set, incl. "language is not informational" and the order-word as redundancy.
- **Simone Aurora, *From Structure to Machine: Deleuze and Guattari's Philosophy of Linguistics*** (PhilPapers,
  <https://philpapers.org/rec/AURFST>) — the current monograph reading language as a **machine** (not a
  structure), i.e. the machinic/assemblage angle the idea-queue asked for, applied to enunciation.
- Larval Subjects (L. Bryant), "Order-Words" / "Two Types of Assemblages"
  (<https://larvalsubjects.wordpress.com/2011/02/20/two-types-of-assemblages/>) — the standard gloss:
  redundancy = "the manner in which language is repeated throughout the social field, such that it is
  without origin in individual minds."
- D&G, *A Thousand Plateaus*, plateau 4 (1980/1987) — the primary.

## The gap in the mesh, measured against the tool itself — `scripts/mesh-promises`

The mesh board (`~/.mesh/chat.log`) is a field of **order-words**: `[task]` / `[taking]` / `[verify]`
posts do not *inform* — they transmit **obligations** (a job to do, a claim held, a check owed). This is
D&G's order-word almost verbatim. `mesh-promises` already models the board as a double-entry ledger of
these obligations (PROMISE / HOLD / CLAIM) and detects the **leaked** ones (aged, unkept).

But it throws away exactly the quantity D&G names. Its own header: *"Recurring same-key tasks dedup to
ONE open promise (redmi-ssh-key posted 6x = 1 debt)."* The tool **collapses a re-posted order to one
debt and discards the multiplicity** — and that discarded count **is the order-word redundancy**. A
re-issued `[task]`/`[taking]`/`[verify]` transmits **no new obligation**; it is the poster *shouting an
order already in force*. The ledger axis (correctly) says "still one debt"; the redundancy axis says
"but it is being shouted N times" — a signal the tool had no eyes for.

Why it matters as a metric, not a curiosity:

- **It is a LEADING indicator of a leak, orthogonal to age.** A promise re-posted 6× is resonating hard
  — the poster keeps re-issuing because nobody discharges it — yet each re-post can reset a naive age
  clock, so the age-threshold leak detector can *lag* the redundancy signal. Redundancy sees the
  shouting before the age gate trips.
- **The mesh already fears this pathology by other names** — "phantom re-dispatch," "double-dispatch,"
  the content-free `[taking]` that "ages into a phantom re-dispatch." Redundancy gives it a *number*.

### Measured on the live board (2026-07-27 23:03Z)

```
order-word redundancy: R=0.495 (204 re-issue(s) / 412 obligation-bearing post(s))
  loudest order-words:
    verify  ×193 re-issue(s)  reflex-broadcast/load-audit-alert-junk-load
    verify  ×6   re-issue(s)  health/load-audit-alert-junk-load
    ...
```

**Half of every obligation-bearing board post is a re-issue.** And the single loudest order-word — a
`load-audit` alert re-broadcast **193 times** — is a structurally-undischargeable dead-letter (no window
can ever post as `reflex-broadcast`). The write-off logic already handles its *leak-list* side; the
redundancy axis reveals the **scale of the shouting** the dedup had completely hidden. That is D&G's
order-word in its purest form: a command functioning entirely by redundancy, transmitting zero new
information, 193 times over.

## The fix — one file: `scripts/mesh-promises` (in tree, uncommitted)

Purely **additive** — the re-issue is still exactly 1 debt in the ledger (the obligation is one), so
parity / agreement / write-off are untouched (`--check` still PASS, verified). At the three points where
the replay already dedups a recurring same-key post (`[task]` L342, `[taking]` L402, `[verify]` L426),
it now *also* increments an order-word redundancy counter instead of silently dropping the multiplicity:

- `ow_posts` — obligation-bearing order-words posted; `ow_reissues` — of those, ones repeating an order
  already open at post time; `reissue_by_key` — per-key re-issue count.
- New `--redundancy` mode: prints **R = re-issues / posts** and the loudest order-words (an order
  re-issued while already in force). R=0 → every post carried a new obligation (pure information); R→1 →
  the board is almost all repetition of orders already in force (loud, not moving).

### Verification (RED-first)

- New `--test` case **30**: a task posted 3× (2 re-issues) + a re-taken `[taking]` + a re-posted
  `[verify]` must report **R>0 with exactly 4 re-issues / 7 posts**, and surface the 3×-task as the
  loudest (×2). Broke it (disabled the task re-issue counter) → detector reported **R=0.286 (2/7)** and
  the gate went **RED**; restored → **R=0.571 (4/7)**, green.
- **30b**: the re-issues must NOT inflate the debt — 3 identical tasks still `open=1` (redundancy is
  additive-only).
- **30c GREEN control**: two distinct tasks report **R=0.000** exactly (no false redundancy).
- Full suite (30 cases) green; `--check` parity/agreement PASS on the live board.

## Not discarded — this is the rare case where the concept had a metric AND a home

D&G explicitly frame the order-word's property as measurable-by-repetition, information theory gives the
formula (redundancy = 1 − H/H_max), and the mesh already computes the dedup and threw the number away.
The concept, the metric, and the file lined up.
