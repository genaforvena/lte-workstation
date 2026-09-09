# SOC & power-law dynamics (live review): local attraction/repulsion as a sensor reflex

**Date:** 2026-09-09  
**Area:** self-organizing criticality and power-law dynamics, cross-domain transfer to a
distributed sensor mesh.  
**Novel target:** `scripts/mesh-light` (ambient-light sense).

## Finding

The new mechanism is **field-coupled local attraction plus repulsion**: each agent uses a
nearby signal to move toward a shared event, while a second local feedback field prevents the
cluster from collapsing into one runaway group.  In the paper, robots attract one another through
phototaxis/visible-light signalling and repel through water-wave disturbances.  The combination
creates correlated clusters, SOC-like avalanches, and a steady state without a global controller;
under an external stimulus, the same swarm forms directed structures and performs collective
pushing.

This is different from the mesh's existing `mesh-criticality` work.  That organ estimates a
branching ratio and has many read-only tests for whether a heavy tail is genuinely critical.  It
does not make a sensor node's sampling or forwarding policy a local attraction/repulsion field,
and it does not make a useful directed structure emerge from corroborating sensor reports.

## Live sources read

- Shiji Zhao, Jiajun Huang, Chaoqun Li & Shengli Mi, **“Self-organized criticality in aquatic
  robot swarm,”** *Science Advances* 12(20), eaec6153 (2026), DOI
  [10.1126/sciadv.aec6153](https://doi.org/10.1126/sciadv.aec6153).  I read the article's design,
  results, discussion, and methods.  The primary article reports optical attraction, hydrodynamic
  repulsion, power-law cluster size/duration distributions, finite-size scaling, and stimulus-led
  directed structures/collective pushing.  The full text is also available through the
  [Science Advances article page](https://www.science.org/doi/10.1126/sciadv.aec6153).
- As a current engineering cross-check, Biziarkin, Litvinov & Korkhov, **“Consensus-based local
  data aggregation in wireless sensor networks under node failures and transmission-power-based
  topology control,”** *Scientific Reports* (2026), DOI
  [10.1038/s41598-026-59707-0](https://doi.org/10.1038/s41598-026-59707-0), keeps the application
  constraint honest: one-hop local information and adaptive communication conditions materially
  change aggregation behavior under failures.  It supports using a local, topology-aware rule,
  but it is not the source of the SOC mechanism.

## One concrete application: `scripts/mesh-light`

Add a **report-only first version** of a light-field reflex, then allow it to drive cadence only
after its tape has been independently verified:

1. Treat a fresh local/beacon `mesh-light` transition as an attractive stimulus.  Neighbor nodes
   that observe the same DARK→LIT (or LIT→DARK) transition within a bounded interval increase
   their light-sense cadence and forward one compact transition marker.  This makes a spatially
   coherent light event form a directed reporting chain instead of polling every node equally.
2. Treat duplicate reports from the same source, contradictory levels, and an already saturated
   reporting neighborhood as repulsion.  Those nodes lengthen their next poll interval and suppress
   duplicate forwarding, with a hard maximum silence bound so repulsion cannot erase coverage.
3. Slowly recharge the local drive after each report and dissipate it after the episode.  The
   resulting local rule is: corroboration pulls a node into the event; congestion/disagreement
   pushes it out; no coordinator sets a global rate.  Log the local attraction, repulsion, chosen
   cadence, and resulting light-event cluster size so `mesh-criticality` can test whether the
   new control loop actually produces scale-free event sizes rather than merely asserting SOC.

The real organ is the **ambient-light sense** in `scripts/mesh-light`; the real reflex is its
poll/forward cadence.  This is an application proposal, not a claim that the current light tape
already has the paper's power laws.  The first implementation gate should be a counterexample:
one isolated light change must increase only its own cadence, while a same-window multi-node change
must form a bounded directed chain and never exceed the repulsion/silence guard.

## Disposition

**Land as a new literature/application concept.**  It applies because the mesh already has a real
light organ, cross-node reachability, and criticality measurement; what is absent is the paper's
local positive/negative feedback that turns sensing into an adaptive collective reflex.
