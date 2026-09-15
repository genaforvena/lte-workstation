# Cross-sense fusion live verification — 2026-09-11T21:01Z

Existing artifact: `scripts/mesh-social-fusion` (executable, declared `orphan-ok`; no new
tool file or wiring change).

The existing tool derives joint relations from heterogeneous axes:

- ambient sound × BLE presence × activity → room occupancy;
- BLE presence × activity × phone social context → operator state.

A live BLE `count=0` is classified as `EMPTY`; a missing, stale, or malformed presence
artifact is `UNKNOWN`/unavailable and cannot mint an all-clear.

## Verification

- `bash scripts/mesh-social-fusion --test` — PASS.
- `tests/test-mesh-social-fusion-occupancy.sh` — PASS.
- `tests/test-mesh-social-fusion-unreachable.sh` — PASS.
- `tests/test-mesh-social-fusion-coupling-audit.sh` — PASS.
- `mesh-autowire --test` — PASS.
- Source mode: executable.

## Real read

`scripts/mesh-social-fusion --json` at `2026-09-11T21:01:40Z`, exit 2:

```json
{"verdict":"UNCERTAIN","reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","relation":"UNKNOWN","coverage":"0/3","social_relation":"UNKNOWN","social_coverage":"0/4","occupancy":"UNKNOWN","occupancy_coverage":"0/3","occupancy_reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","operator_state":"UNKNOWN","operator_coverage":"0/3","operator_reason":"unavailable axis: presence=STALE activity=LIVE social=LIVE","coupling_audit":"COUPLING-DOMINANT-CANDIDATE","local_coverage":"2/3","ambient":"MODERATE","ambient_status":"LIVE","presence":"STALE","presence_observation":"UNKNOWN","devices":"UNKNOWN","activity":"UNCERTAIN","activity_status":"LIVE","social":"DEGRADED","social_status":"LIVE"}
```

## Doctor gate

`mesh-doctor --test` failed an existing unrelated twice-red fixture
(`got 'na'`). The live doctor sweep also reported existing node-wide findings:
egress via `tailscale0`, configured exit node, and a busy default microphone.
No new orphan warning for `mesh-social-fusion` was observed.

Per the operator contract, no `[sense]` board post was made because the required full
`mesh-doctor` gate is not clean. No commit was made.
