# Live literature review — distributed systems coordination

**Area:** gossip / CRDTs / eventual consistency · **Angle:** recent result (2024-2026)
**Date:** 2026-08-15 · **Organ:** `scripts/mesh-chat-sync` · **Status:** uncommitted in tree, steward lands

---

## The concept we did not embody

**Similarity-regime-dependent set reconciliation** — the finding that reconciliation cost is a
*continuous* function of the **Jaccard similarity J** between two replicas, that **no protocol
dominates the range**, and that the winner **flips at a measured crossover** — so the regime must be
known *before* a mechanism is chosen.

Sources, all read this session:

| Paper | Where | What it establishes |
|---|---|---|
| **ConflictSync: Bandwidth Efficient Synchronization of Divergent State** — Pedro Silva Gomes, Miguel Boaventura Rodrigues, Carlos Baquero | [arXiv:2505.01144](https://arxiv.org/abs/2505.01144), May 2025 | First **digest-driven** state-based CRDT sync. Reduces synchronization to the *set reconciliation of **irredundant join decompositions*** — ship the lattice's join-irreducible components, not the state. Up to **18× less transfer** than full-state. **Crossover: Bloom prefiltering cuts overhead up to 50% at J≈0, but pure rateless reconciliation wins above J≈93%** — past that the prefilter is dead weight. |
| **Rateless Bloom Filters: Set Reconciliation for Divergent Replicas with Variable-Sized Elements** — Gomes, Baquero | [arXiv:2510.27614](https://arxiv.org/abs/2510.27614), 31 Oct 2025 | RBF adapts to an *unknown* symmetric-difference size. RBF+IBLT hybrid beats the state of the art by **>20% below J≈85%** — and the paper says plainly it is **not** the right choice for anti-entropy between near-identical replicas. |
| **Practical Rateless Set Reconciliation** (RIBLT) — Lei Yang, Yossi Gilad, Mohammad Alizadeh | ACM SIGCOMM 2024, [arXiv:2402.02668](https://arxiv.org/pdf/2402.02668) | The substrate both build on: encode the difference as a rateless stream of coded symbols, so no advance estimate of \|d\| is needed at all. |

**Why this is new for us.** `mesh-chat-sync` already carries Dynamo-style Merkle anti-entropy as a
documented HELD item — but it frames the gap as a **binary**: "root digests equal ⇒ ship nothing,
else ship everything." The 2024-25 literature says the binary is the wrong shape. And we could not
have chosen between the families anyway, because **the round summary counted lines *gained* and never
lines *shipped*** — the denominator of every efficiency claim about this reflex was missing.

Prior coverage checked (all still embodied, none of them this): G-Set union · PBS t-visibility
(`--lag`) · vAoI/Age-of-Gossip (`gained@last`) · HLC ordering · causal-stability frontier
(`--frontier`, 2026-07-28) · metastable failure (`mesh-quota`) · Lifeguard local health awareness ·
CALM/I-confluence double-hold (`mesh-promises`) · φ-accrual (`mesh-presence`).

---

## Landed: `scripts/mesh-chat-sync --similarity`

Visibility-only. Does **not** change the pull — the mechanism stays the steward-gated held item.

- `jaccard_pm A B` → J in integer per-mille over the **dated-valid uniq line sets** (a board line *is*
  the G-Set element, and ConflictSync's "constituent component"). No bc/python — phone nodes run this.
  Empty union ⇒ **-1 = UNKNOWN**, never a fabricated 0 or 100%.
- `sim_band` → HIGH / MID / LOW at **930‰ and 850‰ — the papers' measured crossovers**, not invented
  round numbers — each naming the protocol family that regime calls for.
- Measured in the pull loop against the **pristine** local snapshot (`$tmp.snap`), *not* the
  accumulating `$tmp`: otherwise a peer's similarity would depend on where it fell in the pull order.
  `count_gained` deliberately uses the accumulating side (realized vAoI = what the round still
  needed) — two different questions over the same two files.
- Persisted as LAGF fields 4-5 (`J‰@last`, `shipped@last`). **Forward-compatible**: verified the
  *deployed* older copy's `--lag` and `--frontier` read the 5-field file correctly.
- Round summary now carries shipped/needed and the redundancy ratio.

---

## What the measurement found (the reason this matters)

First live run, this node vs phaedra:

```
root@100.94.116.17   J=29.2%  shipped=3000  needed=1642  redundancy=1x  [LOW]
```

**J did not move across consecutive rounds.** A convergence metric that never rises is a
non-converging anti-entropy. Diagnosed directly:

```
local board:   3000 lines  oldest=2026-07-31T10:44:13Z
phaedra board: 3000 lines  oldest=2026-07-11T22:01:37Z
union: 4643                                    ← exceeds the tail -3000 cap by 1643
of the 1642 lines phaedra has and we lack: 0 newer than our oldest, 1643 older
```

**Every line pulled is older than our eviction window, so `sort -u | tail -3000` discards all of them
in the same round they arrive — then we re-pull and re-discard them every 3 minutes, forever.** 100%
of a 3000-line transfer wasted per round, while the summary printed *"gained 1642 new line(s)"*,
which reads exactly like progress. This has been green for as long as the fleet union exceeded 3000.

It also **inverts the held Merkle item**: at J=29% a root-digest pre-check would essentially never
match, so it would save nothing here. The real problem is upstream of reconciliation entirely.

### Second landing: `treadmill_verdict` (the incident detector)

`survivors` = lines in the converged merge absent from the pristine pre-round board.
`gained>0 ∧ survivors=0` ⇒ **EVICTION-TREADMILL** on the same summary line the "gained N" claim rides,
plus one debounced `[gap]` board post (6h). A standing condition, not an event. Not a fix — the
cap/eviction-window is a steward call.

**A first draft of this shipped the bug it exists to catch.** It measured survivors against the
*committed* `$LOG`, which also carries local posts made during the round — one such post inflated
survivors 0→1 and silently demoted a total treadmill to `PARTIAL 0%`, suppressing the board post.
Caught live at 02:34Z. It now measures against `$LOG.new`, the pure merge result with no local writer
in it. Live at 02:35Z it fires correctly.

---

## Gates (RED-first, every one proven red then restored)

| # | Mutant | Result |
|---|---|---|
| 1 | `un = na+nb` (union forgets `-ni`) | RED — identical sets → 500 |
| 2 | crossover 930 → 900 | RED — `sim_band 929 → HIGH` |
| 3 | `known -eq 0` honest-UNKNOWN guard removed | RED — rc0 instead of rc1 |
| 4 | regime follows the **average** instead of the worst peer | RED (only after the fixture was rebuilt to straddle a band edge — with both peers in one band this mutant passed) |
| 5 | junk filter dropped on one side | RED — junk counted as an element |
| 6 | `all-redundant` → `-` | RED |
| 7 | `TREADMILL` collapsed to `PARTIAL 0` | RED |
| 8 | quiet-round `g<=0` guard dropped | RED — a converged idle tick reads TREADMILL |
| 9 | non-numeric guard removed | RED **only via the stderr leg** — asserting the stdout verdict alone was vacuous (bash's failed `-le` falls through to OK anyway) |

**Known coverage limit, stated rather than papered over:** the *wiring* inside the SSH pull/merge path
is not offline-testable — mutant 11 (`survived_round="$gained_round"`, which makes the treadmill
unfireable) passes the smoke test. Same boundary the pre-existing `count_gained` call site has. The
helpers are gated; their call sites are proven by the live run above, not by `--test`.

---

## Still open

1. The held Merkle/digest pre-check — now **evidence-informed**: measured J=29.2% puts this fleet in
   the LOW band where a digest binary saves nothing and the literature points at RBF+IBLT. Revisit
   after the eviction window is settled, since J is meaningless while the treadmill runs.
2. The eviction window itself: fleet board union (4643) > cap (3000). Options are a bigger cap, a
   time-windowed rather than count-windowed board, or accepting divergence explicitly. Steward call.
3. `mesh-promises` settling claims with zero propagation-awareness (carried from 2026-07-28).
