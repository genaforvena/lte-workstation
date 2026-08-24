# Deleuze & Guattari → the FOUR types of deterritorialisation on **twin** axes: what a watchdog that reads one diagonal cannot see

**Area:** Deleuze & Guattari — assemblage, rhizome, the machinic, entered from the concrete METRIC the
area uses to measure itself.
**Arm:** treated (assigned) — the target organ `scripts/mesh-tg-watchdog` was drawn by coin at p=0.20
from the 568 never-reviewed tools in the lane's denominator, not chosen by me or by the lane
(randomized re-entry from the outside, Serrano et al. arXiv:2603.28336 Phase 4, trigger moved from the
state to a coin). No retarget.
**Date:** 2026-08-24 · **Lane:** genome literature live-review · **Reviewer:** genome@mesh-home.
**Organ touched:** `scripts/mesh-tg-watchdog` (uncommitted in the tree — steward lands).

## Where the frontier already was (checked BEFORE reading, not after)

`docs/reviews/` holds **292** reviews, **16** of them D&G. This seam is worked deep: rhizome/plane of
consistency, refrain, order-word redundancy, smooth/striated, machinic phylum, disjunctive synthesis,
faciality, transversality, asignifying rupture, double articulation, relations of exteriority,
rhizome-vs-arborescent callgraph, conjugation-vs-connection, rhythm-is-not-meter, the DeLanda knobs
(both of them: territorialisation → `mesh-digest`, coding/decoding → `mesh-digest` 2026-08-21).

Two prior landings sit directly next to this one and neither is it:

- `deleuze-deterritorialization-coefficient-relative-vs-absolute-recapture-2026-07-28.md` →
  `scripts/mesh-novelty --territory`. It landed the **relative/absolute** cut, and it landed it as a
  **single diagonal**: its own words are "**RELATIVE (negative)**" and "**ABSOLUTE (positive)**".
- `deleuze-guattari-conjugation-vs-connection-queue-floor-miners-2026-08-19.md` → conjugation as a
  *flow-joining* operation, on `mesh-cooscillate`/`-correlate`/`-rhythm`/`-leadlag`.

Vocabulary grep over `docs/ scripts/` before landing:

```
reterritorializ 8 · line of flight 6 · absolute-negative 0 · negative deterritorial 0
positive deterritorial 0 · twin axes 0 · four types 0
```

**The cross is zero.** That is the ground.

## The concept not embodied — the axes are TWIN (independent), not one diagonal

Paul Patton, entry *"deterritorialisation + politics"*, **The Deleuze Dictionary** (Adrian Parr, ed.,
Edinburgh UP), retrieved 2026-08-24:

> "Deleuze and Guattari distinguish **four types of deterritorialisation along the twin axes of
> absolute and relative, positive and negative** (D&G 1987: 508–10)."

- **relative negative** — "the deterritorialised element is **immediately subjected to forms of
  reterritorialisation which enclose or obstruct its line of flight**" (it snaps back).
- **relative positive** — the line of flight prevails over secondary reterritorialisations, though it
  may still fail to connect with anything or enter a new assemblage.
- **absolute negative** — **conjugation**: one deterritorialised flow **overcodes** another, "effecting
  a relative blockage of its movement". The element does not come back AND does not go anywhere.
- **absolute positive** — "when it **connects lines of flight**, raises them to the power of an abstract
  vital line or draws a plane of consistency" (D&G 1987: 510).

The metric shape, stated as engineering: **a departure is classified by a PAIR of independent
questions, not by one.** (1) Did it stay inside the actual order of things (relative) or leave it
(absolute)? (2) Was it recaptured/blocked (negative) or did it prevail (positive)? Magnitude answers
neither. The mesh has axis (1) alone, welded to axis (2) at the diagonal.

**What the weld costs is exactly two cells** — and the one that bites here is **absolute negative**: an
element that is neither recaptured nor reporting. A reader that only has the diagonal must file that
case as "recaptured, therefore fine" or as "prevailing, therefore alert", and — this is the failure
direction — **the cheap default is the first, because absolute-negative is SILENT by construction.**

