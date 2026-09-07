# Correlation investigation: `desk=NEAR-IMAC` ↔ `presence=MANY` — spurious, 2026-09-07

**Disposition:** discard as a causal or operational coupling. No fused sense and no reflex.

## Reproduction

`bash scripts/mesh-correlate --dry` reproduced the queued candidate exactly: corrected lift
**1.83**, 24 episodes, 17 occasions, 1253 usable rows, and the `desk=NEAR-IMAC` 13:00–01:00
clock gate. The uncorrected full-window lift is 1.9 and is correctly labelled confounded.
The stable-blanket check is also decisive: **0 of 5 environments** clear the 1.8 floor
(env18 0.00, env24 0.75, env25 1.00, env28 0.86, env29 1.03).

## Reality check

`NEAR-IMAC` is not direct human presence. `scripts/mesh-desk-state` emits it when the iMac
shows RF disturbance while the phone's motion classifier says `STILL`: “phone set down at
desk.” `MANY` is not a count of people; `scripts/mesh-sensor-tape` buckets the BLE scan's
device count, with `MANY` meaning `n > 8`.

The historical source rows show the overlap is a short local regime, not a stable physical
relationship. In the 13:00–01:00 band, the tape contains 29 real `NEAR-IMAC`/`MANY` rows
(31 `MANY` rows across the complete `NEAR-IMAC` history); the matching BLE snapshots range
from 7 to 14 devices. Those snapshots repeatedly include fixed room appliances (Bose,
Samsung TV, Quest, Bluetooth/DV8235) plus rotating `?` devices and ambiguous/random MACs.
Thus the `MANY` token is sensitive to scan population and attribution churn, while the desk
token is a local iMac/phone inference. Neither token identifies “many people near the desk.”

The same tape also shows the effect is not specific to this label: in the same broad band,
`MANY` occurs in 29/69 `AT-DESK` rows and 66/642 `AT-DESK-TYPING` rows, while the `NEAR-IMAC`
rate is 29/56. The environment breakdown is the stronger holdout: the candidate disappears
in every supplied environment.

The live node cannot add a fresh physical confirmation: `mesh-desk-state --json` reports the
iMac and phone unreachable, and `mesh-presence --json` reports no local Bluetooth adapter.
That is an honest unavailable read, not evidence for or against the historical overlap.

## Decision

Discard in one line: `NEAR-IMAC` is an iMac-RF/phone-still inference and `MANY` is a noisy BLE
device-count bucket; their marginal overlap is environment-specific and does not support an
actionable fused presence sense or reflex.

## Verification

- `bash scripts/mesh-correlate --dry` and `--dry --stable` reproduced the candidate and its
  0/5 stable-blanket result without writing the queue.
- Read-only `awk` census over `~/.mesh/sensor-tape.tsv` counted the matching rows and compared
  real desk/presence cells in the clock band.
- Historical `~/.mesh/presence.log` snapshots were inspected for the matching timestamps and
  device attribution mix.
- Live `mesh-desk-state --json` and `mesh-presence --json` were run; both returned honest
  unavailable states.
- No mesh tool was edited, no deployed copy was edited, no reflex was wired, and no commit was
  made.
