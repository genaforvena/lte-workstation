# Live-literature review — information theory of agency: CRYPTICITY (χ = C_μ − E) — excess entropy is NOT the stored memory, only a lower bound on it

Date: 2026-07-30 · lane: genome (idea-queue LITERATURE task — information theory of agency / empowerment /
predictive information, from the angle of a **foundational idea we applied too loosely**) · status: **code
DISCARDED as a hollow sense** (falsified by its own test); concept + falsification landed as this review.
Steward lands the doc.

## Where we had already been (checked before landing, so this doesn't double-count)

Information theory of agency is a heavily-worked mesh seam. The embodied set, confirmed before landing —
every piece measures a quantity of *communicated* or *coarse-grained* correlation:

- **empowerment — action→future-sensor-state MI** → `scripts/mesh-algedonic` AGENCY_INFO sidecar.
- **instrumental / multi-agent empowerment** → `scripts/mesh-mind-control:155`, `:1324`.
- **Maximum Occupancy Principle** → `scripts/mesh-vitality`.
- **predictive information / excess entropy** `E = I(past;future)` as a structure-vs-noise discriminator →
  `scripts/mesh-precision --num` (`pred_info`, lag-1 PI₁ = −½log₂(1−ρ₁²)) + the **memory-depth / nostalgia**
  axis (`pred_depth`, best deeper-lag PI gain); `mesh-sensorium`/`mesh-rhythm`.
- **transfer entropy** (Schreiber 2000) → `scripts/mesh-cooscillate`.
- **synergy / redundancy / O-information** → `scripts/mesh-algedonic --synergy`, `mesh-home-state` ∂ᵢΩ.
- **causal emergence** — Rosas et al.'s PID Ψ criterion (`Ψ(V)=I(Vₜ;Vₜ′)−Σⱼ I(Xⱼₜ;Vₜ′)`, the max-fold is
  provably non-emergent) → `scripts/mesh-situation` header + fold.
- **statistical complexity — the MARTÍN-PLASTINO-ROSSO C_JS** (entropy×disequilibrium, the H–C causality
  plane) → `scripts/mesh-criticality:711`.
- **overwrite vs identification**, **assistive/process empowerment**, **nostalgia/memory-depth**,
  **semantic information** → reviews 2026-07-24 … 2026-07-29.

Two of these are *named* "complexity" or "predictive information" and are the exact things this review is
about — so the check had to be sharper than a keyword grep:

- `mesh-precision`'s `pred_info` is **excess entropy E** = the information the past and future SHARE.
- `mesh-criticality`'s statistical complexity is **MPR C_JS** — a disequilibrium-from-uniform product on
  the permutation-entropy plane. It is **not** Crutchfield's causal-state C_μ; the two share a name and
  nothing else.

**Neither the causal-state statistical complexity C_μ nor the crypticity gap χ = C_μ − E is embodied**
(`grep -riE 'crypticit|causal.state|c_mu|epsilon.machine' scripts/` → 0 real computations; the hits are
MPR C_JS and the Rosas-Ψ prose). That gap is the foundational point below.

## The concept not yet embodied — CRYPTICITY, and the misread it exposes

**J. P. Crutchfield, C. J. Ellison & J. R. Mahoney, "Time's Barbed Arrow: Irreversibility, Crypticity,
and Stored Information," *Phys. Rev. Lett.* 103, 094101 (2009)** — <https://arxiv.org/abs/0902.1209>.
Companion: **Ellison, Mahoney & Crutchfield, "Prediction, Retrodiction, and the Amount of Information
Stored in the Present," *J. Stat. Phys.* 136:1005 (2010)** — <https://csc.ucdavis.edu/~cmg/papers/pratisp.pdf>.
Live 2026 continuation of the same computational-mechanics / structural-complexity program:
**"Way More than the Sum of Their Parts: From Statistical to Structural Mixtures," *Entropy* 28(1):111
(2026)**, doi:10.3390/e28010111 — <https://doi.org/10.3390/e28010111> (structural complexity of
multicomponent systems is strictly more than the statistical mixture of its parts; the field is live).

The move, in one inequality:

