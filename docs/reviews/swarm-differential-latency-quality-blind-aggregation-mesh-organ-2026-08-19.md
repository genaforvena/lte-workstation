# Live-literature review — swarm intelligence / stigmergy: **DIFFERENTIAL LATENCY** — the quality signal
# is carried by *when an agent returns to the pool*, never by anything it publishes (`scripts/mesh-organ`)

Date: 2026-08-19 · lane: genome (idea-queue LITERATURE task) · status: **proposal, uncommitted, nothing
edited** · angle: an operational mechanism, not philosophy

---

## Where the swarm lane has already been (so this lands somewhere new)

`docs/reviews/` carries **fifteen** prior swarm/stigmergy landings. Between them they model the *deposit*
(pheromone-entropy foraging evenness, inverse-stigmergy trace design, sematectonic vs sign-based), the
*decay* (density-adaptive evaporation, no-entry / negative pheromone), the *aggregation threshold*
(tunable quorum speed↔accuracy, response-threshold division of labour, cross-inhibition), the *field*
(collective-gradient margin, fundamental-diagram retrograde capacity, interaction-rate closed loop), and
the *pathologies* (ant mill, asocial-bias zealot, structural bias in an uninformative picker).

Every one of them makes an agent **publish or read a value**: a deposit, a threshold, a count, a margin.
The mechanism below is the one that does not. That is why it is new here.

## The mechanism: majority rule with **differential latency**

**Primary source.** Montes de Oca, Ferrante, Scheidler, Pinciroli, Birattari & Dorigo, *"Majority-rule
opinion dynamics with differential latency: a mechanism for self-organized collective decision-making"*,
**Swarm Intelligence 5:305–327 (2011)** — <https://link.springer.com/article/10.1007/s11721-011-0062-z>.

**Read in full (open PDF, IRIDIA):** Valentini, Birattari & Dorigo, *"Majority Rule with Differential
Latency: An Absorbing Markov Chain to Model Consensus"*, Proc. European Conference on Complex Systems
2012, Springer Proceedings in Complexity, ch. 79, pp. 651–656 (2013) —
<https://iridia.ulb.ac.be/~mbiro/paperi/ValBirDor2012eccs.pdf>. This is the paper I actually read; the
model statement and the finite-size result below are quoted from it.

Lineage the paper itself names: Galam's majority-rule model → Krapivsky & Redner's analytical study →
**Lambiotte et al.'s latency** (an agent that switches opinion becomes *latent* for a stochastic period)
→ Montes de Oca et al.'s **differential** latency (the latency period's duration depends on *which*
opinion was adopted). Still live: the same family is being re-derived for LLM agent swarms in 2025–26
(SwarmSys, arXiv 2510.10047, "pheromone-like traces encoding contextual utility"; SwarmHarness,
arXiv 2605.28764, "credit and trust scores as digital pheromones").

### The exact rule (Valentini et al. §79.1, verbatim structure)

M robots, each holding one of two opinions A/B for two actions with **the same outcome and different
execution times**. `k` latent teams, exponential latency, expected latency **1 for A and 1/λ for B**
with `0 ⩽ λ ⩽ 1`. Each step:

1. a latent team finishes its latency period and becomes non-latent;
2. a new team of **3** is randomly formed *out of the non-latent robots only*;
3. the team applies the **majority rule**, adopts that opinion, and **turns latent** for the period
   belonging to the opinion it just adopted.

That is the whole mechanism. Note what is absent: **no robot measures an execution time, no robot
compares the two options, and nothing is published.**

### Why it works — and why it is a different shape from everything we already have

Majority rule on its own is **quality-blind**: it is a pure voter model with no preference between A and
B. The differential latency is the *only* asymmetry, and it is not a signal at all — it is an
**availability bias**. Holders of the shorter-latency opinion come back to the non-latent pool sooner, so
they are over-represented among team-formers, so they win more majorities, so more agents adopt the short
option. The swarm converges on the shorter execution time with **no explicit knowledge of the
difference**.

> **The one-line import: you can make any quality-blind aggregation rule quality-sensitive without adding
> a metric, a benchmark, a threshold or a comparator — by making the time an agent is *unavailable* after
> acting equal to what the action actually cost it.**

The mesh has repeatedly paid for the alternative. `CLAUDE.local.md`'s STT pin is a hand-run benchmark
that was wrong for weeks (the "0.59s / 25x" broken timer, the RTF-on-a-3s-clip extrapolation that was 28x
off). Our own doctrine already names the disease — *"a median pinned as a constant ROTS"*, *"rank against
the live corpus: self-calibrating, cannot saturate"*. Differential latency is that principle with the
measurement **deleted rather than automated**: the pool's composition is the measurement.

