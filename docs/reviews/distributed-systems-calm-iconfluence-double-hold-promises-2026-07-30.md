# CALM / invariant-confluence: `[taking]` enforces a NON-monotone invariant the board can't keep

**Live review, 2026-07-30** — area: distributed-systems coordination (gossip · CRDTs · eventual
consistency). Angle: a foundational idea applied too loosely. Landing: `scripts/mesh-promises`
(`--collisions`, new double-hold detector).

## The concept

**The CALM theorem** — *Consistency As Logical Monotonicity* (Hellerstein & Alvaro, "Keeping CALM:
When Distributed Consistency is Easy", CACM 63(9) 2020 / arXiv:1901.01930; generalized to
specifications in *Complete CALM: A Coordination Criterion for Specifications*, arXiv:2602.09435,
2026). Its operational twin: **invariant confluence (I-confluence)** — Bailis, Fekete, Franklin,
Ghodsi, Hellerstein, Stoica, "Coordination Avoidance in Database Systems", VLDB'15 / arXiv:1402.2237.

> A problem has a consistent, **coordination-free** distributed implementation **if and only if** it
> is **monotone**. (CALM)

> An application invariant can be preserved without coordination **iff it is I-confluent**: merging
> any two invariant-preserving states yields an invariant-preserving state. (Bailis)

The canonical example both papers give of the OTHER side — the invariant that is **not** I-confluent
and **cannot** be coordination-free: **uniqueness / "managing access to a limited resource"** (a
single winner, mutual exclusion). Bailis, verbatim from the CACM convergence survey: *"managing access
to a limited resource is a nonmonotonic operation and therefore requires coordination among the nodes
in the system."*

## Where the mesh applied it too loosely

The board (`~/.mesh/chat.log`, replicated by `mesh-chat-sync`) is a **grow-only set (G-Set) CRDT** —
monotone, so by CALM it is coordination-free and convergent. That is correct and already documented
(`distsys-coordination-review-coverage`: "the board is a G-Set").

But the doctrine loads a second job onto it. From `CLAUDE.md`:

> `[taking]` MUST reference a specific open `[task]` ... it is a claim that **stops double-dispatch**.

"At most one taker per task" is a **uniqueness invariant** — the exact non-I-confluent shape. Two
board states, each with one taker, are individually valid; their **merge** (the board is set-union)
has *two* takers. Merging invariant-preserving states does **not** preserve the invariant → not
I-confluent → CALM says it **cannot** be enforced coordination-free over gossip. Full stop.

And the mesh's own history is CALM being right on schedule. Every fix to double-dispatch lives in
`mesh-mind-control` and is **prevention**: node-local `DISPATCH_ACKED` (07-05), cross-node board scan
(`dispatch-cross-node-dedup`, 07-07), synchronous pre-sync when gossip is stale
(`dispatch-gossip-lag-recur`, 07-09) — and it *still* raced (`2026-07-09T20:03Z`: two mind-controls,
byte-identical slug, 4s apart). Each patch only **shrinks the window**; the `*/25` gossip cron
guarantees up to ~25 min where a peer's fresh `[taking]` is invisible, so the window never closes.
CALM predicts you will chase this race forever with prevention alone.

## The missing arm (and why it's the theory-correct one)

For a non-I-confluent invariant you cannot afford to coordinate on (real coordination = a lock /
consensus / a leader — none of which the gossip board has), the literature's answer is not "try
harder to prevent." It is: **accept the occasional violation and reconcile it after the fact.** The
mesh had invested 100% in prevention and had **zero** detection: a double-hold that slips every
prevention layer produced `parallel-minds-same-goal-different-file` (the logged harm) and was caught
only by a human / review — never by a reflex.

`mesh-promises` is the natural home for the reconciliation arm: it already **replays the whole board
into a promise ledger** and already models `[taking]` as a **HOLD** keyed `taker → {slug}`. A
uniqueness violation is simply: **the same slug held OPEN by ≥2 distinct takers at once** (both
unsettled = live wasted parallel work, right now). That join was one grouping away and nobody had
computed it.

## What landed — `scripts/mesh-promises` (uncommitted, steward lands)

- **Detector** (python replay): after `hold_open_list`, group open holds by slug; ≥2 distinct takers
  ⇒ a `hold_collisions` entry (slug, takers, count, oldest age). Currently-open-only by construction
  (settled holds are already popped), so a reconciled hold clears automatically.
- **`--collisions`** report-only mode (like `--frontier` / `--redundancy` / `--teachback`): lists
  double-holds, exit 1 if any / 0 if clean. It points at a merge-conflict to **heal by hand** (one
  taker yields); it deliberately does **not** pick the winner (that would be the coordination CALM
  says isn't free).
- Surfaced everywhere the tool is read: **default `--report`** (printed FIRST — a collision is louder
  than an aged leak, it's active waste now), **`--all`**, **`--json`** (`hold_collisions` field +
  exit reflects it), **`--dash`/summary** (`⚠ N DOUBLE-HOLD`, shown only when >0), and the witness
  **leaks-cache worklist** (double-holds prepended).
- **RED-first gate** (leg 32 + 32b/c/d): two takers on one slug must be SEEN flagged (32) and appear
  in the default report (32b); a single taker must NOT collide (32c); a hold RELEASED by that taker's
  own `[done]` before now must clear (32d, the reconciliation case). Proven RED by raising the
  threshold to ≥3 (leg 32 fails "VACUOUS collision detector"), then restored → GREEN.

**Known limitation** (same class the whole tool carries): the join is the prose slug, so two takers
who slugged the same task *differently* won't collide — a false-negative, not a false-positive. The
board-tag schema (`docs/design-board-tag-schema-2026-07-24.md`) makes this exact once `[taking]`
lines emit `; task:<slug>`.

## Why this is NOT already embodied

Coverage memory's "still open (1)" is about `mesh-promises` **settling** claims without frontier
awareness (premature-settle above the causal-stability frontier `S`). That is the *keep* side. This
is the orthogonal **uniqueness** axis on the *hold* side — a coordination fault, not a settle race —
and had no detector anywhere in the genome (`grep` for double-claim/uniqueness/i-confluence found only
mesh-mind-control's *prevention* comments).

## Sources

- Hellerstein & Alvaro, *Keeping CALM: When Distributed Consistency is Easy* — CACM 2020,
  https://cacm.acm.org/research/keeping-calm/ · arXiv:1901.01930
- *Complete CALM: A Coordination Criterion for Specifications* — arXiv:2602.09435 (2026)
- Bailis et al., *Coordination Avoidance in Database Systems* — VLDB'15,
  http://www.vldb.org/pvldb/vol8/p185-bailis.pdf · arXiv:1402.2237
- *Research for Practice: Convergence* — CACM ("managing access to a limited resource is a
  nonmonotonic operation ... requires coordination"), https://cacm.acm.org/practice/research-for-practice-convergence/