> The excess entropy **E** — the information communicated between a process's past and future — **is not,
> in general, the information the process must store in the present. That is the statistical complexity
> C_μ (the Shannon entropy of the process's causal states), and C_μ ≥ E always.** The gap
> **χ = C_μ − E ≥ 0 is *crypticity*: internal state the process holds but HIDES from its own future.**

Where we applied it too loosely: `mesh-precision`'s whole predictive-information doctrine treats
`pred_info` (= E, via the lag-1 autocorrelation) as *the process's structure / stored memory* — the
nostalgia axis literally reads "DEEP ⇒ genuine deep memory, retain to `pred_depth`; a lag-1-only view
discards predictive info," and a `pred_info=NOISE` verdict is taken to license treating the stream as
memoryless (the CV down-weight "is right"). But **E is only a LOWER BOUND on the stored memory.** A
process can read `E≈0` on the surface (past and future share little *observable* information) and still
require substantial hidden state C_μ > 0 to be generated. For such a **cryptic** stream, a NOISE verdict
under-retains: the mesh would discard internal structure that is real but simply never surfaces in the
E-channel. That is a genuine, un-embodied axis — orthogonal to both E (how much the past predicts) and
memory-depth (how far back you must look): crypticity is *how much of the stored state is unobservable
from the future at all*, no matter the window.

## The application I built — and DISCARDED, with the falsifying evidence

Natural home: `mesh-precision`'s **`--cat`** branch (symbolic — computational mechanics operates on
sequences of symbols), which today computes ONLY a surface switch-rate stability and has no memory/
structure axis at all. I implemented a report-only χ = C_μ − E companion: length-L words → next-symbol
distributions → merge words with equal next-symbol distributions into causal states → `C_μ = H[causal
states]`, `E_L = I(word; next-symbol)`, `χ = max(0, C_μ − E_L)`, labelled CRYPTIC/PARTIAL/TRANSPARENT
with an honest-n/a sample floor. It smoke-tested and ran.

**Then its own test falsified it.** Contrasting streams (L=2 causal states):

| stream | truth | estimator said |
|---|---|---|
| period-2 `ABAB…` | transparent (χ=0) | TRANSPARENT χ=0.00b ✓ |
| period-4-in-2-symbols `AABB…` | transparent — *periodic ⇒ reversible ⇒ χ=0* | TRANSPARENT χ=0.00b ✓ |
| period-10 deterministic pattern | transparent (χ=0) | **CRYPTIC χ=1.53b ✗ FALSE POSITIVE** |

The failure is diagnostic, not a bug to patch: a **cryptic process needs *stochastic* hidden states**;
a periodic one is transparent. But when a stream's correlation length exceeds the history order L, the
finite-L `E_L` **under**-counts the true E while the diversity of one-step successor distributions
**inflates** the causal-state estimate — so χ = C_μ − E_L reads high purely from **finite-L bias**, not
crypticity. On the mesh's short categorical windows L cannot be grown far enough (nor multi-step futures
sampled densely enough) to separate "genuinely cryptic" from "L is just too short here." A measure that
fires CRYPTIC on a clean deterministic period-10 sequence is exactly the hollow sense CLAUDE.md is built
to reject — a default indistinguishable from a real read. **Reverted** (`git checkout scripts/mesh-precision`);
nothing shipped in the tree.

## What would make it honest (deferred, not impossible)

- A **correct estimator = CSSR** (Shalizi & Klinkner 2004) with **multi-step futures** and an
  **E-saturation guard** (only emit χ once `E_L ≈ E_{L−1}` — i.e. the process is already well-predicted at
  order L, so the remaining C_μ − E is true crypticity and not finite-L slack). That needs
  samples ≫ alphabet^(L+m): feasible ONLY on the small-alphabet, long state logs
  (`~/.mesh/health-state.log`, `home-state`, `situation` posture — 10⁴–10⁵ lines), never on the short
  sensor windows `--num` sees.
- **Payoff is manual-diagnostic only**: `mesh-precision --cat` has no live reflex consumer today
  (`grep -rn 'precision --cat' scripts/` → only its own usage line). No reflex behaviour improves, so the
  CSSR lift is not worth its reliability risk until something actually keys on the categorical verdict.

**Verdict: concept is real, foundational, and un-embodied; the cheap application is a hollow sense and was
discarded with its falsifying test; the correct application is feasible but scoped to long small-alphabet
state logs as a manual diagnostic, and deferred for lack of a consuming reflex.** The durable landing is
this record — so the next mind reaching for "add crypticity to mesh-precision" starts from the falsification,
not from where I did. The one-line correction that IS true and cheap: `pred_info` (E) is a **lower bound**
on a categorical stream's stored memory, not the memory itself — a NOISE verdict does not license
discarding internal state.

---
*Sources:* Crutchfield/Ellison/Mahoney, PRL 103:094101 (2009), arXiv:0902.1209 · Ellison/Mahoney/Crutchfield,
JSP 136:1005 (2010) · *Entropy* 28(1):111 (2026), doi:10.3390/e28010111 · Shalizi & Klinkner, "Blind
Construction of Optimal Nonlinear Recursive Predictors for Discrete Sequences" (UAI 2004, CSSR).