### The quantitative results, and the caveat that matters most to us

Valentini et al. derive the **exit probability** E(sᵢ) — the chance of reaching consensus on the
short-latency opinion — from the absorbing chain (`N = (I−Q)⁻¹`, absorption matrix `NR`), validated
against 1000 Monte Carlo runs per configuration at (M=20,k=6,λ=0.5), (M=50,k=16,λ∈{1,0.5,0.25}),
(M=101,k=33,λ=0.5). Two findings:

- the larger B's expected latency `1/λ`, the **smaller the initial support A needs** for E > 0.5 — the
  latency ratio moves the critical density away from ½;
- **as M grows, E approaches a step function around the critical density.** Large swarm ⇒ effectively
  deterministic. **Small swarm ⇒ stochastic, and it can absorb on the WRONG (long-latency) option.**

That second point is the reason the paper exists at all: they state plainly that the earlier fluid-flow
and Fokker–Planck approximations *"provide reliable predictions only when the number of robots is
relatively large — e.g., thousands"*, while *"in a finite population, random fluctuations may drive the
system to converge to the long path, even when the fluid-flow model predicts that it should converge to
the short one."*

**Our pools are 2–4 nodes.** We sit at the far bad end of exactly the regime the paper was written to
warn about. So the transfer must **not** take the absorbing/consensus form — an absorbing state that
locks the mesh onto the slow node is a permanent fault with a green liveness face. It must take the
non-absorbing **pool-availability** form, where a fast offerer's advantage is re-earned on every call and
nothing is ever locked in.

---

## Concrete application — `scripts/mesh-organ`, the `cap-scope=fungible` tie-break

### The precondition, and why only this file satisfies it

The mechanism has one hard precondition: **the options must have the same outcome.** Shortest-time-wins
is a correct preference *only* under that assumption. `mesh-organ` is the **only** place in the genome
where that assumption is a declared, checked property rather than a hope: `cap_scope` splits every
capability into `bound` (a link-flap on phaedra is a different fact from one on mesh-home — the router
**refuses** and makes you name the instance) and `fungible` (any offerer will do).

### The quality-blind rule that is there today

`scripts/mesh-organ:369` — *"fungible + >1 offerer: first-offered wins"*; `:574–575` say it outright:

```
decisive: where(cap-scope=fungible) — then FIRST-OFFERED wins; runner(s)-up: ...
NOTE: first-offered is the whole tie-break. The router does NOT retry the runners-up if the
      winner's ssh fails — the header's word 'failover' overstates it.
```

First-offered is **manifest order** — an arbitrary artefact of how `mesh-organs --json` happens to list
nodes. It is Galam's majority rule with the quality knob missing: a rule with no preference at all
between two options the router has already certified as interchangeable. Meanwhile the router **already
writes the missing quantity and throws it away**: every route appends `rc=<n> secs=<n>` to
`~/.mesh/organ-routes.log` (`:113`, `ROUTE_LOG`) and nothing ever reads `secs` back into the choice.

### The proposal

Replace *first-offered* with a **latent-pool draw**, the non-absorbing form:

- after a route to offerer *X* returns, *X* is **latent for the `secs` that route actually took**
  (read from `organ-routes.log`, wall-clock, no probe, no benchmark, no extra traffic);
- a fungible pick draws uniformly from the offerers that are **not currently latent**; if all are latent,
  fall through to today's first-offered (never block, never add a delay to the caller);
- nothing is remembered beyond the last route per offerer — **no absorbing state, no accumulator, no
  consensus**. A node that gets fast again is back in the pool on its next call.

Net effect: a saturated or half-wedged node serves proportionally fewer fungible routes without anyone
declaring it unhealthy, and recovers with zero hysteresis. This is `--qualify`'s residual (*"does the
residual concentrate on ONE offerer the framework calls interchangeable?"*) turned from a **read-only
diagnostic into the routing rule itself** — the file already computes the concentration and already
refuses to act on it.

### The trap this mesh will hit, stated before it does: **a fast failure beats a slow success**

