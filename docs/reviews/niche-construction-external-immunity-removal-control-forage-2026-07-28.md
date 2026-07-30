# Niche construction & the extended phenotype — the REMOVAL control (external immunity)

**Live review, genome, 2026-07-28.** Area: niche construction / extended phenotype. Angle: a
**recent (2025) experimental result** and the one method it contributes that our whole swarm/stigmergy
review set skipped — not another pheromone signal, but the **load-bearing test** for the signals we
already built.

## The recent result

Odling-Smee & Laland's niche construction theory (NCT) and Dawkins' extended phenotype both say an
organism's environmental modifications feed back onto selection — but for decades this was argued from
models, not ablated in the lab. A **2025 bioRxiv preprint** closed that gap experimentally:

> **"Experimental Removal of Niche Construction Alters the Pace and Mechanisms of Resistance
> Evolution"** (bioRxiv 2025.03.27.645637, posted 2025-03).
> https://www.biorxiv.org/content/10.1101/2025.03.27.645637v1

Red flour beetles (*Tribolium castaneum*) secrete a benzoquinone-rich stink-gland fluid **into the
shared flour** — an antimicrobial "external immunity" that suppresses the entomopathogen *Bacillus
thuringiensis* (Bt) for **every beetle in the substrate**, not just the secretor. This secretion is
the textbook extended-phenotype / niche-construction artefact: it persists in the environment and
biases the selection its makers and descendants experience. (The same benzoquinone doubles as a
density-dependent pheromone — aggregation at low concentration, repellent/autotoxic at high — the
"external immunity" review lineage in *PMC9941273* / *Sci. Rep.*.)

The experiment **removed the niche construction** by RNAi-silencing the gene needed to produce the
secretion, then evolved beetles against Bt **with vs without** the secretion. Two results:

1. **Pace.** With construction intact, resistance was acquired **as early as 3 generations** — the
   environmental buffer *facilitated* adaptation. Remove it and adaptation slows.
2. **Mechanism.** RNAseq showed the **genetic pathways** to resistance *differed* between regimes.
   The external buffer did not just speed adaptation — it changed **which** internal solutions got
   selected. Environmental modification and genetic change are **coupled**.

The transferable move is not "beetles secrete stuff." It is the **removal control**: you only know an
environmental modification is *load-bearing* for a collective's adaptation by **ablating it and
measuring that adaptation degrades**. An artefact you never remove might be doing nothing.

## What the mesh already embodies

A great deal. The mesh's shared substrate (`~/.mesh/traces.log`, `chat.log`, and the CLAUDE.md
doctrine) is a niche-construction field, and the swarm review set already lays down the signals:

- **Positive pheromone** — `mesh-forage` reads the Shannon entropy of the `[done]` distribution.
- **Negative pheromone** — the "no-entry" repellent (`swarm-no-entry-repellent-*`): an abandoned
  `[taking]` is a forager that entered an unrewarding branch.
- **Ecological inheritance** — every `Extend it to…` doctrine line is one mind depositing "external
  immunity" against a recurring bug-class (silent fallback, vacuous gate, inert axis) into the shared
  substrate that **all future minds inherit** on a fresh `/clear`. That *is* niche construction with
  ecological inheritance, and it is real.

## The gap the 2025 result exposes

**Not one of the mesh's stigmergic signals has a removal control, and — checked in source — the loop
is open: dispatch never reads them.** `mesh-forage` is `rc`-unchanged, read-only by its own header
("Read-only still… left unwired", `scripts/mesh-forage:61`; "never a red gate", `:98`). `mesh-mind-control`
`--dispatch` does **not** consume the pheromone or repellent map (`grep -n forage|repellent|pheromone
scripts/mesh-mind-control` → only a prose mention, `:193`). So the pheromone-field entropy and the
no-entry repellent are **measured but never acted on**.

Run the beetle paper's test on them: *ablate the repellent — does the collective's adaptation
degrade?* No — because nothing reads it, removal changes **nothing**. By the mesh's own doctrine ("a
gate you have not seen FAIL is not a gate"; "an unseen reflex is absent"; the `umwelt-degeneracy inert
axis` review), a niche-construction signal that survives its own removal untouched **is currently
inert as niche construction** — a `[done]`-histogram and a repellent *map*, not a feedback loop onto
selection. `mesh-forage:53` even *aspires* to the control ("the repellent measurably improves
exploration/coverage over attractant-only colonies") but the loop that would make it testable was
"left unwired."

This is the meta-move the six swarm reviews skipped: they each **added a signal**; none proved any
signal is **causally coupled** to what the colony does next.

## Concrete application — name the file

Close the loop minimally, then gate it with a removal control.

- **`scripts/mesh-mind-control`** (`--dispatch`, the pick / decision point): read `mesh-forage`'s
  no-entry repellent (the aged/abandoned `[taking]` set, already computed via `mesh-promises`) and
  **DE-prioritise** a task/lane carrying a live repellent trail on the next pick — exactly the
  "surfacing … for dispatch to DE-weight a repelled lane at the pick" that `mesh-forage:61` names as
  the unwired next step. This is the *only* change that turns the repellent from a map into niche
  construction.
- **`scripts/mesh-forage`** (`--test`, the acceptance gate): add the **removal control** as the
  test, mirroring the RNAi ablation. Drive the board fixture **with** and **without** the repellent
  term wired into the pick, and assert the WITH regime lowers the **re-claim rate of abandoned
  `[taking]`s** (foragers re-entering the empty branch). If ablating the repellent does **not** raise
  re-claims, the signal is inert and the test must go RED — the mesh's standing rule that a control
  which cannot fail asserts nothing. This is the beetle experiment in one gate: remove the
  construction, watch adaptation degrade, or admit it was decoration.

**Landing rule:** the pick is `mesh-mind-control` routing — single-writer, mind's own hands; wire it
only as a DE-weight (never a hard skip — a repelled task an operator marks `priority:incident` must
still win), and prove it under `mesh-forage --test`'s removal control before trusting it. Until that
control is green, the repellent stays the honest read-only map it is today.

## One-line verdict

Not a discard: niche construction is well embodied as *signals*, but the 2025 removal experiment names
a real, unfilled gap — **no mesh stigmergic signal has been shown load-bearing by ablation**, and the
one that most cheaply can (`mesh-forage`'s no-entry repellent → `mesh-mind-control --dispatch`) is
proposed above with its removal control as the gate.

**Sources.**
- bioRxiv 2025.03.27.645637 — *Experimental Removal of Niche Construction Alters the Pace and
  Mechanisms of Resistance Evolution* — https://www.biorxiv.org/content/10.1101/2025.03.27.645637v1
- Lala et al. 2024, *Palaeontology* — niche construction biases variation exposed to selection —
  https://onlinelibrary.wiley.com/doi/full/10.1111/pala.12719
- *Tribolium* external immunity / benzoquinone as antimicrobial + density-dependent pheromone —
  https://pmc.ncbi.nlm.nih.gov/articles/PMC9941273/
- Ecological inheritance — https://en.wikipedia.org/wiki/Ecological_inheritance
