# Note 3 power/display health finding — 2026-09-12

Task: `health-warning/747d421e2b2009967e9a/triage` (owner `health`).

## Historical event

The 2026-09-09 14:16:47Z board finding was a positive discovery: the Note 3
power/display organ had appeared and was healthy. Its source artifact,
`artifacts/discover/note3-power-display-20260909.txt`, records a real ADB USB
capture on serial `4d00553d61ab90b7` at 13:55:01Z. It contains
`mWakefulness=Awake`, `mInteractive=true`, `mDisplayReady=true`, and a parser
acceptance of 1/1. The original board line separately records the 14:16Z live
read as OFF with fresh `Asleep|false|true` fields and `--test PASS`. This event
was healthy and did not claim stale-cache health or scheduled wiring.

## Current visibility

At 2026-09-12 10:37Z, a fresh `adb devices -l` listed no devices. The current
`mesh-note3-power-display --json` returned exit 2:

```json
{"verdict":"UNKNOWN","age_seconds":0,"capture_utc":"2026-09-12T10:37:47Z","reason":"unreachable-or-malformed"}
```

The real-read `mesh-note3-power-display --test` also returned exit 2 with
`n/a (Note3/ADB unreachable or PowerManager fields absent)`. This is not a
healthy current-state reading: the phone's present display state is unknown
because ADB has no attached Note 3. The script itself documents this case as
`UNKNOWN`, and [the organ's design note](../note3-power-display-20260909.md)
confirms it is read-only and on-demand with no cron/reflex consumer.

## Disposition

Close the historical finding as a healthy discovery. Name the present ADB
absence as a known visibility gap; do not carry forward the 2026-09-09 reading
as current health. No phone, ADB transport, substrate, or configuration state
was changed. The live sensor can be re-read when the Note 3 is attached and
visible to ADB.

Verification: original board event, original capture artifact, design/wiring
note, current `adb devices -l`, live JSON read and exit status, and live-read
`--test` exit status were inspected.
