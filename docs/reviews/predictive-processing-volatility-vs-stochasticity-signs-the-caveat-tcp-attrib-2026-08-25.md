# Predictive processing / the Bayesian brain — an unsigned caveat is a coin flip on the sign of the correction

**Date:** 2026-08-25
**Lane:** LITERATURE (live review)
**Area:** predictive processing & the Bayesian brain, angle = an OPERATIONAL mechanism we could implement
**Arm:** treated (assigned)
**Assigned organ:** `scripts/mesh-tcp-attrib` — drawn uniformly by coin at p=0.20 from the 566
never-reviewed tools in the lane's own denominator. Not retargeted.
**Verdict:** APPLIES. Landed on the assigned organ.

---

## 1. The concept, and where I found it

**Piray, "Not all uncertainty is alike: volatility, stochasticity, and exploration", arXiv:2605.19215,
submitted 2026-05-19.** Found by search, read at `https://arxiv.org/abs/2605.19215`.

The core claim, quoted:

> "Both increase posterior uncertainty, yet we show they drive optimal exploration in opposite
> directions: volatility enhances it, stochasticity suppresses it."

and the failure mode, which is the part that bites:

> "pathological noise inference produces reversed rather than merely impaired exploration"

**Reversed, not degraded.** That is the whole content. An agent that cannot tell *the world is
changing* from *the world is noisy* does not act a bit worse — it acts in the opposite direction to
the correct one. The paper derives a closed-form exploration bonus (CAUSE) over Gaussian state-space
bandits that is *cause-aware*: it conditions on which noise source it thinks it is in.

Ancestry, for the honesty of the dating: the two-source *estimation* problem is Piray & Daw, Nature
Communications 2021, "A model for learning based on the joint estimation of stochasticity and
volatility" (`s41467-021-26731-9`), with a 2024 human follow-up. What is 2026 and new is the
**asymmetry of ACTION** and the proof that mis-inference flips the sign.

## 2. What we already embody, and what we did not

The *estimation* half is landed and I did not re-derive it. `scripts/mesh-precision` carries a
`stovol` axis — a method-of-moments decomposition of observed variance into stochasticity and
volatility, publishing `VOLATILE|STOCHASTIC|MIXED|STOVOL_NA`, `vol_frac`, a measured n-floor of 20 —
filed as `~/.mesh/knowledge/review-predictive-processing-stovol-2026-08-18.md`. It is report-only by
design: it never moves a weight.

So the mesh can *measure* the distinction in one tool and **acts on it nowhere**. Two further places
name the mechanism and explicitly HOLD it (`mesh-presence:303-345`, `mesh-novelty:1008-1045`), and
`docs/reviews/predictive-processing-model-recovery-identifiability-2026-08-04.md:145` states flatly
that "the mesh runs no HGF hierarchy". Behrens and Nassar return zero hits mesh-wide.

**The unoccupied ground is the 2026 claim: not measuring the two apart, but the fact that they demand
OPPOSITE corrections, so a caveat that does not say which one you are in cannot be acted on.**

## 3. The defect in the assigned organ

`mesh-tcp-attrib` takes a paired sample of per-socket retransmit counters and names which flow is
lossy. It carries five properties built in, and property (3) is a caveat repeated in every surface it
renders:

> "THE READING IS A SAMPLE AT ITS WINDOW, NEVER A STATE ... the ratio is nonstationary over minutes
> at ANY window length"

That sentence is **unsigned**, and a consumer can only read it one way: distrust this, take a longer
one. But the tool's only knob is `--window N`, and the two uncertainties behind that caveat want
opposite moves:

| | what it is | correct move | what a wider window does |
|---|---|---|---|
| **stochasticity** | the counts are small; the ratio wobbles by sampling | **WIDER** window | buys resolution, costs nothing |
| **volatility** | the path's true loss rate is drifting | **NARROWER** window | averages *across* the change it should catch |

Same caveat, opposite corrections. Under Piray's result, guessing wrong does not weaken the
correction — it inverts it.

**And this pass can sign it, from counts the tool already reads.** The independent-draw dispersion of
the node-global ratio, `sigma = sqrt(p(1-p)/n)` over the window's own segment count, is the smallest
ratio difference these counts can separate from sampling. Movement inside it is sampling; movement
outside it is a candidate for real change.

### Measured, on the tool's own cited evidence

The header cites three readings as proof of nonstationarity. Tested against the floor:

| cited reading | floor arithmetic | verdict |
|---|---|---|
| 60s window read 4.32%, then 1.46%, 25 min apart | n=5356, p=1.456%, sigma=0.164pp; delta 2.864pp | **17.5 sigma** |
| 5s window read 0/579 while a 60s window read 1.46% | expected 8.43 events, observed 0 | **P = 2e-4** |

**Both of this header's own examples are volatility.** The move they call for is a NARROWER window —
and the caveat as written argues, to any ordinary reader, for a longer sample. The organ was
documenting the case for the reversed correction.

### The second defect, in the ranking

