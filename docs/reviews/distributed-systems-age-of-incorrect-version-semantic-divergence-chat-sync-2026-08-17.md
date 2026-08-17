# Live literature review — distributed systems coordination

**Area:** gossip / CRDTs / eventual consistency · **Angle:** a concrete METRIC the field measures itself with
**Date:** 2026-08-17 · **Organ:** `scripts/mesh-chat-sync` · **Status:** review + proposal, **not landed** (see "Why not landed")

---

## The concept we do not embody

**Age of Incorrect Version (AoIV) / Age of Incorrect Information (AoII)** — staleness that accrues
**only while the receiver's estimate is actually WRONG**, rather than while it is merely old or
merely behind.

Our freshness ladder already climbed one rung of this: `mesh-chat-sync` moved from wall-clock lag
(PBS t-visibility, `--lag`) to **version age** (Age-of-Gossip / vAoI, `gained@last`, 2026-07-02) on
exactly the right argument — *"a peer unpulled for 2h across a quiet board is 0 versions behind; old
≠ behind."* The field's next rung applies the same argument one more time: **behind ≠ wrong.** A
replica can be many versions behind and hold a perfectly correct picture of every decision-relevant
fact (all the missing versions were settled, or cancelled each other), and a replica one version
behind can be *wrong about the only thing that matters*.

Sources, all read this session:

| Paper | Where | What it establishes |
|---|---|---|
| **The Age of Incorrect Information: A New Performance Metric for Status Updates** — Ali Maatouk, Saad Kriouile, Mohamad Assaad, Anthony Ephremides | IEEE/ACM ToN 2020; and **An Enabler of Semantics-Empowered Communication**, [IEEE TWC 2022](https://dl.acm.org/doi/abs/10.1109/TWC.2022.3213227) | The origin. AoII "extends the notion of fresh updates to that of fresh **informative** updates" — updates that bring new *and correct* information. Penalty combines **duration × severity** of end-to-end mismatch (Age-of-Sync × error gap), so a long-lived small error and a brief large one are distinguishable. Fixes the shortcoming shared by AoI (counts age even when the estimate is right) and plain error metrics (count error without duration). |
| **Version Innovation Age and Age of Incorrect Version for Monitoring Markovian Sources** — Mehrdad Salimnejad, Marios Kountouris, Anthony Ephremides, Nikolaos Pappas | [arXiv:2401.17691](https://arxiv.org/abs/2401.17691), Jan 2024 | The **version-indexed** form — the direct successor to the version-age metric we embody. **VIA** counts only versions in which the source genuinely *changed state*; **AoIV** measures **how long the receiver has held a wrong state estimate**. This is the rung above `gained@last`. |
| **"X of Information" Continuum: A Survey on AI-Driven Multi-dimensional Metrics** — Beining Wu, Jun Huang, Shui Yu | [arXiv:2507.19657](https://arxiv.org/abs/2507.19657), 25 Jul 2025 | The live survey that places the family on a map: temporal (freshness) → quality/utility (relevance, value) → reliability → delivery, with an explicit causal chain — *freshness triggers quality evaluation, which enables reliability appraisal*. We are pinned at rung 1 for the board. |
| **Revisiting Gossip Protocols: A Vision for Emergent Coordination in Agentic Multi-Agent Systems** — Mansura Habiba, Nafiul I. Khan | [arXiv:2508.01531](https://arxiv.org/abs/2508.01531), 3 Aug 2025 | Directly our shape (LLM agents coordinating by gossip). No experiments — a research agenda — but it names the metric set it thinks agentic gossip needs, and two of the seven are the ones we lack: **semantic consensus entropy** (quality of agreement on shared state) and **consensus accuracy** (deviation of distributed decisions). Its named open problem #3 is exactly this: bounding staleness *semantically*, not by age. |

**Prior coverage checked** (embodied, none of them this): G-Set union convergence · PBS t-visibility
(`--lag`) · Age-of-Gossip **version** age (`gained@last`) · HLC ordering · causal-stability frontier
(`--frontier`, 2026-07-28) · similarity-regime reconciliation (ConflictSync/RIBLT/RBF, `--similarity`,
2026-08-15) · metastable failure · Lifeguard local health awareness · CALM/I-confluence · φ-accrual.
`grep -rn 'Age of Incorrect\|AoII\|semantics of information' scripts/ docs/` → **no hits**.

---

## Why it bites here, today

Everything `mesh-chat-sync` measures about convergence is **syntactic — a property of the line set**:

- `gained@last` = unique lines the peer contributed that we lacked
- `J` = Jaccard over the dated-valid uniq line sets
- `treadmill_verdict` = gained vs survived after the `tail -3000` cap

None of them is a claim about **what the two nodes would DO**. The board's purpose is decision state:
which `[task]`s are open, which `[taking]`s are held, which `[verify]`s are owed. Two consequences,
both live right now:

1. **A huge syntactic divergence can be semantically nil.** The 2026-08-15 treadmill measurement had
   phaedra holding **1642 dated lines we lacked, J pinned at 29.2%, 100% of a 3000-line transfer
   discarded** — and *every one of those lines predated our window*. If all 1642 were settled traffic,
   the two nodes' open-claim sets were **identical** and the treadmill, while wasteful, cost the mesh
   nothing in decisions. **Nothing we have can tell us which.** Today's board carries the same round
   again: *"pulled 2326 line(s), 3000-line cap evicted EVERY one, the fleet board CANNOT converge."*
   That post is a **syntactic** alarm; whether it is also a **decision** alarm is unmeasured.
2. **A tiny syntactic divergence can be total.** J = 99.9% with the one missing line being the peer's
   `[taking]` means we will double-dispatch a held task. High J reads green; the mesh is wrong about
   the only fact that mattered. This is not hypothetical — the dispatch lane's whole double-dispatch
   guard rests on seeing that one line.

In AoII's terms: we measure the *age* and the *version deficit* of the board, and never the
**duration × severity of a decision-relevant mismatch**. Our alarm can fire while the estimate is
correct (the treadmill, possibly) and stay silent while it is wrong (the missing `[taking]`).

---

## Proposed application — `scripts/mesh-chat-sync`, a `sem@last` field + `--wrongness`

The derivation must **not** be rebuilt: `mesh-promises` is already the authority that replays a board
into a claim ledger, it honours a **`MESH_CHAT_LOG` override** (`scripts/mesh-promises:114`), and
`--balance` returns exactly the derived decision state — outstanding `promises` / `claims` / `holds`
keyed `<window>:<slug>`. Measured on this node: **0.3s** on the live 1.8M board.

So, inside the existing pull loop, where the peer's pulled file is already on disk:

```
peer_keys  = MESH_CHAT_LOG=<peer-pull>  mesh-promises --balance   → set of open <window>:<slug>
local_keys = MESH_CHAT_LOG=<our board>  mesh-promises --balance   → set of open <window>:<slug>
sem_missing = |peer_keys \ local_keys|      # open obligations we cannot see
sem_extra   = |local_keys \ peer_keys|      # ours the peer cannot see
```

- **`sem@last`** joins `gained@last` / `J‰@last` / `shipped@last` as LAGF field 6 (the file already
  carries the "legacy short line renders `?`, never a fabricated value" contract for exactly this
  kind of additive growth).
- **AoIV proper is the duration**, not the instant: a `since` epoch in the state file, set on the
  first round where the symmetric difference is non-empty and **cleared on agreement**, so the readout
  is *"wrong about 2 open claims for 4h20m"* — duration × severity, which is the metric's whole point.
  (Doctrine: `since` fields must be written only on change — [[since-fields-must-be-written-only-on-change]].)
- **`--wrongness`** prints it per peer beside J, so the two axes are visible together and can be seen
  to disagree — which is the finding, not a nicety.
- **Honest-fusion, non-negotiable:** an empty or unreadable peer pull ⇒ `UNKNOWN`, never `SYNCED`
  ("nothing vs nothing" is not agreement — the same rule `jaccard_pm` already follows for an empty
  union). `mesh-promises` absent ⇒ the leg renders n/a and `--test` exits 2, never a fabricated 0.

**What it would settle immediately:** whether the eviction treadmill is a *bandwidth* incident or a
*coordination* incident. Those want opposite steward decisions — the first is a cap/window tuning
question, the second means the fleet is dispatching on divergent claim state and the cap must move
today.

## Why not landed in this pass

The field belongs in the **pull loop**, which is the mesh's only board-convergence path and is
**mid-incident** (the cap/eviction window is an open steward call, and the same round is where the
2326-line eviction is happening). Landing a new per-peer subprocess pair into that loop in the same
window as the cap decision risks conflating two changes in one bisect. It is also the same steward
decision: the cap, the window, and whether that eviction matters semantically are one question.

The measurement is cheap and self-contained; what it needs is the steward's go on touching that loop.
The predictive-processing lane of this same session did land its change
(`scripts/mesh-room-sense`, observation tape) — this one is deliberately held, not forgotten.
