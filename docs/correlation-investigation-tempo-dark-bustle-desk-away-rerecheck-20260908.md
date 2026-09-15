# Correlation investigation rerecheck: `tempo=DARK_BUSTLE` ↔ `desk=AWAY`

**Disposition:** discard as spurious; no fused sense and no reflex.

The queued claim (lift 2.00, 20 episodes, 13 occasions, hour-shadow 0.98,
three-environment unstable) was investigated against the live tape and source
semantics. A fresh `mesh-correlate --dry` / `--stable` run on 2026-09-08 now
reports the same pair as an hour-shadow drop: raw lift 2.96, 20 episodes, the
shadow already scores 1.01 of the crude 1.65, and corrected lift is 1.64,
below the 1.8 floor. The moving tape therefore does not strengthen the claim;
it removes its already narrow corrected margin.

## Reality check

The current aligned tape has 4,801 rows, 207 `DARK_BUSTLE` rows, and only 30
joint `DARK_BUSTLE` + `AWAY` rows. Those 30 rows collapse to the same 13
one-hour occasions described by the finding. The joint rows are concentrated
in eight dates, and 28/30 have `wifi=UNKNOWN`; their corroborating body-motion
values are 13 `UNKNOWN`, 7 `COVERED`, 6 `OFFLINE`, and only 4 `STILL`.
Presence is also not independent confirmation: 9/30 are `STALE`, with the
remainder split across `SOME` (14), `MANY` (4), and `NONE` (3).

The two producers describe different things. `mesh-activity-tempo` defines
`DARK_BUSTLE` as sustained/camera activity while the room is dark; the live
provenance lines repeatedly say `wifi=MOTION`, `light=DARK`, `cam=UNKNOWN` or
camera motion, often with phone axes unavailable. `mesh-desk-state` defines
`AWAY` from `iMac=UNREACHABLE` and explains it as iMac off/asleep. Thus the
joint rows are compatible with a night/availability regime and partial sensor
failure, not evidence that room activity causes the operator to leave the
desk. The three-environment result is explicitly `UNSTABLE`, so it cannot be
generalized even if the local overlap were useful.

The live one-shot probes were also bounded honestly: both
`mesh-activity-tempo --json` and `mesh-desk-state --json` hit the 15-second
observation timeout (rc 124). This is an availability limitation, not a
positive reading and not evidence for a reflex.

**One-line discard:** `DARK_BUSTLE` is weak, frequently phone/camera-partial
night-room activity while `AWAY` is an iMac reachability verdict; their narrow,
environment-specific overlap is shared night/outage structure, not a causal
operator signal.

## Verification

- `rtk bash scripts/mesh-correlate --dry` — rc 0; current hour-shadow drop at
  corrected lift 1.64.
- `rtk bash scripts/mesh-correlate --stable` — rc 0; current stable report
  retains the prior 0/3 environment floor failure for this pair.
- Read-only census of `~/.mesh/sensor-tape.tsv` — 4,801 rows / 207
  `DARK_BUSTLE` / 30 joint rows; counts above.
- Read-only inspection of `~/.mesh/activity-tempo.log` and source definitions
  in `scripts/mesh-activity-tempo` and `scripts/mesh-desk-state` — provenance
  and meaning above.
- Bounded live probes — both timed out at 15 seconds, recorded as unavailable.
- No genome source, deployed tool, queue seed, or reflex was edited; no commit
  was made.
