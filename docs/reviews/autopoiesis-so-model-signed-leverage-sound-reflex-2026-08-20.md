# Autopoiesis / biology of cognition — LIVE literature review, 2026-08-20

**Lane:** autopoiesis & the biology of cognition (Maturana, Varela), angle = an **operational
mechanism** we could implement, not philosophy.
**Standing hazard:** this lane is the most-trodden in `docs/reviews/` — 254 reviews, of which ~12
carry an `autopoiesis-*` slug and ~14 an `enactivism-4e-*` one. Closure, precariousness, adaptivity,
viability space, sympoiesis, semantic closure, constraint conservation are all landed. So the search
was aimed at what the lineage is *publishing now*, not at re-reading Maturana. It landed.

---

## The result

**Natalya Weber, Christian Guckelsberger, Tom Froese, "Untapped Potential in Self-Optimization of
Hopfield Networks: The Creativity of Unsupervised Learning", *Artificial Life* 31(4):435, 2025**
(MIT Press, <https://doi.org/10.1162/ARTL.a.10>); preprint arXiv:2501.04007,
<https://arxiv.org/abs/2501.04007>. Froese is squarely in the Varela lineage — the paper's own frame
is that the Self-Optimization model "has been argued to express characteristics of minimal agency,
which renders it useful for the study of artificial life."

Abstract, verbatim (fetched 2026-08-20):

> The Self-Optimization (SO) model can be considered as the third operational mode of the classical
> Hopfield Network, leveraging the power of associative memory to enhance optimization performance.
> Moreover, it has been argued to express characteristics of minimal agency, which renders it useful
> for the study of artificial life. In this article, we draw attention to another facet of the SO
> model: its capacity for creativity. Drawing on creativity studies, we argue that the model
> satisfies the necessary and sufficient conditions of a creative process. Moreover, we show that
> learning is needed to find creative outcomes above chance probability. Furthermore, we demonstrate
> that modifying the learning parameters in the SO model gives rise to four different regimes that
> can account for both creative products and inconclusive outcomes, thus providing a framework for
> studying and understanding the emergence of creative behaviors in artificial systems that learn.

### The mechanism

The SO loop: relax a Hopfield network to an attractor, **reset** the state, **Hebbian-imprint the
visited attractor into the weights**, repeat. Basins of the visited minima widen, and the restructured
system settles into a better optimum from any start than plain relaxation reaches.

The paper's contribution is the **regime map over the learning rate α**, measured against a *frozen
no-learning baseline* (1000 resets before learning / 1000 during / 1000 after). Two axes, both
defined relative to the before-learning distribution: **novel** = an attractor not visited before
learning; **appropriate** = converged, and to an energy below the pre-learning mean. Verbatim from
the paper (fetched 2026-08-20):

> For a very low learning rate α, there is insufficient learning and there is no convergence
> (Fig. 4a) … For a very high learning rate, the weight matrix is updated according to some initial
> state prior to convergence to a local minimum. This may result in a novel state, but it is not
> appropriate since it does not have any trace of the constraints of the original constraint
> optimization problem … If the learning rate is in an intermediate range … The typical case is
> convergence to a lower energy, but that energy is still within the range of the distribution
> before learning (Fig. 4c), so it is appropriate, but not novel. For some α, the converged energy
> of the system is below the non-learning distribution (Fig. 4d), and hence is appropriate and novel.

And the line that carries the whole operational content:

> In this sense, α can be considered the rate at which one leverages prior experience. Decreasing the
> learning rate too much renders the solution no longer novel, increasing it too much, it is no
> longer appropriate.

### The mechanism we do NOT embody

Not "closure", not "adaptivity" — landed already. **The un-embodied mechanism is that the leverage of
prior experience must be SIGNED by the appropriateness of that experience.** The SO model imprints
whatever attractor it happened to visit, *unsigned*, and the paper's finding is that whether this
helps or harms is decided entirely by one rate that the system does not adapt.

`scripts/mesh-sound-reflex` runs the same loop with the sign flipped — taste memory as a repulsor,
declared in the source: *"Taste memory as a REPULSOR, not a template: the character says where to
aim, history says where we may not land."* — and it has **exactly the unsigned defect**. At
`derive()`:

```python
repel = recent + failed          # recent = renders that SHIPPED
                                 # failed = renders our own verdict called hollow/degenerate
```

and then one `epsilon` (0.22) is applied to the pooled list. **A render the operator kept and a
render we ourselves rejected push the search away by the same 0.22.** One rate cannot express *"come
back here for variety's sake, but never come back HERE"* — and 0.22 is a constant with no live
evidence behind it, the same shape as the frozen `n=29` prior medians `CLAUDE.md` already records
rotting in this very file.

Measured on the real gate before the change (empty params log, one rejected recipe seeded, so the
reported `novelty` *is* the distance to the rejected recipe):

```
unsigned: RECIPE amc l 500 w 5 ss 0.5 s 2.0 … fit 0.22 novelty 0.22 … avoid hard/0.22
```

The next recipe parks at 0.22 — flush against the wall — from a combination we have a verdict saying
renders hollow. That is the paper's regime where prior experience is leveraged at a rate that carries
no trace of the constraint it was supposed to satisfy, and nothing in the reflex could see it.

## The change (uncommitted, in tree)

`scripts/mesh-sound-reflex` — the signed half of the repellent.

- `SR_EPSILON_FAILED` (default `2 × SR_EPSILON`): the wall against the *rejected* store, separate
  from the wall against the *shipped* store. **Declared, not derived** — 2× is a starting point, and
  the review does not pretend otherwise; the paper's own finding is that the right α is empirical
  and seed-dependent, which is precisely why it must be a legible column rather than an invisible
  constant.
- **A preference, never a hard wall** — the same shape (and the same reason) the file already gives
  tempo-band rotation: raising the wall on a store of up to `SR_RECENT` entries can empty the
  admissible set, and a `WALKED-OUT` manufactured by the appropriateness preference would be the
  tail wagging the dog. Tier order: *(clears failed-eps + fresh band) > (clears failed-eps) >
  (fresh band) > (nearest-ideal)*. Appropriateness is the outer preference, variety the inner one.
- **The tier that won is published**: the `RECIPE` line now carries `avoid <hard|soft|none>/<eps>`.
  A preference that silently falls back is indistinguishable from one that bit, and an `avoid=hard`
  minted against an *empty* rejected store would be a bite that never happened — both are refused
  by their own test legs. The token sits after the ` ~ ` meta separator, so every consumer that
  splits on it is unaffected (checked: all consumers are in-file, `scripts/mesh-sound-reflex:1804`
  and `:2076`).

After, same fixture:

```
signed:   RECIPE amc l 160 w 4 ss 1.5 s 0.25 … fit 0.44 novelty 0.44 … avoid hard/0.44
```

### Gate — seen RED, then green

New `--test` leg **3c**, four assertions, the first two each other's red (leg 3b only pinned that a
hollow recipe repels *at all*, never that it repels *harder*):

