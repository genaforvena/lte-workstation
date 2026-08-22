# FEP / active inference — LIVE literature review, 2026-08-22

## The Markov blanket critique's live 2026 answer is the STABLE BLANKET — a strict SUBSET of the Markov blanket, defined by what survives INTERVENTION. Our one data-mining organ selects the whole Markov blanket, pooled, and both findings it is emitting right now fail the invariance test.

**Lane:** free energy principle & active inference (Friston), angle = **a known CRITIQUE of the
area** (the Markov blanket) · **Window:** genome · **Landed:** `scripts/mesh-correlate --stable` +
a seed gate that changes what the tool GENERALIZES, **uncommitted in the tree, not deployed**.

---

## 1. How the live surface was swept

Live, this session, not from a fixed list:

1. **arXiv API, `all:"Markov blanket"` and `all:"active inference"`, newest-first, 30 each**
   (fetched 2026-08-22). The active-inference window since our 08-18 sweep holds `2608.17167` EFE as
   an information constraint on the Bethe Lagrangian, `2608.14165` integrated information in AIF,
   `2608.09512` renormalising generative models, `2608.04232` interoceptive attention as homeostatic
   prioritization, `2608.02440` intention inference under execution noise. All five sit inside
   territory the corpus already holds (`fep-interoceptive-precision-allocation-…-2026-08-15`,
   `second-order-cyb-non-trivial-informational-closure-precision-2026-08-17`,
   `efe-novelty-vs-salience-parameter-uncertainty-2026-07-27`) — checked against the corpus, not
   from memory.
2. **The blanket branch specifically**, because the task asked for a CRITIQUE angle and the Markov
   blanket is where this area has been attacked hardest. Web search + arXiv, then the papers.

Two 2026 items were read and DISCARDED, with the reason:

- **Nuijten, Lukashchuk, van de Laar & de Vries, "What Type of Inference is Active Inference?",
  arXiv:2606.04935** (3 Jun 2026, rev. 7 Jul) — proves EFE-based planning needs an epistemic
  correction *plus* a planning correction. A genuine clarification, but it is a repair of the EFE
  derivation, not a failure mode we can act on; our EFE lane is already at
  `fep-convex-mdp-occupancy-marginal-mirror-descent-sound-reflex-2026-08-20`.
- **Beck & Ramstead, "Dynamic Markov Blanket Detection for Macroscopic Physics Discovery",
  arXiv:2502.21217** (28 Feb 2025) — variational Bayesian EM that *detects* blankets instead of
  assuming them, with **role labels that move over time** ("because these labels are dynamic or
  evolve over time, the algorithm is capable of identifying complex objects that travel through
  fixed media or exchange matter with their environment"). Beautiful, and the right shape for a
  mesh whose uplink dongle keeps switching between *blanket* (a channel reporting the world) and
  *internal* (the thing that is broken). Discarded **for now** on cost, not on merit: it is a
  variational EM over microscopic dynamics, and we have 17 categorical sense columns at a 10-minute
  cadence. Named here so the next sweep does not re-discover it.

---

## 2. The critique, and why the obvious reply was already refused

The Markov blanket has been attacked from two directions and both land here:

- **Bruineberg, Dołęga, Dewhurst & Baltieri, "The Emperor's New Markov Blankets", Behavioral and
  Brain Sciences 45:e183 (2022)** — a conditional-independence structure found *in a model* (a
  **Pearl blanket**) gets read as a *real boundary of the system* (a **Friston blanket**).
- **Aguilera, Millidge, Tschantz & Buckley, "How particular is the physics of the free energy
  principle?", Physics of Life Reviews 40:24–50 (2022), arXiv:2105.11203** — read in full. The
  blanket condition and the restrictions on solenoidal flow "are only valid for a very narrow space
  of parameters", requiring "an absence of perception-action asymmetries that is highly unusual for
  living systems interacting with an environment". Sparse coupling does **not** deliver conditional
  independence.

The mesh already knows this critique. `scripts/mesh-perimeter:60–95` carries a standing inoculation
comment citing Bruineberg verbatim, and it ends `# HELD (behavioral): nothing to change in the fuse`.
And the obvious reply was **considered and refused** on
`docs/reviews/fep-active-inference-epistemic-value-vs-output-diversity-forage-2026-07-30.md:71`:

> "the Markov-blanket misuse critique; a strong *critique* but a thin *reflex* (a boundary-verification
> audit `I(internal;external|blanket)≈0`, not a behavior change)"

That refusal was right, and it is the bar this landing had to clear. **A screening audit is a
measurement.** What follows is not that audit.

## 3. The mechanism we do NOT embody

