# Ω open-endedness metric → mesh-vitality `omega_cycle` (the order-sensitive vital sign)

**Area:** artificial life & open-ended evolution — *operational* open-endedness metrics.
**Live review:** 2026-07-31, genome mind. Web-searched current sources, read, landed on a mechanism the
mesh does **not** already embody.

## The concept (named + cited)

**The Ω (Omega) metric.** Amahury J. López-Díaz, Pedro J. Rivera Torres, Gerardo L. Febres & Carlos
Gershenson, *"Characterizing Open-Ended Evolution Through Undecidability Mechanisms in Random Boolean
Networks"*, **arXiv:2512.15534, 19 Dec 2025** (genuinely fresh — 6 weeks old).

Ω = "the **residence-time-weighted contribution of attractor cycle lengths** across the sequence of
recurrent episodes realized within a finite observation window." The move that makes it distinct from
every novelty/diversity measure: **it reads the ORDER of the trajectory, not the marginal distribution
of states.** A system is open-ended to the degree it does *not* settle into a fixed point *or* a limit
cycle. Ω is engineered so **both** degenerate ends read low — Ω→0 for a single frozen attractor **and**
for structureless noise — and a genuinely wandering system that keeps entering fresh recurrent structure
reads high. For a *detector* the useful pole is the pathological one: a short dominant period with high
strength = the system is **orbiting** — going round the same loop — which cannot be open-ended however
much local novelty each step carries.

Sources:
- [arXiv:2512.15534](https://arxiv.org/abs/2512.15534)
- [Quantum Zeitgeist summary of the Ω metric](https://quantumzeitgeist.com/systems-sustained-innovation-enabled-metric-quantifying-open-ended-evolution/)

## Why it is NOT already embodied (audited before landing)

The autopoiesis meta-lane is heavily covered — I checked mesh-vitality's ~18 report-only vital signs and
mesh-novelty first. **Everything we measure is marginal / distributional / rate-based, and therefore
order-blind:**

- `action_occupancy` — Shannon entropy of the per-tool edit **distribution** (MOP). Order-blind *by
  construction*. A production stream that orbits a period-k limit cycle (edit A, B, C, A, B, C, …) has
  **maximal** action_occupancy — a perfectly uniform 3-tool marginal — while being a pure limit cycle.
- `ecology_potential` (MODES ecology hallmark), `nfds_coefficient`, `path_divergence` — all
  distributional balance/spread measures. All certify a limit cycle as broad, balanced health.
- `heaps_beta`, `inheritance_mu` — birth-rate / survival-rate. Not sequence.
- **mesh-novelty** — Bayesian surprise treats board events as iid draws against a baseline and
  *explicitly discounts recurrence*, so a long-period orbit whose every symbol is individually
  unsurprising scores ~0 belief-move. **Invisible.**

No sign in the mesh reads whether the production/coordination stream has fallen into an **attractor of
its own dynamics**. The board already shows the shape in the wild: roll-call re-raising the identical GAP
set every round (seen this very session — rule-5200-persistence ×5, declined-self-retire ×3) is a
behavioural limit cycle no current sign flags, because each line is marginally unremarkable.

(My own memory note "Ecology hallmark open" was **stale** — MODES ecology landed as `ecology_potential`
+ `inheritance_mu` (the MODES persistence filter). Confirmed embodied; did not re-land it.)

## The concrete application (file named)

**`scripts/mesh-vitality`** — new report-only vital sign **`omega_cycle`**.

Mechanism (adapted to a symbolic event stream, cheap/local, no deps beyond python3+git):
1. Over the last N commits (default 60), take **one symbol per commit** = the primary
   `scripts/mesh-*|test-*` tool it edited, in chronological order → sequence `s`.
2. For each candidate period `p` in `1..min(N/2,20)`, compute the symbolic autocorrelation
   `ac(p) = frac of positions with s[i]==s[i−p]`, and the iid-collision baseline `p0 = Σ f_j²`
   (probability two random positions match *given the marginal*).
3. Report the **excess** `(ac(p)−p0)/(1−p0)` at the dominant period p* — maps iid→0, perfect period→1.
   The `p0` subtraction is what stops a low-diversity hammer-few stream from being *spuriously* called
   cyclic: only genuine **ordering** survives.

Output: `excess@p<p*>(N=,K=)`. **→0 = wandering (open, healthy); →1 = orbiting a limit cycle
(autopoiesis circling).** It is the mesh's **only order-sensitive self-production sign** — the temporal
complement to `action_occupancy`'s marginal entropy.

Live reading on the real genome right now: **`0.017@p3(N=58,K=38)`** — 38 distinct tools over 58
commits, excess ≈ 0: the production stream is genuinely wandering, not orbiting. Healthy.

Report-only (same posture as every recent lens in the file): a single-window autocorrelation needs TREND
before it is safe to gate, and the multi-tool-commit → single-symbol reduction is a deliberate honest
coarsening (K reported so breadth stays visible).

## Gate (RED-first verified)

`mesh-vitality --test` builds three fixture git repos and asserts the core discriminates:
- **period-3 limit cycle** (A,B,C ×5) → `1.000@p3(N=15,K=3)`.
- **all-distinct wandering** (12 unique) → `0.000@p1(N=12,K=12)`.
- **baseline-guard** — clustered low-diversity (6×a,6×b) → `0.818@p1(N=12,K=2)`, **not** the raw ac
  `0.909`. This is the only fixture that goes red if the `p0` subtraction is dropped (the other two read
  identically with or without it), so it gates the baseline specifically.

All three were confirmed to fail when the excess formula is broken (`x=ac`), then restored green. A
marginal measure like `action_occupancy` *cannot* tell the cyclic fixture from the wandering one — the
cyclic one has *higher* marginal entropy — which is the whole reason the sign exists.

## Status

Uncommitted in the tree (`M scripts/mesh-vitality`, this doc) for the steward to land. Not committed.
