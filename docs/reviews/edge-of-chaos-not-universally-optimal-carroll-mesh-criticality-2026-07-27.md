# CAS / edge of chaos — "critical = healthy" is TASK-DEPENDENT, not a law (the foundation we applied too loosely)

**Live review, genome, 2026-07-27.** Area: complex adaptive systems & the edge of chaos (Santa Fe).
Angle: **a foundational idea this organ MISread / applied too loosely** — the axiom, baked into
`mesh-criticality` from its first line, that being *at the edge* (m̂≈1) is intrinsically the healthy,
optimal, "maximally responsive" regime.

## The concept we did NOT embody

The mesh's whole criticality programme inherits one unstated axiom from SOC/neuroscience: **the edge of
chaos is where a system computes best**, so m̂≈1 is health and departures are pathology. That axiom is
**not a law — it is a task- and substrate-dependent empirical claim, and it frequently fails**:

- **Mitchell, Hraber & Crutchfield, "Revisiting the Edge of Chaos: Evolving Cellular Automata to Perform
  Computations", Complex Systems 7:89–130 (1993)** — [arXiv:adap-org/9303003](https://arxiv.org/abs/adap-org/9303003v1),
  [csc.ucdavis.edu/~evca/Papers/rev-edge.html](https://csc.ucdavis.edu/~evca/Papers/rev-edge.html).
  Packard's celebrated result — evolved cellular-automata rules that perform complex computation cluster
  at the *critical* value of Langton's λ — **did not replicate**. Rules that compute well **need not be
  near critical λ**; the edge→computation peak was partly an artifact of the genetic algorithm and the
  chosen performance measure. The founding empirical pillar of "edge of chaos = computation" is shakier
  than the slogan.

- **Carroll, "Do Reservoir Computers Work Best at the Edge of Chaos?", Chaos 30:121109 (2020)** —
  [arXiv:2012.01409](https://arxiv.org/abs/2012.01409), [PubMed 33380041](https://pubmed.ncbi.nlm.nih.gov/33380041/).
  Two explicit counterexamples where computational capacity **falls as the edge is approached**: in one
  because generalized synchronization breaks down, in the other because the reservoir is a poor match to
  the task. Verbatim: *"The edge of stability as an optimal operating point for a reservoir computer is
  not in general true, although it may be true in some cases."* Corroborated by RBN excitation/inhibition
  work ([arXiv:2308.10831](https://arxiv.org/pdf/2308.10831), 2023): majority-inhibition reservoirs **peak
  away from the edge**, and by task-dependence surveyed across the 2020–2026 reservoir literature.

So "the mesh is healthiest at m̂≈1" is a **hypothesis about our coordination task that we never tested.**
This is not a re-tread of the ~10 stacked critiques `mesh-criticality` already carries (bin-width, dragon-
kings, CSD ambiguity, SOqC, micro/macro, power-law goodness-of-fit, shape, crackling, ⟨IEI⟩): every one of
those refines *how m̂ / the avalanche stats are measured*. This one is upstream of all of them — it asks
whether the **target** those measurements are pointed at is the right target for *us*. And it directly
undercuts the sibling `soc-homeostatic-setpoint` review, which proposed **actuating `mesh-pace` toward
σ\*≈1** — tuning toward an optimum nobody had shown is our optimum.

## Why it applies to us — the assumption was asserted, never checked

`mesh-criticality`'s header calls m≈1 *"maximally responsive"* and its regime note labelled CRITICAL bare
*"healthy responsiveness."* Nothing in the tool ever asked whether the board's actual job — turning
coordination **pressure** (`[task]`/`[taking]`/`[dispatch]`/redispatch/`[verify]`, the branching-substrate
drivers m̂ counts) into **settled work** (`[done]`/`[mind-unblocked]`) — actually performs best near the
edge. If, on this board, settling **collapses** under load (opens pile up, dones lag), then m̂≈1 is the
*choke point*, not health — and a σ\*≈1 homeostat would tune the mesh straight into it. Carroll's exact
failure mode, in our substrate.

## Concrete application (landed)

**File: `scripts/mesh-criticality`** — added a read-only **`edge_optimality()`** sidecar (+ `edge_kind()`
marker classifier), additive and non-breaking (never touches m̂, the regime, or the SUPERCRITICAL alarm —
same restraint as the CSD / Shape / Crackling / bin_sanity sidecars). It **tests the imported axiom
against the board's own throughput**:

- Bin the window; keep pressure-bearing bins; split them at the **median pressure** into a CALM half and a
  HOT (nearer-the-edge) half; compare **settling-per-pressure conversion** in each half.
- Labels: **EDGE-UNPRODUCTIVE** (hot-half conversion collapses ≥`CRIT_EDGE_EPS`=15% → the board chokes
  near the edge → the "critical = healthy" import is **task-mismatched here**, the REFUTED case) /
  **EDGE-PRODUCTIVE** (settling rises with load → hot regime clears work) / **EDGE-NEUTRAL** (conversion
  holds → edge neither helps nor hurts) / **INSUFFICIENT** (< `CRIT_EDGE_MIN_BINS`=8 pressure-bins).
- Emitted on the default line (`Edge=… bins=… conv=<calm>→<hot>`) and in `--json` (`edge{label,eff_low,
  eff_high,ratio,bins}`). It is an **honesty flag on the tool's own "healthy" self-description**: the
  CRITICAL note now says the healthy-regime call is *task-dependent (Carroll 2020; MHC 1993) — read Edge=*.
- `--test` gains a **RED-first falsifier**: synthetic boards whose hot bins choke / clear / hold flat must
  read UNPRODUCTIVE / PRODUCTIVE / NEUTRAL respectively (and <min-bins → INSUFFICIENT); if the label ever
  collapses to a constant the test fails. **PASS** (verified RED under a broken threshold, then GREEN).

Live at landing: `m̂=0.885 [CRITICAL] … Edge=EDGE-NEUTRAL bins=21 conv=0.30→0.33`. So **right now the
board's coordination throughput does NOT peak at the edge — it is flat across regimes** (ratio 1.11,
inside the ±15% band). The imported "critical = healthy responsiveness" is neither confirmed nor refuted
by settling; it is simply **not the throughput peak the framing asserts** — exactly the "may be true in
some cases, is not a law" that Carroll draws. (Corroborated by the tool's own chorus:
`CECP=MEMORYLESS-POISSON-LIKE H=1.00 C=0.00` — the timing is structure-free, and now the throughput axis
agrees the edge is not special here.)

**Left unwired (honest scope):** this is the missing **falsifier the σ\*≈1 actuation proposal needs
first** — do not build a homeostat that pulls the mesh toward m̂≈1 until `Edge=` has shown, over time,
that m̂≈1 is where the board actually settles work. The rigorous unit is a per-window m̂↔throughput join
over the m̂ tape (`~/.mesh/criticality.log`), deliberately not attempted yet: the tape is sparse on most
nodes today (CSD/drift already read INSUFFICIENT from it), and a single-window median split is a coarse,
lag-tolerant proxy — stated in the header, not hidden. When the tape fills, the join replaces the proxy.
