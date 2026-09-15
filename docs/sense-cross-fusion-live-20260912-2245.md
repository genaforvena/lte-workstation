# Cross-sense fusion verification — 2026-09-12 22:45 UTC

The existing executable `scripts/mesh-social-fusion` combines ambient sound × BLE presence ×
activity into joint room occupancy, and BLE presence × activity × phone social context into operator
state. Both are relational verdicts with overlap coverage; a single input cannot mint the result.
Missing or stale axes remain visibly unavailable and cannot become an all-clear.

## Verification

- `rtk scripts/mesh-social-fusion --test` — PASS.
- `rtk bash tests/test-mesh-social-fusion-occupancy.sh` — PASS.
- `rtk bash tests/test-mesh-social-fusion-unreachable.sh` — PASS.
- `rtk bash tests/test-mesh-social-fusion-coupling-audit.sh` — PASS.
- `rtk scripts/mesh-presence --test` — exit 2, structural n/a: this node has no Bluetooth adapter.
- Source is already executable and declares `orphan-ok`; no new tool file or source change was needed.

At `2026-09-12T22:45:54Z`, the live `rtk scripts/mesh-social-fusion --json` read exited 2 and
reported ambient `QUIET/LIVE` (52 s), activity `MODERATE/LIVE` (593 s), and social context
`DEGRADED/LIVE` (211 s). BLE presence was `STALE` (1,177,717 s old), so the fused result was
`verdict=UNCERTAIN`, `occupancy=UNKNOWN`, `occupancy_coverage=0/3`, and
`operator_state=UNKNOWN`, `operator_coverage=0/3`. This is a live fusion read with an honest partial
result; the node cannot produce a new BLE read because its adapter is absent.

## Doctor gate and publication

`rtk proxy timeout -k 5 180 mesh-doctor --quiet` exited 124 after 180 seconds. It reported existing
FAILs for egress via `tailscale0` and a selected exit node, plus WARNs for the default microphone,
untimed SSH to `mesh-load-audit`, six declared sole-path bypasses, and five absence-as-negative
sites. No `mesh-social-fusion` orphan warning appeared in the output, but the doctor did not finish
its census, so a clean complete result and the no-new-orphan-WARN gate are unverified. No `[sense]`
post was made. No commit was made.

Next action: resolve the existing doctor blockers through their owners, run one complete
`mesh-doctor --quiet`, then post `[sense]` with this artifact and a fresh fusion read only if the
doctor exits cleanly.

## Follow-up live read — 2026-09-12 23:00 UTC

`rtk scripts/mesh-social-fusion --json` exited 2 at `2026-09-12T23:00:01Z`. Ambient was
`MODERATE/LIVE` (90 s), activity `UNCERTAIN/LIVE` (240 s), and social context `DEGRADED/LIVE`
(158 s), while BLE presence remained `STALE` (1,178,564 s). The fused relation stayed
`UNCERTAIN` / `UNKNOWN`, with occupancy coverage `0/3` and operator coverage `0/3`; local
coverage was `2/3`. The live coupling audit reported `COUPLING-DOMINANT-CANDIDATE`, but its
recovery interval remained `na`, so this single read does not establish joint information.
The earlier incomplete doctor run still does not satisfy the publication gate; no `[sense]`
post was made.
