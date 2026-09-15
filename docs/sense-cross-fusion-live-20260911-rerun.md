# Cross-sense fusion live verification — 2026-09-11

Existing artifact: `scripts/mesh-social-fusion` (executable, declared `orphan-ok`; no new tool
file created). It derives relations from heterogeneous axes: ambient level × BLE presence ×
activity for occupancy, and presence × activity × social context for operator state. A live
`count=0` is an empty observation; a missing or stale presence state is visibly unavailable and
cannot produce an all-clear.

## Verification

- `rtk bash scripts/mesh-social-fusion --test` — PASS.
- `tests/test-mesh-social-fusion-occupancy.sh` — PASS.
- `tests/test-mesh-social-fusion-unreachable.sh` — PASS.
- `tests/test-mesh-social-fusion-coupling-audit.sh` — PASS.
- `rtk mesh-autowire --test` — PASS.
- `rtk mesh-doctor --test` — PASS.
- Source is executable: `-rwxr-xr-x scripts/mesh-social-fusion`.

## Real read

`rtk scripts/mesh-social-fusion --json` at `2026-09-11T05:35:35Z` returned exit `2`:

```json
{"verdict":"UNCERTAIN","reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","relation":"UNKNOWN","coverage":"0/3","occupancy":"UNKNOWN","occupancy_coverage":"0/3","presence_status":"STALE","devices":"UNKNOWN","ambient_status":"LIVE","activity_status":"LIVE"}
```

This is the required honest partial result: stale BLE presence is not converted to `count=0`,
and the three-axis occupancy relation has zero overlap rather than an `EMPTY` verdict.

## Doctor gate

A full `rtk mesh-doctor --quiet` was attempted after clearing a stale 86-minute `arecord` child
that held the shared doctor lock. The run reached the real checks but reported the pre-existing
node failures `egress rides tailscale0` and `exit-node set`; it did not complete a clean doctor
pass. No new `mesh-social-fusion` orphan warning was observed. Per the operator contract, no
`[sense]` board post was made while the full doctor gate is not clean.

No commit was made.
