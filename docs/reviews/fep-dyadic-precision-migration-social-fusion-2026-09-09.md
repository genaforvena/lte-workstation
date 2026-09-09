# LITERATURE (live review) — active inference failure mode: dyadic precision migration

Date: 2026-09-09 · area: Friston / free energy principle / active inference · lane: genome

## Result

The new concept is **dyadic precision migration**: under external-information collapse and
allostatic load, precision can move off an agent's private sensory/world channels and onto the
coupling channel to another agent. The result is not merely “two agents agree”; the partner becomes
the highest-weight evidence source and the pair can enter a shared attractor. This is a failure mode
that does not exist in a single-agent precision audit.

The live source is Beasley, *Folie à deux as a cusp catastrophe in coupled active inference: a
dynamical systems account of shared psychotic disorder*, **Frontiers in Psychiatry**, published 10
August 2026, DOI [10.3389/fpsyt.2026.1886942](https://doi.org/10.3389/fpsyt.2026.1886942). The paper calls
this a fourth precision-weighting failure mode, distinct from over-precise priors, over-precise
sensory likelihood, and failed meta-precision. Its mechanism is explicit: high coupling plus weak
external precision can drive beliefs toward the partner; fast inference can reverse after separation,
whereas slower learning can leave a durable reconfiguration. The paper maps asymmetric coupling to a
cusp catastrophe and predicts hysteresis/recovery-depth differences.

## Why this is a critique/failure mode, not a new slogan

The established computational-psychiatry framing treats precision failures inside one agent. Adams
et al., *The computational anatomy of psychosis*, **Frontiers in Psychiatry** 4:47 (2013),
[doi:10.3389/fpsyt.2013.00047](https://doi.org/10.3389/fpsyt.2013.00047), is the lineage for the
individual prior/likelihood/meta-precision failure modes. Beasley's 2026 paper identifies the blind
spot: a dyadic pathology is invisible when either member is examined alone. It is therefore a failure
of the usual single-agent diagnosis, not a claim that every synchronised pair is pathological.

The same paper is unusually honest about scope: the cusp reduction is not unique to active
inference; bounded-rational Bayesian RL and interactive POMDPs can carry it too. That is a useful
critique of FEP's explanatory reach. FEP supplies the precision vocabulary and coupling mapping,
but does not earn exclusive causal credit merely because the equations can be written as free-energy
minimisation. The source also labels its extensions as testable rather than established empirical
findings. Treat this as a falsifiable mechanism proposal, not a clinical detector.

The live review also checked the current field's adjacent constraint. A 2025 review, Alamia,
*Predictive coding in psychopathology: mechanistic model or metaphorical re-description?*,
**Frontiers in Human Neuroscience** 19, 1743028, [doi:10.3389/fnhum.2025.1743028](https://doi.org/10.3389/fnhum.2025.1743028),
documents dissociations between prediction-error proxies and behavioural updating, and calls for
explicit, testable mechanistic commitments. That rules out treating a new label or a correlated
social signal as proof of precision migration.

## Novelty audit against this tree

The tree already has policy precision / expected precision (`docs/reviews/efe-gamma-probe-confidence-2026-07-29.md`),
epistemic value, dark-room priors, and a read-only homeostatic coupling audit in
`scripts/mesh-load-gate`. That coupling audit asks whether remote distress covaries with a local
shed actuator; it does not model precision moving from independent local senses onto a partner-like
channel, nor distinguish fast attention capture from slow learned reconfiguration.

This is therefore new ground: **channel dominance within a coupled social sense**, not another
confidence score or another “peer state is accessible” check.

## One concrete application

Apply it to the existing social sense/reflex: **`scripts/mesh-social-fusion`**. Add a report-only
`--coupling-audit` mode and an observation-tape field, not a new actuator:

1. Treat ambient microphone, BLE presence, and local activity as the independent/world channels;
   treat phone-derived `.social-context.state` as the coupling/partner channel.
2. On each reading, publish the live overlap and age of all four channels. When local coverage falls
   while social-context remains live, report `COUPLING-DOMINANT-CANDIDATE` rather than allowing a
   social label to look like corroborated local perception.
3. Keep `SOCIAL_ENGAGED` gated on the existing local three-axis overlap; the partner-like channel
   may annotate, but never mint, that verdict. Log recovery time after local channels return: a
   short return is an inference-level episode; persistence after repeated exposure is the candidate
   learning-level episode.

The concrete failure it catches is: microphone/BLE/activity go stale or contradictory, the phone
context remains confidently `SOCIAL-ONLINE`, and a consumer reads the resulting social state as an
observation of the room. The safe reflex is abstention/hold, not a guessed social moment. This
directly instantiates the paper's “external precision collapse + coupling-channel dominance” on a
real organ path (mic/BLE/phone) while preserving the current honest-UNKNOWN contract.

## Boundary / next verification

Do not claim that the mesh has dyadic precision migration today. The artifact above is a proposed
measurement and a target file. Before wiring any behavior, build a replay tape with deliberate local
channel outages, a live social-context channel, and a separation/recovery interval; require a
positive control where independent channels remain predictive and a negative control where the
phone context is shifted. If that audit cannot distinguish coupling dominance from common-cause
staleness, discard the application rather than adding a new label.

## Sources read

- Beasley, 2026, [Frontiers in Psychiatry article](https://www.frontiersin.org/journals/psychiatry/articles/10.3389/fpsyt.2026.1886942/full)
  (failure mode, coupled equations, cusp/recovery predictions, limitations).
- Adams et al., 2013, [The computational anatomy of psychosis](https://doi.org/10.3389/fpsyt.2013.00047)
  (individual precision-failure baseline cited by the new paper).
- Alamia, 2025, [Predictive coding in psychopathology: mechanistic model or metaphorical re-description?](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2025.1743028/full)
  (current critique: proxy/behaviour dissociation and falsifiability constraints).
- Friston et al., 2024, [Federated inference and belief sharing](https://doi.org/10.1016/j.neubiorev.2023.105500)
  (healthy belief-sharing comparison cited by Beasley; the new paper's gap is pathological dyadic
  coupling, not ordinary communication).
