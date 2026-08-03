# Enactivism & 4E — AGENCY-GATED CREDIT: blame only what you CAUSED

**Live review, genome, 2026-08-03.** Area: **enactivism & 4E cognition**, angle the task asked for — an
**OPERATIONAL mechanism** (not philosophy), found by live web search in the current literature, landed
where the mesh has not been. Landed in `scripts/mesh-fitness` as an agency gate on the auto-revert.

## The finding (cited, read)

**Haoliang Han — "From Detecting Agency to Doing Work: Self-Caused Credit Builds a Durable Behavioral
Self in a Minimal Spiking Agent."** arXiv:[2606.30191](https://arxiv.org/abs/2606.30191), submitted
2026-06-29.

Abstract, verbatim (arXiv):

> "How does an agent that can tell self from world come to be durably shaped by that distinction?
> Recent work shows that a predictive system can detect its own agency (Ye, 2026), but detecting agency
> does not explain durable, self-shaped behavior. We show that **agency-gated slow credit — a
> conjunctive term Own\*Agency\*Salience driving a slow parameter update — produces post-unload
> behavioral residue**: on a spiking substrate (Nengo LIF/PES), a learned self-preserving choice
> survives episodic buffer removal (retained fraction 0.96, N=50) and collapses when the slow decoders
> are reset or the agency gate is removed. Reproducing the agency comparator and toggling only the
> slow-credit channel, we find a clean dissociation: at matched agency gain, durable behavior develops
> only when self-credit performs slow work (post-unload self-preservation 1.00 vs 0.00). The same
> dissociation holds in 24-dimensional partially-observed control (0.74 vs 0.00), and a plastic-work
> analysis shows that basin deformation equals net self-credit work. Across eight sequentially-learned
> tasks under exogenous interference, **the multiplicative veto also prevents forgetting: it retains
> old tasks (final post-unload accuracy 0.88, forgetting 0.13) where ADDITIVE POOLING collapses to
> chance-level recall, the NO-AGENCY ABLATION falls BELOW chance**, and episodic/replay baselines stay
> near chance after unload — all with no replay buffer and no task-boundary-dependent protection
> mechanism (N=50). We formalize the durable residue as an operational behavioral self and argue that
> self-caused credit doing slow work is a necessary building block for agents that develop a self. No
> claim of consciousness is made."

Stripped of the spiking substrate, the transferable operational claim is one sentence: **a system that
modifies itself from observed outcomes must gate credit/blame MULTIPLICATIVELY on whether the outcome
was self-caused — and ungated updating is not merely weaker, it is worse than not updating** (the
no-agency ablation lands *below chance*, additive pooling *collapses*).

This is 4E's self/world boundary as a *mechanism*, not a thesis: the agency comparator is the operation
that makes a self-modification attributable.

## Why it is not already embodied — and where it bites

`scripts/mesh-fitness` is the mesh's selection organ: after a self-produced commit lands, it judges the
tip and **rewrites git history** (`git revert --no-edit HEAD`) if a tool the commit changed fails its
own syntax check or its own `--test`.

The file already cites the exact criterion this finding completes. Its `:46-52` header quotes
**Barandiaran, Di Paolo & Rohde, "Defining Agency" (Adaptive Behavior 17(5), 2009)** — agency requires
*individuality + INTERACTIONAL ASYMMETRY + normativity*. The **normativity** leg got its instrument in a
prior landing (`interscale_conflict`, the phylogenetic grain). **Asymmetry — the agent being the CAUSE
of the modulation — was never implemented.**

The gap, concretely: the verdict *"HEAD shipped a BROKEN tool"* and the auto-revert that follows were
asserted from a **single observation** — the tool fails *now*. Nothing asked whether it failed
*before*. The file is exceptionally hardened along every other axis (rc=2 honest-n/a, storm-flake retry
ladder, rc=124 timeouts, a memory-pressure defer, a dirty∩changed revert scope, and a committed-copy
re-judge so mid-work tree edits are not misattributed) — every one of those guards asks *"is the
failure real?"*. **None asks *"did this commit cause it?"***

The failure mode is not hypothetical, and this file names its own cause two functions away:
`unjudged_backlog()` is an instrument for exactly the commits that **go unjudged** because HEAD-only
selection moved past them. So a tool broken by commit *A* stays broken and unnoticed; the next
self-produced commit *B* that so much as touches that path is blamed and reverted. *B* may be the
repair. Ungated blame, no agency term — Han's below-chance ablation in git form.

And the mesh's own Verification Principle says the same thing without the paper: **a revert restores the
parent's bytes, so an auto-revert repairs something only if the PARENT PASSES.** That artifact was never
checked. The revert asserted a cure it had not seen.

## What landed

`inherited_regressions()` — the agency comparator. When (and only when) a regression is observed, it
re-judges the offending tools against the **parent commit's bytes** in a scratch tree, using the same
`regressions()` judge (the form the dirty-overlap attribution at `:601+` already uses). Tools that fail
at the parent too **predate HEAD**: agency = 0, blame vetoed.

