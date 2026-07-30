# Live-literature review — active inference: NOVELTY vs SALIENCE, and the reliability estimate that never says how sure it is

Date: 2026-07-27 · lane: genome (idea-queue LITERATURE task) · status: fix in tree, uncommitted

## Where we had already been (so this doesn't double-count)

The mesh has landed the Free Energy Principle / Active Inference (Friston) canon almost exhaustively:

- **precision-weighting** — `scripts/mesh-precision` (inverse-variance reliability; 2026-07-05)
- **prediction-error / Shannon-surprise**, incl. epistemic-vs-aleatoric / volatility-scaled — `scripts/mesh-novelty`
- **Markov blanket / PEARL partition** — `scripts/mesh-perimeter`
- **good regulator** — `scripts/mesh-homeostasis`
- **Expected Free Energy / active sensing** — `scripts/mesh-interruptibility --probe`
  (`review-efe-epistemic-active-sensing-2026-07-04`)
- homeostatic setpoint / allostasis / CSD — the `docs/reviews/` allostasis + soc-homeostatic set.

That `--probe` landing is the key one: it built EFE's **action** half — "when the posterior is diffuse,
ACT to reduce the uncertainty." But by its own note it embodies exactly **one** of EFE's two epistemic
drives.

## The mechanism not yet embodied — NOVELTY (as distinct from SALIENCE)

The active-inference literature draws a sharp, operational line, usually stated as: **"salience is to
inference as novelty is to learning."** Expected information gain splits by *what* it reduces
uncertainty about:

- **SALIENCE** = expected info gain about hidden **STATES** — act to resolve *where the world is now*.
  This is `mesh-interruptibility --probe` (nominate the sense whose refresh best disambiguates the
  current band).
- **NOVELTY** = expected info gain about **MODEL PARAMETERS** — act to resolve *how my model works*;
  the uncertainty that is **reducible by sampling**. Parameter uncertainty is carried by Dirichlet
  counts: a parameter estimated from **few** observations is under-determined, and a fresh sample there
  has high novelty value.

### The live source

Searched current literature, not a fixed list:

- **Shuo Zhang, Yan Tian, Quanying Liu, Haiyan Wu, "The Neural Correlates of Novelty and Variability in
  Human Decision-Making under an Active Inference Framework", eLife** — Version of Record
  **2025-03-21** (v3 reviewed preprint 2025-02-28), <https://elifesciences.org/reviewed-preprints/92892>.
  Peer-review round pinned the terminology precisely: **novelty = "expected information gain about
  parameters"** (uncertainty reducible through sampling), explicitly separated from salience (variance
  inherent in the environment). Aligned to the Schwartenbeck framework.
- Canonical prior (the mechanism's origin): Friston, Lin, Frith, Pezzulo, Hobson, Ondobaka, **"Active
  inference, curiosity and insight", Neural Computation 29:2633 (2017)** — where the novelty term
  (info gain about model parameters / the Dirichlet `a` counts) is derived as curiosity.
- Read in the same sweep for the state/parameter framing: "Value of Information and Reward Specification
  in Active Inference" (arXiv:2408.06542, 2024); "Sophisticated Inference" (arXiv:2006.04120).

## The gap in the mesh, measured against the tool itself

`mesh-precision` estimates a sense's reliability (precision = inverse variance for `--num`, stability =
1 − switch-rate for `--cat`) and **reports its sample count `n`** — but the **verdict token is asserted
with the same confidence at n=2 as at n=2000.** `RELIABLE(n=3)` and `RELIABLE(n=2000)` printed
identically:

```
precision[num]: RELIABLE — coeff-of-variation=0.009, mean=50.3, sd=0.471 (n=3)
```

`RELIABLE(n=3)` is **not** "low precision" — we do not *know* the sense is noisy. It is high-**novelty**:
the reliability parameter itself is under-determined; a sample there teaches us *how the sense behaves*.
Down-weighting a NOISY sense (we know it's noisy) and active-sampling an UNDER-DETERMINED sense (we
don't yet know) are **opposite actions** the tool could not previously tell apart. (`FROZEN_MIN_N=5` was
already this exact idea applied to one verdict — don't call a flatline FROZEN until enough samples; the
novelty axis generalises it to every verdict.)

## The fix — one file: `scripts/mesh-precision` (in tree, uncommitted)

A **NOVELTY axis** on `--num`/`--cat` output. Every reliability verdict now carries `novelty=HIGH|LOW`
keyed on `n` vs `MESH_PREC_NOVELTY_MIN_N` (default **8** — the point at which the ~`1/sqrt(2n)` standard
error of an estimated sd / switch-rate falls under ~25%):

```
precision[num]: RELIABLE — cv=0.009 … (n=3) · novelty=HIGH (reliability parameter under-determined,
   n<8 — active-LEARNING candidate: sample to resolve it, don't yet act on the verdict)
precision[num]: RELIABLE — cv=0.013 … (n=9) · novelty=LOW (reliability well-determined)
```

`--json` gains `"novelty":"HIGH|LOW","novelty_min_n":8`. It is the **NOVELTY complement to `--probe`'s
SALIENCE**: `--probe` says *sample X to learn the STATE*; this says *sample X to learn the MODEL of X*.
**Report-only / advisory** — it never overrides a verdict or a weight; a consumer weighting fusion must
not treat a HIGH-novelty RELIABLE as settled. Scope: the general `--num`/`--cat` tape analyzer (where
consumers weight fusion); `--room-flap` keeps its existing `len(ev)<2→UNKNOWN` floor — the same
under-determined idea at its own `n` boundary.

## Gate (RED-first verified)

`mesh-precision --test` gains two real-path assertions: a short tape (n=3 < min) → `novelty=HIGH`, a
long tape (n=9 ≥ min) → `novelty=LOW`. Falsified both ways via the knob: `MESH_PREC_NOVELTY_MIN_N=0`
makes nothing under-determined, so the short-tape HIGH assertion goes **red**
(`got novelty=LOW, novelty_min_n=0`); restoring the default goes green. Verified on the edited genome
with `bash ./mesh-precision --test` (`$0`-via-PATH otherwise runs the deployed copy — the drift note).

## Why not discarded

Discardable only if the mesh already distinguished "we know this sense is noisy" from "we haven't
sampled it enough to know" — it did not: `mesh-precision` printed `n` but never *used* it as a
second-order confidence, and `--probe` is state-side (salience) by its own header. The salience/novelty
pair is a first-class, citeable AIF distinction (Zhang et al. 2025; Friston et al. 2017), and the fix is
cheap, read-only, and fits the file it extends.

## Sources

- Zhang, Tian, Liu, Wu — eLife 2025 — <https://elifesciences.org/reviewed-preprints/92892>
- Friston, Lin, Frith, Pezzulo, Hobson, Ondobaka — "Active inference, curiosity and insight", Neural
  Computation 29:2633 (2017)
- "Value of Information and Reward Specification in Active Inference" — arXiv:2408.06542 (2024)
