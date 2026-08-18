# room_activity=QUIET ↔ desk=AWAY — spurious, and the two defects it exposed in the finder

**Date:** 2026-08-18 · **Channel:** discover@mesh-home · **Verdict on the pairing: SPURIOUS.**
**Verdict on the finder: two real defects, one fixed here, one measured and filed.**

> Filed in `docs/` rather than `knowledge/` on purpose: `knowledge/` is gitignored
> (`.gitignore:22`), so the two earlier confound writeups `mesh-correlate` cites
> (`knowledge/correlation-investigation-desk-attyping-psi-calm-spurious-2026-07-08.md`,
> `…tempo-silent-ambient-moderate-spurious-2026-08-17.md`) do not land with the code and are
> absent from a fresh clone. A citation into an ignored directory is a dangling pointer.

## The claim as it reached the queue

```
CORRELATION (auto, real data): when room_activity reads QUIET, desk tends to read AWAY
(lift 6.0, 8 distinct occasions / 16 episodes of 787, window 832.2h; autocorrelation-collapsed …
and episodes less than 1h apart count as ONE occasion so a flapping sensor cannot manufacture support)
```

Re-issued to the idea queue as a CONNECTION with the gloss *"NOT a random pairing, the DATA flagged it."*

## The pairing is spurious — three stacked confounds

The senses: `room_activity` = `mesh-room-activity` (body-motion, audio, node-local wifi RSSI drift,
BLE, phone light, LAN media). `desk` = `mesh-desk-state` (iMac RSSI, iMac input idle, **phone
body-motion**, phone tamper, iMac cam). Shared input: the phone organ.

Measured on `~/.mesh/sensor-tape.tsv` (2896 rows, 2026-07-14T22:40Z → 2026-08-18T15:00Z):

| window / conditioning | P(AWAY) | P(AWAY\|QUIET) | lift |
|---|---|---|---|
| full window, raw bins | 0.033 | 0.365 | **11.10** |
| full window, episodes — *the published number* | | | **6.0** |
| in-era (desk=AWAY first seen 2026-08-15T17:40Z), episodes — *the deciding number* | | | **1.80** |
| in-era, raw bins | 0.261 | 0.493 | 1.89 |
| in-era, phone answering | 0.382 | 0.600 | 1.57 |
| in-era, excl. `desk=PARTIAL-IMAC` **and** `room_activity=UNCERTAIN` | 0.459 | 0.530 | **1.15** |

1. **Regime shift.** `desk=AWAY` has no history before 2026-08-15T17:40Z — 8.3% of the window.
   All 66 AWAY rows and all 35 co-occurrences lie inside it *by construction*; the full-window
   base rate P(AWAY)=0.033 is an artifact of the token's data starting recently. 6.0 → 1.80.
2. **Shared phone-organ gating.** `desk=PARTIAL-IMAC` is *defined* as "phone OFFLINE + iMac
   reachable" — so `desk=AWAY` is **unreachable while the phone is down**, and
   `room_activity=QUIET` needs the phone's body/light axes too. Measured:
   P(phone answering) = 0.088 given PARTIAL-IMAC, 0.636 given AWAY, 0.435 overall. The largest
   joint cell in-era is `(UNCERTAIN, PARTIAL-IMAC)` = 53 — both senses saying "the phone isn't
   answering" in two vocabularies. 1.80 → 1.57.
3. **Blind-token co-occurrence.** Comparing only rows where *both* senses gave a real room/desk
   reading: **lift 1.15**, i.e. nothing, and below every floor in the tool (MIN_LIFT 1.8).

Same shape the regime-gate writeup already names for `tempo=SILENT ↔ ambient=MODERATE`:
*what co-occurs is the organ answering, not the room being at rest.*

## Defect A — the gate's corrected statistic decides, then is discarded (FIXED)