Rows are sorted by retransmit **COUNT** (`sort -k3 -nr`). So the top row is biased toward the
**busiest** flow, and on a node-wide loss condition the busiest flow ranks first whether or not
anything is wrong with it. `--who` hands that peer to `mesh-tcp-retrans` / `mesh-tcp-health` /
`mesh-stress` as a **subject**, with nothing said about whether its rate is distinguishable from the
node-wide rate. A node-wide fault is thereby readable as one peer's fault.

## 4. What was built

`scripts/mesh-tcp-attrib` gains property (6): **the caveat is signed by a published resolution
floor**, and every rate carries whether it is separated from the node-global rate.

- **`resolution:` line, in every text reading** — the node-global ratio, its independent-draw floor at
  one sigma, and both corrections named with their directions.
- **Per-row `vs-node`** — `hi` / `lo` when the row's rate is separated from the node-global rate by
  more than the bar times its own floor; `unresolved` when these counts cannot tell it apart (the
  printed ratio is then a count quotient, not a measured rate); `na` when untestable.
- **`--who` says it in words**, not as a token: an unresolved top flow renders
  `LARGEST CONTRIBUTOR, NOT A SEPARATED SUBJECT ... this names volume, not a flow fault`. Every
  existing caller already parses that line; a bare token would have been missed by all of them.
- Carried into `--json` (`vs_node`, `resolution_floor_pct`, `resolution_note`) and `--peer`.

### Three things the first cut got wrong, all found by running it LIVE rather than on the fixture

1. **The bar was flat at two sigma, but the table is a MAX over every surviving flow.** The largest of
   N standard normals grows like `sqrt(2 ln N)`; at the 111 flows this node actually holds that is
   **3.07**, not 2. Testing 111 candidates at a two-sigma bar buys about five spurious `hi` rows per
   pass, and the tool then ranks one of them first. The bar is now
   `zbar = max(2, sqrt(2 ln N))` and the reading publishes **both** the bar and the N it came from —
   a bar quoted without its N is not checkable by the reader it protects.
2. **VALIDITY.** The first live pass named a flow that sent **one** segment and retransmitted it —
   100.00%, rendered `hi`, off an expected count of 0.0074 events. The normal approximation to a
   binomial says nothing there. A row now renders `na` (untestable) unless it has at least 30
   segments **and** at least one expected retransmit under the node rate. These are two independent
   conditions and the review's fixtures separate them.
3. **The untestable message named a cause that was not the cause.** It read "no segment count to
   separate on" beside a flow carrying 232 segments; the real refusal was 0.4 expected events. It now
   carries the actual numbers: `UNTESTABLE, not a verdict: 232 segs, 0.42 retransmits expected`.

### The honest bound, stated in the reading itself

TCP loss is **bursty** — retransmits are not independent draws, so real sampling dispersion is
**larger** than this floor. The floor is therefore a **lower bound**, and the asymmetry is deliberate
and published: *inside* the floor is conclusive (unresolvable even under the most generous
assumption), *outside* it is only a **candidate** for real change (burst correlation can carry a flow
past an independent-draw bar without the rate having moved).

**Not a second copy of the decomposition.** `mesh-precision`'s stovol is the mesh's one vol-vs-noise
tract and needs a SERIES. `mesh-tcp-attrib` holds a single paired sample, so it publishes the one term
a single pass can honestly compute — the floor — and never a `vol_frac`. The header says so, and
points a reader wanting the decomposition at `mesh-precision`.

## 5. Gate

`--test` grows to six asserted properties. **29 mutants driven RED individually; control green.**

Both bars of the selection correction and both validity conditions needed fixtures that could
separate them, and each was green until its fixture existed:

- a **51-candidate** fixture whose probe sits deliberately *between* the flat bar (2.00) and the
  corrected one (2.80) at 2.26 sigma — so the leg gates the correction, not merely its presence;
- a **high-rate** fixture (20.00% node rate, a 10-segment flow expecting 2.00 events) that isolates
  the sample-size condition from the expected-count one;
- a **one-segment** flow reproducing the live pathology;
- an **idle** pass where the global counters are flat, asserting the floor renders `na` and never a
  fabricated `0.000%`, which would read as perfect resolution on a pass that measured nothing.

### A trap found here, worth its own memory

**Bash `printf` RECYCLES its format string when the arguments outnumber the conversions.** Deleting
the floor's `%s%%` from the reading did *not* remove `0.198` from the output — the format ran a second
time and the orphaned argument reappeared in another field's slot. A bare `*"0.198"*` assertion was
**green against a mutation that had actually deleted the floor**, and the same artifact made a
`--who` mutation look gated when it was not. Two fixes, both landed: assert the number **with its
label**, and **count the line** (`resolution:` exactly once, `--who` exactly one line) so a recycled
format is itself a red.

`mesh-precision`'s ownership of the decomposition, and the burstiness bound, are the two limits on
this landing. It measures a floor; it does not estimate volatility, and it should not.

## 6. Artifacts

- `scripts/mesh-tcp-attrib` — property (6), the floor, the selection-corrected bar, the two validity
  conditions, `vs-node` across all four surfaces, 6 asserted properties, 29 mutants seen red.
  Deployed byte-identical to `~/.local/bin/`. **Uncommitted — the steward lands from the tree.**
- This review.
