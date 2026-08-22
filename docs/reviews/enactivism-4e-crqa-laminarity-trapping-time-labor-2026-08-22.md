# The tool that names the instrument and does not use it: laminarity, trapping time, and a lag-1 lift wearing CRQA's clothes

**Live review, 2026-08-22 — enactivism & 4E cognition, from the angle the task asked for: a concrete
METRIC or experiment the area uses to measure itself.**
Landed in `scripts/mesh-labor` (`--crqa`, read-only; uncommitted — steward lands from the tree).

## What was already ours

Fifteen prior 4E/enactivism landings, several of them metrics: interaction autonomy · participatory
coupling · complexity matching (lead–lag) · coordination MTTR-A · agency-gated credit · enactive
valence · the sensorimotor environment `s = g(m)` · precariousness · hostile scaffolding · role cycling
· representation-hungry absence.

`grep -c CRQA` over the corpus returns 11 hits, so the *name* is thoroughly ours. The implementation is
not. `scripts/mesh-labor:518` says so in its own comment —

> "The field's instrument is cross-recurrence quantification (CRQA; e.g. inter-brain coupling in
> naturalistic interaction, PMC12833299, 2026). … This is a lightweight **directed cross-recurrence**
> over the per-window turn series"

— and then `_coupling_py` computes a **lag-1 conditional lift**: does x acting in a bin raise y's rate
in the *next* bin above y's base rate. One lag, one direction, no recurrence matrix, no line
structure. It is a perfectly reasonable statistic. It is not CRQA, and the difference is not cosmetic.

## The find

**Goldstein, B. M. et al. (2026). "Cross-recurrence quantification analysis captures inter-brain
coupling during naturalistic negotiation: a new dynamic approach for hyperscanning."
[PMC12833299](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12833299/)**, published 2026-01-12 — the
paper `mesh-labor` already cites. Its result is the one that matters here:

> conventional measures of neural synchrony, such as **inter-subject correlation and wavelet coherence,
> showed no relationships with outcomes**, while **CRQA revealed systematic associations** between
> dynamic coupling patterns and successful interaction.

i.e. the coarse synchrony statistic found *nothing* on data where the recurrence **structure** found
something. The live thread continues in the perceptual-crossing paradigm — [Dancing together in virtual
space, *Cognitive Processing* 2025](https://link.springer.com/article/10.1007/s10339-025-01306-4) —
and in the method literature ([multivariate joint RQA, arXiv:2303.16907](https://arxiv.org/pdf/2303.16907)).

CRQA's content is the **line structure of the recurrence plot**, and it separates two things a lag-1
lift scores identically:

| measure | geometry | what it distinguishes |
|---|---|---|
| **DET** | DIAGONAL lines | a *sustained shared trajectory* vs a pile of isolated coincidences |
| **LAM** / **TT** | VERTICAL lines | **intermittency** — how much of the recurrence is the pair sitting **trapped in one shared state** rather than moving together through states |

The vertical axis is the gap. `grep -i laminarity` over 283 reviews and the whole `scripts/` tree
returns one passing mention and **no implementation anywhere in the genome**. High DET with high LAM is
not coordination — it is two windows stuck in the same rut, and the mesh had no way to say it.

## What landed

`mesh-labor --crqa`, over the same `spend.log` turn series `--coupling` already reads:

```
CRQA_SPORADIC rr=0.138 det=0.021 lam=0.470 tt=19.04 eps=8.711 idle_frac=0.807 mask_saturated=no
              windows=6 bins=56 pairs=15
```

- **Recurrence on the per-bin turn RATE** (each series normalised by its own mean), so a fast window
  and a slow one can still recur — never on bare presence.
- **`eps` is searched, not pinned.** Standard CRQA practice fixes the radius so RR lands on a target
  (~5%); the radius is re-derived per call and **published with the reading**, so the numbers are
  reproducible and a shifting corpus cannot silently re-scale the verdict.
- **The verdict names a structure, not a score**: `CRQA_TRAJECTORY` (det > lam) · `CRQA_TRAPPED`
  (lam ≥ det) · `CRQA_SPORADIC` (det < 0.30) · `CRQA_UNKNOWN` with every measure `na`.
- Read-only and advisory. `--coupling` is untouched.

### Two coverage terms, both learned the hard way

**`idle_frac`** — the share of the plane that is both-idle. **The first cut of this counted idle-idle
bin pairs as recurrences and read `rr=0.809 det=0.951 lam=0.989 eps=0.000` on the live 5h window**: the
radius search had nowhere to go, because the mesh being asleep already met the RR target on its own. A
shared *silence* is not a shared *trajectory*. Both-idle is now excluded, and the share it would have
contributed is published as coverage — a reading at `idle_frac=0.92` rests on 8% of the plane.

**`mask_saturated`** — on a sparse corpus the radius search can only reach the RR target by widening
`eps` until every non-idle pair is inside it; RR then equals the non-idle share and DET/LAM are
measuring the **activity mask**, not amplitude similarity. That is still a legitimate reading
(categorical CRQA, Coco & Dale) but a *different* one, so it says which it is instead of wearing the
continuous reading's clothes.

## Verification

GATE 8 in `mesh-labor --test`: an in-step ramp (both windows 1,2,3,1,2,3…) must read `TRAJECTORY`;
flat co-activity must produce a structure verdict carrying a `tt=`; every reading must publish
`rr/det/lam/eps/idle_frac/mask_saturated`; a **sparse** pair with long shared silences must report a
large `idle_frac` **and keep `eps > 0`**; and a lone active window must read `UNKNOWN` with every
measure `na`, never 0.

Driven red three ways, green restored each time:

| mutation | result |
|---|---|
| score verticals as diagonals (delete the LAM/TT axis) | `✗ in-step ramp should read TRAJECTORY, got 'CRQA_TRAPPED … det=1.000 lam=1.000'` |
| restore both-idle recurrence (the degenerate first cut) | `✗ eps collapsed to 0 — shared SILENCE is being counted as shared trajectory` |
| render `UNKNOWN` as 0 instead of `na` | `✗ lone window should read UNKNOWN/na, got 'rr=0 det=0 lam=0 tt=0'` |

The both-idle mutation **survived the first version of GATE 8**, because the trajectory/trapped
fixtures are dense (`idle_frac=0.000`) and never exercise the guard. The sparse fixture exists because
of that miss — a guard driven only where it cannot bite is not a guard.

## Sources

- [Goldstein et al. 2026, CRQA captures inter-brain coupling during naturalistic negotiation (PMC12833299)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12833299/)
- [Dancing together in virtual space: perceptual crossing, *Cognitive Processing* 2025](https://link.springer.com/article/10.1007/s10339-025-01306-4)
- [Multivariate Joint Recurrence Quantification Analysis (arXiv:2303.16907)](https://arxiv.org/pdf/2303.16907)
- [Cross-Recurrence Quantification Analysis of Categorical and Continuous Time Series (arXiv:1310.0201)](https://arxiv.org/pdf/1310.0201)
