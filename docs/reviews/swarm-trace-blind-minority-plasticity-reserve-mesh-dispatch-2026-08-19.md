# Live literature review — swarm intelligence & stigmergy → a distributed sensor mesh

**Date:** 2026-08-19 · **Lane:** genome · **Organ:** `scripts/mesh-dispatch` (new `--plasticity` audit)

## Where the corpus already is

`docs/reviews/` carries ~17 swarm/stigmergy files: tunable quorum, response-threshold division of
labour, cross-inhibition, density-adaptive evaporation, no-entry repellent/negative pheromone,
tandem-run teaching, the ant-mill positive-feedback trap, sematectonic vs sign-based stigmergy,
pheromone-entropy foraging evenness, the fundamental diagram, interaction-rate closed-loop drive,
inverse stigmergy, directed-information lead/lag, differential-latency aggregation. So the standard
mechanisms are embodied, and `mesh-forage` already measures trail-entropy stagnation.

## The concept we did not embody

Aymeric Vellinger, Nemanja Antonic & Elio Tuci, **"From Pheromones to Policies: Reinforcement
Learning for Engineered Biological Swarms"**, [arXiv:2509.20095](https://arxiv.org/abs/2509.20095)
(24 Sep 2025). They establish a theoretical equivalence between pheromone-mediated aggregation in
*C. elegans* and reinforcement learning — stigmergic signals function as distributed reward, and
pheromone dynamics mathematically mirror cross-learning updates. From the abstract, verbatim:

> "In dynamic environments, persistent pheromone trails create positive feedback loops that hinder
> adaptation by locking swarms into obsolete choices. Through computational experiments in
> multi-armed bandit scenarios, we reveal that introducing a minority of exploratory agents
> insensitive to pheromones restores collective plasticity, enabling rapid task switching. This
> behavioural heterogeneity balances exploration-exploitation trade-offs, implementing swarm-level
> extinction of outdated strategies."

The sharp part is **not** "add exploration" — the mesh already has evaporation (`.dispatch-evaporated`),
a repellent (`mesh-ideate`), and inverse stigmergy (`mesh-forage --design`). It is that the
exploration must be **heterogeneous** — a *minority that is insensitive to the trace* — and not
homogeneous noise spread evenly across agents. The two have the same mean exploration rate and
different collective dynamics: a slightly-noisy agent is pulled back by the trail every step, so the
swarm's mass stays on the obsolete arm; a trace-**blind** agent commits to the unreinforced arm and
can then *seed* a new trail the majority follows. Only the second gives the discontinuous switch.

Nothing in the genome measures, or provides, that heterogeneity.

## The transfer: `mesh-dispatch --plasticity`

`mesh-dispatch` **is** the mesh's pheromone — it deposits routing (an open board `[task]` pushed into
a worker pane) and windows follow it. Its `--reliance` audit (added 2026-08-19 from Oberman
arXiv:2608.14795) already computes, per window, exactly the trace-sensitivity this paper's mechanism
is about:

> `eps(W) = advised closures / slugged closures`

and judges each window **alone** (RELIANT / MIXED / AUTONOMOUS, plus a cultivation trend). It has
never asked the collective question: **does the eps distribution contain a genuine trace-blind
minority, and does that minority carry enough throughput to seed a new trail?** A mesh where every
window sits mid-band looks fine window-by-window and, by this paper, has no plasticity at all.

The new mode reuses `--reliance`'s parsing (no new log format, no new sensor) and adds the collective
layer. Three things it refuses to do, each of which is a leg in `--test`:

1. **It does not count windows, it weights by slugged closures.** A blind minority carrying 2% of the
   work cannot switch the colony. Five idle blind windows beside one busy reliant one is a window
   count of 83% and a throughput share of 23%, and only the second is the quantity the mechanism needs.
2. **It does not read `unadvised` windows as blind.** eps=0 from a channel that never arrived is
   *absence*, not insensitivity — `--reliance`'s own distinction, and load-bearing here: folding it in
   mints a plasticity reserve out of a dead channel leg.
3. **It does not grade the share.** The paper reports no fraction, so no threshold is invented. What
   is judged is the *structure*; the share is printed as a number.

