# Cross-sense fusion verification — 2026-09-10

Tool: `scripts/mesh-social-fusion` (existing executable, on-demand `orphan-ok`; no new tool file
or wiring change made).

Focused checks passed:

- `tests/test-mesh-social-fusion-occupancy.sh`
- `tests/test-mesh-social-fusion-unreachable.sh`
- `tests/test-mesh-social-fusion-coupling-audit.sh`
- `scripts/mesh-social-fusion --test`

Live read at 2026-09-10T09:47:16Z:

```json
{"verdict":"UNCERTAIN","reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","relation":"UNKNOWN","coverage":"0/3","occupancy":"UNKNOWN","occupancy_coverage":"0/3","operator_state":"UNKNOWN","operator_coverage":"0/3","ambient":"MODERATE","ambient_status":"LIVE","presence_status":"STALE","presence_age_s":"958199","activity":"MODERATE","activity_status":"LIVE","social":"DEGRADED","social_status":"LIVE"}
```

This is the honest fused result: the BLE presence input is stale, so the joint occupancy and
operator-state relations remain UNKNOWN rather than becoming an empty/all-clear result. A live
`count=0` fixture independently derives `occupancy=EMPTY`.

Hygiene blocker: `mesh-doctor` is not clean on this node. The full sweep reports pre-existing egress
FAILs (`tailscale0` egress and configured exit-node), and `mesh-doctor --test` fails an unrelated
`--sediment` fixture. Therefore no `[sense]` board post was made, per the operator contract.
