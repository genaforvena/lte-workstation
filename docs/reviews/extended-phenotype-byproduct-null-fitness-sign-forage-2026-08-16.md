# The by-product null: an adaptive verdict needs the SIGN of the fitness change

**Live review** — niche construction & the extended phenotype, angle = a foundational idea we
applied too loosely. Landing site: `scripts/mesh-forage` (`nc3()`). 2026-08-16, genome.

## What we already embodied (checked first)

Six axes from this area are already in `mesh-forage`: external immunity/removal (2026-07-28),
the negative inter-scale terminator niche (Coninx 2023), realized-heritability inflation (held,
comment only), collective social niche construction (Sueur/Solé/Deneubourg 2026), driftability as
the variance channel (Fábregas-Tejeda & Ramsey 2024), and NC3 mechanism attribution — choice vs
conformance vs construction (Trappes et al. 2022; Krüger et al. 2026, landed 2026-08-15).

All six are on the **niche-construction** side of the literature. Nothing had come from the
**extended-phenotype** side, and that turns out not to be a gap of coverage but of discipline.

## The concept we did not embody

**The by-product / pathology null, and the fact that only ONE of the four famous criteria for an
adaptive claim survives its own author's review — the fitness effect on the actor.**

The two vocabularies are not synonyms, and the difference is precisely this axis. From the Laland
group's own site (`nicheconstruction.com/what-is-it/related-concepts`, ©2024, citing Dawkins 1982):

> "'Extended phenotype' is a narrower term than niche construction, because it is restricted to
> forms of environmental modification that are **biological adaptations**."

while niche construction deliberately "incorporates evolutionary by-products" — a trait counts as
niche-constructing "regardless of its influence on fitness". So an environmental footprint alone
licenses the NC vocabulary and **not** the adaptive one.

The discipline for the adaptive claim was built in the host-manipulation literature, where the
question is identical: is this something the parasite *does* to the host, or is it just what a sick
animal looks like? Poulin's (1995) four criteria — a priori design conformity including **timing**,
complexity, convergence across unrelated lineages, and fitness benefit to the actor — are the
canonical answer, and the citation almost everyone stops at. Read to the end of the section:

> "In hindsight, Poulin's (1995) criteria as a whole were probably much too strict, or at the very
> least overly conservative. **It is only the fourth, concerning fitness effects for the parasite,
> that should really matter.** Whether the manipulation is simple or complex, whether it seems a
> good fit to its function or not, and whatever its evolutionary origins, it will be favored and/or
> maintained by selection if it improves the fitness of the parasite, making it a true adaptation."

And the null is the *default*, not the alternative:

> "No one expects a sick animal to behave normally. Therefore, the simplest, most parsimonious
> explanation for a difference in behavior … need only involve side-effects of pathology."

**Source:** Poulin R (2010) *Parasite Manipulation of Host Behavior: An Update and Frequently Asked
Questions*, Advances in the Study of Behavior 41:151–186, Academic Press,
doi:10.1016/S0065-3454(10)41005-0 — section II, pp. 153–156. Read as the author's own PDF at
`otago.ac.nz/parasitegroup/PDF papers/Poulin2010-ASB.pdf`.

**The live end (2025):** Miroliubov A, Lianguzova A & Libersat F (2025) *Neural strategies in
parasitic manipulation*, Trends in Parasitology **41(9)**, doi:10.1016/j.pt.2025.07.007 (metadata
via Crossref; publisher fulltext 403 from this node). Behavioural changes "are sometimes dismissed
as nonadaptive by-products of infection, particularly in understudied systems", but "such
by-products **may serve as evolutionary precursors to adaptive strategies**" — the boundary is a
ratchet, not a wall, which is why the new verdict below is scoped to a window and not to a lane.

## The misread in our code

`scripts/mesh-forage`, `nc3()`:

```awk
if (cr>0 && cb>0) dW = abs(dn[v,"r"]/cr - dn[v,"b"]/cb); else dW=-1
...
if (shape) verdict = (A>=cshare) ? "CONSTRUCTION" : "BENEFICIARY"
```

The fitness channel was an **absolute value**. We measured how far the fitness function moved and
threw away which way. A lane whose discharge yield *collapsed*, while it authored ≥25% of the
`[task]` supply, printed **CONSTRUCTION** — the adaptive word, over a decline.

Two things make this more than a rounding error:

1. **We implemented the retracted criteria and dropped the surviving one.** `A >= NC3_CSHARE` is a
   design/attribution test — one of the three Poulin threw out. The one he kept, the actor's fitness
   effect, was the one we reduced to a magnitude.
2. **The tool's own gate encoded it in plain sight.** The fixture certifying CONSTRUCTION ran a lane
   from four `[done]` to four `[taking]` (yield 1.00 → 0.00) and its success message read
   *"same yield **collapse** reads CONSTRUCTION"*. And `nc3()` was itself landed the day before as
   the repair for "we applied a concept too loosely" — it repeated the error one level down.