**Sources** (live, read today):
- Paul Patton, "deterritorialisation + politics", *The Deleuze Dictionary* —
  <https://gilles_deleuze.en-academic.com/45/deterritorialisation___politics> (quotes ATP 1987: 508–10, 56)
- Manuel DeLanda's knobs, for the "assemblage = concept with adjustable parameters" frame that makes
  a 2×2 the right object rather than a scalar: Daniel Little, "DeLanda on concepts, knobs, and phase
  transitions", *Understanding Society*, and *A New Philosophy of Society* —
  <https://understandingsociety.blogspot.com/2016/11/delanda-on-concepts-knobs-and-phase.html> ·
  <https://en.wikipedia.org/wiki/A_New_Philosophy_of_Society>
- Live/current end of the seam (2025), confirming (de)territorialisation is still being handled as a
  *degree* in current publishing rather than a binary: "Territorialisation, Deterritorialisation and
  Power in Democratic Assemblages", **Theoria 72(183), 2025** —
  <https://www.berghahnjournals.com/view/journals/theoria/72/183/th7218302.xml> (abstract via search
  result; the full text 403s from this node — cited for currency of the seam, not for a claim taken
  from inside it)

## The organ, and why the assigned target is the sharpest possible case

`scripts/mesh-tg-watchdog` watches default-string's Telegram organ from a node that can reach Telegram.
Before this change it read **one axis with two values** and fired on **one edge**:

```bash
now=$(timeout 20 ssh … 'mesh-conn --oneline | grep -o "tg=[A-Za-z]*" | head -1')
[ -n "$now" ] || exit 0    # couldn't reach default-string — can't-check ≠ down, don't false-alert
prev=$(cat "$STATEF" 2>/dev/null || echo)
echo "$now" > "$STATEF"
if [ "$now" = "tg=DOWN" ] && [ "$prev" = "tg=up" ]; then mesh-tg "⚠ …"; fi
```

That comment is right about what it refuses and wrong about what it then does. Three consequences, and
they are the three cells the diagonal cannot hold:

1. **Absolute-negative is rendered as nothing.** When the host is unreachable the organ has left the
   observable order entirely — not recaptured, not reporting. `exit 0` writes no state, logs no line,
   alerts never. **Silence is indistinguishable from `tg=up`**, and it is unbounded: default-string can
   be gone for a month and the watchdog stays green. Measured live on this node today, with
   default-string genuinely unreachable (`mesh-peer-addr default-string` → "unreachable — ts
   100.125.157.75 silent"): `--test` printed `smoke-test: ok`, the real run spent **9.0s**, wrote **no
   state file at all**, and exited 0. This is the same hollow-probe shape the 2026-06-12 fix caught one
   layer up (empty HOST); it survived at the next layer down (empty RESULT).
2. **`prev` is a fossil with no age.** The state file held a bare value and nothing else, so an
   up→DOWN edge that straddles a week of blindness was announced as a fresh transition. Recapture and
   non-recapture are told apart by *persistence past the reterritorialising edge* — and the tool had no
   clock at all with which to say how long anything had persisted.
3. **The recaptured cell was never emitted.** DOWN→up produced nothing, so an operator alerted at the
   down edge was never told the departure had been pulled back. The alert stood open forever.

## The change (in the tree, uncommitted)

`scripts/mesh-tg-watchdog` now carries **two axes with their own state, their own `since`, and their own
alerted-marker**, and every cell of the 2×2 has a **named verdict** — including the ones that used to be
silence:

| | recaptured / blocked (negative) | prevailing (positive) |
|---|---|---|
| **relative** (line present, organ reporting) | `still-down` (already alerted) · `reterritorialized` (back up after Ns — discharges the open alert) · `recovered-unalerted` | `departed-fresh` (tg=DOWN, up as recently as Ns ago → alert) · `departed-blind` (edge straddles a blind window → alert, and SAYS the gap) |
| **absolute** (line itself gone — the organ left the observable order) | `line-lost` (under bound, silent but RECORDED) · **`line-lost-absolute`** (past bound → alert: *the tg axis is UNKNOWN, not up*) | `line-returned` (probe line back after Ns) |

Mechanics:

- State is `key=value` lines: `tg`, `tg_observed`, `tg_since`, `tg_alerted`, `reach`, `reach_observed`,
  `reach_since`, `reach_alerted`. **The legacy single-line file `tg=up` parses as the `tg` key with no
  timestamps** — read without a migration step, and honestly: unknown age, so the first edge after it is
  `departed-blind`, never `departed-fresh`.
- `TG_WATCHDOG_UNREACH_ALERT_S` (default 3600) bounds the absolute cell; `TG_WATCHDOG_STALE_S` (default
  1800) is the fossil bound on `prev`. Both are published in the log line, per the mesh's own rule that
  a reading carries its coverage.
- **An unreachable run must never refresh `tg_observed`** — it observed the LINE, not the organ.
  Laundering that timestamp would make `departed-blind` unreachable forever; there is a gate on it.
- The alert for `line-lost-absolute` names itself as **the watchdog's own blindness**, not as a reading
  of the organ. Absence from an unreachable host is UNKNOWN, never DOWN and never up.
- Every run now prints a verdict line, so the reflex has a liveness artifact where it previously had
  a silent `exit 0`.

## Gate — seen RED, then green

The decision is one pure function (`decide`) driven identically by the live path and by `--test`, so
the gate exercises the real classifier, not a copy. `--test` drives **11 cells** plus the
timestamp-laundering assertion plus a state round-trip including the legacy form.

```
MUTANT 1 (unreachable renders as the old silent exit — one axis):
  smoke-test: FAIL (cell 'line-lost' classified as 'held' (silent))                       rc=1
MUTANT 2 (departed edge with no age term — the old fossil-blind behaviour):
  smoke-test: FAIL (cell 'departed-blind' classified as 'departed-fresh'
                    (tg=DOWN — up as recently as 27h ago))                                rc=1
MUTANT 3 (unreachable run laundering the tg timestamp):
  smoke-test: FAIL (unreachable run laundered the tg timestamp (1000000))                 rc=1
RESTORED:
  smoke-test: ok                                                                          rc=0
```

Live path, against the genuinely-unreachable default-string, state file redirected to the scratchpad:

```
run 1                             : line-lost — unreachable 0s (bound 60m)      [state file WRITTEN]
run 2 (UNREACH_ALERT_S=0)         : line-lost-absolute — default-string unreachable for 9s —
                                    the tg axis is UNKNOWN, not up (last known: none, seen unknown ago)
                                    → sent to operator TG
run 3 (already alerted)           : line-lost — unreachable 19s (bound 0s)      [no re-fire]
```

**Side effect owned:** run 2 sent one real Telegram to the operator. The bound was forced to 0 to drive
the previously-silent cell; the message itself is a true statement about a live condition
(default-string IS unreachable from this node right now), but it was minted by a test drive, not by the
default cadence.

## What this does NOT claim

- It does not claim the prior `mesh-novelty` landing was wrong *in its own domain* — a novelty surge may
  well be adequately read on the diagonal. It claims the diagonal is the source's *special case*, that
  the mesh has never held the cross, and that on a **watchdog** the missing absolute-negative cell is the
  failure mode itself.
- `absolute positive` (connection of lines of flight into a new plane) has **no** operational analogue in
  a two-node liveness probe; `line-returned` occupies that cell as a bookkeeping verdict only, and the
  review says so rather than inventing a mechanism to fill a table.
- The tool is deliberately **unwired on this node** (on-demand canon: node-bound, runs where Telegram is
  reachable). Nothing here wires it. `--test` passing and being wired remain unrelated facts.
