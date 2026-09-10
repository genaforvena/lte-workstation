# LITERATURE review — second-order cybernetics → `scripts/mesh-phone-ear`

**Area:** second-order cybernetics (Gordon Pask, with the observer/participant problem made explicit).
**Arm:** treated (assigned)
**Target organ:** `scripts/mesh-phone-ear` — assigned by coin at p=0.20; not chosen by the reviewer or
the lane.
**Reviewer:** genome mind · live web review, 2026-09-10.

## One concept not already embodied

The useful mechanism is **Paskian conversation as reciprocal concept construction**, not merely a
feedback loop. A conversation has at least two actors who perturb one another, externalise descriptions,
and refine a shared conceptual domain; the relevant representation is an **entailment structure/mesh**
of topics and their relations. The point that is easy to misread is that a stream of observations sent
to a board is not yet a conversation: it lacks the return leg by which the observer/participant can
test and revise what was understood.

This is a genuinely unembodied mechanism in the assigned organ. `mesh-phone-ear` records only after a
confirmed unlock, sends one filtered transcription to `mesh-chat`, and retains no transcript or
confirmation state. Its path is therefore `microphone → transcription → board`, not a reciprocal
concept-refinement loop. The broader mesh has many feedback and acknowledgement conventions, but this
organ does not implement a Paskian conversation or an entailment mesh of what its utterances mean.

## Live sources read

- Tilak, Manning, Glassman, Pangaro & Scott, **“Gordon Pask’s Conversation Theory and Interaction of
  Actors Theory: Research to Practice,”** *Enacting Cybernetics* 2(1), 2024, DOI
  [10.58695/ec.11](https://doi.org/10.58695/ec.11). The open UCL record describes the paper’s three
  parts: core CT/IA concepts, Pask’s CASE/THOUGHTSTICKER systems, and design pathways in which tools
  mediate learning and make users intermediaries rather than passive consumers
  ([UCL Discovery record](https://discovery.ucl.ac.uk/id/eprint/10196048/)). This is the current
  source anchoring the review, rather than treating Pask as a closed historical list.
- Pask, **“Cybernetic Theory of Cognition and Learning,”** *Journal of Cybernetics* 5(1), 1975,
  DOI [10.1080/01969727508546082](https://doi.org/10.1080/01969727508546082). The abstract states
  that the paper presents a cybernetic theory of conversational interaction and an embodiment in
  CASTE.
- Pask, **“The representation of knowables,”** *International Journal of Man-Machine Studies* 7(1),
  1975, DOI [10.1016/S0020-7373(75)80003-4](https://doi.org/10.1016/S0020-7373(75)80003-4). Its
  abstract describes constructing representations of tutorial-conversation domains and the
  knowledge structures used by the participants.

## Assigned-organ verdict

**Discard for `scripts/mesh-phone-ear`: Conversation Theory genuinely does not apply to this organ in
its present one-way, no-confirmation form; adding a second actor would be a redesign of the organ, not
an honest application of the reviewed mechanism.**

No source code was changed: a unilateral transcript post cannot be relabelled as a Paskian
conversation, and silently adding a reply protocol would violate the fixed-organ refusal condition.

## Verification

The target source was read before the review and still has only the one-way `board_feed` path; the
existing source tree was searched for Pask/Conversation Theory/entailment implementations before
calling this absent. This artifact records the assigned target and the refusal; no deployed copy was
edited and no commit was made.
