# Machine senses experiment receipt — 2026-09-16

Task: `operator-machine-senses-experiment-20260916/design-and-run-machine-senses-experiment`
Owner: `senses`
Run: `2026-09-16T07:20:11Z` UTC

## Hypothesis

A joint observation across heterogeneous axes carries more useful state than either
axis alone: room presence plus Bluetooth inventory should distinguish occupied/familiar
from an empty or transient room, while light provides an independent environmental axis.

## Procedure and inputs

Commands were run locally with bounded timeouts where noted:

```text
mesh-presence --status
mesh-room-sense --status
mesh-light --status
timeout 15s mesh-sense-reception --json
timeout 15s mesh-operator-state --status
```

## Observations

- `mesh-presence --status` returned `8 device(s) in range`; strongest RSSI was `-62 dBm`;
  personal presence was `ACTIVE_NEAR`; occupancy was `PRESENT`; the scan was a 6-second-old
  coalesced result, not a new radio scan.
- `mesh-room-sense --status` returned `PRESENT`, last update 162 seconds old, dwell 5700 s,
  21 changes in 24 h.
- `mesh-light --status` returned `DIM`, webcam source, localized scene, spread luma 229,
  frame age 0 s.
- `mesh-sense-reception --json` timed out at 15 s (`rc=124`); no reception JSON is claimed.
- `mesh-operator-state --status` timed out at 15 s (`rc=124`); no operator-state value is claimed.

## Result

The joint pattern is consistent with `PRESENT + ACTIVE_NEAR + DIM`, but this is an
observation, not a causal proof: presence was coalesced/cached for 6 s and room state
was 162 s old. The timed-out reception and operator-state axes reduce coverage, so the
experiment does not establish a full “understands” capability.

## Acceptance checks and limits

The receipt records commands, timestamps, positive outputs, timeouts, and separates
observations from interpretation. No actuator was used. A repeat with `mesh-presence
--fresh` and a live reception/understanding producer is required before treating the
joint relation as stable or causal.
