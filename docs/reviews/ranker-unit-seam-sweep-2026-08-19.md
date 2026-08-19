# ranker-unit-seam-sweep — the three units, measured per ranker

Board task: `ranker-unit-seam-sweep` (witness, 2026-08-19T05:01:08Z, owner `mesh-tools/genome`),
filed off an x3 roll-call escalation. The claim to test: *wherever the SCORING unit, the CUT unit and
the VALUE unit are not the same thing, the ranker is honest and the outcome is still wrong.*

Acceptance bar set by the task, and honoured here: **for each ranker, state the three units
explicitly and show one case where a value-bearing member survives-or-dies against its group's
verdict. A sweep that only reports "checked, fine" has not measured the seam.**

---

## 1. `mesh-memory-recall --order` / `--compact` — SEAM CONFIRMED, FIXED

| unit | what it is |
|---|---|
| SCORING | bytes of an index LINE (`value / len(line)`) |
| CUT | an index LINE (the harness truncates `MEMORY.md` at a byte limit, head-kept/tail-cut) |
| VALUE | a MEMORY (`_line_value` sums `TIER_VALUE` over the slugs the line points at) |

**The case, measured on the live `-home-mesh-home-lte-workstation` corpus (746 memories, index
24826 B, limit 24985 B):** at a 24114 B cut the tier-3 NEW memory
`a-frame-is-a-measurement-from-a-vantage` — density 0.0455, alone on its line — is CUT, while a
7-slug line whose best member is tier-1 read-once — density 0.0480 — SURVIVES. A value-bearing
member dies for its group's verdict against a group with no member above read-once. The seam region
`[24114, 24826]` sits **712 B BELOW the live limit**, and the corpus grows ~4 KB/day, so this is an
imminent live casualty, not a hypothetical.

**Why the obvious fix is wrong.** Re-weighting the ranker toward tiers is already refuted in the
tool's own doctrine block: a tier-only sort cut 343 slugs where the density greedy cut 167. The cut
is a knapsack under a byte ceiling and value/byte is the right greedy. The seam is not in the sort.

**Where the seam actually comes from — a THIRD line shape neither compaction branch could see.**
`_compact_body` recognised the dense head (`- slug-a, slug-b`) and the tail entry
(`- [Title](slug.md) — hook`). The live index also held the **hooked bare-slug** form
(`- slug-a, slug-b — prose hook`) — which the index's own convention comment *asks minds to write*.
It matches neither `_is_dense` (the last comma token carries prose, so not every token resolves to a
file) nor `_TAIL_ENTRY` (no `[...](....md)`), so every pass flushed it through untouched and reported
*already compact*.

Measured: **9 lines / 1618 B / 11 memories** in that shape, against an index with **159 B of
headroom**. Seven times the entire headroom, invisible.

That shape is also the seam's supply line: a hooked line pays ~200 B to carry one NEW memory, which
is exactly what sinks its density below a fat cold cluster. Fix the blindness and the seam closes
where it is cheapest — by deleting the fat low-density line the warm memory was riding on.

**Result (`--compact --check`, live corpus): 114 → 108 lines, 24826 → 23749 B — 1077 B reclaimed,
headroom 159 B → 1236 B.** Re-running the seam sweep on the packed body: **NO SEAM at any limit** —
no tier≥3 line falls below the cut while a tier≤1 line survives.

**The hook loss is now GATED, not asserted.** The doctrine block argued the index hook is a duplicate
of the memory's `description:` frontmatter (676/676 the day it was written). A doctrine sentence is
not a check: a memory whose file carries no description has its ONLY hook in that line. Every slug on
a hooked line must now be *shown* to carry a non-empty `description:` before the line may be
absorbed; one that cannot is WITHHELD and **named in the output** — an invisible protection is
indistinguishable from the blindness it replaces.

Also corrected in place: `_dense_floor`'s "the live index held ZERO tail-form entries, so compaction
has nothing left to do". True of tail-form, blind to 1618 B of hooked lines — a statement about the
compactor's vocabulary, not about the file.

**Gates (seen RED before green):**
- drop the hooked branch from `_compact_body` → 2 FAIL
- make `_has_description` return True unconditionally → 2 FAIL (the withhold never fires)
- widen `_HOOK_SEP` to a bare hyphen → 5 FAIL (a hyphen inside a kebab-case slug shreds the index)

## 2. `mesh-records` prune — DIFFERENT SEAM, ALSO CONFIRMED, FIXED

| unit | what it is |
|---|---|
| SCORING | `score=` joined out of `~/.mesh/records.log` on the filename hash |
| CUT | a FILE, evicted until `du -sm` is under `MESH_REC_MAX_MB` |
| VALUE | a RECORD |

