# Antifragility / convexity / ruin — live review: RESTART IS NOT FREE, AND A HEALER'S OWN TAPE CANNOT JUDGE IT

**Date:** 2026-08-22 · **Node:** mesh-home · **Lane:** LITERATURE (live review), idea-queue
**Landed in:** `scripts/mesh-link-heal` → `restart_benefit()` + `--restart [--json]` (read-only lens,
uncommitted in the tree, steward lands) · **Doctrine line:** one, in `CLAUDE.md`

## The sweep (what "live" meant here)

Prior art in this area is deep — 13 `antifragility-*` reviews plus `ergodicity-breaking-*`: κ and the
pre-asymptotic minimum-n, the CAFE Jensen gap, Taleb–Douady left-tail *direction*, Sontag log-rate
convexity, the threshold-fishing trap, Parisian ruin *dwell*, the generalized drawdown barrier, the ω
bankruptcy-rate function, degeneracy vs redundancy, joint-failure nonlinearity, the criticality
boundary, and (2026-08-19) the decision-centric plug-in buffer. So this went to the **live arXiv
listing** by submission date rather than to a reading list: `all:"ruin probability"`,
`all:antifragility`, `abs:"tail risk" AND abs:convexity`, then the resetting sub-thread the first
query surfaced.

Checked and **not** landed:

- *Beyond Resilience: Antifragility in Critical Infrastructure Cybersecurity* (arXiv:2607.29550) and
  *When Stress Becomes Signal: Detecting Antifragility-Compatible Regimes in Multi-Agent LLM Systems*
  (arXiv:2605.02463, 2026-05-04) — both score a **distributional Jensen gap under a convex stress
  potential**, which is the axis `mesh-convexity` already is. CAFE is a nicer packaging of a thing we
  have, not a thing we lack.
- *On the Expected Maximum Deficit and the Optimal Allocation of Reserves* (arXiv:2605.16448) — the
  interesting half is allocation across multiple lines; the mesh has one budget.
- *Spectral Duality and Reset-Neutral Distributions …* (arXiv:2605.00657, 2026-05-01) and *Critical
  Spectral Invariants in Random Walks with Geometric Resetting* (arXiv:2603.24803, 2026-03-25) —
  these are what pointed the sweep at restart. They solve **gambler's ruin under resetting** and
  exhibit *reset-neutral* reset distributions, for which the ruin probability is independent of the
  resetting rate γ entirely. Kept as a named opening (a healer whose reset TARGET is neutral w.r.t.
  the barriers buys nothing by firing more often), not landed: mapping our ladder onto a biased walk
  on `{0..a}` would be a model we cannot measure the parameters of.

## The concept we did not embody

> **First passage under restart, and its benefit criterion.**
> Reuveni, *Optimal Stochastic Restart Renders Fluctuations in First Passage Times Universal*,
> **Phys. Rev. Lett. 116, 170601 (2016)** — at the optimal restart rate, CV of the completion time = 1.
> Pal & Reuveni, *First Passage Under Restart*, **Phys. Rev. Lett. 118, 030603 (2017)**
> (arXiv:1607.06048) — restart lowers the mean iff **CV > 1**.
> Eliazar & Reuveni, *Mean-performance of sharp restart I: Statistical roadmap*, **J. Phys. A 53,
> 405004 (2020)** (arXiv:2003.14116): *"if there exists a restart protocol that improves
> mean-performance, then there exists a sharp-restart protocol that performs as good or better"* —
> **sharp** restart being a fixed deterministic timer, which is exactly what an escalation rung is.
> Eliazar & Reuveni, *Mean-performance of Sharp Restart II: Inequality Roadmap* (arXiv:2102.13154),
> in the most usable form: *"restart impedes/expedites mean completion when the underlying
> statistical heterogeneity is low/high"*, measured by **inequality indices** — Gini, Bonferroni,
> Pietra.

Exact arithmetic for a sharp timer τ with per-restart overhead c:

```
E[T_τ] = ( E[min(T,τ)] + c·(1−p) ) / p ,   p = P(T ≤ τ)
```

## The foundational idea we had applied too loosely

`CLAUDE.md` says: *a detector is not a closed loop — a recurring fault with a one-line idempotent
remedy needs a RE-APPLIER.* True, and earned. The half we never examined is that **restarting is a
win**. The literature does not grant it: restart expedites completion only where the completion time
is **over-dispersed**. For an under-dispersed recovery — a link that reliably comes back at about the
same age — *every* timer strictly increases the mean, and the ladder is motion, not repair. Nothing
anywhere in the genome measures the dispersion of a recovery time. `mesh-link-heal --dwell` (landed
2026-08-20) is the nearest thing and it is a different question: it asks **where** a rung should sit
given two MEDIANS (τ_recur, b_inv) — a location statistic. Two tapes with identical medians, one over-
and one under-dispersed, produce byte-identical `--dwell` output and opposite restart verdicts.

## The trap, which is the finding