1. signed arm stands ≥ `EPS_FAILED` from the rejected recipe;
2. unsigned control (`EPS_FAILED=EPSILON`) parks *inside* that — if this arm also cleared, the leg
   above is passing on something other than the signed epsilon;
3. `EPS_FAILED=9` still grinds (no manufactured `WALKED-OUT`) and reports `avoid=soft`;
4. an empty rejected store reports `avoid=none`.

Both breaks driven and watched:

| break | red |
|---|---|
| `eps_failed = epsilon` (collapse to unsigned) | 2 FAILs — "the next recipe sits 0.22 from a recipe our OWN verdict called hollow"; "EPS_FAILED=9 … did not report avoid=soft" |
| `avoid` hardcoded to `"hard"` | 2 FAILs — the fallback leg and the empty-store leg |
| restored | `--test` exit 0, `smoke-test: ok`, 0 FAILs |

## Scope, stated

Primary grid only (`f/s/ss/w/c`). Grids B and C go through `nearest_ideal()`, which already falls
back to the ideal itself rather than refusing, and carries a different tradeoff; extending the signed
epsilon there is a separate call, not smuggled in here.

Not taken up: the paper's *attraction* half — imprinting good attractors so their basins widen. That
fights an explicit operator design decision (repulsor, not template) and would need him, not a
review.

## Cite

- Weber N., Guckelsberger C., Froese T. (2025). *Untapped Potential in Self-Optimization of Hopfield
  Networks: The Creativity of Unsupervised Learning.* Artificial Life 31(4):435.
  <https://doi.org/10.1162/ARTL.a.10> · arXiv:2501.04007 <https://arxiv.org/abs/2501.04007>
- Di Paolo E. (2005). *Autopoiesis, adaptivity, teleology, agency.* Phenom. Cogn. Sci. 4:429–452.
  <https://doi.org/10.1007/s11097-005-9002-y> — the adaptivity layer this lane already embodies;
  read to confirm the SO regime map is not a restatement of it. It is not: adaptivity is about
  regulating *with respect to* viability conditions, the SO regimes are about the *rate* at which
  past outcomes are allowed to reshape the search.
