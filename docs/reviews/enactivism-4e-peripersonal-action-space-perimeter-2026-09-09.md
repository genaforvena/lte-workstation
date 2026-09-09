# Enactivism / 4E — peripersonal action-space, not geographic proximity

**Date:** 2026-09-09 · **Lane:** genome, live literature review · **Angle:** cross-domain transfer to a distributed sensor mesh · **Status:** proposal only; no mesh tool edited

## The live finding

The concept is **peripersonal space (PPS) as a plastic sensorimotor interface**: the relevant
“near” is not simply a metric radius around a body. It is the multimodal region in which stimuli
are action-relevant to that body, and it changes when the body’s available action repertoire
changes.

I read three current sources:

- Mustile, Borghi, De Tommaso & Wykowska, **“Peripersonal Space Perception Is Similar When We
  Interact With Other Humans or With Humanoid Robots,”** *QJEP* (online 2026-01-03; issue July
  2026), [PubMed 41482888](https://pubmed.ncbi.nlm.nih.gov/41482888/). Across four experiments,
  reachability judgments changed in a social context; participants narrowed their own PPS and
  represented the human/robot partner’s action space differently.
- D'Angelo et al., **“Dealing with the world close to our body. Characterizing determinants of
  peripersonal space plasticity,”** *Neuropsychologia* 229 (2026),
  [doi:10.1016/j.neuropsychologia.2026.109490](https://doi.org/10.1016/j.neuropsychologia.2026.109490).
  The current result is operationally useful: PPS plasticity is multimodal, **effector-dependent**,
  both egocentric and allocentric, and expands around the effector used in training (hand rather
  than foot in their experiment).
- McCarthy et al., **“Adult age differences in the modulation of peripersonal space after tool use
  in virtual reality,”** *Scientific Reports* (2026),
  [doi:10.1038/s41598-026-41116-y](https://doi.org/10.1038/s41598-026-41116-y). The paper
  describes PPS as graded with distance, selective for action relevance, and malleable after tool
  use; its experiment measured the change with a visuo-tactile facilitation curve before/after the
  tool routine.

The broader 2026 framing also matters: Ward, **“What Is Enactivism?”** (*Adaptive Behavior*,
2026, [doi:10.1177/10597123261450094](https://doi.org/10.1177/10597123261450094)) warns that
“enactivism” is too easily flattened into generic embodiment. The PPS result is a good guard
against that flattening: it is not merely “the body matters,” but a measurable remapping of what
the body can act on. Rafiee & Sutton, **“Toward Enactive Artificial Intelligence,”** arXiv:2605.24238
([abstract](https://arxiv.org/abs/2605.24238)), likewise identifies action–perception
inseparability and embodiment as AI design gaps, while explicitly leaving them not yet
operationalized. The PPS work supplies a concrete operational shape.

## Novelty check against this genome

This is **not already embodied** as an action-conditioned PPS:

- `scripts/mesh-perimeter` fuses outside/network/physical observations into CALM/NOTICE/ALERT.
  It has a perimeter, but its “near” is LAN/radio/camera proximity and its verdict is read-only;
  it does not ask whether this body can reach, affect, or recover the nearby entity with a live
  actuator path.
- `scripts/mesh-sensorium --self-prior` learns a multimodal **body schema** over the node’s own
  state. That is a self-state familiarity test, not a spatial/action field around the body.
- `scripts/mesh-path-watch` classifies each peer as direct/relay/offline and samples latency.
  That is link quality, not the plastic combination of link quality, available effector, and
  task/action outcome that defines an operational PPS.

The corpus does contain an earlier note naming PPS as a gap, but it was explicitly left as a lead:
the present review turns that lead into one testable mesh application using the new 2026 plasticity
results. A search of `scripts/` found no `peripersonal` implementation or action-space field.

## One concrete transfer

**Target file:** `scripts/mesh-perimeter`.

Add a read-only `--action-space` mode and a cached `pps=` field to the perimeter state. For each
nearby peer/device, estimate an **operational PPS score** from three live terms:

1. `proximity`: the existing BLE/LAN/camera evidence;
2. `coupling`: the current path mode and latency from `mesh-path-watch` (direct/relay/offline,
   with freshness); and
3. `effector`: whether a named actuator/reflex can actually affect or query that peer now, with a
   measured recent success rate and recovery latency.

The score should be a graded distance/action curve, not a binary “inside perimeter” bit. A peer
whose radio signal is strong but whose only path is stale DERP and whose actuator has no successful
recent action is **outside the current operational PPS**; a farther peer with a fresh direct path
and a working action route can be inside it. Recompute the field when the available effector or
path changes: this is the mesh analogue of tool-use expansion/contraction of PPS.

The first consumer should remain the existing **physical perimeter reflex**, which can annotate a
NOTICE as `near-but-unreachable` rather than escalating every geographically near device. The
artifact must publish the three component terms, freshness, and the action probe outcome, so an
unreachable organ is `unknown`, never a low PPS score masquerading as safety. No new actuator is
required for the first landing; the mode can use existing read/query reflexes and report only.

## Why this is a genuinely different 4E landing

The mesh already has coupling, valence, body schema, direct-vs-relay path quality, and a static
perimeter. PPS adds the missing **action-conditioned boundary**: the boundary is constituted by
what the distributed body can currently do, and is plastic when its sensorimotor repertoire or
social/tool context changes. That is a cross-domain transfer, not a relabeling of “near” or an
additional health threshold.

## Verification obligation if implemented

The implementation must include fixtures that force the boundary to move: (a) strong proximity +
direct path + successful action → inside; (b) identical proximity + stale/relay path → outside or
unknown; (c) a simulated newly available effector expands the field; and (d) missing action
evidence remains `unknown`, never `CALM`. The live `mesh-perimeter --test` must drive the real
emitter and its cached state shape.

