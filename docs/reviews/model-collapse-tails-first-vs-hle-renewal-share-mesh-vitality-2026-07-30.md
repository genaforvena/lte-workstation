# Early model collapse ("the tails vanish first") vs our HLE renewal-share — mesh-vitality

**Date:** 2026-07-30 · **Node:** mesh-home · **Lane:** genome (live literature review) ·
**Area:** homeostasis / allostasis / ultrastability → *the idea we applied too loosely* ·
**Verdict:** ONE concept surfaced, **HELD** as an instrument proposal on `scripts/mesh-vitality`
(cheap proxy would be hollow — see §5), zero behavior change.

## 1. Where we already are (do not re-land)

The mesh is saturated on this area. `docs/reviews/` + `scripts/mesh-vitality` already embody:
requisite variety (`channel_variety`), Ashby ultrastability trials-to-stable-field
(`mesh-homeostasis`), critical slowing down (`mesh-algedonic`/`mesh-therm-watch`), allostatic
load incl. Mahalanobis joint-dysregulation (`mesh-algedonic`), reactive scope (`mesh-stress`),
structural homeostasis (`loop_closure_frac`), MSPD multi-scale divergence (`path_divergence`),
action-space occupancy (`action_occupancy`), NFDS/ecology evenness, and — crucially — the
**Hypernetic Law of Experience** itself, landed **2026-07-06** as `renewal_trend()`:

> *"Optimized to Death: The Hypernetic Law of Experience", Systems (MDPI) 14(2):197 (Feb 2026),*
> https://www.mdpi.com/2079-8954/14/2/197 — generalizes Ashby's neglected **Law of Experience**
> (repeated transformation erodes a system's initial distinctions; variety cannot increase and
> usually diminishes — *An Introduction to Cybernetics*, 1956) to stochastic adaptive systems:
> under sustained **directional** experience, internal variety is consumed and trajectories
> converge to ever-narrower regions of state space. **Collapse when compression outpaces renewal.**

`renewal_trend` operationalizes that as a **balance of shares**: fraction of recent-window commits
that ADD a new tool (renewal) vs the prior window; a falling share tags `COMPRESSING`.

## 2. The idea we applied too loosely

The MDPI note's own headline cross-domain instance is **recursive model collapse** — "a system
trained on its own outputs narrows" — and our `renewal_trend` comment names the mesh's exact
version of it: *the idea-queue re-samples its own committed corpus
(`mesh-generate`→`mesh-feed`→genome→back into the sample pool)*. So we correctly identified the
loop. **But we measured the wrong moment of it.**

The foundational result on recursive collapse is precise about *what moves first*:

> **Shumailov, Shumaylov, Zhao, Papernot, Anderson & Gal, "AI models collapse when trained on
> recursively generated data", _Nature_ 631, 755–759 (2024)**
> (https://www.nature.com/articles/s41586-024-07566-y; PubMed 39048682; preprint *The Curse of
> Recursion*, arXiv:2305.17493, 2023). Also arXiv:2510.05133 (2026, synthetic-mixing empirics)
> and arXiv:2502.15654 (2025, detection-as-prevention) confirm it is live, unsolved literature.

Their central finding — verified via WebSearch 2026-07-30:

> *"an **early** model collapse [is distinguished] from a **late** model collapse. In early
> collapse the model begins **losing information about the tails of the distribution**; ... in
> late collapse the model converges to a point estimate with very little variance."*
> The tails of the original distribution **disappear first**.

**The moment that moves first is the high tail. The moment that moves last is the bulk / the
mean.** `renewal_trend` reads a **first-moment share** — a bulk statistic. By the collapse
literature's own result, that is the *last* quantity to shift: the renewal share can read
`balanced` for many generations while the boldest, most-distant novelty has already been culled
from the self-fed pool. We applied HLE at the mean; the early-warning lives in the tail.

## 3. Why the adjacent signs don't catch it either

- `action_occupancy` (normalized Shannon entropy of the per-tool edit distribution) is the
  closest cousin, but **entropy is a whole-distribution scalar dominated by the bulk**. Tail-loss
  with an intact bulk barely moves entropy — that is exactly the early-collapse regime entropy is
  blind to. (Late collapse — variance→0 — *does* crush entropy, but by then it is not early.)
- `channel_variety`/`nfds`/`ecology_potential` are *count / rich-get-richer / evenness* reads over
  the board or persistent-taxa — none isolates the **high tail of a self-fed generative pool**.
- The HELD Hughes block (novelty+learnability) is observer-relative predictability of the whole
  stream, not a two-rate tail-vs-bulk contraction.

## 4. The concept, named

**Early model collapse / "tails-vanish-before-the-mean" as the leading indicator of a
self-consuming variety loss** — distinct from the first-moment renewal share (`renewal_trend`) and
from whole-distribution entropy (`action_occupancy`). It is the *early-warning* half of the same
HLE we already measure at the *bulk*.

## 5. Concrete application (HELD) — `scripts/mesh-vitality`, companion to `renewal_trend()`

`tail_first()` — on the SAME self-fed generative pool `renewal_trend` scans (added-tool commits),
compute a **novelty-distance** per newly-added tool = `1 − max token-Jaccard(new tool, every tool
that existed BEFORE it)` (added-tool A-scan, distance vs the pre-existing corpus only → no
same-window leakage). Then compare the **high tail (P90) recent-vs-prior** against the **median
recent-vs-prior**: `TAILS-THINNING` when P90 falls materially while the median holds (the
Shumailov early signature) — reported *beside* `renewal_trend`, never gating a kill (same
report-only posture as every sign in the file).

**Why HELD, not shipped (honest hollowness check):** only a handful of commits ADD a tool per
40-commit window, so a per-window P90 over ~3 items is noise, not a tail — the exact "a default
indistinguishable from success" trap the operator doctrine warns against. A faithful version needs
either a longer accumulation window or a denser generative distribution (e.g. the boldness of
every commit's *reach into previously-untouched files*, not only tool births) validated against a
real narrowing episode in `vitality.log` before it can even be report-worthy. So this lands as a
`# HELD FIX` note in the file (matching the existing precariousness / Hughes HELD blocks), plus
this doc — **zero behavior change.**

## Sources

- Shumailov et al., *Nature* 631:755 (2024) — https://www.nature.com/articles/s41586-024-07566-y · PubMed 39048682
- *The Curse of Recursion*, arXiv:2305.17493 (2023) — https://arxiv.org/abs/2305.17493
- "Optimized to Death: The Hypernetic Law of Experience", *Systems* 14(2):197 (2026) — https://www.mdpi.com/2079-8954/14/2/197
- Characterizing model behavior under synthetic-data training, arXiv:2510.05133 (2026)
- Ashby, *An Introduction to Cybernetics* (1956) — Law of Experience (variety cannot increase under repeated transformation)
