# The ghost: a dead reflex's artifact goes on steering, and nothing measured that

**Live review, 2026-08-19 — niche construction & the extended phenotype, from the angle the task
asked for: a concrete METRIC this area measures itself with.**
Landed in `scripts/mesh-reflex-health` (uncommitted; steward lands from the tree).

## What was already ours

Before searching, the genome's existing footprint in this area, so the review could not re-land on
it:

| embodied | where |
|---|---|
| Fogarty & Wade 2022, niche construction as a modified breeder's equation (feedback term) | `mesh-vitality:488` |
| Odling-Smee/Laland/Feldman 2003, **inceptive vs counteractive** NC | `mesh-ideate:303` |
| Kurtz, **experimental removal** of niche construction | `mesh-ideate:273` |
| Odling-Smee & Endler, NC alters variability/strength of selection | `mesh-reflex-health:465` |
| facilitation-cascade succession of ecosystem engineers | `mesh-reflex-health:617` |
| **negative** niche construction (Wade & Sultan) | `mesh-forage:132`, `mesh-knowledge-sync:27` |
| Ayres et al. 2009 **home-field advantage index** | `mesh-promises --homefield` |
| Martinez-Saito, BUNCH / lifeness `L = t·I` | `mesh-reflex-health` |

Every one of these is about a **living** constructor. That is the shape of the gap.

## The find

**Albertson, L. K., Sklar, L. S., Tumolo, B. B., Cross, W. F., Collins, S. F. & Woods, H. A. (2024).
"The ghosts of ecosystem engineers: Legacy effects of biogenic modifications." *Functional Ecology*
38(1):52–72. doi:10.1111/1365-2435.14222.** Data: Dryad doi:10.5061/dryad.w6m905qss. Part of that
year's *Functional Ecology* special feature on ecosystem engineers (Briones et al.,
doi:10.1111/1365-2435.14418).

A biogenic structure keeps modifying habitat and resource flows **after its builder is gone** — the
**ghost effect**. The review's finding is that legacy persistence is predicted by traits of the
structure and its builder (body size, life span, living strategy), *not* by the builder still being
present; and it names the open end plainly — how engineering influence decays with the structural
legacy over time is unmeasured. Sibling literature reaching the same place: Saldaña et al. 2024
(*TREE*) on dead foundation species, and *Science Advances* "Legacies of foundation species shape
life after death" (doi:10.1126/sciadv.aef9983).

**The concrete metric underneath it** is older and explicit — Jones, Lawton & Shachak, "Organisms as
ecosystem engineers", *Oikos* 69:373–386 (1994), refined in *Ecology* 78(7):1946–1957 (1997). An
engineer's total effect decomposes into six factors, and exactly two of them **survive the
engineer**:

- *the durability of impacts in the absence of the original engineer*
- *the number and type of resource flows modulated… and the number of species depending on these flows*

Ghost magnitude ≈ **durability × recipients**.

## Where it bites us

`mesh-reflex-health`'s entire vocabulary ends at the builder. It declares a reflex DEAD and stops:
the alert names which reflex died and how stale its artifact is, and the story is over. But the
artifact does not stop existing when its writer stops — it sits at its last value and **every
consumer keeps reading it as a current reading**.

Both of Jones's surviving factors were computable and **neither was published per entry**:

- **Durability** — the alert printed bare `age`, which counts the window in which the artifact was
  still legitimate. A reflex one minute past its window and one dead for a day differ only in a
  digit buried in `stale 10801s>600s`.
- **Recipients** — `fanin_count()` already existed, but only to **rank**: `highest_fanin_stale()`
  picks the single widest-blast-radius name as a triage hint and throws every other entry's count
  away. A dead artifact with six live readers and one with none rendered *identically*.

This is not the `value-frozen` or `aliased` axes. Those ask whether a **live** artifact's bytes
move. This asks what a **dead** one is still doing — a question about its readers, not its writer.

## The change