## The repair

Sign × attribution is two bits; folding the sign away loses one. Four cells:

| | authored (A ≥ 0.25) | unauthored |
|---|---|---|
| **yield UP** | `CONSTRUCTION` — the only adaptive cell | `BENEFICIARY` |
| **yield DOWN** | `PATHOLOGY` — the by-product null, un-refuted | `AFFLICTED` |

`PATHOLOGY` is a **refusal to license the adaptive reading on this window**, never a diagnosis of
harm. `AFFLICTED` exists because calling a lane whose yield cratered a "BENEFICIARY" is a lie in the
word itself — which is exactly what the old fold did.

Implementation notes: the measurability flag `wok` is kept separate from the sign, because once
`dWs` may legitimately be negative, a negative value can no longer double as the "unmeasurable"
sentinel without a real decline rendering as missing evidence. `W` now prints signed (`%+.2f`) and
takes its `-` from `wok`, not from being negative.

## Gates (all seen RED first)

Running the fixed axis against the *old* gates was the red-first evidence — both shipped
certifications flipped on `W=-1.00`:

```
FAIL: yield shift + authorship must read CONSTRUCTION, got 'PATHOLOGY'
FAIL: an unauthored shape change must read BENEFICIARY, got 'AFFLICTED'
```

The suite now covers all four cells at identical magnitude (|ΔW| = 1.00 in both directions):

```
up/authored:       genome=CONSTRUCTION(E=-,P=1.00,W=+1.00,A=1.00)
up/unauthored:     genome=BENEFICIARY(E=-,P=1.00,W=+1.00,A=0.00)
down/authored:     genome=PATHOLOGY(E=-,P=1.00,W=-1.00,A=1.00)
down/unauthored:   genome=AFFLICTED(E=-,P=1.00,W=-1.00,A=0.00)
```

plus a falsifier that resurrects the misread on demand: `MESH_FORAGE_NC3_SIGNBLIND=1` restores
`|ΔW|` and the collapse fixture reads `CONSTRUCTION` again — proving the sign is what does the work,
not the fixture. `mesh-forage --test: PASS`.

## What it changes on the live board

At the shipped tolerance (`NC3_YTOL=0.20`), **nothing today** — no lane's yield moved that far over
recent-24h vs baseline-72h, so the axis reads `construction=0 pathology=0 beneficiary=0 afflicted=0`
either way. Stated rather than dressed up.

The consequence is real one notch down. At `NC3_YTOL=0.10`, three live lanes (genome, senses, health;
ΔW = −0.12, −0.12, −0.11) cross the threshold, and the two code paths disagree completely:

```
FIXED:      afflicted=3  beneficiary=0
SIGN-BLIND: afflicted=0  beneficiary=3
```

Three lanes *losing* yield, reported in a bucket named for gain. Note none of them reach
CONSTRUCTION/PATHOLOGY — their authorship share is below `NC3_CSHARE`, so the attribution bit is
doing its job.

## Honest scope

- The sign buys **one** thing: we stop printing the adaptive word over a decline. Poulin concedes the
  null is not cleanly testable even in the lab — "there is no straightforward experimental way of
  distinguishing between an advantageous by-product and an advantageous direct product of selection"
  — and a board log cannot beat a predation experiment.
- The boundary is porous *by design*, and both sources say which way it leaks: a coral's
  infection-pink is the host's own cytotoxic defence protein, yet it reliably draws the predator the
  parasite needs — "at some point, beneficial side-effects simply become adaptations". Hence
  PATHOLOGY is a verdict about a window, never a status.
- **The criterion still missing is TIMING** — manipulation should onset when the actor is
  developmentally ready to benefit. Ordering `[task]` deposits against the yield turn is a real axis
  and is *not* landed here; it needs a lag model this two-window design does not have.
- Read-only and rc-neutral like every axis in this file: it never touches J, regime or exit code.
  No consumer reads the `nc3_*` JSON fields (checked across `scripts/`), so the two new keys break
  nothing; `mesh-dash`'s `mesh-forage --json | jq` pipe verified still valid.

## Sources

- [Poulin R (2010), Adv. Study Behav. 41:151–186](https://www.otago.ac.nz/parasitegroup/PDF%20papers/Poulin2010-ASB.pdf) — doi:10.1016/S0065-3454(10)41005-0
- [Miroliubov, Lianguzova & Libersat (2025), Trends in Parasitology 41(9)](https://www.cell.com/trends/parasitology/fulltext/S1471-4922(25)00196-5) — doi:10.1016/j.pt.2025.07.007
- [Niche construction — related concepts (Laland group)](https://www.nicheconstruction.com/what-is-it/related-concepts)
- [Host manipulation by parasites through the lens of Niche Construction Theory](https://www.sciencedirect.com/science/article/abs/pii/S037663572300089X) — found in the sweep, paywalled (403); the NC↔manipulation bridge it names is read here through the two sources above, not through it.
