# Lead-lag investigation: `Smart TV Pro` → `ваня тв` (+60min event coincidence)

**Date:** 2026-09-23
**Disposition:** **SPURIOUS / discard.** No fused sense and no reflex.
**Queue rows:** 1963 (`[ ]` RHYTHM/EVENT-COINCIDENCE), 1964 (`[~]` CONNECTION, data-seeded).

## Reproduction

`mesh-leadlag --dry` / `--list` with `LEADLAG_WINDOW_H=48` on the live tape: **no `Smart TV Pro`
finding at all — honest empty.** The queued candidate (trigger rate 0.60 of 5 eligible onsets,
reverse 0.12, net 0.47, surrogate p=0.035, 48h window, 600s bins) does not survive the live tape.

## Reality check (full-tape replication, `presence.log`: 4650 scans 2026-07-15→2026-09-23)

- `Smart TV Pro`: 255 sightings (first 2026-07-21), 41 GAP>1800s appearance onsets.
- `ваня тв`: 135 sightings, 75 onsets.
- **Joint scans: 3** (3/255 = 1.2% of ST sightings) — near-disjoint sighting histories, NOT
  co-visible beacons. Contrast the Samsung→ваня case (113/127 = 89% joint): there the "lead" was
  scanner-phasing of one sweep; here there is not even shared-sweep structure to phase.
- Full-tape ST→VN 30–90min hit rate: **8/41 = 0.20** vs the queued in-window 0.60 of 5.
  The 0.60 lives on **5 eligible onsets** — the minimum-adjacent sample is the whole signature
  (sibling of the coosc nd=9..11 trap: Bluetooth×Smart TV Pro r=+0.88 → out-of-window r=-0.08).
- Both endpoints are **stationary TV beacons**, not arrival processes. Per the coosc review,
  Smart TV Pro is "a persistent fixed broadcaster — present across most scans at a stable level";
  its "appearances" are flicker across the scan detection floor — the Keenetic-8813 / TP-Link_97E0_5G
  shape, not a device arriving. No physical process exists by which one TV's flicker-onset drives
  another TV's appearance 60 min later.
- Median scan interval measured 600.0s — confirms the grid note, and the signal still lives in the
  binning: a 5-onset coincidence at p=0.035 on the global max over pairs×lags is a window-lucky draw,
  rejected by the live tape's own re-test.

## Decision

Discard in one line: **two stationary TV beacons with near-disjoint sighting histories (3/255
joint), a 5-onset in-window coincidence unreplicated on the live tape (dry/list honest-empty), and
no arrival process at either end is scan-floor flicker phasing, not a propagating coupling.**

## Verification

- `LEADLAG_WINDOW_H=48 scripts/mesh-leadlag --dry` + `--list` — rc=0, no Smart TV Pro row.
- presence.log counts above recomputed from the live file, not quoted from the queue row.
- No tool edited (guards — surrogate, reach-control, blackout — all already exist and the live
  re-test did the rejection); receipt left uncommitted for steward landing.
