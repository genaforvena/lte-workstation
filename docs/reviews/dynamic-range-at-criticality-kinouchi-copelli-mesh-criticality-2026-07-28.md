# Dynamic range at criticality — the functional payoff the m̂ proxy never measured

**Live literature review · 2026-07-28 · complex adaptive systems / edge of chaos, angle = an
OPERATIONAL mechanism · landed in `scripts/mesh-criticality` (`dynamic_range()` + `--dynrange`)**

## The concept (named, cited)

**Dynamic range Δ, maximized at criticality** (Kinouchi & Copelli, *Nature Physics* 2, 348–351,
2006, "Optimal dynamical range of excitable networks at criticality"; measured *in vitro* by
Shew, Yang, Petermann, Roy & Plenz, *J. Neurosci.* 29(49):15595–15600, 2009, arXiv:0906.0527,
"Neuronal Avalanches Imply Maximum Dynamic Range in Cortical Networks at Criticality").

A network of excitable units has its **dynamic range** — the span of *stimulus intensities* it
codes into **distinguishable responses** — **maximized exactly at the critical point** (branching
σ≈1) and **collapsing away from it**: a subcritical net is insensitive (weak inputs die, only
strong ones register); a supercritical net saturates on the faintest input (any input → full
activation). Only at the edge does the stimulus→response transfer function F(S) become a broad
power law, spreading the response over the widest band of inputs.

Operationally: **Δ = 10·log₁₀(S₉₀/S₁₀) dB**, where S_x is the stimulus intensity evoking a
response x% of the way from spontaneous (F_0) to saturated (F_max). Shew et al. shifted the E/I
balance of cortical cultures off criticality in both directions and watched Δ fall from its σ≈1
peak — a *measured*, not merely theorized, criticality signature.

## Why this is NEW ground (not a re-tread)

`scripts/mesh-criticality` already carries ~10 stacked SOC/edge-of-chaos reviews (branching ratio
m̂, dragon-kings, avalanche shape/crackling exponents, CSD, entropy-complexity, bin-width sanity,
edge-optimality, the Widom-line drive axis). Every one of them measures a **property of the
process** — how the events cascade, how the exponents relate, whether the estimate is stationary.

**None measure the FUNCTIONAL PAYOFF** the whole edifice is justified by. The tool asserts m̂≈1 =
"healthy/maximally responsive" and reports m̂ (the branching-ratio **proxy**). But *why* is m̂≈1
supposed to be good? Kinouchi & Copelli's answer — the original operational justification — is
**dynamic range**: the edge is where a system distinguishes the widest range of input intensities.
The tool measured the proxy and never the thing the proxy is claimed to buy.

The nearest sidecar, `edge_optimality()`, is genuinely different: it asks whether the edge is
where *throughput is best* (a 2-point conversion-efficiency check, calm-pressure half vs
hot-pressure half). Dynamic range asks a different question with different math — **how wide is
the demand band the board codes AT ALL** (the full multi-level transfer function, a log-ratio of
10%/90% crossing stimuli). This directly continues the 2026-07-27 theme of the edge-optimality /
Widom landings: **measure the function, don't assume the proxy.**

## The implementation (read-only sidecar; no alarm, no board post)

`dynamic_range(events, win_h, bin_s)` in `scripts/mesh-criticality`:

- **Stimulus** = pressure count / bin (the branching drivers m̂ counts:
  `[task]/[taking]/[dispatch]/[redispatch]/[verify]`, via the existing `edge_evs` `'P'` markers).
- **Response** = settled count / bin (`[done]/[mind-unblocked]`, the `'S'` markers).
- Bin the window → build the empirical transfer function **F(demand) = mean settled per bin at
  each distinct demand level**, take its saturating (Kinouchi-Copelli monotone) envelope, find the
  demand levels crossing 10% and 90% of the response range (linear interp), report **Δ dB**.
- **Labels are STRUCTURAL, never an assumed dB cutoff** (the constant-outlives-its-reader rule):
  - `GRADED` (Δ>0) — settling tracks demand across a band; a **wide Δ** is the critical
    sensory-coding ideal, a narrow Δ is the sub/supercritical saturating regime. The magnitude is
    left to the live corpus, not a hardcoded WIDE/NARROW band.
  - `DECOUPLED` — response FLAT across all demand (settling saturated or unresponsive): the
    functional deficit criticality is claimed to prevent. Δ undefined.
  - `INSUFFICIENT` — <8 stimulus-bearing bins or <4 distinct demand levels → no fabricated verdict
    (same honest-empty discipline as CSD/drift/edge on sparse nodes).
- **Never touches m̂/regime/alarm** — same restraint as CSD/Shape/Widom/edge. Exposed as
  `--dynrange`, a `Dynrange=` field on the default line, and a `dynrange{}` block in `--json`.

**RED-first `--test`:** four fixtures on an *aligned* synthetic transfer function (a WIDE graded
response, a NARROW one saturating early, a DECOUPLED flat one, and a single-level INSUFFICIENT
one). Assertions: labels are correct AND **Δ strictly tracks coding width** (wide Δ > narrow Δ).
Verified red-then-green: forcing Δ to a constant → `wide 1.0 !> narrow 1.0` FAIL; forcing
DECOUPLED→GRADED → the flat-response FAIL; restored → `smoke-test: ok`. (A subtlety worth its own
note: `dynamic_range` needs *exact* per-level means, so its test bins must land on the 300s grid —
the shared `_edge` helper's `base=1000+b*300` offset splits a bin across the boundary, which
`edge_optimality`'s coarse median-split tolerates but this does not; the dynrange test uses an
aligned `_dyn` helper with a P=0 grid-anchor.)

## Live reading on this board (mesh-home, 2026-07-28)

- 12h default window: `Dynrange=INSUFFICIENT levels=0` — only 4 pressure-bearing bins, honestly
  empty (exactly as CSD/edge read on today's sparse tape).
- 96h window: **`Dynrange=GRADED Δ=4.7dB levels=4`**, alongside `Edge=EDGE-UNPRODUCTIVE
  conv=0.43→0.36` over the same window.

The complement is the point: the board **does** have a graded response to demand (dynamic range is
non-degenerate — settling rises across a ~4.7 dB band of demand intensities, *not* DECOUPLED), yet
its conversion efficiency *falls* in the hot half (edge-unproductive). Two different questions,
two different answers on the same tape — the board codes demand into graded settling but clears it
*less* efficiently under load. Neither the m̂ proxy nor edge_optimality alone said that.

## Unwired next (deferred, honestly flagged)

The rigorous unit is a **per-window Δ ↔ m̂ join over the m̂ tape** — does the board's dynamic range
actually PEAK when m̂≈1, as Kinouchi-Copelli predict, or is Δ flat/inverted vs distance-to-edge on
*this* substrate? (Same deferral as edge_optimality's m̂↔throughput join: the m̂ tape is sparse on
most nodes today.) That join is the falsifier for "our board is healthiest at m̂≈1" from the
*sensory-coding* side, complementing edge_optimality's throughput-side falsifier.