Both the clock gate and the regime gate re-measure the lift inside the only window where the
finding can be honest, compare **that** to `MIN_LIFT`, and then drop it on the floor. The emit
block printed the full-window `lift`. So a finding that survived a correction was published with
its **pre-correction** magnitude: **6.0 instead of 1.80** — a 3.3x overstatement of a finding that
cleared the 1.8 floor by 0.005.

The idea text makes it worse by being *specific* about the other guards
("autocorrelation-collapsed…, occasion…"): the enumeration reads as a complete provenance list,
so a downstream reader takes 6.0 at face value. It also fed the ranking — `sc=lift*occ` — so a
regime-corrected marginal outbid honest pairs for the one emit slot per run.

**Fix** (`scripts/mesh-correlate`): each gate that re-measures and *passes* records
`(corrected lift, episodes, why)`; the emit publishes the most-corrected number, names the
correction, and discloses the full-window number **marked CONFOUNDED**; the score uses the
corrected lift. Measured on the new fixture: score **100.000 → 24.000**, text
`lift 8.3` → `lift 2.00 … the full-window lift is 8.3 but that number is CONFOUNDED`.

**Gate seen RED then GREEN.** New `--test` leg with a fixture whose corrected lift *survives*
(2.00) — the pass path the two existing drop-legs never exercised. Two independent mutants, each
red for its own reason: reverting the text fix → "does not publish the gate-CORRECTED lift 2.00";
reverting `sc=elift*occ` alone → "candidate SCORED on the confounded lift".

## Defect B — the threshold was crossed by drift, with zero new evidence (FILED, not fixed)

From `~/.mesh/correlate.log`, every logged run of this pair:

| run | global lift | episodes | era cover | **in-era lift** | outcome |
|---|---|---|---|---|---|
| 10:53Z | 5.86 | **16** | 7.9% | **1.66** | DROPPED |
| 12:23Z | 5.92 | **16** | 8.0% | **1.73** | DROPPED |
| 12:53Z | 5.93 | **16** | 8.1% | **1.74** | DROPPED |
| 13:23Z | 5.93 | **16** | 8.1% | **1.75** | DROPPED |
| 13:53Z | 5.95 | **16** | 8.2% | **1.77** | DROPPED |
| 14:23Z | 5.96 | **16** | 8.3% | **1.78** | DROPPED |
| 14:53Z | — | — | — | ≥1.80 | **EMITTED** |

**The episode count is pinned at 16 across all of it.** Not one new co-occurrence was observed
between the first rejection and the acceptance. The era's right edge is *wallclock now*, so the
corrected lift is a function of time even when the sensors observe nothing: as the era grows
without new AWAY episodes the marginals shift and the ratio drifts — here monotonically,
~0.034/hour. Any pair parked near the floor is therefore admitted **eventually, by waiting**, and
once emitted the "recently emitted" suppression means it is never re-adjudicated. The drift is
one-way.

Not fixed here because every candidate remedy needs a constant I cannot yet justify from one
case (a hysteresis margin, a "corrected lift must have moved on new evidence" rule needing per-pair
state). Defect A's fix defuses the *harm*: such a finding now enters the queue labelled
`lift 1.80 … 1.80 vs the 1.8 floor is the whole margin this finding has`, which no reader mistakes
for "lift 6.0, NOT a random pairing".

## Rules

- **A gate that corrects a statistic must publish the corrected one.** The uncorrected number is
  evidence about the confound, not about the coupling — quoting it is quoting the number the tool
  itself disqualified.
- **An enumerated provenance list makes its own omissions invisible.** Naming three guards and
  silently skipping the fourth reads as completeness.
- **A threshold on a wallclock-dependent statistic is crossed by waiting.** Before believing a
  pass, check whether the *evidence* changed — here the support was pinned at 16 for 3.5 hours
  across seven verdicts.
- **Two senses that share a gating organ co-occur on the organ, not on the world.** A token that is
  unreachable while an input is down (`desk=AWAY` vs `PARTIAL-IMAC`) can only ever co-occur with
  other tokens that need the same input.
