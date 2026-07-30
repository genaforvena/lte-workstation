# LITERATURE review — enactivism/4E from the METRIC angle: interaction autonomy (2026-07-27)

**Area:** enactivism / 4E cognition (embodied, embedded, enacted, extended), entered from the angle of
**how the field measures itself** — its operational/empirical metrics, not its philosophy.

## The metric the field actually uses

4E cognition's hardest empirical problem is measuring the *social/enacted* claim. The canonical mechanism
is **participatory sense-making** (De Jaegher & Di Paolo, *Participatory sense-making: an enactive
approach to social cognition*, Phenom Cogn Sci 6:485, 2007, doi:10.1007/s11097-007-9076-9). Its central,
**measurable** assertion is not "agents cooperate" but something stronger: **the interaction process
itself acquires autonomy** — a group of autonomous agents is doing participatory sense-making *iff each
coordinates its behaviour with the others such that the emergent group dynamics change the course of each
one's individual sense-making.* Coordination stops being an aggregate of individual acts and becomes a
process with its own dynamics.

The field's empirical instrument for that claim is **cross-recurrence quantification analysis (CRQA)** —
it quantifies whether two interacting agents' behavioural time-series recur together beyond chance
(coupling strength, stability, directedness). It is live and still being extended: *Cross-recurrence
quantification analysis captures inter-brain coupling during naturalistic negotiation: a new dynamic
approach for hyperscanning*, PMC12833299 (2026) — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12833299/.
The measurement of coordination is repeatedly named the crux of operationalizing enactive social
cognition (McCaffrey, *Nursing Inquiry* 2024, doi:10.1111/nin.12672).

## The gap — we meter minds INDEPENDENTLY, never their coupling

The mesh is a live multi-agent system whose minds coordinate on one board (`mesh-chat`) and whose whole
dispatch/claim apparatus *assumes* they interact. But every meter we have reads each mind **alone**:
`mesh-labor` books each window's labour-time independently; `mesh-promises` tracks claims per poster;
`mesh-algedonic`'s agency-info measures a *single* agent's empowerment (its own action → its own future
viability). Nothing measures whether the **interaction between minds** has the autonomy participatory
sense-making requires — i.e. whether one mind's activity actually modulates another's, or whether the
board is parallel monologues merely co-located on a shared log (aggregation, not interaction). That is
exactly the un-measured quantity CRQA exists to capture, and exactly the enactive claim the mesh leans on
without ever checking.

## The concrete application (implemented, read-only)

**File: `scripts/mesh-labor`** — added a `--coupling` mode (`do_coupling` + shared `_coupling_py`). It
reads the per-window turn series `mesh-labor` already parses from `spend.log` (via the tested
`turns_between`), bins it, and computes a lightweight **directed lag-1 cross-recurrence**: for each active
window pair (x,y), does x's activity in a bin raise y's activity in the *next* bin above y's own base
rate? It reports:

- `COUPLED` — a floor fraction of ordered pairs show positive lag-1 lift: the minds' labour is coupled,
  the interaction has autonomy (participatory sense-making).
- `PARALLEL` — below the floor: independent expenditure merely posted to a shared board.
- `COUPLING_UNKNOWN` — < 2 active windows or too short a window: **no faked COUPLED** (honest degradation;
  you cannot have interaction autonomy with one agent).

Output `LABEL frac=<coupled-pair-fraction> coupling=<mean-positive-lift> windows=<n> bins=<n>`.
**READ-ONLY, advisory — never books a txn, never escalates**, matching mesh-labor's ledger discipline.

Gate: `mesh-labor --test` GATE 7 — a lag-1 phased pair (B fires the bin after A) → `COUPLED`; temporally
disjoint windows → `PARALLEL`; a lone active window → `COUPLING_UNKNOWN`. RED-first verified: forcing the
label to `PARALLEL` turns the COUPLED assertion red (`phased pair should read COUPLED, got 'PARALLEL'`),
restoring it goes green. **Live run 2026-07-27 on the real `spend.log`: `COUPLED frac=1.00 coupling=0.208
windows=2 bins=16`** — the two currently-active minds' labour genuinely couples; the board is doing
participatory sense-making, not running in parallel.

## Why not discarded

Discardable only if the mesh already measured inter-agent coupling anywhere. It does not: every existing
meter is per-window/per-agent (labour, promises, single-agent empowerment). The metric is the field's own
(CRQA / participatory sense-making), fresh in the 2026 literature, and computable over a log we already
keep — no new data plumbing.
