# LITERATURE (live review) — performative antifragility: the stressor changes when the system learns

**Date:** 2026-09-09 · **Area:** antifragility, convexity & ruin theory (Taleb) · **Angle:** a known
failure mode of treating a locally convex response as a durable property · **Status:** review artifact;
application proposed, not implemented

## The concept we did not already embody

**Performative antifragility** is the failure mode in which the intervention used to make a system
stronger also changes the distribution of future disturbances. A convex response measured under the old
stressor distribution is then not transportable: the system may improve against the shocks it has seen
while its own policy moves the next population of shocks into a harder tail. This is the antifragility
analogue of performative prediction: the response function is not merely `f(stressor)`; deployment makes
the environment a function of the deployed policy, `D = D(policy)`.

The important distinction is:

```text
ordinary chaos result:       stressor ~ D₀ → recovery response → learn
performative result:         policyₜ → Dₜ(policyₜ) → responseₜ → policyₜ₊₁
```

The failure is not “adaptation is bad.” It is that a rising recovery score can be a **moving-target
artifact**. The policy can lower measured harm by changing what gets presented, or can induce strategic
counter-pressure that raises the next stressor's severity. A convexity/antifragility claim needs a
policy-conditioned distribution check or it is only a claim about the historical environment.

## Sources actually read

1. **Liu, Liu, Chen, Tsai, Gao & Yang, “Understanding Endogenous Data Drift in Adaptive Models with
   Recourse-Seeking Users,” AIES-25 (2025), pp. 1598–1610.** The authors model the bidirectional loop
   explicitly: decisions change user behavior, retraining changes the decision rule, and the resulting
   feedback can push models toward higher standards, higher recourse cost, and less reliable recourse
   over time. This is a concrete failure mechanism, not a metaphor:
   [AAAI/ACM paper and abstract](https://ojs.aaai.org/index.php/AIES/article/view/36659).

2. **Cyffers, Pydi, Atif & Cappé, “Optimal Classification under Performative Distribution Shift,”
   NeurIPS 37 (2024).** This formalizes deployment-induced distribution change as a push-forward measure
   and shows that even convexity of the *performative risk* requires assumptions about the direction of
   the shift. That is the missing qualification for a Taleb-style “convex response” claim: convexity of
   the payoff under a fixed input law does not imply convexity after the policy moves the law.
   [NeurIPS paper](https://proceedings.neurips.cc/paper_files/paper/2024/hash/7de665476d0adc8a54d3b8744f932bbf-Abstract-Conference.html).

3. **Li, Chen, Mao, Lei & Deng, “Performative Risk Control: Calibrating Models for Reliable Deployment
   under Performativity,” NeurIPS 38 (2025).** This is the current risk-control continuation: ordinary
   calibration assumes a fixed data-generating distribution, whereas their method iteratively refines
   calibration while the deployed predictions alter the distribution. It supplies the operational
   direction: risk must be checked during the policy/distribution loop, not only before deployment.
   [NeurIPS paper](https://papers.neurips.cc/paper_files/paper/2025/hash/d6c71e8beb41e142e463b16818537ed0-Abstract-Conference.html).

## Why this is genuinely absent here

The repository already has several neighboring ideas, but none is this mechanism:

- `scripts/mesh-chaos` has `--adaptive`, yet its adaptive log contains iteration, recovery duration,
  and success/failure only. It does not record whether the induced stressor rate, target mix, or dose
  distribution changed after the learned policy was deployed.
- `scripts/mesh-chaos-verify` now measures a dose ladder and detects saturation/non-monotonicity. That
  varies the input deliberately, but it does not ask whether the reflex itself changes the later input
  distribution.
- The existing convexity reviews cover bounded curvature, tail direction, ruin accumulation, critical
  boundaries, and dose resolution. Those are properties of the response or of a supplied history; they
  do not estimate `D(policy)` or separate exogenous drift from policy-induced drift.

This is therefore not another threshold, tail, or recovery-duration axis. It is a **causal closure
condition on the stress experiment**: the experimenter is part of the data-generating process.

## One concrete application

Apply it to **`scripts/mesh-chaos`**, specifically `--adaptive`:

1. Before the first intervention, snapshot a baseline stressor distribution from `chaos.log` (target
   identity, dose, inter-arrival time, and failure class).
2. After each adaptive policy update, write the same fields plus `policy_epoch` and compare the next
   stressor window with a no-policy/control window. Publish `shift = distance(Dₜ₊₁, D₀)` beside the
   recovery improvement.
3. Admit “antifragile improvement” only when recovery improves **and** the stressor shift is either
   measured as exogenous/control-matched or explicitly reported as policy-induced; otherwise emit
   `performative-unknown`, never `antifragile`.

The first implementation should be report-only and use the existing opt-in, substrate-deny, and
one-experiment guardrails. The key falsifier is a fixture where recovery time improves while the
post-policy dose/target mix becomes harder; the old adaptive result would call that learning, while the
new axis must call it a moving distribution. No tool edit is made in this review turn; this is the
concrete next landing if the queue dispatches implementation.

## Honest disposition

**Keep.** It applies directly to the mesh's only explicitly adaptive antifragility reflex and closes a
causal gap left by response-only convexity measurements; it does not justify automatically injecting
harder faults or weakening the existing safety boundary.