`ghost_clause()` + `ghost_dur()` in `scripts/mesh-reflex-health`, wired into both call sites (the
`--check` STALE line and the `[reflex-stale]` board alert). Report-only; computed only when
something is actually stale.

Live render, two reflexes identically stale for the same 2h50m:

```
· ghost (Jones 1994 durability×recipients; a dead artifact still read is still steering):
  psi(dead 2h50m past its window, 6 reader(s))
  orphan(INERT: dead 2h50m past its window, no reader)
```

**The triage inverts.** A stale reflex nobody reads is an inert legacy — a structure decaying in
place, fixable on its own schedule. A stale reflex *with* readers is a ghost actively steering live
verdicts from a frozen value, and every hour it stays dead is another hour of that. The alert could
not previously tell those apart.

Details that are decisions, not defaults:

- **Durability is age MINUS the window**, never bare age — the artifact was a legitimate reading up
  to `max_age`, so counting age inflates every entry by one full window.
- **A missing artifact renders `absent`, not `dead 0m`** — no age means no measurement, and a
  fabricated 0 would read as a real one (the honest-`na` rule).
- **The product orders; it is never printed as a score** (`a-key-named-price-is-not-a-price`). Both
  factors are shown separately, so `solo(1h, 1 reader)` correctly outranks `foundation(10m, 2
  readers)` without either number pretending to be the magnitude.
- **`age` is now reset per row.** It was only ever assigned in the artifact-exists branch, so a
  *missing* artifact silently inherited the previous reflex's age — a latent bug the ghost factors
  would have consumed directly.

## Gates

6 unit + 2 end-to-end assertions, folded into the existing consumer fixture (the recipient factor
*is* `fanin_count`) and the existing backdated-artifact/stubbed-chat harness. **7 mutants seen
red**: durability using bare age; INERT collapsed into haunting; ordering by reader count alone; a
missing artifact rendered as a 0-second haunting; the clause unwired from `--check`; unwired from
the board alert; the negative-age floor removed.

One methodological note earned during the run: the first mutant pass came back red on
`fanin_count`, not on the ghost gates — mutant copies were named `r.sh`, and `fanin_count`'s
self-exclusion is keyed on `basename $0`, so the fixture's own `mesh-reflex-health` stopped being
excluded and every count read one high. Mutants of this tool must be run under its real filename
(`a-self-exclusion-keyed-on-basename-false-reds-a-renamed-mutant-copy`).

## Not done

Albertson et al.'s actual open question — *how the influence decays* — is still open here too. This
publishes the ghost's magnitude at a point in time; it does not measure the decay curve of a stale
artifact's influence on its readers' verdicts. That would need the readers' outputs held against a
counterfactual, which is the experimental-removal design already embodied in `mesh-ideate`, pointed
at a dead engineer instead of a live one.

## Sources

- Albertson et al. 2024, *Functional Ecology* 38(1):52–72 — https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/1365-2435.14222
- Dryad dataset — https://datadryad.org/dataset/doi:10.5061/dryad.w6m905qss
- Briones et al. 2024, special feature editorial — https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/1365-2435.14418
- Jones, Lawton & Shachak 1994, *Oikos* 69:373–386 — https://webpages.ciencias.ulisboa.pt/~vlamaral/EXPL_MAR-EST_1226_2013_files/7-Jones%201994.pdf
- Jones, Lawton & Shachak 1997, *Ecology* 78(7):1946–1957 — https://esajournals.onlinelibrary.wiley.com/doi/abs/10.1890/0012-9658(1997)078[1946:paneoo]2.0.co;2
- Saldaña et al. 2024, *TREE*, dead foundation species — http://www.altierilab.org/uploads/6/9/0/2/69026451/saldana_etal_2024_tree__dead_foundation_species_drive_ecosystem_dynamics___online_early.pdf
- "Legacies of foundation species shape life after death", *Science Advances* — https://www.science.org/doi/10.1126/sciadv.aef9983
