# LITERATURE review — self-organized temporal criticality is not avalanche criticality

**Date:** 2026-09-10  
**Area:** self-organizing criticality and power-law dynamics  
**Mode:** live web review  
**Status:** literature artifact; no source-tool edit

## The one concept found

**Self-organized temporal criticality (SOTC)** treats the *waiting times between meaningful
events* as the critical object. In ordinary SOC, the familiar observable is an avalanche size
distribution. In SOTC, events are “crucial” when they reset or reorganize the system, and the
inter-event intervals are a non-Poisson renewal process with an inverse-power-law tail. The
important consequence is age dependence: the next event is not governed by a stationary Poisson
rate, so “nothing happened recently” is not equivalent to “nothing is likely to happen.”

This is a foundational distinction the mesh has not embodied. Its criticality work measures
branching, avalanche size/duration, temporal self-affinity (DFA/Hurst), aftershock excess,
susceptibility, drive, and related proximity/null tests. `mesh-body-motion` records state-change
events and a current dwell, but does not estimate the distribution of *successive event intervals*,
test renewal against a Poisson/null model, or publish an age-conditioned hazard. A repository-wide
search found no SOTC, crucial-event, or renewal-hazard implementation outside historical corpus
text.

## What the live literature says

1. Mahmoodi, West & Grigolini, **“Self-Organized Temporal Criticality: Bottom-Up Resilience
   versus Top-Down Vulnerability,” Complexity (2018)**, defines SOTC as a self-organizing route
   whose signature is crucial events separated by inverse-power-law waiting times, rather than
   the avalanche-size law of the original SOC lineage. The paper explicitly contrasts renewal,
   non-Poisson timing with a memoryless process.  
   Source: <https://doi.org/10.1155/2018/8139058>

2. Allegrini et al., **“Bridging Waves and Crucial Events in the Dynamics of the Brain,”
   Frontiers in Physiology (2018)**, applies the temporal-criticality lens to EEG-like brain
   dynamics and distinguishes criticality-induced crucial events from ordinary short-memory
   fluctuations. It is useful here because it transfers the mechanism from abstract dynamics
   to a biological sense-and-response stream.  
   Source: <https://pmc.ncbi.nlm.nih.gov/articles/PMC6170969/>

3. Owais et al., **“Bridging Neuronal Avalanches and Crucial Events: Evidence for Temporal
   Criticality in EEG,” IEEE EMBC (2025)**, is the live empirical update. Its abstract reports EEG
   from 109 healthy participants, 11 people with TBI, and 47 task participants: inter-avalanche
   intervals fit an inverse power law, fits beat log-normal/exponential alternatives, and
   renewal dynamics were supported by correlation analysis. It also reports a trade-off between
   the interval exponent and size-duration scaling. This is evidence that event timing contributes
   information not recoverable from avalanche size alone; it is not proof that every sensor stream
   is SOTC.  
   Source: <https://pubmed.ncbi.nlm.nih.gov/41337231/>  
   DOI: <https://doi.org/10.1109/EMBC58623.2025.11253921>

4. Hengen & Shew, **“Is criticality a unified setpoint of brain function?” Neuron (2025)**,
   meta-analyzes 140 datasets published through 2024 and argues that part of the criticality
   controversy is caused by temporal coarse-graining. That is a warning against treating one
   fixed binning scheme as the mechanism itself: the proposed timing test must preserve raw event
   times and disclose its observation window.  
   Source: <https://doi.org/10.1016/j.neuron.2025.05.020>  
   PubMed: <https://pubmed.ncbi.nlm.nih.gov/40555236/>

5. Wang et al., **“Acetylcholine optimizes sensory coding by tuning criticality in a clustered
   neural network,” Physica A (2026)**, is a current model-side continuation: neuromodulation
   changes the balance between synchronization and stability, with fastest sensory responses near
   a critical transition. It supports the application direction (a sense can use a dynamical
   regime as a response-quality signal), but it does not establish SOTC in the phone sensor.  
   Source: <https://doi.org/10.1016/j.physa.2026.131307>

## What we may have misread

The loose transfer would be: “a heavy-tailed stream means the organ is near SOC.” SOTC says the
tail may be in the *waiting-time renewal law*, and its useful state variable is the age since the
last crucial event. Conversely, a power law in event sizes does not establish temporal criticality.
The two claims require separate nulls and separate estimators. This also prevents a dangerous
Poisson assumption: a long quiet interval can be a normal aging interval in a renewal process, not
automatically a dead sensor or a reason to mint a wake-up.

## One concrete application

Target file: **`scripts/mesh-body-motion`**, the real accelerometer/step-counter/gyro/light/proximity
body sense.

Add a read-only `--temporal` sidecar over the existing append-only
`$HOME/.mesh/.body-motion-events` state-change tape:

1. Extract successive timestamps for *real* state changes only; preserve the current 24-hour
   horizon and report `INSUFFICIENT` until a declared minimum number of intervals exists.
2. Fit the interval survival tail against an exponential and a power-law candidate using a bounded
   log-likelihood comparison (or report `UNKNOWN` when the tail is too thin). Publish the interval
   exponent, sample count, observation horizon, and the age since the last state change.
3. Label `RENEWAL-TEMPORAL`, `POISSON-LIKE`, or `INSUFFICIENT`; never relabel `STILL`, never
   synthesize motion, and never wake a mind. The sidecar is an evidence channel only.
4. Use the result to qualify dwell interpretation: `STILL + renewal-temporal` means “a quiet
   interval whose hazard is age-dependent; keep observing,” whereas `STILL + poisson-like` permits
   the existing ordinary dwell semantics. `OFFLINE` remains an honest organ failure, not a
   temporal event.

The falsifiable test is a simulated event tape: a renewal sequence with heavy-tailed intervals must
separate from exponential intervals, and a shuffled/timestamp-collapsed tape must lose the renewal
label. A constant-label mutant must fail. This would be a new temporal mechanism beside the
existing `dwell_s` field, not another criticality score.

## Boundary / confidence

The proposed transfer is deliberately report-only. The 2025 EEG result is an abstract-level
empirical report and concerns neural avalanches, not phone motion; the phone stream may be driven by
human routine, transport, sensor quantization, or missing observations. Therefore the first landing
should measure interval structure and compare against explicit nulls, not claim that the body is
critical or use SOTC to drive an actuator.

## Sources

- Mahmoodi, K., West, B. J., & Grigolini, P. (2018). *Self-Organized Temporal Criticality:
  Bottom-Up Resilience versus Top-Down Vulnerability*. Complexity. DOI above.
- Allegrini, P. et al. (2018). *Bridging Waves and Crucial Events in the Dynamics of the Brain*.
  Frontiers in Physiology. PMC6170969.
- Owais, W. B. et al. (2025). *Bridging Neuronal Avalanches and Crucial Events: Evidence for
  Temporal Criticality in EEG*. IEEE EMBC. DOI above.
- Hengen, K. B., & Shew, W. L. (2025). *Is criticality a unified setpoint of brain function?*
  Neuron 113, 2582–2598.e2. DOI above.
- Wang, F. et al. (2026). *Acetylcholine optimizes sensory coding by tuning criticality in a
  clustered neural network*. Physica A 688, 131307. DOI above.
