# Autopoiesis live review — SEMANTIC CLOSURE: who wrote the sense's threshold

**Task:** auto idea-queue — LITERATURE (live review): autopoiesis & the biology of cognition
(Maturana, Varela), from the angle of a concrete METRIC or experiment the area uses to measure itself.
**Date:** 2026-08-16 · owner: genome · **Landed** (uncommitted in tree; steward lands)
**Artifact:** `scripts/mesh-closure --semantic` (+ `--semantic-sites`), report-only.

---

## The concept — and it is LIVE, not a fixed-list classic

**Semantic closure.** Autopoiesis asks whether a system produces its own *components*. Semantic
closure asks the sharper question one level up: does the system produce its own **interpreters** —
the constraints that map a signal to a functional consequence?

Found in the live literature, published 2025 and still moving:

- **Amahury Jafet López-Díaz & Carlos Gershenson, "Closing the loop: how semantic closure enables
  open-ended evolution?", *Journal of the Royal Society Interface* 22(233):20250784 (2025)** —
  PubMed [41537873](https://pubmed.ncbi.nlm.nih.gov/41537873/); preprint
  [arXiv:2404.04374v7](https://arxiv.org/html/2404.04374v7) (read 2026-08-16, full text).
  Also presented at the Santa Fe Institute (2025).
- Lineage: Pattee's semantic closure → Rosen (M,R)-systems → Hofmeyr (F,A)-systems, given a
  **temporal parametrization** by this paper.
- Same author pair as **arXiv:2606.23122** ("A Matter of Time"), which this repo already cites for
  `mesh-closure --timescale`. This is a **different criterion** from that paper's constraint
  conservation — the lineage is live, the concept is new to us.

**The measurable the paper supplies** is a ladder, each rung a formal-language class, and the rung
is set by *where the interpreter comes from*:

| rung | class | interpreter |
|---|---|---|
| 1 | finite automaton / regular | imposed by the environment (geochemistry) |
| 2 | automaton with memory / context-free | loop not self-closing; still external |
| 3 | stream X-machine / context-sensitive | partially intrinsic, not self-constructing |
| 4 | **semantically closed** | *"symbols actively construct and interpret their own functional contexts"* — the system manufactures its own measurement and control apparatus |

Verbatim on the boundary: a system whose interpreters are provided from outside "remains
computationally simulable" and is robust **only while the environment keeps supplying** them; only
self-construction gives robust self-replication and open-endedness.

## Why this is NOT already embodied

Zero prior hits for `semantic closure` anywhere in `scripts/` or `docs/` (checked).

Every closure axis the mesh already owns is about the **producer of a component or a commit**:

| existing axis | asks |
|---|---|
| `mesh-vitality allopoiesis_gap()` | who closes the land loop (latency) |
| `mesh-vitality heteronomy_index()` | who pays for the cognition (dollars) |
| `mesh-closure` graph / `--timescale` / `--symmetry` | which reflex enables which, at what clock, in which causal direction |

**Not one of them asks who wrote the THRESHOLD.** Yet a sense's threshold is precisely an interpreter
in Pattee's sense: `[ "$temp" -gt 82 ]` is the constraint that turns a number into "hot", and 82 was
chosen by an author outside the organization. Nothing regenerates it; nothing measures whether it
still cuts where the node's own data cuts.

The mesh has the *doctrine* already — and every instance of it was found by hand, one at a time:
`stress-thermal-bands-calibrated-to-a-dead-regime`, `a-decode-table-copied-from-memory-baselines-away-the-alarm`,
`a-constant-outlives-its-reader`, and CLAUDE.md's own soundscape rule ("calibrate a derived axis
against the REAL corpus, never an assumed 0..1 … a median pinned as a constant ROTS"). What did not
exist was the **metric**.

## What was built — `mesh-closure --semantic`

A **decision site** is a numeric comparison in a tool's shell body (`-gt/-ge/-lt/-le` in a test, or
`< > <= >=` inside `(( ))`). The compared-against operand is the interpreter, classified by provenance:

- **SELF** — traces to a runtime read of the mesh's own record (a command substitution touching a
  `mesh-*` tool or a `.mesh/` / `.log` / `.tsv` / `.jsonl` artifact) — an interpreter the
  organization manufactured.
- **IMPOSED** — a numeric literal at the site, or a variable whose *every* assignment is a literal
  or a `${ENV:-<number>}` default. An env override is still external instruction.
- **UNRESOLVED** — untraceable operand. Honest n/a, never folded into a class.
- **TRIVIAL** — cut-point 0 or 1. A presence/emptiness test has no calibratable degree of freedom,
  so it is not an interpreter; excluded from SCI and reported.

**SCI = SELF / (SELF + IMPOSED)** over non-trivial traceable sites.
Rung: `IMPOSED` (0) · `PARTIAL` · `CLOSED` (1) · `n/a`.