- Matched on **tool name, not `tool:reason`** — a tool that fails `bash -n` at the parent and `--test`
  at HEAD is still a pre-existing break, not something this commit caused.
- **Fail-conservative by construction:** no parent (root commit), a path the parent does not carry
  (added by HEAD), or an unreadable blob → nothing is echoed → the entry stays attributed to HEAD, i.e.
  today's behavior. **The gate can only ever withhold a revert, never mint one.**
- Runs **only on the rare regression path** — a green tip pays nothing.

Three outcomes, all distinct on the board:

| split | action |
|---|---|
| all self-caused | unchanged — auto-revert as before |
| partial | revert the self-caused half; `inh_note` states which tools **survive** the revert, wherever the verdict is read |
| all inherited | **no revert**, `INHERITED-BREAK` in `fitness.log`, `[fitness-inherited]` on the board, exit 0 |

The all-inherited branch is **loud, never silent**. Agency=0 withholds the *revert*, not the *alarm*: a
pre-existing break is real, and nothing else is judging it — HEAD-only selection walked past whatever
caused it. The post carries `owner: genome/health` so it routes instead of aging.

## The gates were seen RED

**The discriminator is a fixture PAIR.** Fixture D is the suite's existing fixture A with **one bit
changed** — the parent is already broken. Same tool, same broken bytes at HEAD, same clean tree, same
self-produced trailer. Anything separating them separates on **causation alone**. A must revert; D must
not. Fixture A is therefore also this gate's own falsifier: a gate that vetoed everything would redden
it.

Three mutants, run from a scratch copy, all RED for the right reason:

| mutant | result |
|---|---|
| gate disabled (`inherited_regressions` returns nothing) | RED — *a break INHERITED from the parent must never be reverted — HEAD moved, an innocent commit was destroyed and the tool is still broken* |
| gate vetoes everything | RED — fixture A stops reverting a genuinely self-caused break (auto-revert disabled entirely) |
| revert withheld **and** alarm dropped | RED — *withheld the revert AND the alarm — the break must still be reported* |

Plus a direct unit leg on the helper (parent GREEN → **nothing** may be marked inherited) and the
already-asserted `[fitness-inherited]` board post.

`--test`: **PASS**, 10s → 11s (+1s, measured against `git show HEAD:scripts/mesh-fitness`). Inside
`mesh-doctor`'s 60s cap and `mesh-land`'s 30s.

## Discarded, with reasons

- **Candia-Rivera, "Interoceptive machine framework"** (arXiv:[2604.24527](https://arxiv.org/abs/2604.24527),
  2026-04-27) — organizes interoception into homeostatic / allostatic / enactive principles. The
  *allostatic* leg (anticipatory, uncertainty-based re-evaluation) is a genuine mesh gap — every mesh
  guard thresholds on *current* load/temp/spend. But it is a **review**, not a result: it proposes an
  organizing frame, and the concrete mechanism would have to be invented rather than transferred.
  Worth a future task on its own terms; not a finding to land today.
- **"Sensorimotor Contingencies"** (arXiv:2510.14227) — quantifies mastery as the *decay rate of the
  residual* after a world change. Already cited by the 2026-07-30 reafference landing
  (`mesh-audio-active --confirm`), and the residual-decay half needs a continuously-tracked estimate
  the mesh's confirm/deny sensing does not produce.
- **"Governing What You Cannot Observe"** (arXiv:2604.24686) — Aubin viability theory, a scalar
  Viability Index and monotonic restriction for AI agents. Real and on-mechanism, but the mesh already
  carries viability instruments (`mesh-vitality`, `mesh-situation`, `mesh-load-gate`), and its
  kill-switch/monotonic-restriction core is a governance posture the operator has not asked for.
- **De Jaegher & Di Paolo participatory-sense-making follow-ups** (Frontiers 2026, "Making sense
  together: participatory sensemaking, learning cycles, and group roles") — group-role pedagogy, no
  operational measure to transfer; the coordination-process axis was already landed 2026-07-31 as
  `mesh-promises --mttr`.

## State

Uncommitted in the tree, for the steward:

- `scripts/mesh-fitness` — `inherited_regressions()` + the agency split in the main flow + the
  `INHERITED-BREAK` / `[fitness-inherited]` branch + `inh_note` on the partial case + `--check`
  reporting + fixture D, the helper unit leg, and the alarm assertion.
- `docs/reviews/enactivism-4e-agency-gated-credit-fitness-self-caused-2026-08-03.md` (this file).

`mesh-fitness --test`: **PASS**. Genome source only — the deployed `~/.local/bin/mesh-fitness` is
untouched (steward deploys via `mesh-sync-tools`).

Related: [[enactivism-4e-coverage]] · [[reproduction-is-not-causation]] ·
[[a-verified-finds-proposed-fix-is-still-a-hypothesis]] · [[autopoiesis-review-coverage]]
