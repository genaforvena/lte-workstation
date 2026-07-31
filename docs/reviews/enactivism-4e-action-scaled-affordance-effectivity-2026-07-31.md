# Enactivism / 4E live review — the AFFORDANCE RATIO, and scaling it to CURRENT effectivity

**Date:** 2026-07-31 · **Window:** genome@mesh-home · **Landed in:** `scripts/mesh-load-gate`
(uncommitted in tree — steward lands)

## The metric this area measures itself with

Ecological psychology / 4E's oldest *quantitative* instrument is the **π-number**: an affordance
boundary expressed as a **dimensionless ratio** of an environmental dimension to a body dimension.
Warren's stair-climbing ratio and the aperture ratio A/S ≈ 1.30 (shoulder width) are the canonical
ones — the claim being that the ratio, not the absolute size, is the invariant that transfers
between bodies.

The live literature's refinement is the part that matters here: **the correct scaler is the actor's
CURRENT action capability (effectivity), not its static geometry.**

- **Flach, Schotborgh, Withagen & Smith (2021), "Perception of maximum distance jumpable remains
  accurate after an intense physical exercise and during recovery", *Attention, Perception &
  Psychophysics*, [doi:10.3758/s13414-021-02315-z](https://doi.org/10.3758/s13414-021-02315-z)**
  (open access, [PMC8550116](https://pmc.ncbi.nlm.nih.gov/articles/PMC8550116/)). Squatting to
  exhaustion cut actual jumping distance by ≈32 cm, and *perceived* maximum jumpable distance
  tracked it down and back up during recovery. The body's geometry never changed; the boundary
  moved anyway. Their framing: "affordances exist by virtue of the relationship between the action
  capabilities of the actor and the physical characteristics of the environment."

- **Wang, Mazalek, Sabiston & Welsh (2026), "Virtual reality alters perceived functional body size",
  *Virtual Reality*, [doi:10.1007/s10055-026-01368-5](https://doi.org/10.1007/s10055-026-01368-5)**
  (Crossref issued 2026-05-29; verified live via Crossref + Semantic Scholar — Springer's HTML is
  behind an IdP redirect). This is the metric stated explicitly and freshly: the **affordance ratio
  = perceptual threshold / action threshold**, n=60, passable-aperture paradigm. VR raised *both*
  thresholds; once the vergence-accommodation depth compression was corrected for, "the affordance
  ratios in VR became equivalent to those in UR … demonstrat[ing] a recovered invariant geometrical
  scaling, suggesting that perception remained functionally attuned to action capabilities."

So the measurable is: **perceptual threshold ÷ action threshold**, and a healthy system holds it
constant *by moving the perceptual threshold when the action threshold moves*.

## What we did not embody

`scripts/mesh-load-gate` is the mesh's shed gate in front of ~30 wired heavy reflexes (grind, relay,
vision, librosa, diary). Its boundary was already a π-number — `thr = nproc * 0.9`, load1 expressed
as a dimensionless ratio of the body's core count. That is precisely the **body-scaled** half, and
the wired cron lines don't even use it: every one passes a literal `11`.

The gap is the other half. **`nproc` is static geometry — leg length.** The node's *effectivity*
moves constantly: 16 cores at half clock are not 16 cores of work-per-second, and a run queue of 10
on a down-clocked box drains at half the rate. When the action threshold halves, `11` does not
move, so this gate's affordance ratio silently **doubles** and it admits a heavy grind onto a box
that cannot do the work — exactly the ssh-starvation the gate exists to prevent (operator
2026-07-22, "it keeps killing my ssh").

The sharp part: **the mesh already senses its own effectivity and the gate never read it.**
`scripts/mesh-cpufreq` computes `cur / cpuinfo_max` per CPU, folds it to a band
(BOOST/NOMINAL/REDUCED/THROTTLED/IDLE/OFFLINE), runs on cron `2-59/5`, and caches the ratio at
`~/.mesh/.cpufreq-state`. The fatigue signal was on disk, refreshed every five minutes, unread.

## What landed — `mesh-load-gate --effectivity`

`thr_eff = thr × clamp(effectivity, floor, 100) / 100`, read from mesh-cpufreq's **cached** artifact
(data-frugal; no `/sys` re-probe). Opt-in via `--effectivity` or `MESH_LOAD_GATE_EFFECTIVITY=1` —
default OFF, so all 30+ wired cron lines are byte-identical (verified: `--thresholds` line unchanged
vs `git stash`).

Live artifact, same box, same load, same nominal threshold — only the scaler differs:

```
load1=27.32, thr=41.0, forged THROTTLED artifact (ratio=42%)
  body-scaled   (thr=41.0)        rc=0  PROCEED
  action-scaled (thr=41.0 × eff)  rc=1  SKIP
  → SKIP demo-action — load1=27.32 > threshold=20.5 [effectivity=42% (floored at 50) — thr 41.0 -> 20.5]
```

Design decisions, each with a reason rather than a default:

- **Asymmetric clamp — BOOST grants no bonus (cap 100).** Inherited from the file's own stated
  fail-open asymmetry: a false PROCEED costs one tick of load, a false SKIP silently disables a
  reflex forever. Shedding *more* under throttle is the safe direction; raising the ceiling the
  operator hand-tuned against ssh starvation is not. This is a deliberate departure from "both
  edges of a signal need the same gate", stated in the header so it reads as a decision.
- **Floor (`MESH_LOAD_GATE_EFF_FLOOR`, default 50).** No absurd reading can drive the threshold
  toward zero and permanently disable every heavy reflex.
- **Honest-fusion.** Unknown / missing / stale (> `MESH_LOAD_GATE_EFF_TTL`, default 1800s) /
  `OFFLINE` / unparseable effectivity → **unscaled**, never a fabricated 100. mesh-cpufreq calls
  `mesh-state-touch` on every successful eval, so mtime is a true liveness signal and the TTL check
  can't be fooled by a change-gated write.
- **Parse trap handled.** The state line is `LABEL|…|ratio=NN|…|<reason>` and the free-text reason
  *also* contains `ratio=NN%`. A greedy `sed 's/.*ratio=//'` reads the reason. Parse is field-exact
  (`split on '|'`, take the field that is exactly `ratio=<digits>`), with a decoy fixture asserting it.
- **`MESH_LOAD_GATE_LOG` added** so the `--test` child can be driven end-to-end without writing the
  real shed log — a test that writes the artifact a watchdog reads for liveness forges the evidence
  it exists to check (09f7914). Verified: `--test` leaves `~/.mesh/load-gate.log` at 3668 → 3668 lines.

## Gate, RED-first

18 effectivity cases on top of the existing 12, plus the real-read gate (`--test` now asserts the
live `.cpufreq-state` parses to an integer, else the axis is hollow).

The load-bearing one is **E9, end-to-end**: E1–E8 assert the pure functions and E7 asserts they
compose, but a first pass had all of them green while a mutation that computed the scaled value and
*discarded* it still passed — source text is never behaviour. E9 drives the script itself, same
load, two flag states, and demands the exit code **flip** (`thr = load1 × 1.5` straddles the band).
It isolates the disk axis, scrubs inherited `MESH_LOAD_GATE_EFFECTIVITY` from the child, and prints
its own absence loudly if `load1` is too low to straddle (no silent caps).

Eight mutations, all verified RED, restore green:

| # | mutation | red leg |
|---|---|---|
| M1 | drop the boost cap | `eff-boost-cap` (11 → 14.3) |
| M2 | drop the floor | `eff-floor` (11 → 0.3) |
| M3 | greedy `sed` parse | `eff-parse-field` (got 77, want 42) |
| M4 | fake 100 on unknown | `eff-unknown` |
| M5 | accept a stale artifact | `eff-stale` (got 42, want empty) |
| M6 | compute scaling, discard it | `e2e-eff` (flag never moved THR) |
| M7 | parse `--effectivity`, ignore it | `e2e-eff` |
| M8 | drop the log attribution | `e2e-note` |

## Why this is a genuinely new place for us

Prior 4E landings sat on *sensing* (`mesh-audio-active --confirm`), *significance*
(`mesh-novelty --valence`), *extended memory* (`mesh-handoff` trust/glue) and *coordination repair*
(`mesh-promises --mttr`). This one lands on **action capability** — the effectivity half of the
affordance relation, and the first mesh gate whose boundary is scaled to what the body can do *now*
rather than what it is made of. It also converts an existing, already-cron-wired sense
(`mesh-cpufreq`) from a dashboard reading into something that changes a decision.

**Not enabled anywhere yet** — the axis is opt-in and no cron line was touched. The obvious first
consumers are the grind/render reflexes (`sound-reflex`, `music-session`, `soundscape`), which are
both the heaviest and the most cosmetic; that wiring is the operator's/steward's call, not this
review's.
