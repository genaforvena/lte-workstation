# The rare-enemy principle: a 403 is the LAST signal that would ever fire, so a channel gated on it is blind by construction

**Live review, 2026-08-22 — niche construction & the extended phenotype, from the angle the task asked
for: a known CRITIQUE / failure mode of the area.**
**Arm:** treated (assigned)
**Target organ:** `scripts/mesh-tg-roz` — assigned by coin at p=0.20, drawn uniformly from the lane's
570 never-reviewed tools. Not chosen by me and not chosen by the lane.
Landed in `scripts/mesh-tg-roz` (`--reciprocity` + a send-path report; uncommitted — steward lands from the tree).

## What was already ours (checked first, so the review could not re-land)

Fourteen prior landings in this area (`docs/reviews/niche-construction-*`, `extended-phenotype-*`).
The critique-angle ones:

| embodied critique | where |
|---|---|
| negative NC / inter-scale conflict (Wade & Sultan) | `mesh-forage:132` |
| driftability — NC changes drift probabilities, not only selection | `mesh-forage` `drift_null()` |
| the **by-product null** — an adaptive verdict needs the SIGN of the fitness change | `mesh-forage` `nc3()` |
| NC3 mechanism attribution — most of what we called construction is *choice* | `mesh-forage` `nc3()` |
| the removal control (external immunity, *Tribolium* 2025) | `mesh-ideate:273` |
| mere recurrence — an inheritance channel with no evidence of transmission | `mesh-knowledge-sync --lineage` |
| ghost legacy / durability / recipients | `mesh-reflex-health` |
| home-field advantage, contemporaneous reference class, sublinear memory τ_e | `mesh-promises`, `mesh-reflex-health`, `mesh-situation` |

Every one of them asks about the **construction**: is it real, does it help, does it drift, was it
ablated, who inherits it. `grep -ril 'rare.enemy\|life-dinner\|arms race'` over all 283 reviews returns
one incidental mention and no landing. **Nothing we hold asks what the RECIPIENT of an extended
phenotype does back, or how we would notice.** That is the gap this organ sits in.

## The find

