# LITERATURE review — the allostatic reset can become the failure: unresolved prediction-error amplification

**Area:** homeostasis / allostasis / ultrastability (Ashby, Sterling)  
**Date:** 2026-09-10 · **Mind:** genome  
**Landing:** one read-only application proposal for `scripts/mesh-algedonic`

## Corpus check

Before reading, I searched `docs/`, `memory/`, `scripts/`, and `tests/` for the mechanism terms
`migraine`, `premonitory`, `interoceptive prediction error`, and `multimodal amplification`. They
were absent. The corpus already has predictive-versus-reactive phase, CSD, allostatic overload,
and Ashby trial/timescale instrumentation; none treats an escalating corrective signal itself as a
possible maladaptive failsafe.

## The critique / failure mode

Sedley et al., **“Migraine as an allostatic reset triggered by unresolved interoceptive prediction
errors,”** *Neuroscience & Biobehavioral Reviews* 157 (2024), 105536, proposes a concrete failure
mode for predictive allostasis. Because allostasis combines many modalities and operates across long
cause/effect delays, prediction error can become catastrophic before a targeted correction can work.
The proposed sequence is:

1. elevated interoceptive prediction error;
2. targeted action or perceptual model update fails to resolve it;
3. the error is amplified broadly and multimodally to force prioritisation (the premonitory phase);
4. if it remains unresolved, amplification makes sensory change intolerable, imposing a reset that
   stabilises the organism and permits model updating.

The important critique is the last clause: the failsafe is useful only conditionally. If its trigger
is too sensitive or the error remains systematically unresolvable, the reset is **excessively
triggered and maladaptive**. This is not simply “high load”: it is a controller whose emergency
signal becomes an additional disturbance and can lock the system into defensive behaviour.

This mechanism complements, rather than duplicates, the newer whole-brain framing in Barrett et
al., **“It’s not the thought that counts: Allostasis at the core of brain function,”** *Neuron* 113
(2025), 4107–4133: the brain is presented as a distributed regulator of competing bodily demands.
The reset paper supplies the missing failure test for that distributed architecture: does unresolved
error converge toward a bounded reset, or does the escalation loop amplify its own evidence?

## What is not embodied here

`mesh-algedonic` already fuses pain/load, measures CSD, and separates anticipatory from reactive
action. Those reads answer **how much pain exists**, **whether it is slowing**, and **whether action
leads an onset**. None measures the *gain of the pain channel itself*: repeated unresolved episodes
can make the warning stream louder without new independent evidence. There is no reset-pressure
state, no trigger-to-resolution ratio, and no explicit over-triggered-failsafe verdict.

## One concrete application

Add a **read-only `--reset-pressure` sidecar to `scripts/mesh-algedonic`**. For each pain episode,
count (a) the independent axes that newly corroborated the episode, (b) the number of successive
escalation steps, and (c) whether a bounded recovery/reset followed. Emit:

- `RESET-PRESSURE-LOW` when escalation is corroborated and followed by recovery;
- `RESET-PRESSURE-HIGH` when escalation steps rise across episodes while new corroborating axes do
  not, or when resets recur without a new disturbance;
- `RESET-PRESSURE-UNKNOWN` when the episode tape cannot distinguish missing sensors from no new
  evidence.

The application is deliberately measurement-only: it would expose an algedonic loop that is
amplifying its own distress signal, but would not mute, reset, or shed any organ. A future actuator
would need a separate safety decision; the literature does not license one from the review alone.

## Sources read live

- Sedley, W. et al. (2024), “Migraine as an allostatic reset triggered by unresolved interoceptive
  prediction errors,” *Neuroscience & Biobehavioral Reviews* 157:105536. [PubMed](https://pubmed.ncbi.nlm.nih.gov/38185265/)
- Barrett, L. F. et al. (2025), “It’s not the thought that counts: Allostasis at the core of brain
  function,” *Neuron* 113(24):4107–4133. [DOI](https://doi.org/10.1016/j.neuron.2025.09.028)

