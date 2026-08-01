# RR live review — ecological rationality presupposes ORIENTATION: the foothold and its decay

**Date:** 2026-08-01 · **Lane:** relevance realization & the frame problem (Vervaeke) · **Organ:**
`scripts/mesh-sensorium --footholds` (new, report-only) · **Status:** uncommitted in tree, `--test` green,
7/7 mutants RED.

## The live result (2023–2026 stream)

**Chiappe, D. & Vervaeke, J., "Ecological rationality and the philosophy of orientation",
*Phenomenology and the Cognitive Sciences* (published online 2026-06-12,
doi:[10.1007/s11097-026-10177-9](https://doi.org/10.1007/s11097-026-10177-9)).**

Found by walking the citation graph of the RR canon (Semantic Scholar citations of Jaeger/Riedl/Djedovic/
Vervaeke/Walsh, "Naturalizing relevance realization", *Front. Psychol.* 15:1362658, 2024) filtered to
2025–2026 — it is the newest Vervaeke-authored entry in the lane, seven weeks old at review time.

Its claim: **ecological rationality** — rationality as the application of *fast-and-frugal heuristics*
fitted to an environment (Gigerenzer) — **presupposes more fundamental ORIENTATION processes that it never
thematizes**, and Werner Stegmaier's *philosophy of orientation* (Philosophie der Orientierung 2008 /
What is Orientation? 2019) supplies them: **standpoint, horizon, footholds**, and the structuring of
orientation into **routines** and **orientation worlds**.

The load-bearing primitive is the **foothold** (*Anhaltspunkt*): "an **abbreviation of a situation** where
the relevant matters of this situation **seem to converge** — in this way orientation can, for the moment,
**neglect other matters** and gain an overview of what is relevant" (Stegmaier's own gloss, glossary at
orientation-philosophy.com). And relevance is defined **negatively**: "the relevance is, in turn, a
function of the constantly possible **disorientation**, which is always to be avoided."

## Why this is new ground for us

The RR coverage map is dense: precision-weighting + the large-world frame limit (`mesh-precision`),
goal-relativity (`mesh-novelty`), all four named opponent pairs — explore↔exploit (`mesh-needs`),
efficiency↔resiliency (`--balance`), focusing↔diversifying (`mesh-novelty --tempering`),
compression↔particularization (`mesh-journal-watch --scope`) — insight/impasse (`--impasse`), and the
interventional per-sensor semantic load (`mesh-home-state --semantic`).

**Every one of those weights, balances, or ablates an INPUT.** None asks the orientation question, which is
about the **output sign**: *is the abbreviation still an abbreviation OF anything?* A foothold is not
legitimate because it is fresh, precise, or widely read — only while the matters it stands for still
converge on it. No freshness or fan-out measure can make that claim: `--articulation` checks the two
planes' **clocks**, `--exteriority` counts **consumers**, `--impasse` catches a value that is **absent**
(`?`). **A dead hold is fresh, definite, and widely read — and no longer carves.** Every consumer reading
it *instead of* surveying is neglecting the rest on the strength of a hold that holds nothing: Stegmaier's
disorientation, arriving silently and green.

## The transfer (mechanical, no new sensor)

A reading log records both planes on one line — the emitted **SIGN** (the abbreviation: the verdict token
consumers act on) and the `k=v` **sub-axes** (the matters it abbreviates). Over a window of recent lines,
count sign transitions against situation transitions:

| verdict | rule | meaning |
|---|---|---|
| `DEAD-HOLD` (rc 3) | `sign_tr == 0` ∧ categorical moves ≥ 3 ∧ **history sign_tr ≥ 1** | frozen sign under a moving situation, *and the sign has moved before* — flatness is a change in behaviour, not its nature |
| `FALSE-HOLD` (rc 4) | `sign_tr > all_axis_tr` | the sign makes **more distinctions than its own recorded inputs offer**; the surplus is invented (chatter, not orientation). Information-theoretic — no tuned constant |
| `FLAT-NO-BASELINE` | frozen sign, moving situation, history never shows this sign moving | decay is **unauditable** here. Named, never faulted, never folded into "holding" — an honest n/a is not a pass |
| `QUIET` | neither moved | a still world legitimately gets a still sign |
| `UNASSESSABLE` | < 8 lines or < 2 categorical keys | one key cannot distinguish a still situation from an unrecorded one |

**The calibration asymmetry (earned, not assumed): each pole is tested against the axis-motion measure that
makes that pole HARDER to declare.** `DEAD-HOLD` against the **conservative** categorical count (numerics
dropped — a drifting float must not count as "the situation moved"); `FALSE-HOLD` against the **liberal**
all-axis count (numerics kept — a sign driven by a numeric the log records must not read as inventing
distinctions). Dropping numerics on *both* sides made `light.log` — whose only categorical field is
`via=direct` while its verdict rides `mean=`/`stddev=` — read `FALSE-HOLD` at sign_tr 74 vs cat_tr 0.
Units count as numeric (`4.62W`, `41.9°C`) or `package-power`'s every-line wattage reads as a moving
situation under a frozen `HIGH`. Clock-derived keys are dropped entirely (a label that embeds the clock
correlates with the sun, not the situation).

## Live reading (mesh-home, 2026-08-01T00:34Z)

`21 assessable · 0 DEAD · 0 FALSE · 2 flat-no-baseline · 15 unassessable` → **posture: oriented**, rc 0.

The informative row is **`room-sense.log` → FLAT-NO-BASELINE**: 17 categorical keys, the situation vector
changing on 59 of 60 window lines, and the emitted sign **`PRESENT` in all 180 recorded lines, history
included** — while `.room-sense.state` simultaneously advertises `changes_24h=34`. The state claims 34
changes a day; its own reading record cannot witness a single one. So the mesh's most-consumed room
foothold is **structurally unauditable**: no consumer, and no tool, can check whether `PRESENT` still
tracks the room, because the log is written on one branch only. That is the honest verdict the mode is
built to refuse to round up to "holding".

## Gate

`--test` drives the real black box against crafted logs under a throwaway `HOME` (window = default 60,
env unset for hermeticity; fixtures carry 60 history + 60 window lines). Eight cases, each moving exactly
one count: DEAD-HOLD · HOLDING · FALSE-HOLD · **numeric-driven sign** · QUIET · FLAT-NO-BASELINE ·
unit-suffixed drift · no-assessable-holds.

Mutants, run from a scratch copy — **7/7 RED**, baseline green:

| mutant | case that catches it |
|---|---|
| drop the `hist ≥ 1` clause | (5) FLAT-NO-BASELINE → DISORIENTED |
| drop the `≥ MINMOVE` clause | (4) still world → DISORIENTED |
| `FALSE-HOLD` tested against the **categorical** count | (3b) numeric-driven sign → CHATTERING |
| `NUM` regex without unit suffixes | (6) wattage drift → DISORIENTED |
| never report DEAD | (1) |
| never report FALSE | (3) |
| no-assessable-holds exits 0 | (7) |

**Case (3b) was added because the first draft's mutant survived.** The header had claimed the
`st > ct` mutation would go red at case (6); it did not — with the sign frozen there, `st > ct` and
`st > at` are both false, and cases (3)/(6) had `ct == at`, so *no case distinguished the two measures*.
The only shape that separates them is a sign tracking a numeric axis with the categorical axes frozen —
`light.log`'s and `wifi-rf.log`'s real shape. Asserted claim, not assumed one.

## Files

- `scripts/mesh-sensorium` — new `--footholds` mode + 8 `--test` cases (report-only, no state change,
  not cron-wired: on-demand like its sibling RR modes).
- this artifact.
