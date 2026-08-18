# Autopoiesis & the biology of cognition — live review: THE ENTITY IS DISCOVERED, NOT DECLARED

**Area:** autopoiesis & the biology of cognition (Maturana, Varela), angle = a RECENT result
(2023–2026) carrying an OPERATIONAL mechanism, not the philosophy.
**Date:** 2026-08-18. **Window:** genome (mesh-home).
**Status:** landed, uncommitted in the tree (steward lands).
**Tool:** `scripts/mesh-reflex-health` — new co-failure-entity axis (report-only, on the `--check`
line and the `[reflex-stale]` board alert).

---

## I. What is live in this area right now

Searched 2026-08-18 (WebSearch). The area is publishing steadily; the 2025–2026 cluster I surfaced:

| Work | Where | Why not this |
|---|---|---|
| "Toward aitiopoietic cognition: bridging the evolutionary divide between biological and machine-learned causal systems" | *Frontiers in Cognition*, Jun 2025, doi:10.3389/fcogn.2025.1618381 | A comparison of causal regimes (autopoietic vs. statistically-optimized). Real, but it hands you a distinction, not a procedure. |
| "Closing the loop: how semantic closure enables open-ended evolution?" | *J. R. Soc. Interface* 22(233):20250784, Dec 2025 | **Already ours** — semantic closure landed 2026-08-16 (`autopoiesis-semantic-closure-interpreter-provenance-closure-semantic-2026-08-16.md`). |
| "Autopoiesis, Autonomy, and Organizational Biology" (Bich & Arnellos) | HAL hal-04808806 / ADDI | Organizational-closure framing we embody twice over (`mesh-closure`, `autopoiesis-closure-of-constraints-organizational-2026-07-28.md`). |
| "Life as Plasmas: Autonomy and Interactivism in-materio" | arXiv:2607.09747, 2026 | In-materio substrate autonomy. No transferable procedure for a software mesh. |
| **"Defining and finding lifelike entities with a lazy filter"** | **arXiv:2504.14774 (22 Apr 2025); journal version *BioSystems*, S0303264725002825, 2025.** Mario Martinez-Saito, Institute of Cognitive Neuroscience, HSE University. Author's own keywords include **autopoiesis**. | **Landed here.** |

Read: `arxiv.org/abs/2504.14774` and the full text at `arxiv.org/html/2504.14774v1`.

## II. The result, and the two things in it we did not embody

**(1) BUNCH — "bottom-up bisect-unite nodes clustered hierarchically".** A parameter-free filter that
*infers* which particles constitute an entity **from the dynamics alone**. Leaves are particles,
internal nodes are clusters of clusters, the root is the "omnientity". A cluster is admitted when the
joint model beats the separate ones on evidence, and a birth-death step *"remove[s] short-lived,
low-likelihood clusters"*. Nobody hands the algorithm a list of entities: **the boundary is a
conclusion**, and a group that does not persist is not one. The "lazy" is the tractability strategy —
clustering separately at each level, bottom to top, no global re-optimisation, no backtracking.

**(2) LIFENESS.** Verbatim from the paper:

> "Given an entity E of complexity I that persists for t time, we simply propose that the product of
> these two variables is a reasonably good measure of lifeness: **L = t·I**"

— complexity *integrated over lifetime*; *"long-lived and complex things look 'alive'"*. Neither
factor alone is the measure: a big transient and a tiny immortal both score low. (The paper's own
preliminary finding — lifeness correlates with distance to criticality across 41 simulated particle
worlds — is a result, not a mechanism, and is not what is transferred here.)

## III. Where it bites this mesh

**Every grouping this mesh can express is one a human wrote down.** A filename, a `# reflex-cadence:`
header, a source reference. `mesh-reflex-health`'s two existing triage axes are both greps over the
*declared* graph — `fanin_count()` counts who mentions an artifact, the in-degree block counts who
writes it. `mesh-closure` polls a static source graph. `mesh-correlate`/`mesh-cooscillate` do mine
observed structure, but out of the **sensor tape**, between *readings*. **Nothing in the genome has
ever concluded that two reflexes are one thing from watching them behave, and the FAULT axis has no
miner at all.**

The cost is concrete on this node. The sole uplink is a USB dongle that wedges (`CLAUDE.local.md`);
when it does, `mesh-wifi-link`, `mesh-wifi-motion`, `mesh-presence`, `mesh-arrivals` and
`mesh-lan-health` go stale in the same tick. The board gets **one `[reflex-stale]` line listing five
independent-looking names**, and the facilitation-cascade hint then nominates whichever has the most
grep-hits — a quantity with no relation to the wedge. Five names for one event is exactly the case
BUNCH answers: *describe the cluster, not its members*. The 2026-08-17 16:04→17:03Z outage ran that
way for 55 minutes, and ended in the operator's hands.

## IV. What shipped — `scripts/mesh-reflex-health`

Report-only, an attribution never a verdict. Never alarms, never changes an exit code, never
suppresses the existing fan-in hint.

- **`cofail_record()`** appends this run's stale **set** to a rolling window (`MESH_REFLEX_COFAIL_WINDOW`,
  default 144 ≈ 24h at `*/10`). **Scheduled runs only** — a `--check` feeding the history would forge
  the evidence it then reads, the named test-writes-the-artifact fault. Runs with **nothing** stale are
  recorded too: they are the denominator's honest zeroes.