> **Hanqing Xiang, "Stable Blanket with Hidden Variables and Cycles", arXiv:2605.01856 (3 May 2026).**
> Read from the HTML, not the abstract.

Stabilized regression asks for "a set of predictors whose conditional relationship with a response
variable remains invariant across different environments". Its Setting 2.1:

> the stable blanket of Y is the smallest set S ⊆ N^−int such that Xʲ ⊥⊥_d Y | X^S, ∀ j ∈ N^−int \ S

Three load-bearing results:

1. **The stable blanket is a strict SUBSET of the Markov blanket.** Their worked Fig. 1:
   MB(Y) = {X¹,X²,X³,X⁴,X⁵,X⁶}, SB(Y) = {X¹,X²,X⁵,X⁶}.
2. **They coincide only when there are no intervened sub-districts** (Thm 3.16, cond. 1). An agent
   that *acts* is exactly the case where they come apart — which is the FEP's own agent.
3. **Hidden variables and CYCLES move both sets:** they "can change both the Markov blanket and the
   set of predictors that remain stable under interventions", and under feedback "variables that are
   not locally adjacent to the response may still carry information about it".

So the honest predictor set is not the one that fits best. It is the one that survives intervention.
**That is a rule about which findings may be GENERALIZED — a behavior change, not a measurement.**
It is the answer to the 07-30 refusal, and it is a different object from the audit that was refused.

## 4. Why it binds on `scripts/mesh-correlate` specifically

`mesh-correlate` is the mesh's predictor-selection surface: it mines `~/.mesh/sensor-tape.tsv` for
cross-stream structure, emits one finding to `ideas-queue`, and writes the pair to
`~/.mesh/.correlation-seeds`, which **mesh-ideate consumes as established structure** to fuse new
CONNECTION ideas from (`scripts/mesh-ideate:35-38`). Its own header records what generalizing an
unearned pair cost once: `home_state↔desk`, raw lift 1.01, laundered into **4 mind-dispatches** on
2026-06-21.

Every existing guard is **pooled over the whole window** — the permutation null, the Bonferroni
family, the density floor, the hour-matched shadow, the occasion gate, the agency gain, the
exogeneity check. Not one asks whether the relation holds in *every* environment or in only one.
And the mesh is the worst case Xiang describes, on both counts:

- **CYCLES** — our reflexes act on what they measure. `mesh-exit-node-lan-heal` rewrites the FIB that
  `mesh-card` measures; every healer is a feedback edge. The mesh intervenes on itself all day.
- **HIDDEN VARIABLES** — 17 sense columns are not the node's state. A dongle wedge, a swallowed LAN,
  a 9-hour power-off are all unlogged in the tape and all move the marginals.

The mesh already wrote the consequence on the board hours before this landed (health@,
2026-08-22T12:00:45Z): a hand power-off split the tape and *"THIS EXPLAINS ALMOST EVERY OTHER DELTA
BELOW — read them as reboot consequences, not as things that got better … that ratio is downtime,
NOT an improving RTL8822BU."* A pooled miner reading across that seam is doing exactly the thing
that check warned a human against.

**Nearest existing neighbour, and why it is not this.** The REGIME GATE (`REGIME_COVER`) re-measures
a finding inside *one token's own era* because that token has no history over the rest of the window
— a coverage repair on a single axis. This is the opposite question and it is adversarial: given a
finding that already cleared every pooled gate, does it survive being asked separately in each
environment?

## 5. What landed

`scripts/mesh-correlate` (+283/−11), **uncommitted, not deployed**:

- **The environment axis is read from the tape itself**, so it plants on any node with no
  node-specific tool: an environment is a maximal run of rows with no **outage-sized hole**, the hole
  defined against the tape's *own* median cadence (self-calibrating — the corpus-rank rule in
  CLAUDE.md). A hole in the sensor tape IS a node outage. Live: median cadence 10.0 min, threshold
  60 min, **21 environments over a 926 h / 3358-row tape**, 14 of them ≥ 40 rows. The segmentation is
  robust to the multiplier: 21 environments at 3× and 6×, 19 at 12×, 18 at 24× — and **14
  environments of ≥ 40 rows at all four**, so the partition the verdict actually rests on does not
  move with the knob. The largest holes are real and named:
  66.5 h, 61.2 h, 43.3 h, and a **560-minute hole at 2026-08-22T00:30Z**, which is precisely the
  9 h 07 m hand power-off the health check reported.
- **Per-environment recomputation** in both lanes, using the *same* arithmetic (`episode_stats` was
  factored out so `episode_lift` and the per-environment call cannot drift).
