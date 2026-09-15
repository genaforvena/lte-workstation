# Correlation re-check: `tempo=SILENT` ↔ `ambient=MODERATE` — discard

Date: 2026-09-09  
Disposition: **SPURIOUS; discard.** No fused sense or reflex.

## Result against the live tape

The queued claim (lift 3.8, 8 occasions / 8 episodes of 171, 815.7 h) is the
same late-regime artifact documented in the earlier investigation. The current
aligned tape has 4,941 data rows from 2026-07-14T22:40:01Z through
2026-09-09T22:10:02Z. After the correlation miner's missing/fault-token filter:

| measurement | result |
|---|---:|
| usable rows for both senses | 1,571 |
| `tempo=SILENT` rows | 237 |
| `SILENT` + `MODERATE` overlaps | 113 |
| overlap occasions after the one-hour flap collapse | 18 |
| first `SILENT` tape row | 2026-08-15T23:40:01Z |

The original overlap is therefore not 8 independent events over 815.7 hours;
it is a token that only became reachable late in the tape. Restricting to the
readable era beginning at that first `SILENT` row gives 606 usable rows, with
`MODERATE` in 254 (0.419). Among those, `SILENT` has 113 `MODERATE` rows out
of 237 (0.477): a small, non-actionable difference, not the reported lift.

## Reality / mechanism

`scripts/mesh-activity-tempo:21,40,507,520` defines `SILENT` from dark light
plus no motion (with a fallback using the phone-bound tamper axis). The live
log's first such transition is 2026-08-15T23:38:01Z. In contrast,
`scripts/mesh-ambient-clock:9,14,48` derives the tape's `ambient` token from
BLE appliance advertisements in `presence.log`; it is not microphone loudness.
That feeder is now explicitly marked `orphan-ok: DECAYED` in the source, and
its live `presence.log` mtime is 2026-08-30, so current `ambient` readings also
cannot support a new causal claim.

The apparent relationship is the onset of a new light/tempo sensing regime
overlapping an appliance-clock regime, plus shared availability/night
structure. It does not say that a quiet room causes moderate ambient sound.

**One-line discard:** `tempo=SILENT` only became readable in a late,
light/phone-gated regime, while tape `ambient=MODERATE` is an independent
BLE/appliance-clock label (and its feeder is now stale); the overlap is regime
and availability structure, not a useful causal signal.

## Verification

- `rtk bash scripts/mesh-correlate --test` — PASS.
- `rtk bash scripts/mesh-correlate --dry` — read-only; no current candidate for
  this pair.
- Independent stdlib-only count over `~/.mesh/sensor-tape.tsv` — counts and
  timestamps above; NUL bytes were stripped only in the read-only counter.
- `rtk bash scripts/mesh-ambient-clock --test` — PASS.
- `timeout 25s bash scripts/mesh-activity-tempo --test` — timed out (`rc=124`)
  during its real `mesh-tamper` leg after printing its smoke assertions; no
  source or live artifact was changed by that test.
- No mesh tool was edited, no deployed copy was edited, and no commit was made.

Prior evidence retained in
`docs/correlation-investigation-tempo-silent-ambient-moderate-spurious-2026-09-08.md`.
