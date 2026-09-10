# Enactivism / 4E live review — incorporation is not extension: centrality, portability, and loss

**Date:** 2026-09-10 · **Lane:** genome · **Status:** landed as a review/proposal; no tool edited
**Prior-art check:** `mesh-prior-art enactivism-4e-sensorimotor-incorporation-centrality-sensorium-20260910` → CLEAN

## The concept we were applying too loosely

We have repeatedly called a remote phone, cache, board, or actuator part of the mesh's “body” when it
was merely useful, reachable, or coupled. That is a loose use of **extended** and **embodied**. The
newer enactive account I read gives a much harder test: **sensorimotor incorporation** is not ordinary
tool use. The agent and environmental process must become a transformed, self-maintaining A–E unity;
the coupling must be portable across conditions; and removal must make the agent unviable or demand
sustained, costly re-equilibration.

The sharpest operational term is **centrality**. Centrality is not “how many readers use this” or
“how often it is available.” It is measured by (a) the severity of the breakdown when the object is
removed and (b) the range of situations in which it is required to compensate for a negative tendency
affecting viability. A particular object can be replaceable while the *class of equivalent objects*
remains central. This prevents a common misread in our mesh: declaring every redundant sensor
incorporated, or declaring a single indispensable sensor healthy merely because it is load-bearing.

## Sources read live

- Ramírez-Vizcaya, **“Sensorimotor incorporation: an operational definition,”** *Phenomenology and
  the Cognitive Sciences* (published 2025-09-24), [doi:10.1007/s11097-025-10103-5](https://doi.org/10.1007/s11097-025-10103-5).
  Sections 5–9 define centrality, concrete objects, transformed agency, portability, and
  irreversibility. The paper explicitly separates incorporation from weaker functional
  replaceability/tool use and gives the four-part definition: precarious self-individuation,
  transformed agency, portability, and irreversibility.
- Mojica, **“The concrete life of artifacts: normative sensorimotor environments beyond immediate
  action,”** *Synthese* (published 2025-10-22), [doi:10.1007/s11229-025-05308-9](https://doi.org/10.1007/s11229-025-05308-9).
  This extends the timescale: artifacts retain normative constraints while not being actively used,
  and the material environment can sustain or constrain a person's sensorimotor agency beyond the
  instant of an action.
- Ramírez-Vizcaya, **“Extending the enactive concept of habit: from sensorimotor schemes to regional
  identities,”** *Synthese* 206 (2025), [doi:10.1007/s11229-025-05237-7](https://doi.org/10.1007/s11229-025-05237-7).
  This supplies the scale warning: a habit is not a rigid stimulus-response pairing, and enactive
  organization can span seconds, activities, and longer-lived regional identities.

## Novelty check against this genome

The mesh already has several neighboring ideas, but none performs this test:

- `mesh-sensorium --exteriority` measures whether a cached stream is detachable by consumer fan-out;
  that is a structural coupling count, not proof that the stream has become central to the body's
  viability.
- `mesh-sensorium --balance` measures producer redundancy; redundancy is useful for robustness but
  says neither that a sensor is incorporated nor that the category it serves is central.
- `mesh-perimeter` and the 2026-09-09 PPS review describe action-conditioned nearness; PPS is the
  boundary of what can currently be acted on, while incorporation is the historical transformation
  and costly-loss test for what has become part of the acting body.
- `mesh-sensorium --self-prior` learns familiar own-state combinations; familiarity is not
  portability, and a familiar stream can still be non-central.

Searches for `incorporat`, `centrality`, `sensorimotor incorporation`, `portable`, and
`irreversib` found no implementation or state field that records removal cost plus replacement
equivalence. The concept therefore survives the corpus check.

## One concrete application

**Target file: `scripts/mesh-sensorium`.** Add a report-only `--incorporation` mode for each external
body/sense stream that the sensorium treats as part of its perceptual body (for example the remote
phone presence stream, room microphone, and Note3 speech/output path). It should maintain a small
append-only episode record, not a permanent “is incorporated” bit, with:

1. `loss`: during a bounded, safe holdout or observed outage, the count and severity of percept
   categories that became UNKNOWN or lost their live action/reflex path;
2. `range`: the number of distinct situations/reflexes in which that stream compensated for a
   degraded or absent alternative;
3. `replacement`: whether an equivalent named stream can be substituted, and the measured
   re-equilibration cost (time/attempts until the same categories recover); and
4. `portability`: whether the same coupling works across at least two contexts, rather than only in
   the one device/room where it was first learned.

Render `INCORPORATED-CANDIDATE` only when the evidence shows high loss, repeated cross-context use,
and a successful equivalent replacement with a recorded adjustment cost. Render `CENTRAL-NOT-
INCORPORATED` when loss is high but portability/transformation evidence is absent; render `MEDIATED`
when the stream is simply useful. Missing outage or replacement evidence stays `UNKNOWN`.

This is deliberately report-only. It makes the mesh stop saying “this remote phone is part of my
body” merely because it is reachable, while also preserving the important enactive result that a
replaceable class (several equivalent phones/sensors) can be central even when no particular device
is indispensable. The first real organ to exercise is the **presence/room-sense fusion** in
`mesh-sensorium`; a safe test fixture can remove one producer, substitute an equivalent fixture, and
assert that replacement cost and category loss are distinct fields.

## Disposition

This is a genuine gap, but not yet a safe code landing: the required “removal” experiment must be
bounded and must not intentionally take the live room ear or phone credential lane offline. The
artifact lands the mechanism and one implementable application; implementation should begin with a
fixture-backed `--incorporation` report and only later add passive live episode accumulation.