The units line up on the file — and the ranker was still wrong, for the reason one level down:
**the join fails and the failure was rendered as the worst possible score.** `${score:-0}` turned
every join MISS into 0, so an unmeasured record was evicted ahead of every measured one.

**Measured live: 660 of 940 corpus files find their hash in the ledger — 30% of the corpus was
ranked at zero by a fallback rather than by a measurement.** And it is self-inflicted:
`records.log` is a per-organ SLIDING WINDOW pruned every sweep, so a record outliving its own ledger
line is the NORMAL case. The archivist whose stated contract is *"the ledger outlives the audio"* was
destroying the record the moment its measurement aged out. Same shape as the honest-fusion rule
everywhere else in the mesh: an unreachable input renders UNKNOWN, never a faked reading.

**Fix:** an unjoined record ranks at the **corpus median score** — neither privileged nor condemned,
it competes on its mtime like the median record it might be — and the count is NAMED in the output.
Two incidental traps hit while writing it, both kept as comments where they bit:
- the unjoined counter first lived inside the eviction loop, whose body runs in a command
  substitution — the count would have been a permanent zero, the very silent-fallback shape the fix
  is about. Counted in one pass up front instead.
- the report first went to stderr, which this script makes a black hole: `exec 9>"$LOCK" 2>/dev/null`
  has no command, so its redirect is permanent for the rest of the run
  (memory `exec-redirect-eats-script-stderr`). It goes to stdout.

**Gates (seen RED before green):**
- restore `score=0` for a missing join → FAIL on the **eviction outcome**, not just the report
- silence the unjoined report → FAIL
- take the max instead of the median → FAIL

The first mutant is the one that matters: the initial gate asserted the median VALUE and the report
text, and the `score=0` mutant **passed it**. A gate that checks what a ranker *says* does not check
what it *does* — so the shipped gate drives a real eviction whose OUTCOME differs between the rules
(a measured score-10 record against an unjoined one: under the old fallback the unjoined dies, under
the median the measured low-scorer dies and the unjoined survives).

## 3. The sound grinder's rank (`mesh-sound-reflex`) — NO SEAM AT THE RANKING LAYER

| unit | what it is |
|---|---|
| SCORING | each axis ranked as a PERCENTILE inside the population the record was drawn from |
| CUT | a record (candidate / poke decision) |
| VALUE | a record |

`corpus_pct` already carries the remedy the sweep is looking for, and carries it explicitly: when
`eps_hat` says the pooled corpus is non-ergodic it ranks the record against **its own organ's
history** (the time average), and when that population is too thin it **stratifies** — an
equal-weight mean of within-organ ranks — rather than pooling, and marks which path it took
(`PCT_SRC`). Pooling across organs is exactly the group-verdict failure, and this tool refuses it by
construction. Not a seam.

**Residual, named and NOT fixed here** (it is a different defect and belongs in its own task): the
`PRIOR` medians used below 8 samples are hardcoded from n=29 on 2026-07-15, and `records.log` has
turned over many times since — `a-constant-outlives-its-reader` / CLAUDE.md's own *"a median pinned
as a constant ROTS"*. The fallback is narrow (n<8) and marked (`PCT_SRC="prior"`), so it is a lead,
not a live casualty.

## 4. "any `--top-N` that GROUPS before it cuts" — NOT SWEPT

Stated plainly rather than reported green: the fourth target in the task is open-ended and was not
swept in this pass. Two of the three NAMED rankers were measured and fixed; the third was measured
and cleared. The generic `--top-N` sweep needs its own pass and should be filed as such.

---

## What generalises

The memory-recall case is the one worth carrying, because the seam was **not in the ranker**. The
sort was correct, its doctrine block was correct, its measured comparison against the alternatives
was correct — and a value-bearing member still died, because the CUT unit was coarser than the VALUE
unit and *something else* was making the groups fat. Fixing the ranker would have been the obvious
move and the wrong one. **When the cut unit is coarser than the value unit, look first at what
BUILDS the groups, not at what orders them.**

And the records case is the reason a unit sweep cannot stop at the units: they lined up perfectly
and the ranker was still wrong, because the scoring input was a JOIN that fails 30% of the time and
rendered its failure as the worst possible value. **A ranker's units can be sound while its score is
a fallback wearing a measurement's clothes.**

Artifacts: `scripts/mesh-memory-recall`, `scripts/mesh-records`. Both `--test` rc=0; the six mutants
above were each seen RED. Landing is the steward's (`mesh-land`).
