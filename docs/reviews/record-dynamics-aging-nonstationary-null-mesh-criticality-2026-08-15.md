# RECORD DYNAMICS — the non-stationary null `mesh-criticality` never had, and the one that a rebooting mesh actually needs

**Date:** 2026-08-15 · **Window:** genome · **Tool:** `scripts/mesh-criticality` (new read-only `--aging` sidecar) · **Area:** self-organized criticality & power-law dynamics, cross-domain transfer to a distributed sensor mesh

## What was already embodied (checked first, not assumed)

`mesh-criticality` carries eleven lenses: m̂/regime, `--shape`, `--crackling`, `--complexity`,
`--dynrange`, `--suscept`, `--coherent`, `--margin`, `--hurst`, `--coarse`, `--dtc`. Sixteen landed
reviews sit in `docs/reviews/`, and the coverage memory lists bin-width artifacts, edge-optimality,
quasicriticality/Widom, dynamic range, SOB-vs-SOC, prescribed burn, susceptibility, coherent noise,
reverberating margin, DFA/1-f, subsampling deflation, and the CSD noise confound.

Three candidates died on contact with that check, which is the point of doing it:

- **Avalanche shape collapse / crackling scaling relation** — already `--shape` + `--crackling`, and
  the header already cites Papanikolaou 2011 and de Candia et al. 2026.
- **Griffiths phase / stretched criticality** — reviewed 2026-06-20
  (`~/.mesh/knowledge/griffiths-phase-stretched-criticality.md`), which already cites arXiv:2512.03409.
- **Clauset-style power-law goodness-of-fit** — `--powerlaw` was prototyped and deliberately rejected
  (free-`x_min` overfit); `--shape` supersedes it.

## The concept we did NOT embody: record dynamics

