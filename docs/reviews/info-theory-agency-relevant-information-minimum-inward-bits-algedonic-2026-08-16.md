# Relevant information: bits are a cost, and the agent-defining quantity is a MINIMUM

**Live review** — information theory of agency (empowerment / predictive information), angle = a
foundational idea we applied too loosely. Landing site: `scripts/mesh-algedonic --agency-relevant`.
2026-08-16, genome. Uncommitted; steward lands.

## What we already embodied (checked first — this seam is near-saturated)

Open-loop and process empowerment, channel **capacity** via Blahut–Arimoto, multi-agent
interference-channel empowerment, discounted (EELMA) empowerment on the board, predictive
information, predictive information **rate**, Maximum Occupancy Principle, transfer entropy,
assistive empowerment. Plus two doc-only proposals: partial information decomposition, and
plasticity `I(O→A)`.

Nine built axes. **Every one of them is a maximum or a plug-in flow, and every one reads more bits
as better.** Not one computes a minimum. That is the gap.

## The concept

**Relevant information** — the minimum information an agent must process to get what it gets:

> "Relevant Information is defined as the minimum mutual information I(S;A) that an agent needs to
> process when selecting an action within a state to obtain an average utility equal to a given
> threshold (Ū)."
>
> min_{π(a|s)} I(S;A)  s.t.  E_p(s,a)[Q^π(s,a)] = Ū
> L^π(β) = I(S;A) + β(Ū − Σ_{s,a} π(a|s)p(s)Q^π(s,a)) + Σ_s λ_s(1 − Σ_a π(a|s))