The obvious move is to measure the criterion on the bare arm: episodes closed with `last rung
attempted: none`. **That arm is not a sample of the link's unrestarted recovery time.** `rung=none`
means *the episode cleared before the first rung fired*, so the arm is that distribution **conditioned
on being shorter than 120 s** — by construction, not by accident. An episode that ran long got helped
and left the arm, taking its tail with it.

**The healer truncates precisely the tail whose weight decides whether the healer helps.**

Measured on this node, live, at the moment of writing:

| | |
|---|---|
| arm | truncated (`rung=none`), n = 133 |
| helped episodes excluded | 35 — **longest 9089 s** (2 h 31 m) |
| E[T] · sd | 57.3 s · 4.3 s |
| CV · Gini | **0.074** · 0.035 |
| best sharp timer | **none** — no τ improves the mean |
| quantisation floor | sd would have to exceed 17.3 s (= TICK/√12) to be resolved at all |
| first rung fires at | 120 s |

Read naively that is a crisp "restart cannot help this link, retire the ladder" — and it is exactly
what a blind lens produces. Two independent biases, **both pointing the same way**, generate it:

1. **Truncation by the ladder itself.** Removing the tail removes the over-dispersion.
2. **Quantisation by the check cadence.** Dark seconds are a lower bound stamped at TICK = 60 s; a
   sample whose whole spread is 40–61 s is one bin wide. There is no resolved dispersion to test.

Both shrink apparent heterogeneity, so both push the reading toward *no-gain* — **the direction that
would disarm a working reflex**. The verdict must therefore be polarised, not symmetric.

## What landed: `mesh-link-heal --restart`

A read-only lens (`restart_benefit()`), no action, no state write, no log line, `MESH_LINK_HEAL_LOG`
overridable so `--test` drives it on scratch fixtures.

- **Three arms, never folded.** `holdout` (deliberately unhelped — the only uncensored sample of the
  environment) · `none` (self-cleared, truncated at the first rung) · everything else measures the
  **healer**, not the fault, and may not enter the sample at any weight.
- **The exact sharp-restart sweep** over the sorted sample (the optimum is attained at an observed
  value), with the restart cost c declared and printed; c = 0 is the optimistic end, so a no-gain
  reading at c = 0 is a fortiori.
- **Polarised verdicts.** From a truncated arm, `helps` **is** issuable — the biases only work against
  it, so a gain measured despite them stands. `no-gain` is **not** issuable there; it renders
  `unresolved`, naming both blindnesses separately. A negative verdict requires a holdout arm **and**
  resolved dispersion.
- **It names what would lift the refusal:** ≥20 episodes closed as `last rung attempted: holdout`.
  The lens prefers that arm the moment it exists.
- Reports CV **and** Gini (the roadmap's own index), τ*, E[T_τ*], the gain, the quantisation floor,
  and the ladder's own first-rung dwell beside them.
- Says explicitly what it does **not** claim: this is a mean-completion criterion, and the higher
  rungs exist for the **wedge** — where the link does not come back at all — whose value is not a mean
  but an avoided absorbing state.

## Gates

`--test` gains 10 legs (`8a`–`8h`, total suite 105 green). Six mutants driven **RED** against the
final file, control green:

| mutant | leg that caught it |
|---|---|
| truncation leg removed | `8a2` — a *resolved* but truncated arm concluded (`8a` alone could not catch it: its spread is also sub-quantum, so either leg holds it — hence the isolating fixture) |
| helped episodes folded into the sample | `8f` — an all-helped tape produced a verdict instead of `na` |
| `c·(1−p)` term dropped | `8d` — a 2000 s restart still read as a win |
| quantisation floor removed | `8e` — an uncensored one-bin arm read `no-gain` |
| `helps` blocked on a truncated arm | `8b` — a real gain that survives its own bias was refused |
| minimum-n gate removed | `8g` — a verdict off four points |

## Honest bounds

- The verdict on this node today is **UNRESOLVED**, not a finding about the ladder. Nothing here says
  a rung has harmed anything.
- Dark seconds are lower bounds; the true durations are unknown at sub-TICK resolution.
- The **holdout arm is specified but not implemented.** Marking it requires the ladder to withhold a
  rung on a sampled fraction of episodes — a behavioural change to the actuator that tends this
  node's **sole** uplink, touching `choose_rung`'s state machine. That is a separate, drillable
  change with its own risk, and it is deliberately not smuggled into a literature review. The lens
  reads the arm the moment it appears, and the tape format needs nothing new: `last rung attempted:
  holdout`.
- Reset-neutrality (arXiv:2605.00657) is left as a named opening, not a claim.

## Sources

- Reuveni, PRL 116, 170601 (2016) — https://arxiv.org/abs/1512.01600
- Pal & Reuveni, PRL 118, 030603 (2017) — https://arxiv.org/abs/1607.06048
- Eliazar & Reuveni, J. Phys. A 53, 405004 (2020) — https://arxiv.org/abs/2003.14116
- Eliazar & Reuveni, *Inequality Roadmap* — https://arxiv.org/abs/2102.13154
- Gambler's ruin under geometric resetting — https://arxiv.org/abs/2603.24803 · https://arxiv.org/abs/2605.00657
- CAFE / antifragility-compatible regimes — https://arxiv.org/abs/2605.02463
