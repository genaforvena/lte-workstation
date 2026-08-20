# Mere recurrence: the tier calls itself an inheritance channel and 63% of it has no evidence anything was ever transmitted

**Live review, 2026-08-20 — niche construction & the extended phenotype, from the angle the task asked
for: a known CRITIQUE / failure mode of the area.**
Landed in `scripts/mesh-knowledge-sync` (`--lineage`, report-only; uncommitted — steward lands from the tree).

## What was already ours (checked first, so the review could not re-land)

Thirteen prior landings in this area. The four that are *also* critique-angle:

| embodied critique | where |
|---|---|
| **negative** NC / inter-scale conflict / terminator niche (Wade & Sultan) | `mesh-forage:132`, `mesh-knowledge-sync` header |
| **driftability** — NC changes drift probabilities, not just selection (Fabregas-Tejeda & Ramsey 2024) | `mesh-forage` `drift_null()`, `mesh-knowledge-sync --status` |
| the **by-product null** — an adaptive verdict needs the SIGN of the fitness change | `mesh-forage` `nc3()` |
| **NC3 mechanism attribution** — most of what we called NC is choice, not construction | `mesh-forage` `nc3()` |
| the **removal control** (external immunity, *Tribolium* 2025) — ablate the construction | `mesh-ideate:273` |
| **model-collapse / self-referential reviews** (outbound citation axis) | `mesh-knowledge-sync --provenance` |

All six ask about the **construction**: is it real, does it help, does it drift, was it ablated, is the
*review* grounded. None asks whether the claimed **inheritance channel carries anything**. That is the gap.

## The find

