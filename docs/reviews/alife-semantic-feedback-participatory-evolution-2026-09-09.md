# Live literature review — semantic feedback as an evolutionary control signal

**Date:** 2026-09-09  
**Area:** artificial life / open-ended evolution  
**Review question:** which foundational idea are we still reading too loosely?  
**Disposition:** finding; concrete application proposed, not implemented and not committed.

## Finding: participation is not just selection

The distinct mechanism is **semantic feedback**: natural-language intent is a continuous control
signal inside the evolutionary loop, not a one-time prompt and not merely a human who accepts or
rejects the final offspring. Li et al. describe a pipeline in which a prompt-to-parameter encoder
maps language into behavioural parameters, CMA-ES searches the population, and a CLIP-based semantic
score feeds the result back into subsequent generations. Their implementation also accumulates prompt
history to derive higher-order rules for later evolution.

The likely misread is treating "the mind is the value filter" as participation. In this repository,
`scripts/mesh-ideate` emits a connection or literature candidate, then a human may keep or discard it;
its persistent state is recent-key suppression, repellents, and illumination coverage. A review can
therefore affect one candidate's fate, but the review's meaning is not a semantic state that changes
the next generation's candidate parameters. `rg` finds no semantic-feedback loop, prompt-history
encoder, or evaluator-driven parameter update in the ideation/reflex path. This is distinct from our
already-landed novelty, MAP-Elites illumination, pressure/neglect, MCC, and compression-progress
mechanisms: those select by novelty, coverage, minimal criteria, or learnability, not by an evolving
human-language meaning signal.

The source is a 2025 preprint/conference work, not a timeless textbook list. Its strongest useful
claim is architectural (language enters the loop and modulates behaviour); the reported user-study
alignment should remain a hypothesis until independently reproduced. The authors also frame
open-endedness as maintaining diversity, legibility, and revision, not as producing unbounded novelty
blindly.

## One concrete application

**Target:** `scripts/mesh-ideate`, the literature/connection reflex.

Add an opt-in semantic-feedback sidecar, e.g. `~/.mesh/.ideate-semantic-feedback.jsonl`: after the
operator's `[done]`, `[yield]`, or one-line discard verdict, record the reviewed idea text plus the
operator's short natural-language direction (for example, “more artificial-cell closure, less
novelty metric”). On the next `mesh-ideate --lit` pass, use that history to perturb the literature
generator's area/angle parameters toward the expressed direction, while retaining the existing
illumination and repellent gates. The reflex should emit both the chosen semantic direction and the
candidate, so the feedback is auditable; an absent or unparseable sidecar must mean `na`/no semantic
steering, never a fabricated preference. A future test should prove that the same seed plus a changed
feedback phrase changes the selected candidate, while an empty feedback history preserves the current
selection distribution.

This is a proposal only: no mesh tool or deployed copy was edited.

## Sources read live

- Li, Wang, Fang, Huang, Asadipour, Mi & Sun, **“Participatory Evolution of Artificial Life Systems
  via Semantic Feedback,”** arXiv:2507.03839 (2025), abstract and paper record:
  <https://arxiv.org/abs/2507.03839>.
- Author project page, **“Participatory Evolution of Artificial Life Systems via Semantic Feedback,”**
  describing the BERT prompt-to-parameter encoder, CMA-ES, CLIP evaluation, accumulated prompt history,
  and SIGGRAPH Asia 2025 presentation:
  <https://yitongsun.com/artificial-life>.
- Open preprint record and downloadable paper:
  <https://interactives.pub/paper/AZbau_JZ>.

## Verification / handoff

- Repository-gap check: `rg` over `scripts/`, `docs/`, `README.md` found no semantic-feedback control
  loop for `mesh-ideate`; existing nearby literature mechanisms were explicitly excluded above.
- Artifact: this file.
- No tests were run because no executable code changed. No commit was made, per task instruction.
