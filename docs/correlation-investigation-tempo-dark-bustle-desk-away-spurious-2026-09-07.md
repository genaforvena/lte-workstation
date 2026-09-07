# Correlation investigation: `tempo=DARK_BUSTLE` ↔ `desk=AWAY`

**Disposition:** spurious as a causal/useful fused sense; discard. No fused sense or
reflex.

## Reproduction

`bash scripts/mesh-correlate --dry` and `--stable` reproduce the queued candidate:
lift **2.00**, 20 episodes, 13 one-hour-collapsed occasions, 666 aligned rows,
1298.8 h; the hour-matched shadow is **0.98** and the unstratified lift is 3.0.
The stable-blanket result is `UNSTABLE`: none of three qualifying environments
clears 1.8 (env18 1.47, env20 1.52, env29 1.49). The seed was withheld as
required for an environment-specific relation.

## Reality check

The raw aligned tape contains 174 `DARK_BUSTLE` rows, but only 30 are also
`desk=AWAY`; those 30 rows form the same 13 occasions reported by the analyzer.
The `AWAY` evidence is independently explicit in the desk log: `iMac=UNREACHABLE`
and usually `input=UNREACHABLE`, with the desk tool describing this as “iMac off or
asleep.” It is not inferred from tempo.

The supposed joint occasions are not corroborated by a healthy motion stream:
most have `wifi=UNKNOWN`, and many have `body_motion=UNKNOWN` or `body_state=DEGRADED`.
The activity-tempo transition log, in contrast, explains `DARK_BUSTLE` as sustained
WiFi/camera motion in darkness, often with `tamper=UNKNOWN` and `cam=UNKNOWN`.
That is room motion during an iMac-off/asleep interval, not evidence that room
motion causes the operator to leave the desk. `presence` is also mixed (`NONE`,
`SOME`, `MANY`, and `STALE`), so it cannot repair operator attribution.

The live `mesh-activity-tempo --json` and `mesh-desk-state --json` probes both hit
the 12-second observation bound on this node; this is recorded as unavailable live
verification, not treated as a positive reading. The retrospective logs and tape
remain real artifacts for the finding itself.

## Decision

Discard: `DARK_BUSTLE` is weak/partly unavailable room-motion evidence while
`AWAY` is an iMac reachability verdict; their environment-specific overlap is a
shared outage/night regime, not a causal coupling worth acting on.

## Verification

- `rtk bash scripts/mesh-correlate --dry` — exact candidate reproduced, rc 0.
- `rtk bash scripts/mesh-correlate --stable` — exact three-environment unstable
  breakdown reproduced, rc 0.
- Read-only Python census over `~/.mesh/sensor-tape.tsv` — 4532 rows, 174
  `DARK_BUSTLE`, 30 joint rows, 13 one-hour-collapsed joint occasions.
- Read-only inspection of `~/.mesh/activity-tempo.log` and
  `~/.mesh/desk-state.log` — independent transition/provenance evidence above.

No genome source or deployed tool was edited, no reflex was wired, and no commit
was made.