- **`cofail_entity()`** seeds on the most-often-stale member of the *current* stale set and unites every
  other member whose **Jaccard overlap** with the seed clears `MESH_REFLEX_COFAIL_J` (default 70%) —
  the bisect-unite step reduced to the one level we have. Then the **birth-death step, which is the part
  that matters**: a member seen fewer than `MESH_REFLEX_COFAIL_MIN_APPEAR` (3) times is dropped, and
  below `MESH_REFLEX_COFAIL_MIN_RUNS` (12) recorded runs the axis renders `na` **with its run count**
  instead of a cohort. Without it one flapping tick mints a permanent "entity" — the set-signature
  failure this mesh has already been bitten by.
- **`lifeness`** `L = t·I`, with `t` = trailing **consecutive** runs the whole cohort held and `I` =
  member count. `I` is a **member-count proxy, not a description length** — said in the output itself,
  because the paper's `I` is an MDL over a Gaussian-mixture model and ours is not.

Rendering (board alert + `--check`):

```
· cofail-entity: mesh-arrivals+mesh-presence+mesh-wifi-link — co-stale at Jaccard ≥70%,
  held 9 consecutive runs, lifeness 27 = 9 runs × 3 members. They fail TOGETHER: a co-occurrence,
  NOT a named shared cause — a shared observable cannot name the mechanism. Members count as the
  complexity proxy, not a description length
```

## V. What it does not claim

A cohort is a **co-occurrence**. It does not name a shared dependency, and the clause says so in
words: *a shared observable cannot name the mechanism*, and reproduction is not causation. Two
reflexes wired to the same cron minute co-fail on a node-wide pause with no organ in common. The
output is a lead for a human, on the same contract as every other report-only axis in this tool.

Determinism: members are sorted and the seed tie-breaks lexically, so member order can never move the
rendering. No parentheses anywhere in the clause — `ow_edge_key()` harvests `name(` tokens and
`mesh-needs` scrapes `[a-z-]+\(stale` off the `--check` line; a parenthesised cohort word would inject
a phantom reflex name into one and a phantom dead reflex into the other. Both asserted.

## VI. Verification — 19 mutants, all red, zero vacuous

`--test` grew a CO-FAILURE-ENTITY block. Every gate was mutation-tested from a scratch copy; **two
came back GREEN and were rewritten, and one guard was deleted as provably unreachable**:

- The birth-death gate used a *2-of-14 flapper against two always-stale members* — that is Jaccard
  14%, so **Jaccard already excluded it** and the gate stayed green with `minapp` deleted. It was
  re-asserting Jaccard, not birth-death. Replaced with a 2-run co-failure at **Jaccard 100%**, where
  the appearance floor is the only thing that can kill it.
- The order-independence gate used **two** members, where the seed tie-break alone pins `M[1]` and the
  remaining member is the whole tail either way — invisible to a deleted sort. Now three members.
- The appearance floor on the **seed** selection was **unreachable code**: the seed holds the maximum
  appearance count, so if it fails the floor every candidate fails it too and the unite step already
  returns a 1-member "solo". Deleting it left every gate green. Removed, with the algebra recorded in
  place. The floor is now enforced once, on the unite step, and asserted at the reachable end of the
  `jmin` knob (`MESH_REFLEX_COFAIL_J=50`, where a 2-appearance member clears 50% against a
  3-appearance seed).
- One gate matched `*x*` for the excluded member and hit the word **"proxy"** in the clause's own
  prose — a substring scan turning prose into a verdict. Now matches the `+x` member token.

Gates that fire (each verified red under its mutant): short history renders `na` **with both
numbers** · a 14/14 cohort renders sorted with `lifeness 28 = 14 × 2` · 3-member cohort sorted,
rendering order-independent · no parenthesis in the clause · a 2-co-stale-run flap at Jaccard 100% is
killed by the appearance floor · a never-before-seen name renders no cohort (`sparse` keeps its own
branch, distinct from "seen but not together") · Jaccard-0 alternation is **not** a cohort · a cohort
broken in the most recent run scores `t=0` · an empty stale set renders nothing · `--check` never
writes the history · a scheduled run records even with nothing stale · the window trims ·
**END-TO-END**: over a synthetic two-row backdated table in a sandbox `HOME`, the cohort reaches
**both** the board alert and the `--check` line, with the `mesh-chat` PATH shadow itself asserted (a
shim that changes nothing would otherwise pass while posting to the real board).

One real bug caught by the gates going red: `stale_names` was unbound under `set -u`, crashing every
`--check` path in the tool.

Live path driven on this node: `--check` reads `reflex-health: ok (7 per-run reflex(es) fresh …)`,
emits no cohort clause (nothing stale — correct), and **wrote no history file**; a scheduled run
appended exactly one honest-zero line.

## VII. Sources

- [Defining and finding lifelike entities with a lazy filter — arXiv:2504.14774](https://arxiv.org/abs/2504.14774) · [full text](https://arxiv.org/html/2504.14774v1) · [BioSystems version](https://www.sciencedirect.com/science/article/abs/pii/S0303264725002825)
- [Toward aitiopoietic cognition — Frontiers in Cognition 2025](https://www.frontiersin.org/journals/cognition/articles/10.3389/fcogn.2025.1618381/full)
- [Closing the loop: how semantic closure enables open-ended evolution? — J. R. Soc. Interface 2025](https://royalsocietypublishing.org/rsif/article/22/233/20250784/364699/Closing-the-loop-how-semantic-closure-enables-open)
- [Bich & Arnellos, Autopoiesis, Autonomy, and Organizational Biology](https://hal.science/hal-04808806/document)
- [Life as Plasmas: Autonomy and Interactivism in-materio — arXiv:2607.09747](https://arxiv.org/html/2607.09747)
