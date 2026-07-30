# Autopoiesis as a complexity ratio — A = C_system / C_environment

**Area:** autopoiesis & the biology of cognition (Maturana, Varela) · **Angle:** a concrete METRIC or experiment this area uses to measure itself
**Date:** 2026-07-29 · **Named in:** `scripts/mesh-vitality` (review block above the VSM homeostat section) · **Status:** HELD (steward-gated — the blocker is the environment partition, not the math)

## The metric

Nelson Fernández, Carlos Gershenson & Carlos Maldonado give the field's one explicitly
**information-theoretic, computable** self-measure of autopoiesis — *"Information Measures of Complexity,
Emergence, Self-organization, Homeostasis, and Autopoiesis"* (in Prokopenko, ed., *Guided
Self-Organization: Inception*, Springer 2014; companion arXiv:
[1409.7475](https://arxiv.org/abs/1409.7475) *"Requisite Variety, Autopoiesis, and Self-organization"*,
*Kybernetes* 2017).

The construction, from a variable's normalized Shannon entropy:

- **Emergence** `E = H / H_max` — novelty / variety.
- **Self-organization** `S = 1 − E` — order / constraint.
- **Complexity** `C = 4·E·S = 4·E·(1−E)` — maximal at the `E=½` balance of order and disorder, `≈0` at
  either a frozen constant (`E→0`) or pure noise (`E→1`).
- **Autopoiesis** `A = C_system / C_environment` — a unity is autopoietic to the degree its **own**
  organized complexity **exceeds** that of the environment driving it. `A>1` = self-produced order
  dominates external forcing (autonomous); `A<1` = environment-dominated (heteronomous).

This is exactly the "measure of autopoiesis as the ratio between the complexity of a system and the
complexity of its environment" the current literature cites — the operational, quantitative counterpart
to Maturana & Varela's qualitative autonomy.

## Why it is not already embodied — and the subtlety

Autopoiesis is the **most-embodied** area in this codebase: operational-closure / closure-fraction,
closure-of-constraints, the cognitive-domain perturbation-partition (`mesh-chaos`, Beer 2014/2020),
structural determinism (`mesh-dispatch`), Di Paolo adaptivity (`mesh-body-power`), irruption/absorption
(`mesh-needs`), precariousness (`mesh-vitality`, HELD), autopoiesis-vs-allopoiesis loop-closure
(`mesh-vitality` `allopoiesis_gap`, landed 2026-07-29), and MTTR self-repair (`mesh-reliability`).

The subtlety that makes this a genuine gap: the **ingredients are already here**.
`action_occupancy()` already computes *exactly Fernández's E* for the **system's** self-production stream
(normalized entropy `H_n` of edits-per-tool), and `channel_variety()` computes Ashby requisite variety of
the coordination channel. But **no vital sign forms the ratio** — `C_system` relative to `C_environment`.

So vitality can read a healthy broad-occupancy self-production (`action_occupancy≈1`) while being **blind**
to whether that internal complexity is genuinely self-*determined* or merely tracking an equally-complex
environmental drive. A mesh that only ever edits the tool the operator just asked about has high
`action_occupancy` **and** `A≈1` — busy, not autonomous. The ratio is the autopoietic reading a
single-stream entropy cannot give: emergence-of-order **relative to** the environment. The mesh already
reads the autopoiesis/allopoiesis distinction on the **loop-closure** axis (`allopoiesis_gap`, wall-clock
latency); this is the same distinction on the **information-complexity** axis, which is unread.

## Distinct from everything embodied

- **NOT `action_occupancy`** — that *is* `E_system` alone: a single-stream entropy, no environment, no
  ratio. And `C=4·E·(1−E)` is not monotone in `E`, so `A` is not even recoverable from
  `action_occupancy`'s number.
- **NOT `channel_variety`** — Ashby requisite variety of one channel's inflow-vs-closure, not a
  self/environment complexity ratio.
- **NOT `autonomy_ratio`** — a **count** fraction (self-vs-forced commits). A stream can be 100%
  self-authored yet `A<1` if its structure merely mirrors the environment's.
- **NOT `allopoiesis_gap`** — loop-**closure** latency in wall-clock, not an information measure.
- **NOT the homeostasis-measure** — Fernández's separate H-measure is the *stability of the same E over
  time*, not the system/environment ratio.

## What is HELD, and why

`C_system` is in hand (`action_occupancy`'s E → `C_sys = 4·E·(1−E)`). Shipping `A` needs a **defensible
`C_environment`** — an entropy over the stream the mesh does **not** produce (operator asks + external
sensor / network / API perturbations), cleanly separated from the mesh's own production.

That partition is exactly the *"what is environment vs self"* call that `mesh-chaos`'s cognitive-domain
HELD and the precariousness block both flag as needing validation before it can carry a verdict — a
mis-drawn boundary makes `A` a confident-but-meaningless number (the assert-from-a-proxy failure the
genome warns against). So the **ratio** stays HELD until the environmental-inflow stream is grounded and
validated against `vitality.log`; the math and `C_system` are ready the moment it is. Report-only when it
lands, never a gate — an `A<1` spell is a reading, not a fault.

## One-line summary

Named the Fernández–Gershenson–Maldonado information-theoretic autopoiesis measure **A = C_sys/C_env**
(arXiv:1409.7475), the field's one computable self-measure; the mesh already computes `E_system`
(`action_occupancy`) but never the **ratio against the environment** — HELD in `scripts/mesh-vitality`
on grounding a defensible `C_environment`, the same self/environment-boundary caveat the cognitive-domain
and precariousness reviews carry.