**Buskell, A. & Tennie, C. [2025]. "Mere Recurrence and Cumulative Culture at the Margins." *British
Journal for the Philosophy of Science* 76(1):123–145. doi:10.1086/717776.** Preprint:
[PhilSci-Archive 19778](https://philsci-archive.pitt.edu/19778/). Live thread in the same debate, 2025:
**Moore, R. & Tennie, C., "Know-How Copying Is Fundamental to Human Culture: Sterelny, Cultural
Evolution, Niche Construction, and Ecological Inheritance," *BJPS* Letters to the Editors** —
arguing against Sterelny's position that niche construction plus individual learning make copying
largely superfluous. Found by live web search 2026-08-20.

Buskell & Tennie reject the consensus definition of cumulative culture ("high-fidelity transmission
+ incremental improvement") in favour of a **minimal** one built on *copying know-how* and the
**transmission of trait FORM**. Dropping "incremental improvement" buys coverage of marginal cases —
and immediately raises the bill they name:

> **mere recurrence** — distinguishing cumulative culture from *other processes that sustain a
> recurrent behaviour*.

A constructed environment that reliably **re-elicits** a behaviour in every successor produces
observations identical to inheritance — same trait, every generation — while **nothing is transmitted
at all**. Only one of the two accumulates; the other plateaus at whatever a single individual can
re-derive unaided (Tennie's *zone of latent solutions*). This is the sharpest live critique of the
claim that a constructed niche IS a second inheritance channel — and that claim is written verbatim in
the header of `mesh-knowledge-sync`.

## The defect it names in us

`scripts/mesh-knowledge-sync` opens by declaring the tier an extended phenotype and an **ecological
inheritance** channel (Odling-Smee/Laland/Feldman 2003; Lehmann 2008 posthumous extended phenotypes):
a mind writes a doc, the mind is compacted or gone, the doc persists, gossip carries it to every mind
node, and every future mind inherits it.

The mesh's evidence that this **works** is that successors behave consistently with the docs. But a
successor mind re-derives the same fix from the same failure shape **whether or not it ever read the
doc** — and the mesh's minds re-derive constantly; that is what they are for. So:

- `--status` measures **presence** — how many *copies* of a doc exist across nodes.
- the driftability landing measures **copy population** — how exposed a doc is to drift.
- **Neither measures transmission.** Present-on-every-node is a claim about copies, not about anything
  crossing the channel. The tier's central claim had no test.

## The discriminator the paper supplies

Transmission of **trait FORM**. Re-derivation converges on the **function**; copying carries the
**arbitrary specifics**. A successor doc that reuses an ancestor's *coined slug* is evidence the form
crossed the channel; one that reaches the same functional point in independently-invented vocabulary is
**indistinguishable from re-derivation**.

## What landed

`mesh-knowledge-sync --lineage` — read-only, local, no ssh, one awk pass over the tier (~0.4 s for 845
docs). Per doc it counts how many **other** docs reuse its form, and reports the two shapes the critique
cares about. Live on mesh-home, 2026-08-20:

```
lineage (mere-recurrence discriminator — Buskell & Tennie 2025, transmission of trait FORM):
  corpus: 838 doc(s) with a coined (hyphenated, >=8ch) slug, 5 skipped — too short or a single ordinary
          word, which carries no ARBITRARY form and so cannot be transmission evidence
  TRANSMITTED (>=1 other doc reuses this doc's form/slug): 303/838 (36%)
  INDISTINGUISHABLE (0 inbound): 535/838 (63%) — NOT a usage verdict: the content may still recur in
          successors by RE-DERIVATION, and the tier cannot tell that from inheritance
  ACCUMULATION: 166 interior doc(s) (cited AND citing) — chains, vs a flat field of independent re-derivations
  most-transmitted: no-fixed-mind-stigmergic-skeleton(22) survival-without-brains(17)
                    capabilities-are-text(17) tmux-append-only(12) observer-effect-criticality(11)
WARN: 63% of the tier has no inbound form-citation — gossip effort is UNIFORM across a corpus whose
      inheritance claim is untestable for most of it (mere recurrence). Report-only.
```

**63% of the tier is mere-recurrence-indistinguishable, and 20% (166/838) shows the chain structure
that would make it cumulative rather than a flat field of independent re-derivations.** Every one of the
845 docs is gossiped with equal effort.

### The measurement bug the first live run exposed

The first run put `ONBOARDING.md` **second most-transmitted at 21 inbound** — every hit a prose use of
the ordinary noun "onboarding". A stem that is a single common word carries **no arbitrary form**:
successors write it because it is English, not because they inherited it, and counting it *manufactures
transmission edges nobody wrote*. The fix is the paper's own criterion applied to our substrate — a stem
is transmission evidence only if it is a **coined, hyphenated slug**. This is now the `(c)` gate, and it
is the mutant that changes the headline number most.

Two other rules are load-bearing and asserted:
- **self-mention is not transmission** (a doc's own text is excluded from its own count);
- **repeat mentions are one transmission event** (count DOCS, not mentions) — a doc citing a slug
  twenty times did not inherit it twenty times.

And token matching, never `grep -F`: substring matching fires on a stem contained inside a *longer*
stem, inventing edges.

## Gates, each seen RED

| mutant | result |
|---|---|
| drop the arbitrary-form (hyphen) rule | **RED** — `onboarding(3)` becomes top most-transmitted off prose alone |
| count self-mentions as transmission | **RED** — `alpha-beta-gamma(3)`, expected 2 |
| count repeat mentions instead of one event per doc | **RED** — `alpha-beta-gamma(5)`, expected 2 |
| `interior = cited` (lose the chain requirement) | **RED** — accumulation count wrong |
| empty tier renders `0 docs` instead of `na` | **RED** — "an empty tier is BLIND (na), not a 0% corpus" |

Restored green: `smoke-test: ok (… lineage: counts, accumulation, arbitrary-form rule, self/repeat dedup, na-on-empty)`

## What this does NOT claim

- **A leaf is not a useless doc.** The render says `INDISTINGUISHABLE`, never "unused" (asserted). The
  finding is that the tier cannot tell inheritance from re-derivation for that doc.
- **Inbound form-citation is a lower bound on transmission**, not a measure of it. A mind that read a
  doc, acted on it, and never wrote a doc leaves no edge here. The critique's point survives that
  precisely: there is no cheap observation that settles it, which is why the discriminator is form.
- **It measures the doc tier, not the mesh's behaviour.** A stronger test — does a fix cite the doctrine
  it obeys — needs a different substrate (commits, board posts) and is not attempted here.
- **Sync semantics are untouched.** Still newest-wins, still never deletes. What a low-lineage corpus
  should *cost* — gossip priority, a half-life, pruning — is the steward's call, and it composes with
  the two HELD items already in this file's header (the environmental/staleness term, and driftability).

## Sources

- Buskell & Tennie 2025, *BJPS* 76(1):123–145 — https://www.journals.uchicago.edu/doi/10.1086/717776 · preprint https://philsci-archive.pitt.edu/19778/
- Moore & Tennie 2025, *BJPS* Letters to the Editors — https://www.thebsps.org/letters/sterelny-cultural-evolution/
- Scott-Phillips et al. 2014, "The niche construction perspective: a critical appraisal," *Evolution* 68(5):1231 — https://academic.oup.com/evolut/article/68/5/1231/6851729 (read as context: the "includes everything an organism ever does" over-inclusiveness critique; not landed)
- Laland et al., "Niche Construction Theory: A Practical Guide for Ecologists," *QRB* 88(1) — https://www.journals.uchicago.edu/doi/10.1086/669266
