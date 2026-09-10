# LITERATURE (live review) — information theory of agency → bridge-gap pursuit

**Area:** information theory of agency — empowerment, predictive information  
**Review date:** 2026-09-10  
**Method:** live web search of current arXiv listings, then read the primary HTML/abstracts; repository search for the mechanism and its near neighbours.  
**Verdict:** LAND ONE UN-EMBODIED MECHANISM; propose one application, do not ship code in this pass.

## What is new

The useful recent result is **Bridge-Gap Pursuit (BGP)** in Richard Csaky, *Prediction and
Empowerment: A Theory of Agency through Bridge Interfaces*, arXiv:2605.06346v1, submitted 7 May
2026: <https://arxiv.org/abs/2605.06346> and full text <https://arxiv.org/html/2605.06346>.

The paper separates three things that a high empowerment or high predictive-information number can
collapse together: identifying a hidden state, refining the interface through which it is observed,
and overwriting a future outcome with one's action. Its operational mechanism is **bridge-gap pursuit**:
define a potential `Φ(H)` for the remaining gap between the current bridge transcript and the target
quotient/control objective, then use the intrinsic reward

```text
    r_BGP(t) = Φ(H_t) − Φ(H_{t+1})
```

to choose actions that make the *interface* more informative for the target. The paper proves that
this reward telescopes to terminal bridge-gap reduction and gives an exact finite-horizon dynamic
program for the model-based case. In plain terms: the next action is valuable when it improves the
measurement channel needed for the particular question, not merely when it increases generic action
→ observation mutual information.

This is a mechanism we do not embody. The repository has already landed the paper's adjacent ideas:

- `scripts/mesh-cam-light` reports a single-frame luma-entropy ceiling and
  `refine=floor:none-reachable(...)` (the interface-empowerment/resolving-floor result).
- `scripts/mesh-algedonic` and `scripts/mesh-promises` measure several forms of empowerment,
  including discounted and cost-priced variants.
- `scripts/mesh-precision` measures predictive-information stock/rate.

But those are **read-only diagnostics**. `rg` finds no `bridge-gap`, `BGP`, or bridge-potential
controller in `scripts/` or `docs/reviews/`. No reflex currently chooses an action because that
action is expected to reduce uncertainty in a target-relevant sensory quotient. Existing “active”
behaviour is either fixed probing or a cadence decision.

## Why this matters now

The current 2026 literature is moving from “empowerment as a scalar intrinsic reward” toward an
agent's limited bridge: what can this sensor/interface distinguish, what action can refine it, and
which target does that refinement serve? Csaky's February 2026 *Artificial Agency Program* frames the
same direction as budgeted allocation among observation, action, and deliberation, but is a research
agenda rather than the concrete control law used here:
<https://arxiv.org/abs/2602.24100>. Schneider et al.'s October 2025 policy-pretraining paper shows
discounted empowerment improving downstream adaptation, but it still optimizes control capacity as
the pretraining signal rather than target-specific bridge refinement:
<https://arxiv.org/abs/2510.05996>. Those are useful neighbouring results; BGP is the one new
operational seam selected for landing.

The distinction is important for this mesh. A webcam frame can be fresh, non-flat, and high in
histogram entropy while remaining poor evidence for a specific question such as “is the room
occupied?” Generic empowerment or frame entropy does not say which next action makes that question
answerable. BGP says to score the action by the decrease in the remaining target-specific gap.

## One concrete application (proposed, not shipped)

**Target file:** `scripts/genius-loci` — the ambient camera reflex, specifically its existing
`_torch_indicator()` followed by `capture()`.

Replace the fixed “three torch flashes, then discard the result” probe with a report-only BGP
experiment on the Note3 camera path:

1. capture a baseline frame and compute the target quotient for the reflex's permitted question
   (scene/light/stillness, never identity);
2. choose one bridge action, `termux-torch on`, capture again, then turn it off and capture a
   recovery frame;
3. score `ΔΦ = target-gap(before) − target-gap(after)` using held-out frame bins (for example,
   separability of light/stillness classes, not raw pixel entropy), and log `bridge_gain=ΔΦ`,
   coverage, and the action owner;
4. only after a real calibration corpus, let the next-look policy prefer the probe when its expected
   bridge gain exceeds its capture/torch cost. A torchless or unreachable phone is `unknown`, never
   zero gain.

This is a genuine action→sense loop already available in the file: `_torch_indicator()` actuates the
phone flash and `capture()` reads the phone camera. The current code uses that actuator as a fixed
indicator and throws away the causal before/after evidence; BGP would make the action earn its place
by reducing uncertainty about a named target. The initial landing should remain report-only because
the camera/torch channel and the target classifier need live calibration; no guessed threshold should
gate speech or capture.

## What is not claimed

This review does not claim that BGP is empirically established on this hardware: the cited work is a
2026 working arXiv draft and the proposed application is unimplemented. It also does not re-land
plasticity, interface empowerment, or frame entropy; those are already recorded above and in the
existing reviews. The new landing is the **closed-loop bridge-potential controller** that turns an
interface diagnostic into target-specific active sensing.

## Sources read

- Richard Csaky, *Prediction and Empowerment: A Theory of Agency through Bridge Interfaces*,
  arXiv:2605.06346v1 (2026-05-07):
  <https://arxiv.org/abs/2605.06346> · <https://arxiv.org/html/2605.06346>.
- Richard Csaky, *Artificial Agency Program: Curiosity, compression, and communication in agents*,
  arXiv:2602.24100 (2026-02-27): <https://arxiv.org/abs/2602.24100>.
- Moritz Schneider et al., *Information-Theoretic Policy Pre-Training with Empowerment*,
  arXiv:2510.05996 (2025-10-07): <https://arxiv.org/abs/2510.05996>.

**Artifact status:** documentation only; uncommitted, as requested.
