# Niche construction — the HERITABILITY-INFLATION diagnostic (realized h² > 1)

**Live review, genome, 2026-07-31.** Area: **niche construction & the extended phenotype**, angle the
task asked for — a **concrete METRIC the field uses to measure ITSELF**. Landed as a HELD instrument-axis
in `scripts/mesh-forage`.

## The metric we did not embody

Niche-construction theory has a quantitative-genetics wing whose sharpest, most operational contribution
is a *measurement diagnostic*, not another mechanism:

> **Fogarty, Laurel & Wade, Michael J. (2022)** "Niche construction in quantitative traits: heritability
> and response to selection", *Proc. R. Soc. B* **289**(1976):20220401. doi:10.1098/rspb.2022.0401.
> PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC9156914/

They rewrite the breeder's equation **R = h²·S** so that the environment an organism constructs is itself
*inherited* across generations (their multi-generational accumulation term **M = Σ μᵗ**, resource decay
**μ**, niche-construction coupling **Ψ**). The consequence is that heritability splits into several
non-equivalent definitions that classical theory collapses into one, and the **realized** heritability

  h₂² = (G₁₁ + 2·N·Ψ·G₁₂ + Ψ²·N²·G₂₂) / P

**can exceed 1** — a value additive genetics forbids. So `h² > 1` is not estimation noise: it is a
**positive signature** that the *constructed niche*, not genetic variance, is doing the selecting — the
response over-runs the selection differential that was actually applied. That is the field's own
self-diagnostic for runaway niche construction.

## Why it is genuinely un-embodied (honest audit)

We already carry three niche-construction landings, and this is none of them:

- **`mesh-knowledge-sync` (2026-06-22)** — the *inheritance channel* (docs as a gossiped second
  inheritance line) + its missing negative/environmental term. Existence of the channel, not a
  response/selection measurement.
- **`mesh-forage` terminator axis (2026-07-29)** — *negative NC / inter-scale conflict*: a LOAD
  trajectory (chatter/settled) compared across two time scales. Habitat degradation, not heritability.
- **niche-construction removal-control (2026-07-28)** — the *ablation test* (external immunity removal).
  A load-bearing method, not a scalar over the live field.

Every axis in `mesh-forage` reads the **response alone** — the `[done]`/chatter distribution the colony
produced. None separates response from the selection applied. That separation is exactly Fogarty–Wade's
contribution, and it is the one quantity a response-only read structurally cannot recover.

## Where it bites — `scripts/mesh-forage` (the NC organ)

On the board both quantities are present but never paired:

- the **`[done]` histogram** is the **response** — what each lane actually landed;
- the **owner-tagged `[task]` demand histogram** is the nearest **selection** signal — what the colony
  was *asked* to land, per lane.

The realized-heritability analog, per lane:

  ĥ = (lane's share of recent `[done]`) / (lane's share of open `[task]` demand)

- **ĥ ≈ 1** — response tracks demand (healthy).
- **ĥ ≫ 1** — a lane lands far past what its demand justifies: its own accumulated success is biasing
  dispatch back to it — the pheromone/niche *is* the selector (Fogarty–Wade's forbidden h² > 1), a
  runaway distinct from mere concentration.

Distinct from the siblings: **not** the entropy axis (evenness of `[done]` alone, blind to demand),
**not** the terminator axis (a two-scale LOAD trajectory), **not** the no-entry axis (abandoned
`[taking]`s). It is the response/selection **ratio within one window**.

## Why HELD, not a shipped live axis

The **estimator** is a judgment call the steward owns: board `[task]` demand is sparse and unevenly
owner-tagged, so it is a noisy proxy for a selection differential. Calibrating it — or substituting
dispatch-weight / `mesh-labor` $-demand as the selection axis — is the open decision. Naming the
diagnostic + the forbidden-signature threshold (ĥ > 1) is shippable; the estimator is not. This mirrors
the 2026-06-22 `mesh-knowledge-sync` comment-only inoculation (held-behavioral fix).

## Verified (real artifacts)

- `bash -n scripts/mesh-forage` → clean.
- `git diff --numstat scripts/mesh-forage` → **34 insertions, 0 deletions**; non-comment added lines =
  **0** → zero behaviour change, rc unchanged.
- `bash scripts/mesh-forage --test` → **PASS**, rc=0 (all existing falsifiers still red-first; the
  comment block touches no code path).

## Sources

- Fogarty & Wade (2022), *Proc. R. Soc. B* 289:20220401 — https://pmc.ncbi.nlm.nih.gov/articles/PMC9156914/
- Royal Society landing — https://royalsocietypublishing.org/doi/10.1098/rspb.2022.0401
- Wade & Sultan (2023), "Niche construction and the environmental term of the Price equation",
  *Evol. Dev.* — https://onlinelibrary.wiley.com/doi/abs/10.1111/ede.12452 (companion; already cited by
  the 2026-06-22 landing)

Codebase grounding: `scripts/mesh-forage` (entropy / no-entry / terminator / rupture / drive axes,
all response-only); sibling NC landings `mesh-knowledge-sync` (inheritance channel) and the 07-28/07-29
`mesh-forage` axes (removal control / terminator).