Heterogeneity is **tested, not eyeballed**: with small per-window n, one common reliance rate produces
eps scatter that looks like a blind minority. The Pearson dispersion of the per-window advised counts
is compared against a **seeded homogeneous-rate null** — every scored window redrawn `Binomial(n_w, p̄)`
at its **own** n_w — so the band widens exactly where the counts are thin. p̄ is fitted from the same
data, which makes the test conservative.

Verdicts: `BLIND-MINORITY` · `BLIND-MAJORITY` (the channel is not steering the mesh) ·
`HETEROGENEOUS-NO-BLIND` · `HOMOGENEOUS` (the failure mode this paper names — no committed blind
agents whatever the mean exploration looks like) · `UNDER-DISPERSED` (windows track one common rate
*more* closely than chance — a shared driver, not independent agents) · `INSUFFICIENT`.

## Live reading (2026-08-19, this node)

```
window      slugged  advised    eps  role
adint             7        0   0.00  TRACE-BLIND (eps<0.30)
genome           97       44   0.45  trail-following
health           12        1   0.08  TRACE-BLIND (eps<0.30)
senses           63       28   0.44  trail-following
tg               15        3   0.20  TRACE-BLIND (eps<0.30)

verdict: BLIND-MINORITY
  dispersion  = 13.91  (seeded homogeneous-rate null band [1.15,10.81] med=4.40, 2000 draws)
  population  = 194 slugged closures across 5 scored windows, p̄=0.392 advised
  blind share = 17.5% of slugged throughput carried by eps<0.30 windows (adint:7, health:12, tg:15)
```

So the eps spread is **real** — 13.91 sits above the 95th percentile of what one common rate produces
at these counts, so the low-eps windows are not small-n noise — and the mesh does carry a committed
trace-blind minority holding 17.5% of slugged throughput. By this paper that is the configuration
that can still switch when the board's trail goes stale. The share is reported, not graded: the paper
gives no fraction, and inventing one here would be the threshold the corpus keeps catching.

Bounds carried honestly: eps is bound by the **board's** sliding window (3.3d) even though
dispatch.log reaches 26.1d, and both spans are printed. Five windows (`job`, `pub`, `vpn`, `wake`,
`witness`) sit below the 6-slugged-closure floor and are excluded rather than scored on 4-5 samples.

## Gates (7 legs in `mesh-dispatch --test`, 223 assertions total, all green)

The load-bearing pair: **one eps pattern (1/6, 2/6, 3/6, 3/6, 4/6, 5/6 over six windows) built at two
scales.** The eps values are identical at both scales and so is the blind share (16.7%), so any
verdict read off the eps numbers must return the same answer twice. It does not: at n=6 per window the
scatter reads `HOMOGENEOUS` (dispersion 6.67 inside band [2.00, 12.00]); at n=24 the same pattern
reads `BLIND-MINORITY` (26.67 against [1.67, 12.50]). A third leg asserts the two shares are equal, so
the pair cannot pass for the wrong reason.

That pair straddles any fixed cut between 6.67 and 26.67, so on its own it cannot separate a simulated
null from a hardcoded threshold. The leg that can: the null's width is a function of **how many
windows** are compared, so the same per-window counts and the same p̄ must give a wider band at ten
windows than at three. A constant cannot track that, whatever value it is set to.

Remaining legs: throughput-weighted share (23.1%, not the 83.3% a head count gives) · `unadvised`
listed, and out of both the blind set and the population denominator (72 = 3×24, not 80) ·
`INSUFFICIENT` naming the window count on a 2-window fixture · exit 2 with no dispatch.log · read-only
(the sandbox MESH is byte-identical after two runs, asserted on this mode's own code path).

Mutants run from a scratch copy, all five caught: P1 null → fixed threshold · P2 share by window count
· P3 `unadvised` folded into scored · P4 window floor removed · P5 dispersion computed on unweighted
eps instead of counts.

## Not wired, and what it would take

`--plasticity` is read-only: it dispatches nothing, writes nothing, posts nothing. The paper's
*intervention* — designating a fraction of dispatch passes as fully trail-blind rather than adding
homogeneous noise to every pass — is deliberately **not** built. That would change live work
allocation, and the honest order is to measure the reserve first and see whether it moves before
touching the picker. The measurement now exists and has a null behind it.