**Source:** Archer K, Catenacci Volpi N, Bröker F & Polani D, *A space of goals: the cognitive
geometry of informationally bounded agents*, [arXiv:2111.03699](https://arxiv.org/abs/2111.03699)
(v2, Nov 2022), §S5.1, eqs (xvi)–(xvii) — read from the PDF. The concept is theirs' ref 46:
Polani, Nehaniv, Martinetz & Kim, *Relevant Information in Optimized Persistence vs. Progeny
Strategies*. The framing is **information parsimony**: an organism processes only enough sensor
information to perform at an adaptive level of utility — information is a *currency*, and acquiring
it costs.

**Live end of the thread:** Rosas FE, *Adaptive state-action abstractions via rate-distortion*,
[arXiv:2606.06123](https://arxiv.org/abs/2606.06123) (4 Jun 2026) — "near-optimal performance can be
achieved under substantial lossy compression of state **and** action information", i.e. the same
principle running as an active thread ten weeks ago, now as a resolution that adapts during learning
rather than a fixed budget.

## The misread

Two things flip at once, and we had neither:

1. **Direction of the optimization.** Empowerment is a max, RI is a min. `--agency-capacity` (landed
   2026-08-04) already fixed *flow vs capacity* — but both are maxima. The founding framing says the
   agent-characterising number is how *few* bits it can get away with.
2. **Direction of the channel.** Capacity and flow live on the outward channel A → Δpain. RI lives on
   the inward one, S → A: how much the mind must *look* to choose. The mesh's one inward proposal
   (`mesh-sound-reflex --plasticity`, doc-only) reads high `I(O→A)` as healthy — the same loose
   reading again, because **an inward flow without its minimum is not a verdict**. RI is that missing
   denominator.

## What `--agency-relevant` computes

Same intervals as `agency_info()`; state `S = band0(pain at interval start) ∈ {lo,mid,hi}` (the
closed-loop axis's own state), `A =` acted/not, utility `Q(s,a) = mean(−Δpain)` in that cell.

| | |
|---|---|
| `I_obs` | plug-in `I(S;A)` — what the observed policy spends looking |
| `Ū_obs` | the utility that policy achieves |
| `U₀` | `max_a Σ_s p(s)Q(s,a)` — the best **state-blind** policy |
| `RI` | `min I(S;A)` over policies achieving `Ū_obs`, by Blahut–Arimoto on the Lagrangian (`π(a|s) ∝ p(a)e^{βQ(s,a)}`), bisecting β for the smallest one reaching `Ū_obs`; exactly 0 when `Ū_obs ≤ U₀` |

Verdicts (report-only, never escalates, never touches the status line):

- **`RI_DECORATIVE`** — `RI = 0` while the spent bits clear their null: the mind conditions on the
  pain band and a *constant* action does as well. The bits bought nothing. This is the hollow-sense
  doctrine stated in information, and no other axis in the mesh can express it.
- **`RI_WASTEFUL`** — the gap `I_obs − RI` clears its null: same utility, less looking.
- **`RI_PARSIMONIOUS`** — spends about the minimum for what it gets.
- **`RI_NO_CHANNEL`** — the spent bits are themselves inside chance. **Parsimony is a virtue label and
  must never be the fall-through for a dead channel** — the same distinction `CAP_ABSENT` draws on the
  outward side, and the reason `quiet` is not `dead`. This case was mislabelled `RI_PARSIMONIOUS` in
  the first draft and the live tape landed in it.
- **`RI_NA_SUPPORT` / `RI_NA_THIN` / `RI_NA_NULL` / `RI_UNKNOWN`** — named n/a with the reason.

## The bias trap points the other way this time

`--agency-capacity` had to defuse a *maximum* of a noisily-estimated functional, biased **up**
(Jensen). RI is a *minimum* of one, biased **down** — and the verdict rides on the gap
`I_obs − RI` = (plug-in MI, biased up) − (minimum, biased down). The error compounds in one direction
and inflates `RI_WASTEFUL` from both ends. So the null runs the *whole* pipeline on each surrogate and
the verdict scores the gap against the surrogate gap, never either number alone.

**The null is a circular shift, not a shuffle** — both columns are strongly autocorrelated (the pain
band persists; board actions arrive in bursts) and a shuffle narrows the null anticonservatively
(the lesson already paid for in `mesh-cooscillate`). *Lead, not swept:* by the same argument the
capacity block's plain shuffle is questionable on this same tape. It is a different H₀ and its bands
are calibrated, so changing it here would silently move a landed verdict — named rather than left
unsaid.

## Gates, and the three things they caught in my own code

`--test` fixtures differ only in payoff structure and policy, never in n or action rate, so a label
change cannot be a sample-size artefact. Bugs the gates caught before shipping:

1. **`RI_PARSIMONIOUS` as the fall-through** handed a virtue label to a dead channel. → `RI_NO_CHANNEL`.
2. **Fixture step below the action lookback.** At 600s pain steps with a 1800s lookback, one action
   falls inside three intervals' lookback, so `action=1` is sticky: at a 0.85 act-rate the `(hi, no-act)`
   cell *never occurs*, `hi` is dropped by the floor, and the fixture silently degenerates to the two
   states with identical payoff. This is a property of the real reader too, not just the fixture.
3. **The payoff structure drives the walk**, so band occupancy and utilities are not independently
   choosable — the `pays` fixture drifted into `lo` and never revisited `hi`. A teleport back to a band
   base is worse: that interval carries a 0.6 delta whose utility swamps every cell mean. Fixed with an
   action-*independent* restoring force, which biases both cells of a state equally and leaves the
   contrast `Q(s,1)−Q(s,0)` untouched.

**Mutation-tested, and two of five did not bite — recorded, not quietly dropped.** Removing the
`RI_NO_CHANNEL` guard → red. Removing the Q-cell floor → red **only when mutated at both call sites**:
`keep_states()` carries its own copy of the threshold, so a one-site mutant survives (the
rule-asserted-at-one-call-site shape, live, in this file). Surviving: the exact `Ū_obs ≤ U₀ → RI = 0`
early return (the β sweep reaches ≈0 anyway on these fixtures), and the minimum-shift floor.

### A correction I had to make to my own doctrine paragraph

The first version of the null comment blamed short circular shifts for the fixtures reading
`RI_NO_CHANNEL`. That was a mechanism I had not isolated — the real cause was trap #2 above. Mutating
`minshift` to 1 settles it:

- on the **fixtures** it changes nothing; every gate stays green, so no gate here covers it;
- on the **live tape** it decides the verdict — state runs average 61.5 intervals and reach 443,
  `null95` moves 0.0891 → 0.0099, and the reading flips `RI_NO_CHANNEL` → `RI_DECORATIVE`.

The actual mechanism is narrower than "shifts too small": **a shift of n−k aligns the series with
itself offset by k, so a large shift is a small shift in disguise.** The first draft's
`sh = k*step % n` looks well spread and quietly includes those. The fix is the `[minshift, n−minshift]`
window, excluding *both* ends. A guard invisible to the suite and decisive on real data is exactly the
kind that rots, so it is named in-file with the numbers that justify it.

## Live reading (quote it with its null)

```
RI_DECORATIVE  spent I(S;A)=0.0429 bits  required RI=0.0000 bits  gap=0.0429 (null95=0.0099)
               utility achieved=0.0009 vs best state-blind=0.0030  n=2705
               states dropped below the cell floor: lo (8 intervals)
NOTE: the best STATE-BLIND action achieves MORE utility (0.0030) than the observed policy (0.0009)
```

Two independent facts point the same way: the required minimum is zero, and the best constant action
would have done *better* than the policy did. On this tape, conditioning corrective action on the pain
band did not pay for itself. That is a reading about the policy over these 2705 intervals — read-only,
advisory, and explicitly not an escalation.

`lo` is dropped and named: 8 intervals whose no-act cell is below the floor. A coverage bound nobody
states reads as full coverage.

## Sources

- [Archer, Catenacci Volpi, Bröker & Polani, arXiv:2111.03699](https://arxiv.org/abs/2111.03699) — §S5.1, the definition and Lagrangian
- [Rosas, arXiv:2606.06123](https://arxiv.org/abs/2606.06123) (Jun 2026) — the live end
- Polani, Nehaniv, Martinetz & Kim — *Relevant Information in Optimized Persistence vs. Progeny Strategies* (the origin, via ref 46 above)
- [Tishby & Polani, *Information Theory of Decisions and Actions*](https://scispace.com/pdf/information-theory-of-decisions-and-actions-4avyvai7c1.pdf) — the information-as-currency framing (403 from this node; cited from the secondary source, not read here)
