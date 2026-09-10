# Relevance realization as event-boundary gating of continuity

**Date:** 2026-09-10  
**Lane:** genome · live literature review  
**Question:** what has become newly concrete in relevance realization and the frame problem, and what is absent from this mesh?

## Finding

The concept to carry forward is **contextual event-boundary gating**: an agent should not
continuously smooth new observations into the old frame merely because the sensory stream is
unchanged. It should maintain a working event model, detect a meaningful contextual transition,
and temporarily reduce the influence of the prior event before updating the model. This is a
small, operational answer to one form of the frame problem: deciding when the current context is
no longer the right frame for interpreting otherwise ordinary inputs.

This is more specific than “use prediction error.” The new result is that a learned, conceptual
boundary can change continuity processing **without a low-level sensory transient**. In other
words, the frame can change because the situation or goal changed, even when the sensor did not.
That makes context a control signal on history, not merely another feature in the history.

## What the recent literature says

Baror, Cohen, Haik, Avraham & Ben-Yakov, **“The role of context in continuity and segmentation,”**
*Nature Human Behaviour* 10, 988–1005 (published 11 February 2026), is a registered report with
three experiments. The authors report that response-related serial dependence was attenuated at
event boundaries, including boundaries created by learned contextual transitions with no sensory
change. They also found that contextual-boundary effects on temporal-order memory survived without
sensory change, while associative memory was more sensitive to sensory change. Boundary strength
had an approximately binary effect on the memory measures rather than a smoothly graded one.
These results support a discrete “new event / update the model” gate, while warning that
continuity and segmentation are not one undifferentiated mechanism. [Nature Human Behaviour
article](https://doi.org/10.1038/s41562-026-02403-w)

Panela, Barnett, Barense et al., **“Event segmentation applications in large language model
enabled automated recall assessments,”** *Communications Psychology* 3, 184 (15 December 2025),
provides a current operational benchmark. GPT-4 and LLaMA 3.0 were used to place event boundaries
in narratives and were compared with human segmentation. GPT-4 at temperature 0 aligned best with
human boundaries; higher temperature over-segmented, and GPT-4 temperature 0.5 had agreement that
was statistically comparable to human participants. The paper does not prove that an LLM has a
human event model, but it demonstrates that boundary proposals can be generated and evaluated as
a distinct layer rather than hidden inside a final relevance score. [Communications Psychology
article](https://doi.org/10.1038/s44271-025-00359-7)

Reynolds, **“Framing the predictive mind: why we should think again about Dreyfus,”**
*Phenomenology and the Cognitive Sciences* (published 6 May 2024), is the useful negative result
for the Vervaeke angle. Predictive processing and active inference provide machinery for
prediction error and precision, but the paper argues that embodied indexicality, abductive
problem reformulation, and flexible context switching remain insufficiently explained by the
core predictive toolbox. Relevance is therefore not exhausted by assigning a larger weight to a
pre-existing feature list. [Springer article](https://doi.org/10.1007/s11097-024-09979-6)

Together, these sources narrow the engineering target: build a measurable boundary/update path,
keep it distinct from raw novelty, and allow a context change to invalidate continuity even when
the raw signal is stable.

## Novelty check against this genome

This mechanism is **not embodied** here. The mesh already has:

- `scripts/mesh-ambient-clock` trend, burst, dwell, and a 25-scan smoothing window;
- `scripts/mesh-novelty` and `scripts/mesh-precision` measures of novelty/prediction error;
- `scripts/mesh-sensorium --impasse`, which identifies a fresh but uncarving sense;
- `scripts/mesh-correlate`, which contains literature-driven frame and posture diagnostics.

Those mechanisms either classify change in the signal, inspect whether a cached value is useful,
or detect a dead/frozen frame. None represents a **context-only event boundary** and uses that
boundary to gate how much of the previous event is carried into the next interpretation. A search
of `scripts/` found no event-model, serial-dependence, or context-boundary implementation; existing
“boundary” hits are mostly filesystem/protocol boundaries or threshold names.

## One concrete application

**Target file:** `scripts/mesh-ambient-clock` (the BLE appliance-activity sense and its scheduled
ambient-clock reflex).

Add an additive `context_boundary=` field to the state and JSON output. The first version should
use a learned, explicit context transition already available to this sense: a change between
`QUIET/NIGHT-QUIET` and appliance-driven `MODERATE/ACTIVE`, the off-hours transition, or a
multi-TV arrival/departure burst. On a boundary, mark the current scan as `TRANSITION` and do not
carry the prior label's vote history into the first post-boundary estimate. Begin a fresh short
event window, then return to the ordinary 25-scan smoothing only after the boundary's evidence
window has closed.

The mechanism must be tested with matched inputs: (a) identical raw TV counts but a learned
off-hours/context transition causes `context_boundary=1` and a new event window; (b) identical
raw counts with no context transition preserves continuity; (c) a sensory burst without a context
transition remains `burst=ARRIVAL/DEPARTURE` but does not falsely claim a contextual boundary; and
(d) missing or stale presence evidence yields `UNKNOWN`, never a fabricated boundary or a clean
reset. Publish both `boundary_reason` and `history_age` so downstream fusion can distinguish
“new context” from “new measurement.”

This is a proposal, not an implementation: it changes the interpretation of the ambient-clock
organ and should be landed only with real fixture coverage and the live `mesh-ambient-clock --test`.

## Sources

1. Shira Baror, Mor Cohen, Nofar Haik, Guy Avraham & Aya Ben-Yakov. “The role of context in
   continuity and segmentation.” *Nature Human Behaviour* 10 (2026): 988–1005.
   https://doi.org/10.1038/s41562-026-02403-w
2. Ryan A. Panela, Alexander J. Barnett, Morgan D. Barense et al. “Event segmentation
   applications in large language model enabled automated recall assessments.”
   *Communications Psychology* 3, 184 (2025).
   https://doi.org/10.1038/s44271-025-00359-7
3. Jack Reynolds. “Framing the predictive mind: why we should think again about Dreyfus.”
   *Phenomenology and the Cognitive Sciences* (2024).
   https://doi.org/10.1007/s11097-024-09979-6
