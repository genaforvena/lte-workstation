# SOC & power-law dynamics (live review): latent-driver null for `mesh-child-sim`

**Date:** 2026-09-09  
**Area:** self-organizing criticality & power-law dynamics, from the angle of a **known critique**.  
**Target:** `scripts/mesh-child-sim` (assigned; no retargeting).  
**Arm:** treated (assigned)

## Finding

The new concept is the **latent-driver null**: a slowly varying shared latent variable can make a
population look avalanche-critical, including power-law-like activity, without fine-tuning the
coupling parameters and without the observed units forming a genuine cascade. The diagnostic is
mechanistic, not another exponent: condition on or infer the shared driver, then test whether the
tail and avalanche signatures remain.

This is a failure mode for reading a heavy tail as evidence of self-organized criticality. A common
driver can synchronize otherwise independent units; aggregation then supplies the apparent
criticality. In this target, the hard population cap and the birth-time fitness mutation are also
finite-size and background mechanisms that can shape the tail, so an unconditioned child-generation
distribution would be non-identifying.

## Live sources read

- Mia C. Morrell, Ilya Nemenman & Audrey J. Sederberg, **“Neural criticality from effective latent
  variables,”** *eLife* 12:RP89337 (version of record, 2024). The authors show avalanche criticality
  from populations driven by latent dynamical variables without fine-tuning; the article’s
  assessment explicitly warns that independent units driven by a slowly varying latent can produce
  the appearance. [eLife article](https://doi.org/10.7554/eLife.89337.3) · [arXiv:2301.00759](https://arxiv.org/abs/2301.00759)
- Flavio R. Rusch, Osame Kinouchi & Antonio C. Roque, **“Influence of topology on the critical
  behavior of hierarchical modular neuronal
  networks,”** *Communications Physics* (2025). It distinguishes SOC from self-organized
  quasicriticality and notes that apparent criticality can require fine-tuning; it also uses
  cross-observable scaling relations rather than treating one power law as decisive. [Nature
  Communications Physics](https://www.nature.com/articles/s42005-025-02074-5)
- Markus J. Aschwanden & Felix Scholkmann, **“Power Laws Associated with Self-Organized
  Criticality: A Comparison of Empirical Data with Model Predictions,”** arXiv:2505.00748 (2025).
  Their cross-domain comparison reports that background treatment, fitting range, small-number
  statistics, and finite-system size make many apparent SOC fits inconclusive. [arXiv paper](https://arxiv.org/abs/2505.00748)

The 2025 paper is live and current enough to expose the present terminology, while the eLife paper
is the direct mechanistic result. I read the abstracts/results discussion and the relevant caveat
sections, not just search snippets.

## Why this is not already embodied here

The existing `mesh-child-sim` models a capped population and reports lineage, generation, engine,
and synthetic fitness. It has no shared latent-pressure field, no pressure-conditioned null, and no
comparison of a tail before versus after conditioning. Its cap is a safety constraint, not evidence
of criticality. This concept is therefore not a duplicate of the existing SOC tooling: it is a
mechanism-level confound test attached to this assigned simulation.

## One concrete application

When an avalanche/readout is added to `scripts/mesh-child-sim`, record `latent_pressure` and
`MESH_CHILD_SIM_CAP` on every tick, then compare the observed child birth/cull-size tail with a
matched null that samples children independently conditional on the same pressure sequence. If the
power-law-like tail disappears after conditioning, emit `LATENT-DRIVEN` and do not call it SOC; if
it survives, require the separate parent-to-child cascade evidence before using a criticality label.

This is a proposal for the assigned simulated organ, not a claim that its current JSON population
already exhibits a power law.

## Landing

The source landing is the literature guard in `scripts/mesh-child-sim` immediately after its
simulation contract. No deployed copy was edited, and no live child/window/node was created.