## The live reading (mesh-home, 2026-08-16, 637 tools)

```
decision sites: SELF=3  IMPOSED=1008  UNRESOLVED=522 (honest n/a)
TRIVIAL=888 excluded    OPAQUE=175 tools
SCI = 0.0030 over 1011 assessable sites
```

**And the three SELF sites do not survive being read.** All three are gate assertions inside smoke
probes — `mesh-chat` comparing its `chat.log` line count before/after a post (×2), `mesh-dispatch`
comparing two line numbers it greps out of its own source. So the shell-visible **production**
reading is **SCI = 0 — rung 1, the whole sensorium**. This is why the tool prints every SELF site in
full rather than a count: a bare `SELF=3` would have read as partial closure.

Deepest interpretive debt (freestanding cut-points per tool):

```
mesh-dash 43 · mesh-light 30 · mesh-socket-state 23 · mesh-dispatch 21 · mesh-stress 19
mesh-ambient-clock 17 · mesh-ideate 17 · mesh-sensorium 16 · mesh-mind-control 15 · mesh-bruno 12
… 282 further tools carry at least one
```

## Honesty bounds (the blind spot is a printed number, not silence)

- **Shell comparisons only.** A tool that computes a robust baseline inside an embedded awk/python
  body and cuts on it there — `mesh-ambient-shift`'s median+MAD, `mesh-algedonic`'s trailing-median
  habituation — is genuinely *partially* self-calibrated and this scan cannot see it. Tools with no
  traceable non-trivial site but an embedded awk/python/jq body are counted **OPAQUE=175** and
  named. **SCI under-counts SELF**, and says so on every render.
- **IMPOSED is conservative**: a variable is IMPOSED only when *every* assignment in the file is a
  constant expression; any untraceable assignment demotes it to UNRESOLVED. The debt list is a
  high-precision lower bound.
- **Test-harness bodies are skipped** (the same exact-`_`-component rule `--enacted` uses), by
  **brace DEPTH** rather than the first column-0 `}`. That refinement was forced by this tool's own
  `--test`: its fixtures write file text containing a column-0 `parse_x() { … }`, a depth-blind skip
  ended there, and 6 of the tool's own fixture literals (42, 7, 99, `$LIM`, `$T`, `$V`) entered the
  live census. Found by watching the live TRIVIAL count drift 898→900→901 across runs while only the
  tool's own source changed. Fixture `mesh-fs6` reproduces the shape and is the only leg that
  falsifies the depth counting.
- **Provenance is not appropriateness.** A literal can be exactly right (a protocol constant, a
  percentage bound). This axis measures who wrote the interpreter, never whether the value is
  correct. Report-only, advisory, judges nothing, touches no state.

## Gate — RED-first, 6 mutants each seen red for the right reason

Fixture: 6 synthetic tools pinning one instance of each class, asserted as an **exact set** (not
just counts — a class landing on the wrong tool would keep every count green).

| mutant | observed |
|---|---|
| drop the TRIVIAL set (driven from outside via `MESH_CLOSURE_SEM_TRIVIAL=""`, so this leg is executable, not asserted in a comment) | TRIVIAL 2→0, IMPOSED 4→6, SCI moves off 0.2000 |
| `kindof()` command-substitution arm → `IMPOSED` | SELF 1→0, rung PARTIAL→IMPOSED, closed-organ line gone |
| delete the pass-2 full-line-comment skip | fs2's prose threshold 99 becomes a 5th IMPOSED |
| `varclass()` → always `IMPOSED` (fold the honest n/a away) | SELF 1→0, IMPOSED 4→6, UNRESOLVED 1→0 |
| drop the OPAQUE emit | OPAQUE 1→0, the blind-spot line disappears |
| depth-blind test-body skip (first column-0 `}`) | fs6's fixture literal 77 enters: IMPOSED 4→5 |

`mesh-closure --test`: **PASS**, 3.3s, every pre-existing leg (graph / cadences / timescale /
enacted / symmetry / leakage guard) still green.

## What it does NOT do, and the next step

It does not recalibrate anything and must not: a value-norm that rewrites a live threshold is the
false-revert danger the `mesh-fitness` normativity review is already held on. The honest next step is
the one the metric now makes cheap — take the top of the debt list (`mesh-stress`'s thermal bands are
already a *known* dead-regime calibration) and derive those specific cut-points from the node's own
recorded distribution, turning them SELF one organ at a time, with the SCI trajectory as the receipt.

**Why the number is not an indictment:** the paper's own claim is conditional — an imposed
interpreter is fine *while the environment keeps supplying it*. A mesh whose thresholds are authored
by minds and an operator is exactly that. What SCI names is the **dependence**, and it turns the
recalibration frontier into a ranked list instead of a memory of past incidents.