**Record dynamics (RD).** Sibani & Jensen, *Record dynamics of evolving metastable systems: theory and
applications*, **Eur. Phys. J. B 94, 24 (2021)** ([arXiv:2008.12684](https://arxiv.org/pdf/2008.12684));
applied to cascades in Boettcher & Gago, *Instability cascades in disordered systems indicate record
dynamics*, **[arXiv:2312.12254](https://arxiv.org/html/2312.12254v1) (2023)**. Found via live search;
the RD-vs-SOC framing is stated explicitly in the EPJB review.

The mechanism: in an aging metastable system, progress requires a **record-breaking** fluctuation.
Each record sets the clock, and records get exponentially harder to break, so:

| | stationary (SOC) | record dynamics |
|---|---|---|
| event rate | λ constant | λ(a) ∝ 1/a |
| count | ⟨n⟩ ∝ a − a_w | ⟨n⟩ ∝ ln(a/a_w) |
| inter-event times | exponential in time | exponential in **log**-time (log-Poisson) |
| time-translation | invariant | **not** invariant — the clock starts at the quench |

And the sentence that makes this load-bearing rather than decorative: **"the relaxation effects of
quakes can generally be described by power laws unrelated to criticality."** An aging system mints
heavy tails with no critical point anywhere near it.

This is a genuinely *different* null from the two already here. `--coherent`'s null is **exogenous
stress**; the Griffiths phase is **quenched topological disorder**; record dynamics is the system's
**own history**. Nothing in the tool asked whether the event *rate itself* was decaying.

## The cross-domain transfer

Every other lens in `mesh-criticality` assumes the tape is **stationary**. m̂ is a windowed branching
ratio; the avalanche exponents pool cascades across the window; `--hurst` detrends each box but still
fits one self-affine slope; `--dtc` asks whether CSD reads drive rather than distance. Non-stationarity
appears in the tool only as a *confound to flag* (drift / CSD / Widom) — never as a mechanism with its
own law and its own test.

A mesh is a near-perfect RD substrate: this node reboots, redeploys and restarts services, and **every
one of those is a quench**. If incidents cluster after a boot and thin out as ~1/a, a window straddling
that transient measures an aging transient and reports it as a stationary regime. This is the
already-known `blocky-context-is-confounded-with-nonstationarity` failure, with a named mechanism and a
falsifiable law attached.

## The mechanism landed: `mesh-criticality --aging`

Conditional on n events over an interval, a **constant** rate puts arrival times uniform in *elapsed*
time; a rate **λ(a) ∝ 1/a** puts them uniform in *log-elapsed* time. So map the same events both ways
and take two KS distances:

- `u_i = (a_i − a_min)/(a_max − a_min)` — uniform under stationarity
- `v_i = (ln a_i − ln a_min)/(ln a_max − ln a_min)` — uniform under record dynamics

where `a_i = t_i − t_w`. **`t_w` is the quench** — node boot via `/proc/uptime`, or `CRIT_AGING_TW` —
**never the tape origin**: aging is measured from the perturbation, not from wherever the log happens
to start. No fitting, no free exponent, no `x_min`.

Verdicts: `STATIONARY` · `AGING-LOG-POISSON` · `AMBIGUOUS` (within `CRIT_AGING_EPS`), plus honest `n/a`
with a stated reason when there are too few events, no origin, or the window reaches back past the
quench.

**The verdict is comparative, and the code says so in its own output.** Both variates are conditioned
on the same endpoints, so the two D's are directly comparable — but SOC avalanches are *clustered*,
which inflates both, so a small D is never a certificate that the tape is Poisson. When both are
rejected at p<0.01 the label carries `(both-rejected)` and the winner is only the less-bad
description. This is the `a-sub-axis-is-not-the-verdict` discipline applied at authoring time rather
than after a review catches it.

## Live reading — a real negative, independently corroborated

```
criticality record-dynamics/aging: STATIONARY (n=367, t_w=boot, elapsed 12.9h..24.8h;
  KS-vs-uniform D_linear=0.073 p=0.038 · D_log=0.135 p=0.000)
```

Node uptime 1d 0h 49m, so the 12h window sits 12.9–24.8 h after the quench. The constant-rate law wins
decisively (D smaller by ~2×, p larger by ~38×). Note the honesty the design forces: `p_linear=0.038`
is itself marginal — the tape is not cleanly Poisson either, exactly as the clustering caveat predicts —
so this is "the stationary law describes it better", not "the tape is Poisson".

Independent corroboration from a lens that shares no code with this one: the same run reports
`CECP=MEMORYLESS-POISSON-LIKE n=366 H=0.99 C=0.01`.

So: **this window is not an aging transient**, and the stationarity every other sidecar silently
assumed is, for once, checked rather than presumed. The value of the lens is that it can now come back
`AGING-LOG-POISSON` after the next reboot — which is precisely when m̂ would otherwise be read at face
value.

## Artifact — each gate seen RED before green

`--test` green (`smoke-test: ok` + `alarm-test: ok`). Fixtures are the two laws in pure form off a
pinned `t_w`, so the node's real boot clock cannot leak into the assertion: arrivals uniform in elapsed
time → `STATIONARY` (D_lin 0.017 vs D_log 0.428); geometric arrivals, uniform in log-elapsed →
`AGING-LOG-POISSON` (D_log 0.017 vs D_lin 0.572). Four mutants, run from a scratch copy:

| mutant | result |
|---|---|
| verdict comparison swapped | `FAIL (arrivals uniform in ELAPSED time must read STATIONARY, got AGING-LOG-POISSON)` |
| MIN_N guard removed | `FAIL (below MIN_N must be an honest n/a WITH a reason, never a verdict, got AMBIGUOUS n=3)` |
| pre-quench guard removed | `FAIL (a window reaching back past the quench … must be n/a naming that)` |
| label pinned constant | `FAIL (arrivals uniform in LOG-elapsed time … must read AGING-LOG-POISSON, got STATIONARY)` |

The suite also asserts the two KS distances **swap order** between the fixtures — otherwise one of them
could be unused and the axis would still look like it tracked.

## Scope

Read-only. Never touches m̂, the regime, the alarm, or the board. `--aging` is on-demand; it is not
wired into cron and does not appear in the default banner.

## Sources

- [Sibani & Jensen, *Record dynamics of evolving metastable systems*, EPJB 94:24 (2021) — arXiv:2008.12684](https://arxiv.org/pdf/2008.12684)
- [Boettcher & Gago, *Instability cascades in disordered systems indicate record dynamics*, arXiv:2312.12254 (2023)](https://arxiv.org/html/2312.12254v1)
- [Sibani, *Record Statistics and Dynamics* (Springer encyclopedia entry)](https://link.springer.com/referenceworkentry/10.1007/978-1-4614-1800-9_160)
- Checked-against-and-rejected as already covered: [de Candia et al., *Symmetry breaking and avalanche shapes in modular neural networks*, Front. Comput. Neurosci. (2026)](https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2026.1744991/full) · [Griffiths phases in hierarchical modular networks, Sci. Rep. 5:14451](https://www.nature.com/articles/srep14451)
