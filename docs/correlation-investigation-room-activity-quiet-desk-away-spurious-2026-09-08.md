# room_activity=QUIET ↔ desk=AWAY — still spurious, no fused sense

**Date:** 2026-09-08  
**Artifact:** current `~/.mesh/sensor-tape.tsv` audit plus configured `mesh-correlate --dry`  
**Verdict:** discard; do not build a fused sense or reflex from this pairing.

## Claim checked

The queued claim was: `room_activity=QUIET` tends to coincide with `desk=AWAY`,
lift 6.0, 8 occasions / 16 episodes. The old 2026-08-18 investigation already
identified this shape as spurious; this artifact re-checks the live tape instead of
assuming that conclusion persisted.

## Current live evidence

The tape spans `2026-07-14T22:40:01Z` through `2026-09-08T18:20:02Z` (1339.7 h).
After excluding non-readings from both axes, there are 2885 aligned rows:

| audit | count |
|---|---:|
| `room_activity=QUIET` | 155 |
| `desk=AWAY` | 253 |
| joint `QUIET ∧ AWAY` | 64 |
| raw-bin lift | 4.71 |
| joint episodes, with <1 h merged | 27 |

The raw number is not evidence of a stable world relation. The configured
`mesh-correlate --dry` re-measures the candidate and reports:

```
lift 2.32 (37 episodes), hour-stratified shadow baseline 1.52;
full-window lift 2.8 is CONFOUNDED; 26 distinct occasions / 37 episodes;
invariance=UNSTABLE (clears the 1.8 floor in 2 of 4 environments)
```

The environment-specific lifts are `1.50`, `2.04`, `1.22`, and `4.56`.
That is not a stable coupling: the apparent support is carried by particular
recording environments, not reproduced across the tape.

The independent row audit also shows strong clock structure. Joint rows occur
mostly at hours 21–02 and 20/23; there are no joint rows at 06–07 or 16–18.
The pair therefore tracks the schedule/night regime in which an iMac is more
likely to be asleep, rather than a causal transition from quiet room activity to
absence from the desk.

## Reality / causal check

`desk=AWAY` is emitted when the iMac is unreachable/off/asleep; it is not a direct
person-presence observation. `room_activity` is a fusion of audio, node-local WiFi
motion, BLE/presence, and phone light/body axes. Thus the pairing mixes an iMac
power/availability state with a multi-sensor quiet classifier, under a shared
availability regime.

In the 64 joint rows, `body_motion=OFFLINE` appears 39 times and `UNKNOWN` 19
times. The two axes consequently often say “the phone/inputs are unavailable” in
different vocabularies. That is a measurement-path confound, not evidence that a
quiet room causes the operator to be away.

## Decision

**SPURIOUS / discard:** `AWAY` is an iMac reachability/night-regime token, while
`QUIET` partly loses or degrades the same phone-dependent inputs; the corrected
relation is unstable across environments, so no fused sense or reflex is justified.

## Verification

The following real source checks passed after the audit:

```
scripts/mesh-correlate --test
scripts/mesh-room-activity --test
scripts/mesh-desk-state --test
```

No genome tool was edited and no commit was made.
