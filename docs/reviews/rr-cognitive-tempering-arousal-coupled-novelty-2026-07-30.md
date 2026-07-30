# RR live review — cognitive tempering (focusing↔diversifying), arousal-coupled

**Date:** 2026-07-30 · **Lane:** relevance realization & the frame problem (Vervaeke) · **Angle:** a recent
result naming an opponent pair we do not yet embody.

## What was already taken

The frame-problem / RR area is dense in the genome — I checked the coverage map before landing:

- **precision-weighting** + **large-world frame limit** — `mesh-precision` (already cites Andersen/Vervaeke
  2022 & 2025, Jaeger et al. 2024 "not computational", Darling/Corcoran/Hohwy 2025 active inference, and
  Parvizi-Wayne 2025 rebuttal — this sub-area is near-exhausted).
- **explore↔exploit** (cognitive *prioritization*), demand-tracking edge — `mesh-needs --balance`.
- **efficiency↔resiliency** (the general opposition) — `mesh-sensorium --balance`.
- **insight / reframe-at-impasse** — `mesh-sensorium --impasse`.
- **diametric autism↔psychosis precision pole** — `mesh-correlate --posture`.
- **EFE novelty vs salience** (the action half) — `mesh-novelty`, `mesh-interruptibility --probe`.

## The concept landed (not previously embodied)

**Cognitive TEMPERING: focusing ↔ diversifying** — Vervaeke's *third* RR opponent pair, distinct from
the two the mesh already reads. It is how **concentrated vs spread** the agent's finite resources/attention
are over its options.

- **Taxonomy source:** Vervaeke, Lillicrap & Richards, *"Relevance Realization and the Emerging Framework in
  Cognitive Science"*, J. Logic & Computation 22(1):79–99, 2012
  (http://sites.utoronto.ca/jvcourses/jolc.pdf) — names the three nested opponent processes: cognitive
  *prioritization* (explore↔exploit), cognitive *scope* (general↔specific), cognitive *tempering*
  (focusing↔diversifying).
- **The RECENT result that makes it operational (2025):** Andersen, Miller & Vervaeke, *"Predictive
  processing and relevance realization: exploring convergent solutions to the frame problem"*, Phenomenology
  and the Cognitive Sciences **24**:359–380 (2025, doi:10.1007/s11097-022-09850-6). It shows the whole
  tradeoff *family* is the tradeoff inherent to **precision-weighting (gain)**: raising precision/gain
  **narrows** attention (focus); lowering it **broadens** attention (diversify). So tempering **IS** the gain
  knob — and, like every RR opponent, its set-point is **not a fixed midpoint** but an **arousal-tracking
  edge** (Vervaeke: *the edge moves*). The search also surfaced the companion 2025 papers on the same lane
  (Darling/Corcoran/Hohwy; Parvizi-Wayne) — all already caveated in `mesh-precision`, confirming the
  precision/active-inference sub-area is taken and tempering is the open neighbour.

**Why it is genuinely new here:** the mesh has *diversifying* pressures (`mesh-forage` pheromone-entropy on
the literature lane; the sound grind's repel-from-recent) and *focusing* pressures (dispatch priority;
precision down-weighting) — but **nothing reads the focus↔diversify balance of the mesh's own activity, and
nothing couples that balance to arousal.** The arousal coupling is the load-bearing part: a fixed
focus/diversify set-point that ignores the body-state is exactly the misread RR warns against.

## Concrete application (shipped, report-only)

**File:** `scripts/mesh-novelty` — new `--tempering` mode (report-only, `--json`, RED-first `--test`).

It is the one tool that already carried **both** halves of the mechanism:

- **diversify axis** = `diversity()`'s Pielou evenness *J* of the activity-type distribution (reuses its
  already-calibrated bands 0.35 / 0.75 — no second magic constant to rot);
- **arousal axis** = `read_posture()`'s honest-fused `.situation.state` (NOMINAL/WATCH/ALERT), the same
  read `--valence` uses.

`_tempering_verdict(j, posture)` emits the **same edge-not-midpoint shape** as `mesh-needs`'
`_demand_verdict`:

| evenness | arousal | verdict | reading |
|---|---|---|---|
| FOCUSED (J<0.35) | ALERT/WATCH | **NARROWED-TO-THREAT** | RR-correct — gain up, attention narrows to the threat |
| FOCUSED | NOMINAL | **FIXATION** | **fault** — narrowed with no arousal to justify it (tempering's dark-room) |
| DIFFUSE (J>0.75) | ALERT/WATCH | **SCATTERED** | suboptimal — RR says gain should rise and narrow, not hedge broad |
| DIFFUSE | NOMINAL | **EXPLORING** | RR-correct — nothing presses; broad hedging is the right edge |
| mid | any | **TEMPERED** | balance held |
| any | UNKNOWN | **POSTURE-UNKNOWN** | pole named, edge not judged (honest — never fake an all-clear) |

`FIXATION` is the tempering analogue of the explore-edge **DARK-ROOM** in `mesh-needs`: activity collapsed
onto few types with no viability pressure calling for the narrowing.

**Verification:** RED-first `--test` asserts every cell of the arousal×evenness matrix **plus a falsifier**
(the same low evenness under ALERT must NOT read as FIXATION — a verdict blind to posture is vacuous).
Broke the FIXATION cell → `--test` went RED (`arousal-blind (focus verdict ignores posture)`); restored →
GREEN. Live: `J=0.68, posture WATCH → TEMPERED` (balance held, 96 activity types).

Report-only: zero effect on the wake gate or any verdict/weighting logic — purely a new self-measurement,
consistent with every prior RR landing on this lane.

## Sources

- Vervaeke, Lillicrap & Richards 2012, J. Logic & Computation 22(1):79–99 — http://sites.utoronto.ca/jvcourses/jolc.pdf
- Andersen, Miller & Vervaeke 2025, Phenom. & Cog. Sci. 24:359–380 — https://link.springer.com/article/10.1007/s11097-022-09850-6
- (context) Darling, Corcoran & Hohwy 2025, Philosophical Psychology — https://philpapers.org/rec/DARSTR
- (context) Parvizi-Wayne 2025, Philosophy and the Mind Sciences 6 — https://philosophymindscience.org/index.php/phimisci/article/view/12118
- (context) Jaeger, Riedl, Djedovic, Vervaeke & Walsh 2024, Frontiers in Psychology 15:1362658 — https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2024.1362658/full
