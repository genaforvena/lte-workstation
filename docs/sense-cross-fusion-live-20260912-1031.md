# Cross-sense fusion live verification — 2026-09-12 10:31 UTC

The existing `scripts/mesh-occupancy-kind` derives whether occupancy is a person, likely person,
appliance-only, empty, or ambiguous by combining device attribution with body motion, recent light
change, and room-sense. No individual input can produce the person/appliance distinction. Its
`PARTIAL-EMPTY` branch preserves the difference between no devices plus an unreachable room axis
and a room confirmed empty. The tool is an existing on-demand executable with an `orphan-ok` header;
no new tool file or source change was needed in this verification.

## Verification

- `scripts/mesh-occupancy-kind --test` — PASS (14 classifier assertions and a real cached read).
- `scripts/mesh-social-fusion --test` — PASS (6 assertions plus joint relation/coverage contract).
- Both tools are existing executable sources with `orphan-ok` headers.
- No commit was made.

## Fresh live reads

At `2026-09-12T10:31:44Z`, `scripts/mesh-occupancy-kind --json` returned:

```json
{"label":"DEGRADED","reason":"presence dark","inputs":{"presence":"OFFLINE"},"ts":"2026-09-12T10:31:44Z"}
```

The device-population input is absent/stale, so the tool declines to infer an occupancy class.
This is a live read of the fusion path, but it does not provide a positive room classification.

At `2026-09-12T10:31:45Z`, `scripts/mesh-social-fusion --json` returned exit 2 with ambient and
activity live, BLE presence stale (`1,133,668` seconds old), and social context live. It published
`occupancy=UNKNOWN`, `occupancy_coverage=0/3`, `operator_state=UNKNOWN`, and
`operator_coverage=0/3`; the absent/stale presence input was not treated as empty.

## Doctor publication gate

`timeout -k 5 180 mesh-doctor --quiet` exited 124 at its 180-second bound. It reported egress via
`tailscale0`, an exit node set, a busy/broken default microphone, two recent `doctor.log` errors, and
other existing warnings before stalling. The run did not complete its orphan census, so a clean
doctor result and the no-new-orphan-WARN gate are unverified. No `[sense]` board line was posted.

Next: resolve the node-level doctor blockers through their existing owners, then rerun
`mesh-doctor --quiet`; only after a clean complete run, post `[sense]` citing this artifact and a
fresh successful or honestly partial live fusion read.