- **Qualification is on the MARGINALS, not the co-occurrence** — the load-bearing choice. An
  environment qualifies when *both* tokens each occurred ≥ `STABLE_MIN_N` times in it, i.e. the pair
  had a fair chance there. Qualifying on `nxy` instead would let a relation disqualify every
  environment in which it simply did not happen, so "never occurred here" would read as "unmeasurable
  here" and **the gate could never fire on the case it exists for** — that is mutant M2 below.
- **The behavior change:** an `invariance=UNSTABLE` finding is still **emitted** to `ideas-queue` —
  it is a real observation and the mind is the value filter — but it may **not be generalized**: the
  seed is withheld, loudly, on stderr, carrying the verdict text that decided it.
- **`invariance=na` NEVER suppresses.** Fewer than 2 qualifying environments → `na`, and `na` is not
  stability. A node that has not rebooted inside the window can make no invariance claim and must not
  behave as if it had.
- **Disclosed limit, because it is real:** the segmentation is outage-defined, so for a pair whose
  senses are themselves outage-coupled (anything on the `wifi` axis here) the environment label is
  not exogenous to the pair. A second node-specific axis (journalctl boot ids) would cross-check it
  and is deliberately NOT wired — it would make the gate node-bound for a partition the tape already
  carries.

## 6. The live artifact

**Both findings `mesh-correlate` is emitting today are UNSTABLE.** Run
`mesh-correlate --stable`; measured 2026-08-22T12:44Z on the live tape:

```
LIFT  desk=AWAY <-> psi=BUSY        UNSTABLE — clears the 1.8 floor in 1 of 3 environments:
        env17 nxy=5/24x13 of 166  lift=2.66
        env18 nxy=0/30x5  of 162  lift=0.00
        env20 nxy=23/43x36 of 87  lift=1.29
LIFT  psi=BUSY <-> presence=NONE    UNSTABLE — clears the 1.8 floor in 0 of 2 environments:
        env18 nxy=1/7x8  of 58    lift=1.04
        env20 nxy=9/37x13 of 83   lift=1.55
```

Read the first one. Its published lift is 1.95 (already gate-corrected down from a confounded 4.0),
and 1.95-vs-1.80 "is the whole margin this finding has" in its own words. Per environment: in **env18
the two tokens were both amply present — `desk=AWAY` 30 times, `psi=BUSY` 5 times — and never once
co-occurred**; in env20, which carries 23 of the 30 co-occurrences, the lift is **1.29, below the
floor**; only env17 clears it. The pooled number is built by mixing environments with different base
rates. It is in the Markov blanket and not in the stable blanket, exactly as Xiang's Fig. 1 says.

The second is starker: it clears the floor in **zero** of its two qualifying environments.

Both are still emitted as hypotheses. Neither now seeds `mesh-ideate`.

Numbers are a MOMENT, not a constant — the tape slides and these re-derive. The **CLAIM** is the
gate ("both currently-emitted findings are environment-specific"), re-derivable with
`mesh-correlate --stable`; never quote the figures back without re-running it.

## 7. Gates driven RED then GREEN

`mesh-correlate --test` is green, with three new arms over **one tape shape** (40 rows, a 57 h
outage-sized hole, then 8 rows) so the only thing that varies is the thing under test:

| arm | env2 | verdict | queue | seed |
|---|---|---|---|---|
| GREEN | keeps the link | `STABLE` (2/2: env1 5.00, env2 2.00) | emitted | **written** |
| RED | decouples (both tokens present, never together) | `UNSTABLE` (1/2: env1 5.00, env2 0.00) | emitted | **withheld** |
| OPEN | one environment only | `na` | emitted | **written** |

The two lift arms are **mutual falsifiers**: a hard-wired verdict in either direction fails one of
them. Three mutants, run from scratch copies (never the tree), each RED with a distinct message:

- **M1** seed-gate case never matches → `UNSTABLE finding was seeded anyway — the gate is not load-bearing`
- **M2** qualify environments on `nxy` instead of the marginals → `a link present in only ONE environment did not read UNSTABLE — the gate cannot fire`
- **M3** `na` treated as a failure → `invariance=na SUPPRESSED a seed — na must fail OPEN`

## 8. Knobs

`CORRELATE_STABLE_GATE` (1) · `CORRELATE_STABLE_GAP_MULT` (6 × median cadence opens an environment) ·
`CORRELATE_STABLE_MIN_N` (4 — LIFT per-environment marginal episode floor) ·
`CORRELATE_STABLE_MIN_SAMPLES` (20 — PRED per-environment sample floor). The two live verdicts above
are invariant across `STABLE_MIN_N` ∈ [2,6] as measured today.
