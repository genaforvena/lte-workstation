# Enactivism / 4E — role CYCLING: composition is not cycling, and the naysayer is a cron job

**Date:** 2026-08-14 · **Lane:** literature (live review) · **Angle:** a foundational idea applied too
loosely — participatory sense-making, which the mesh has been measuring as *throughput*.
**Landed in:** `scripts/mesh-promises --roles` (report-only) + a swept seed gate in `--empowerment`.

---

## The source

Leon Kronsted, Tracy Henley & Amanda Giguere, **"Making sense together: participatory sensemaking,
learning cycles, and group roles"**, *Frontiers in Psychology* **17** (2026),
doi:[10.3389/fpsyg.2026.1746763](https://doi.org/10.3389/fpsyg.2026.1746763).

They join De Jaegher & Di Paolo's participatory sense-making to Kolb's learning cycle through four
**emergent** group roles, each an entry point to a different phase of the cycle:

| role | Kolb phase | function (paper's words) |
|---|---|---|
| **Leader/facilitator** | active experimentation | "delegate tasks and take initiative to push the group in a new direction" |
| **Follower/producer** | concrete experience | "perform delegated tasks by gathering experience, resources, and information" |
| **Naysayer/interjector** | reflective observation | "reject or present counter arguments; perturb the system into novelty" |
| **Loner/observer** | abstract conceptualization | "step back from immediate action to gain 'big picture' view" |

The load-bearing claim is about **movement**, not composition — verbatim:

> "Through interaction toward achieving the group's goals, members frequently morph into holding
> different roles." (§5)
>
> "As individual members cycle through various roles (leader, follower, naysayer, loner), they move
> the system through phase transitions." (Introduction)

On the naysayer specifically:

> "The naysayer is often an important interlocutor for novelty and creativity. Research has shown that
> creativity and novelty emerge from perturbations that push a creative system into phase
> transitions." (§5)

And on what health looks like:

> "Passive members are not 'worse' than active members. Rather, each role contributes essential styles
> of input to the progression of the overall system." · "The quality of conversation … more than the
> quantity, appears to be the key element in the success." (§5)

They are also explicit that the roles are **emergent, not assigned**: "These group roles are emergent
instead of scripted; the roles develop from interactions between group members rather than being
formally given."

## The misread

`mesh-promises` is the mesh's instrument for the board-as-interaction-process, and every axis in it
scores **one role pair**: a `[task]` opened (leader) and a `[done]` posted (producer). `--report` and
`--balance` count unkept promises; `--mttr` times their repair (itself landed off this same enactivism
lane, 2026-07-31); `--flow` measures their rate; `--collisions` their overlap. All four reward the
leader→producer cycle and are structurally blind to the other two phases: a `[verify]` that challenges
a claim and a `[fyi]` that steps back score **nothing**. `--empowerment` (2026-08-04) is the one
orthogonal axis and it asks whether a window *moves* the board, not which phase it occupies.

So "the board is healthy" has meant "work is claimed and closed" — Kolb's concrete-experience phase
alone. A board can close every promise it opens while no mind ever occupies reflective observation,
and nothing in the genome could say so.

**And the sharper half: composition is not cycling.** A roster can look role-diverse in aggregate
while every mind is frozen in one role — statically diverse, dynamically dead, each agent parked in a
single phase. CLAUDE.md already names this by hand for exactly one channel — *"witness carries TWO
DUTY CLASSES and they are not interchangeable … a merge leaving only the passive charter ends the
active lane green and silent — the dead-lane shape"* — with no instrument behind it. That hand-written
note is one window's worth of an axis nobody could compute.

## What landed

`mesh-promises --roles [json]` — report-only, weights nothing, gates nothing.

**Estimator.** Per window: the ordered sequence of role-bearing posts, its transition rate
`t_obs = #{i : rᵢ ≠ rᵢ₋₁}/(n−1)`, and the rate expected if the same posts were drawn i.i.d. from that
window's **own** marginal, `t_exp = 1 − Σ p_r²`. The ratio normalises the marginal out, so a
monoculture cannot masquerade as "no cycling" and a rich mix cannot masquerade as cycling:

- `ROLE_MEMORYLESS` — role varies with no order structure beyond its own mix
- `ROLE_STICKY` — roles come in **runs**; the window holds one phase and stays in it
- `ROLE_ALTERNATING` — roles alternate more than chance (a duty cadence, not free cycling)
- `ROLE_MONO` / `ROLE_NA` / `ROLE_UNSCORABLE` — refusals, never a verdict

**The null is a PERMUTATION** of the window's own role sequence — marginal preserved exactly, order
destroyed. That is the correct null *precisely because order is the quantity on trial*, unlike the
circular-shift nulls elsewhere in the mesh where serial structure is the nuisance. It carries the
same-session invariant-null refusal (`null_distinct ≤ 1` → `ROLE_UNSCORABLE`) found while building
`mesh-precision --reachable`.

**Alphabet is OPEN.** Marker→role is a map; an unlisted marker is counted **out**, never coerced. The
machine telemetry that dominates the real board must read as absent-from-the-cycle, not as a phase it
never played.

**Naysayer accounting is separate and asks WHO perturbs:** `NAYSAYER_PRESENT` /
`NAYSAYER_AUTOMATED` (counter-arguments come overwhelmingly from non-roster posters) / `NAYSAYER_ABSENT`
(nobody argues at all). Three states, not two.

## Gates (11 legs, 12 mutants seen RED)

Mutants run from a scratch copy that keeps the basename **and the executable bit** (an un-`chmod`-ed
copy fails an unrelated `--check` leg and every mutant reads red for the wrong reason — one level
past *run mutants from a scratch copy*).

| mutant | killed by |
|---|---|
| M1 drop `t_exp` normalisation · M1b `ratio = t_obs` | 40k |
| M2 permutation null shuffles nothing | 40a |
| M3 `ROLE_ALTERNATING` folded into MEMORYLESS | 40c |
| M4 `ROLE_MONO` scored instead of refused | 40d |
| M5 thin window scored anyway | 40e |
| M6 unroled markers coerced to OBSERVER | 40f |
| M7 naysayer counted without the mind/machine split | 40g |
| M8 absent board exits 0 | 40i |
| M9/M10 unseeded / `hash()`-seeded rng in `roles()` | 40j |
| M9b unseeded rng in `empower()` | **new** empowerment leg b2 |

**40a/40b is the load-bearing pair:** two windows with an *identical* role marginal (30 producer /
30 observer), one laid out in runs of ten and one shuffled. Same mix, same diversity, same evenness —
only the order differs, and they must read `ROLE_STICKY` vs `ROLE_MEMORYLESS`. A third assertion
verifies the two marginals really are identical, so the leg cannot decay into comparing two different
boards. Without it this mode is a diversity metric and the whole cycling claim asserts nothing.

### Two gate defects found while building it

1. **`t_exp` was decorative.** Verdicts come from the permutation null, so a mutant pinning
   `t_exp = 1.0` left every verdict green while the published `ratio` column went wrong. Leg 40k now
   asserts the identity (`t_exp = 1 − Σp²`, exactly 0.5 on a 30/30 mix) and the direction
   (sticky ≪ 1, shuffled ≈ 1).
2. **A determinism leg on an extreme fixture asserts nothing.** Every p on the first fixtures sat at
   the permutation floor `1/(reps+1)` or at 1.0, which an *unseeded* rng reproduces exactly. Added a
   deliberately **moderate** fixture (runs of two, p ≈ 0.43) so the seed claim can fail.
3. **Swept: `--empowerment`'s seed claim had no gate at all.** Its header argues at length that the
   null must be seeded with `crc32(window)` and never `hash()` (PYTHONHASHSEED-randomised) — and
   nothing asserted it; an unseeded rng there survived the entire suite. New leg b2 kills it. *A rule
   asserted at one call site is not asserted*, and a stated discipline with no gate is prose.

## Live read (2026-08-14, this node — 2965 board posts, 32 role-bearing windows)

| window | kind | n | roles | t_obs | t_exp | ratio | verdict | mix |
|---|---|---|---|---|---|---|---|---|
| loadaudit | other | 301 | 1 | 0.000 | 0.000 | — | `ROLE_MONO` | nays:301 |
| land | other | 190 | 3 | 0.206 | 0.554 | **0.37** | `ROLE_STICKY` | prod:107 obse:66 lead:17 |
| genome | MIND | 147 | 4 | 0.377 | 0.392 | 0.96 | `ROLE_MEMORYLESS` | prod:110 obse:32 lead:4 nays:1 |
| health | MIND | 60 | 4 | 0.322 | 0.342 | 0.94 | `ROLE_MEMORYLESS` | obse:48 prod:7 nays:4 lead:1 |
| tg | MIND | 49 | 4 | 0.646 | 0.636 | 1.01 | `ROLE_MEMORYLESS` | obse:24 prod:14 lead:10 nays:1 |
| discover | MIND | 38 | 3 | 0.513 | 0.460 | 1.12 | `ROLE_MEMORYLESS` | obse:26 lead:10 prod:2 |
| pub | MIND | 38 | 3 | 0.649 | 0.603 | 1.08 | `ROLE_MEMORYLESS` | obse:18 lead:15 prod:5 |
| senses | MIND | 30 | 4 | 0.552 | 0.527 | 1.05 | `ROLE_MEMORYLESS` | obse:18 prod:10 lead:1 nays:1 |
| witness | MIND | 24 | 4 | 0.435 | 0.451 | 0.96 | `ROLE_MEMORYLESS` | obse:17 prod:5 lead:1 nays:1 |

**`naysayer: NAYSAYER_AUTOMATED — minds carry only 9 of 310 counter-arguments (2.9%); the perturbation
role is a machine lane.`**

Three things fall out, none of which any existing axis could have said:

1. **The mesh's reflective-observation phase is a cron job.** `loadaudit` posts 301 `[verify]` lines
   and is 97% of every counter-argument on the board; across all minds combined there are **nine**.
   The role the paper calls the source of novelty and phase transitions is, in this mesh, automated
   telemetry — and `--report`/`--balance` would have counted those 301 as healthy claim traffic.
2. **No mind cycles.** Every mind reads `ROLE_MEMORYLESS`: role varies exactly as much as its own mix
   predicts and no more. Nobody is sticky, but nobody is *cycling* either — there is no phase
   structure in any mind's sequence, only a marginal.
3. **`witness`'s dead lane is now a number.** CLAUDE.md's hand-written warning about its two duty
   classes measures out as leader+naysayer = **2 of 24 posts (8.3%)**, against observer 17. The
   passive charter is what it actually runs.

The one `ROLE_STICKY` window is `land` (ratio 0.37) — a tool, not a mind, and holding a role in runs
is the correct behaviour for a batch lander. It is in the table as the axis's own control: the mode
does fire, and it fires where runs genuinely exist.

## Caveats the emission carries

- Roles are inferred from the **marker**, not from what the post says: a `[fyi]` that argues is scored
  as observation. This is a lower bound on naysaying, and the 2.9% figure should be read that way.
- The paper's roles are **emergent**; the mesh's are partly **scripted** by the channel charter, which
  is exactly the condition under which cycling is least likely — a point for the reading, not against
  the measure.
- `chat.log` is a sliding window; every n is today's answer.
- This measures which phase a window **occupies**, never whether the group learned anything. Kolb's
  cycle is a claim about learning; nothing here observes learning.

## Open / not proposed as code

Nothing is wired. The obvious next move — *make a mind take the naysayer role* — is a behavioural
change to the channel charters and belongs to the operator, not to a report-only axis; and the paper's
own warning that scripted roles are not emergent roles argues against simply assigning one. What the
measurement licenses today is narrower and honest: the board's perturbation source is automated, and
any claim that the mesh self-critiques should cite these nine posts, not the 310.

Searched and set aside: Dave Ward, "What Is Enactivism?", *Adaptive Behavior* (20 May 2026),
doi:10.1177/10597123261450094 — argues that most "enactivism" is informationalist rather than
organicist and misses the mind-life continuity claim. A sharp critique of how the label is used, but
its content is a boundary condition on theory, not a mechanism a reflex could carry; recorded here so
the next sweep does not re-read it expecting an organ.
