# correlation investigation: body_state=REJECTED ↔ presence=SOME — SPURIOUS (support is one incident), 2026-07-27

**Seeded pairing:** `CONNECTION (data-seeded)` — "body_state and presence are empirically coupled
(lift 1.9, 9 distinct episodes of 212, window 304.7h; autocorrelation-collapsed so a persistent run
counts once)". Produced by `mesh-correlate`'s LIFT lane, routed to discover via `mesh-ideate`.

**Verdict: SPURIOUS.** The "9 distinct episodes" are **2 incidents**. Eight of the nine lie inside a
single 10.8h phone-auth event; there is no coupling to explain. But the *reason* the generator
believed there was one is a real, general defect in the support measure, and that is the deliverable.

## What the pairing actually is

`body_state` carries **no body information at all** in this window. Every one of its 1378 real-reading
rows is a fault verdict:

```
body_state:  DEGRADED 1315 · REJECTED 63 · STALE 3      (n=1381 rows, 2026-07-14T22:40Z → 2026-07-27T15:50Z)
```

`REJECTED` is `mesh-body-state`'s "phone UP, key REJECTED/auth-rotated — not offline"; `DEGRADED` is
"phone unreachable". So the seeded question — "what mechanism links the *body_state sense* and the
*presence sense*?" — has a false premise: the axis is a **phone-link fault mode**, not a body state.

Raw per-row association is weak: P(SOME | REJECTED) = 1.000 over 63 rows against a row-level base of
0.856 → **row lift 1.17**. The reported 1.9 comes from the episode collapse, which deflates the base
(episode-level P(SOME) = 0.523, because presence flickers SOME↔FEW↔MANY in short blips that each
weigh the same as a 10-hour SOME stretch). That gap alone is the documented collapse-inflation tell.

## The measurement that settles it

The nine episodes, placed on the wall clock (row-level runs of `REJECTED`):

```
2026-07-24 20:10 → 20:30   3 rows   0.33h   presence=[SOME]
2026-07-24 21:10 → 22:30   9 rows   1.33h   presence=[SOME]
2026-07-24 22:50 → 00:00   8 rows   1.17h   presence=[SOME]
2026-07-25 00:30 → 02:10  11 rows   1.67h   presence=[SOME]
2026-07-25 02:30 → 02:50   3 rows   0.33h   presence=[SOME]
2026-07-25 03:10 → 03:10   1 row    0.00h   presence=[SOME]
2026-07-25 03:50 → 06:10  15 rows   2.33h   presence=[SOME]
2026-07-25 06:30 → 07:00   4 rows   0.50h   presence=[SOME]
2026-07-27 14:20 → 15:30   8 rows   1.17h   presence=[SOME]     ← the only other one
```

Eight episodes are one incident: `body_state` **chattered** REJECTED↔DEGRADED every 20–40 min for
10.8 hours while the phone's SSH key was rotated. The episode collapse breaks a run whenever
**either** axis changes — so a flapping axis manufactures episodes at will. Effective support = **2**.
With two occasions and an episode base rate of 0.52, P(both land in SOME) ≈ 0.27. Nothing to explain.

Two nulls were run before reaching that conclusion, and **both were misleading** — worth recording:

- **Circular-shift permutation** (preserves each series' own autocorrelation, destroys alignment):
  p = 0.001 over all 1379 shifts. It looks decisive and is answering the wrong question — it asks
  whether an 11h block lands on an uninterrupted SOME stretch by chance, which is a fact about
  `presence`'s run structure, not about `body_state`.
- **Day-aligned shift** (shift by whole days, preserving hour-of-day): p = 0.000 over 9 shifts —
  but n=9 cannot resolve p below 0.11, and the diurnal confound is weak here anyway
  (P(SOME) = 0.876 night vs 0.840 day), so the clock-gate correctly does not fire on this pair.

A significance test on autocorrelated data cannot rescue a support count of 2. **The unit of evidence
had to be fixed, not the p-value.**

## The fix (scripts/mesh-correlate, uncommitted — steward lands)

`MIN_SUPPORT`'s documented meaning is "co-occurred on N **separate occasions** — what makes a link
surprising, not one long stretch the tape happened to sample N times". The episode collapse defends
that against **persistence** but not against **flap**. Support is now counted in **occasions**:
consecutive (x,y) episodes whose wall-clock gap is less than `CORRELATE_OCCASION_GAP_H` (default 1h,
0 disables) are ONE occasion. The lift arithmetic is untouched; only the gate changed — and a
candidate dropped by it is announced LOUDLY on stderr, never silently discarded.

Default calibrated against the live tape, **both directions measured**:

| pair | episodes | occasions@1h | outcome |
|---|---|---|---|
| `body_state=REJECTED ↔ presence=SOME` | 10 | **2** | dropped — one flap |
| `light=DARK ↔ ambient=NIGHT-QUIET` | 9 | **9** | kept by this gate (9 genuinely separate nights), then dropped by the CLOCK gate — its own class |

That second row is the control: the new gate distinguishes "9 nights" from "1 chatter" instead of
suppressing everything, and it does not preempt the clock-gate's job. Live run after the fix:

```
occasion-gate: DROPPED body_state=REJECTED <-> presence=SOME (lift 1.86, 10 episodes) — those
  episodes are only 2 separate occasion(s) once co-occurrences less than 1h apart are merged:
  ONE incident with a flapping sensor, not 10 independent co-occurrences
clock-gate:    DROPPED light=DARK <-> ambient=NIGHT-QUIET (lift 2.35, 9 episodes) — ...
no correlation/prediction meets thresholds (need more data — honest empty, not a failure)
```

**RED-first test** (`--test`): a tape **byte-identical to the existing positive control except the
timestamps** — the same 8 alternating BUSTLE↔STALLED episodes, compressed from 1h spacing to 10min so
the whole thing is one 2.5h incident. Pre-fix both tapes emit the identical finding (score 16.000,
lift 2.0) — seen RED. Post-fix the hourly one still fires and the compressed one does not, plus a
**falsifier**: with `CORRELATE_OCCASION_GAP_H=0` the compressed finding must come back, proving the
suppression is this gate and not the tape being short (a gate that passes for the wrong reason
asserts nothing). Also asserts the drop is announced, so a silent mute fails the test.

## Not fixed here — filed instead: fault tokens pass the not-a-reading filter

`NOT_A_READING = {NOLOG, STALE, UNKNOWN, ""}` does not include the **sensor-side fault verdicts** that
several senses actually emit, so they enter the analysis as if they were states. Share of
real-reading rows that are a fault verdict, measured on this tape:

```
body_state  1.000   (DEGRADED 1315 · REJECTED 63)   ← every value; the axis is 100% fault
social      0.967   (DEGRADED 1054)                  ← plus 36 rows whose value is literally "AND"
tempo       0.384   (DEGRADED 410)
perimeter   0.150   (UNREACHABLE 207)
```

A sense that is ≥96% one fault token is a near-constant and pairs cheaply with anything — the
high-base-rate inflation source already documented in this tool, arriving through a door the honest-
fusion filter was supposed to close. Deliberately **not** changed unilaterally: `DEGRADED` could be a
legitimate world-state for some future sense ("the thing I sense is degraded" ≠ "I failed to sense"),
and this tool's precedent is to validate a suppression before shipping it. The `social` column's
literal `AND` value (36 rows) looks like a field-splitting bug in the tape writer and is a separate
defect.

## Dead-end record

Traced as `gen-pair-deadend body_state×presence` so the queue resolves and a future explorer greps it
before re-investigating: the coupling is a fault-mode artifact; the useful residue is the occasion gate.