**McLean, D. J., Herberstein, M. E. & Kokko, H. (2024). "Asymmetric arms races between predators and
prey: a tug of war between the life–dinner principle and the rare-enemy principle." *Proceedings of the
Royal Society B* 291(2032): 20241052. doi:[10.1098/rspb.2024.1052](https://royalsocietypublishing.org/doi/10.1098/rspb.2024.1052).**
Open access at [PMC11461046](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11461046/). Found by live web
search 2026-08-22; the same search surfaced the sibling live thread —
[Host manipulation by parasites through the lens of Niche Construction Theory](https://www.sciencedirect.com/science/article/abs/pii/S037663572300089X)
(ScienceDirect) and the standing
[Criticisms of Niche Construction Theory](https://synergy.st-andrews.ac.uk/niche/criticisms-of-niche-construction-theory/)
page at St Andrews.

The extended phenotype's manipulation machinery rests on Dawkins & Krebs's **life–dinner principle**:
the rabbit runs faster than the fox because the rabbit runs for its life and the fox only for its
dinner, so the manipulated party should be *ahead* in the arms race. McLean et al. note this model "has
undergone surprisingly little theoretical scrutiny", derive it analytically, and find that
**coevolutionary outcomes do not always align with it**. The reversing force they name is the
**rare-enemy principle**: predators are usually outnumbered by their prey, so the *per-encounter*
asymmetry is diluted — selection on the prey to resist is relatively **weak**, because most prey never
meet the enemy. Their structural point is the one that travels: Dawkins & Krebs's informal argument
**conflates a per-encounter asymmetry with an evolutionary consequence**, and the two can point
opposite ways.

## Why that is exactly this organ's failure mode

`mesh-tg-roz` is the mesh's clearest extended phenotype: an organ whose whole function is to modify the
environment of an organism outside the mesh — a real person, Rozalia, in her own Telegram. The tool's
cost asymmetry is textbook life–dinner: **we spend a curl, she spends attention.** And its entire
resistance-detection apparatus is one branch — Telegram `error_code: 403`, the bot blocked:

```bash
if err_code=... [ "$err_code" = 403 ]; then    # debounced board alert on blocked/deleted chat
```

Under the rare-enemy principle that gate is blind **by construction, not by accident**. A block is the
single most expensive act available to her and the rarest; every graded degree of *answering less* —
the actual signal — sits below it and is rendered by this tool as `sent ok`. Worse, the tool posts a
board `[alert]` when a 403 *clears*, so the only thing it can say about the relationship is the two
edges of its least likely event.

## Measured on the live corpus, not asserted

`~/.mesh/roz-in.log` (this channel's own record, 1300 lines) replayed 2026-08-22:

| quantity | value |
|---|---|
| outbound `[OUT]` / inbound `[IN]` | **81 / 54** |
| completed unanswered-run lengths | n=**54**, median **1**, p90 = **2**, max **10** |
| **current trailing run** | **4** |
| inbound-lane coverage | lag **0**, tg-roz window present → the silence is REAL |

The channel is right now in an unanswered run longer than ~90% of the runs it has ever produced, the
inbound lane is verifiably healthy so it is not a writer failure, no 403 has fired, and **nothing in
the mesh said so.** The state that the critique predicts would be invisible was in fact invisible.

## What landed

`scripts/mesh-tg-roz`, `--reciprocity` plus a report on every successful send (both the text and
`--doc` paths, called **after** the `[OUT]` append so the run includes the message just sent):

```
run=4 thr=3 p90=2 n=54 out=81 in=54 lag=0 winch=present coverage=ok state=asymmetric
since=na(inbound-ts-truncated-by-roz-channel)
```

- **The threshold is derived from this channel's own completed runs** (`thr = max(3, p90+1)`),
  re-derived on every read, never a pinned constant — and with fewer than 5 completed runs it renders
  `p90=na` and a *marked* default rather than a silent number.
- **Coverage before verdict.** The `[IN]` half of that log is written by `mesh-roz-channel`, not by
  this tool. If the poller is behind its own input (`.roz-channel.offset` < `tg-strangers.log` lines)
  or its target window is gone — it `exit 0`s silently without one — an unanswered run is a *writer*
  failure and says nothing about the recipient. That case reads `coverage=partial` / `state=unknown`,
  and the state file is **held, not cleared**.
- **Edge-triggered, and the recovery is silent.** One board `[fyi]` per crossing, keyed on a state
  file like the 403 path; coming back does not post, so a channel that simply resumes does not wake a
  reader twice per episode.
- It **does not gate the send.** The channel is hers, not ours; the organ publishes an asymmetry it
  previously could not state, and that is the whole intervention.

## Found on the way, not fixed here (single-file landing)

`scripts/mesh-roz-channel:41` cuts the inbound timestamp with `grep -oE '^[0-9TZ:]+'` — a character
class with no `-`, so every ISO date truncates at the first hyphen and all 54 `[IN]` lines in
`roz-in.log` carry the literal stem `2026`. That is why the better axis (*age* of the last inbound
line) is unavailable and is rendered `since=na(inbound-ts-truncated-by-roz-channel)` — an `na` naming
its own cause — instead of a plausible 0. One-character fix in a different file; posted as `[fyi]`
rather than smuggled into this landing.

## Verification

`--test` drives the axis against fixtures rather than grepping the source: a 6-completed-run corpus
with a trailing run of 4 must read `run=4 thr=3 p90=1 n=6` and `state=asymmetric`; the same log with
the poller two lines behind must read `lag=2 coverage=partial state=unknown`; and a missing tg-roz
window fails **loud** ("the inbound half of this channel is dead") rather than being excused.

Driven red three ways, each restored to green:

| mutation | result |
|---|---|
| `thr = max(3, p90+9)` (threshold too lax) | `FAIL (reciprocity misread the fixture: … thr=10 … state=reciprocal)` |
| `if lag > 99999` (coverage blind) | `FAIL (writer lag did not render the run unknown: … coverage=ok state=asymmetric)` |
| `startswith('[OUTX]')` (run counter dead) | `FAIL (… run=0 … out=0 …)` |
| restored | `smoke-test: ok (bot=Меш/месх, chat=140230022; --doc refuses a missing file; reciprocity: run/thr from the corpus, writer-lag -> unknown)` |

## Sources

- [McLean, Herberstein & Kokko 2024, *Proc. R. Soc. B* 291(2032):20241052](https://royalsocietypublishing.org/doi/10.1098/rspb.2024.1052) · [PMC11461046](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11461046/) · [PubMed 39378992](https://pubmed.ncbi.nlm.nih.gov/39378992/)
- [Host manipulation by parasites through the lens of Niche Construction Theory (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S037663572300089X)
- [Criticisms of Niche Construction Theory — St Andrews](https://synergy.st-andrews.ac.uk/niche/criticisms-of-niche-construction-theory/)
- [Wells, *The extended phenotype(s): a comparison with niche construction theory* (PhilPapers)](https://philpapers.org/rec/WELTEP)