Differential latency ranks by *elapsed time*, and the fastest possible outcome is an instant error. A
node whose camera is wedged and returns `rc=1` in 0.2s would be latent almost never and would win **every**
draw — the mechanism exactly inverted, and wearing a "fast, healthy router" face while doing it. This is
our own [[a-fallback-whose-default-is-another-lanes-success]] and [[a-timeout-is-not-a-refusal]] in a new
costume. So the latency must be taken from **`rc=0` routes only**, and a failure must impose an explicit
latency penalty (the cap's timeout, not its elapsed time) rather than the 0.2s it really took. The paper
does not contain this hazard because its two paths always succeed; it arrives with the transfer.

### The gate, and the mutants that must be SEEN RED

Not "the pick changed" — that is source text, not behaviour ([[a-gate-that-greps-its-own-source]]):

1. drive a fungible cap with 2 stub offerers, one sleeping 2s and one 0.05s, over ~20 routes; assert the
   fast offerer takes a **strict majority**. Mutant: revert to first-offered ⇒ the split must go ~50/50
   or to manifest order, i.e. **red**.
2. make the fast offerer exit `rc=1` in 0.01s and the slow one exit `rc=0` in 2s. Assert the **slow,
   successful** offerer still takes the majority. Mutant: count failures' `secs` ⇒ the wedged offerer
   sweeps the draw, **red**. This is the gate that matters; without it the change is a regression.
3. all offerers latent ⇒ assert the caller is served immediately by first-offered and **never delayed**.
   Mutant: block until the pool frees ⇒ a fungible route acquires an unbounded stall, **red**.

### Honest statement of what this does NOT fix today (measured, not assumed)

Measured on the live fleet at 2026-08-19T04:01Z: every capability with more than one offerer
(`irq`, `link-flap`, `dlna-tv`, `tv`, `shadowsocks` — all mesh-home + phaedra) resolves
`cap-scope=**bound**`, so the router refuses and asks for `<name>@<node>`. `mesh-organ --why dlna-tv`
and `--why shadowsocks` both print *"the router REFUSES (exit 1) and makes you name the instance"*.
`~/.mesh/organ-routes.log` is **27 lines**, and every `decisive=where-fungible+first-offered` row in it
(`cap=whycap offerers=3`) is a `--test` row.

So: **the target lane is real in code and reachable by the suite, but no production capability currently
exercises it.** That cuts both ways and both must be said. It is not a live pain being fixed — do not
sell it as one. It is also why the change is cheap and safe to land: on day one it alters the behaviour
of exactly zero live routes, and it is in place before the first genuinely fungible multi-offerer
capability (a second camera, a second speaker, a second relay pool) makes manifest order load-bearing.

## One discard, for the boundary

**STT model selection (`mesh-whisper-run` `_pick_model`, gigaam vs whisper) — discarded**, and it is the
clearest illustration of the precondition: the options do **not** have the same outcome. Measured in
`CLAUDE.local.md`: base is 4.4x faster than gigaam and 2.6x less accurate (WER 0.812 vs 0.312). Applying
differential latency there would drive the room's ear to the *worst* transcriber at maximum speed, with
every liveness frame green. Shortest-time-wins is a preference only where "same outcome" is declared and
true — which is precisely why the landing above is `mesh-organ` and nowhere else.

---

## Sources

- [Majority-rule opinion dynamics with differential latency — Swarm Intelligence 5:305–327 (2011)](https://link.springer.com/article/10.1007/s11721-011-0062-z)
- [Majority Rule with Differential Latency: An Absorbing Markov Chain to Model Consensus — ECCS 2012 / Springer 2013 (open PDF, read in full)](https://iridia.ulb.ac.be/~mbiro/paperi/ValBirDor2012eccs.pdf)
- [Automatic design of stigmergy-based behaviours for robot swarms — Communications Engineering 3:30 (2024)](https://www.nature.com/articles/s44172-024-00175-7)
- [SwarmSys: Decentralized Swarm-Inspired Agents for Scalable and Adaptive Reasoning — arXiv 2510.10047 (2025)](https://arxiv.org/html/2510.10047v1)
- [SwarmHarness: Skill-Based Task Routing via Decentralized Incentive-Aligned AI Agent Networks — arXiv 2605.28764 (2026)](https://arxiv.org/html/2605.28764)
- [The Best-of-n Problem in Robot Swarms: Formalization, State of the Art, and Novel Perspectives — Front. Robot. AI (2017)](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2017.00009/full)
- [A Simple Threshold Rule Is Sufficient to Explain Sophisticated Collective Decision-Making — PMC3101226](https://pmc.ncbi.nlm.nih.gov/articles/PMC3101226/)
