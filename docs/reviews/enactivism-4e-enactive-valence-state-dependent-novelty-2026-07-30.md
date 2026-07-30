# Enactive valence: significance is a RELATION to viability, not a property of the signal

**Live review, 2026-07-30** — area: enactivism & 4E cognition. Angle: an OPERATIONAL mechanism (not
philosophy) we could implement. Landing: `scripts/mesh-novelty` (`--valence`, new state-dependent axis).

## The mechanism

**Enactive VALENCE / state-dependent significance** — the operational core of enactive sense-making:
an autonomous system does not *process information*, it *makes sense* — and an encounter's significance
is its **relation to the agent's current viability**, not a property of the signal. The operational
consequence, stated directly across the literature: **"the same environmental situation gets a
different valence depending on the agent's internal state."**

- De Jaegher & Di Paolo, *Participatory Sense-Making*, Phenomenology and the Cognitive Sciences 6:485
  (2007), doi:10.1007/s11097-007-9076-9.
- Ezequiel Di Paolo, *Autopoiesis, Adaptivity, Teleology, Agency*, PCS 4:429 (2005),
  doi:10.1007/s11097-005-9002-y — **adaptivity** is the capacity to regulate w.r.t. viability
  boundaries *before* they are breached; it is what lets encounters acquire graded valence at all.
- Giovanna Colombetti, *The Feeling Body: Affective Science Meets the Enactive Mind*, MIT Press 2014 —
  primordial affectivity: valence as the lived significance of a situation for a self-maintaining body.
- IEP, *Enactivism* (read 2026-07-30): "a sense-making system **evaluates** the environmental situation
  as nutrient-rich or nutrient-poor" — value is generated relative to current need, not read off the
  stimulus. https://iep.utm.edu/enactivism/

## Where the mesh applied it too loosely

`mesh-novelty` is the mesh's attention/wake sense, and it is *saturated* with axes — marginal
surprisal, `--conditional` (predictive coding), `--bayesian` (Itti & Baldi belief-move), `--levels`
(local-global), `--territory` (deterritorialization κ), `--diversity` (Zipf), omission / negative-PE,
and the prior-preference dark-room floor. **Every one of them scores an event from the BOARD ALONE —
an agent-independent information quantity.** The file's own thesis is printed on it: *"attention
follows information, not volume."*

That is exactly the enactive inversion, applied too loosely. Sense-making says attention follows
**viability-significance**, and significance is a *relation* the signal cannot carry by itself. The
prior-preference floor (`PREF_TAGS = incident health-fail gap`) is the closest sibling — but it is a
**fixed, state-independent** set: it attends `[health-fail]` with identical weight whether the node is
calm or collapsing. A `[gap]` carries the same Shannon bits under NOMINAL and under ALERT — yet its
viability significance is not the same: **a fault arriving while the node is already degraded compounds
toward collapse and should attend more.** No axis on the file could express that, because none reads
the mesh's own body-state.

## What landed — `scripts/mesh-novelty --valence` (uncommitted, steward lands)

The **first axis on the file that reads the mesh's own viability state**, not the board:

    significance(event) = viability-valence(tag) × state_mult(current fused posture)

- **Body-state input**: `read_posture()` reads `~/.mesh/.situation.state` — `mesh-situation`'s
  *committed* NOMINAL/WATCH/ALERT posture (a documented consumer contract, honest-fused from
  internal/external/physical axes). Cheap: it reads a cached verdict, never re-probes (the file must
  stay light — it gates mind wake).
- **State multiplier**: `NOMINAL:1.0, WATCH:1.5, ALERT:2.0` (env-overridable). An aversive event under
  already-degraded viability is `AMPLIFIED`; under a neutral posture it is `BASELINE`.
- **The dissociation it surfaces** (distinct from every information sibling): Shannon/Bayesian score a
  `[gap]` identically regardless of the mesh's condition; valence says the same `[gap]` is 2× as
  significant when the node is already ALERT — *identical bits, higher enactive significance.* This is
  the enactive turn from **information** (board-only) to **significance** (board × viability).
- **Honest-fusion**: a missing OR stale (`>VALENCE_TTL`, default 1800s) posture → `UNKNOWN` →
  state-neutral (×1.0), `STATE-UNKNOWN` class — never a faked all-clear nor a false alarm (the
  [[na-must-be-a-claim-about-the-node]] discipline).
- **Report-only / advisory** — like `--levels`/`--territory`/`--bayesian`, it does NOT touch
  `mean_bits`/`scored` nor the `--threshold` wake gate. It names *which* wakes viability would
  re-weight; the SPEND wiring stays the steward's (same discipline as the file's other HELD/advisory
  axes). New `--valence` mode + `--json`; default report untouched (consumers grep it — [[cross-sense-vocab-contract]]).
- **RED-first gate** (test leg 9): the SAME `[gap]` must score higher significance under ALERT than
  NOMINAL; an `UNKNOWN` posture must be state-neutral; a non-viability tag (`[done]`) must NOT be
  valenced. Proven RED by `MESH_NOVELTY_STATE_MULT="NOMINAL:1,WATCH:1,ALERT:1"` (multipliers collapse →
  state-dependence vanishes → `sig_alert > sig_nom` fails), then restored → GREEN.

## Why this is NOT already embodied

`mesh-stress`/`mesh-situation` *compute* the viability posture but do not use it to appraise EVENTS;
`mesh-novelty`'s eight axes appraise events but are all board-only/state-blind, including the
prior-preference floor (fixed set, no state). The operational join — *event significance = f(event,
current viability state)*, the same event carrying different valence in different internal states — had
no home in the genome. It is the enactive "value/valence generation" mechanism (IEP §3), and it is the
first time this attention sense reads the mesh's own body.

## Considered and not picked

- **CRQA structural coordination** (%DET/laminarity; Coco & Dale 2014, arXiv:1310.0201) — the standing
  runner-up, but it overlaps the queued block-bootstrap coupling-null work on `mesh-cooscillate`; left
  for that lane.
- **Extended-mind "trust and glue" reliability criteria** (Clark & Chalmers 1998) — the
  *reliably-available* half is already embodied by `mesh-pane-watch` (frozen-pane hash watchdog),
  `mesh-freshness` (render-lease), and `mesh-pane-reload`; not a fresh landing.

## Sources

- De Jaegher & Di Paolo, *Participatory Sense-Making*, PCS 2007 — doi:10.1007/s11097-007-9076-9
- Di Paolo, *Autopoiesis, Adaptivity, Teleology, Agency*, PCS 2005 — doi:10.1007/s11097-005-9002-y
- Colombetti, *The Feeling Body*, MIT Press 2014
- IEP, *Enactivism* — https://iep.utm.edu/enactivism/
