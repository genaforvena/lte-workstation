# Relevance realization → the frame problem, transferred to a distributed sensor mesh (2026-07-28)

**Angle:** cross-domain transfer of Vervaeke's *relevance realization* (RR) to a distributed sensor
mesh. **Landed:** `mesh-sensorium --balance` — a read-only **efficiency ↔ resiliency** opponent-
processing report over the sensorium (uncommitted; steward lands).

## The concept (named + cited)

RR is Vervaeke's account of how a cognitive agent solves the **frame problem** — zeroing in on the
relevant and intelligently ignoring the (vastly larger) irrelevant — *without* a fixed relevance
function. The mechanism is **opponent processing**: antagonist drives held in dynamic tension and
self-organized to the agent's own economy, not a static rule. The **general opposition that subsumes
all the others** (exploration↔exploitation, generality↔specialization, focusing↔diversifying,
compression↔particularization) is **EFFICIENCY ↔ RESILIENCY**:

> "resiliency entails increased variation while efficiency involves selection, or a culling of
> unnecessary cognitive structures … the need to be efficient while remaining resilient results in
> increasing complexification."

- Vervaeke, Lillicrap & Richards, **"Relevance realization and the emerging framework in cognitive
  science"**, *Journal of Logic and Computation* 22(1):79–99 (2012) —
  <http://sites.utoronto.ca/jvcourses/jolc.pdf> (origin of the opponent-processing pairs).
- Re-affirmed as **self-organizing / bioeconomic and non-computational** in Riedl, Djedovic, Vervaeke
  & Walsh, **"Naturalizing relevance realization: why agency and cognition are fundamentally not
  computational"**, *Frontiers in Psychology* 15:1362658 (**2024**, PMC11231436) —
  <https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2024.1362658/full>.
- Companion recent result: Andersen, Miller & Vervaeke, "Predictive processing and relevance
  realization", *Phenomenology and the Cognitive Sciences* 24:359–380 (**2025**).

## Why this is somewhere we have NOT been

The mesh has landed RR's neighbours well: **precision-weighting** (`scripts/mesh-precision`), the
**large-world frame limit** (mesh-precision's `frame_coverage` — a signal outside the sense catalog is
*unmeasurable*, not low-precision), **goal-relativity of relevance** (`mesh-novelty`), and — crucially —
the **specific** explore↔exploit opponent balance as a read-only report in `scripts/mesh-needs`. What
was **not** embodied is the **general** opponent opposition, efficiency↔resiliency, read over the
**sensorium itself**. Vervaeke's own framing makes explore↔exploit a *special case* of efficiency↔
resiliency; the mesh had the special case but not the general one, and had it over *work* (needs), never
over *perception*.

## The cross-domain transfer

A distributed sensor mesh faces exactly the RR trade-off. A sensorium where each percept-category rests
on **one** cached stream is maximally **efficient** (nothing redundant to keep warm) but **brittle** —
that one stream dying blinds the whole category: a single point of sensory failure. A category backed
by **several independent live streams** is **resilient** (redundant variation) but costs more. RR says
an agent must not pick a fixed point on this axis: it must *watch the balance and re-organize*. The mesh
had no measurement of it — `mesh-precision` weights *among* reachable senses but never asks how many
independent streams a percept rests on; honest-fusion renders a dead stream as UNKNOWN but never counts
the sensorium's overall efficiency↔resiliency posture.

This is the perception-side twin of the doctrine already in the tree: the `writer-redundancy-blinds-
mtime-liveness` lesson is the *efficiency* argument (redundancy has a cost — it can mask a dead writer);
`--balance` supplies the *resiliency* side of the same opponent pair and makes the tension visible.

## The concrete application (named file)

`scripts/mesh-sensorium --balance` — read-only, reuses `--cached` (the one source of truth for what is
live) so it can never diverge from the roll-call. Per percept-category (BODY, ROOM, PRESENCE, HOUSEHOLD,
SITUATION, COORDINATION, NODE) it counts **depth = LIVE cached streams** (fresh/recent/aging) vs dead
(STALE / absent / OFFLINE), and reports:

- per-category depth (`depth k/n live`), flagging **single-source** (depth 1 = single point of sensory
  failure) and **blind** (depth 0);
- a summary (resilient depth≥2 · single-source · blind, of N categories);
- a **posture** with an exit code a consumer can gate on: `balanced` (0), `BRITTLE` / efficiency-pinned
  when ≥½ the categories rest on a single stream (3), `BLIND-SPOTS` when any category has no live stream
  (4). Mirrors `mesh-needs`' explore↔exploit pole-collapse report: it changes **nothing** — it makes
  the balance visible so a deliberate re-organization (add a redundant organ to a brittle category) is
  data-driven.

**Honest granularity caveat** (in the `frame_coverage` spirit): depth is measured at *cached-stream*
granularity. A category rendered as one fused field (PRESENCE fuses many organs into `presence.log`)
reads single-source even so — because at the sensorium level that one stream dying blinds the category
regardless of how many organs feed it upstream. That is a real brittleness, not an artifact of the
measure.

### Gate (seen RED then GREEN)

`mesh-sensorium --test` drives the real `--balance` black-box against three crafted-state fixtures under
a throwaway HOME, pinning all three verdict branches so no hardcoded verdict passes: **BLIND** (empty
roll-call → exit 4), **BRITTLE** (one live stream per category → exit 3), **balanced** (multi-stream
categories filled → exit 0). Falsified by disabling the `brittle*2 >= cats` branch → the BRITTLE fixture
goes RED (verified: `got rc=0: balanced`). Live run on mesh-home: `4 resilient · 3 single-source · 0
blind → balanced`.

## Tuning / next step (unwired, deliberate)

On-demand diagnostic (like `mesh-forage` / `mesh-needs`' balance report) — not cron-wired. Natural next
step: surface the posture line in `mesh-dash sense` so the node watches its own perceptual resiliency
live, and let a persistent `BRITTLE`/`BLIND-SPOTS` posture file a `[task]` to add a redundant organ to
the brittle category.
