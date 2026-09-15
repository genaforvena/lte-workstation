# Cross-sense fusion live verification — 2026-09-11

Extended the existing `scripts/mesh-social-fusion` relation consumer with an explicit
`presence_observation` field. A live BLE census with `count=0` now publishes `EMPTY`; a missing,
stale, or malformed BLE input publishes `UNKNOWN` and cannot enter occupancy as zero. The existing
occupancy relation remains a three-axis overlap of ambient × BLE presence × activity, and operator
state remains presence × activity × social context.

## Verification

- `bash -n scripts/mesh-social-fusion` — PASS.
- `scripts/mesh-social-fusion --test` — PASS.
- `tests/test-mesh-social-fusion-occupancy.sh` — PASS.
- `tests/test-mesh-social-fusion-unreachable.sh` — PASS.
- `tests/test-mesh-social-fusion-coupling-audit.sh` — PASS.
- Source remains executable: `-rwxr-xr-x scripts/mesh-social-fusion`.
- No new tool file was created; the existing `orphan-ok` header and wiring are unchanged.

## Real read

At `2026-09-11T16:46:46Z`, `scripts/mesh-social-fusion --json` returned exit `2`:

```json
{"verdict":"UNCERTAIN","reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","occupancy":"UNKNOWN","occupancy_coverage":"0/3","presence":"STALE","presence_observation":"UNKNOWN","devices":"UNKNOWN","ambient_status":"LIVE","activity_status":"LIVE"}
```

This is a live partial result: the BLE axis is stale, so the fused occupancy is visibly UNKNOWN
with zero overlap rather than a false EMPTY/all-clear. The focused fixture tests also exercise the
opposite, genuine live-empty case (`count=0` → `occupancy=EMPTY`).

## Doctor gate

`mesh-doctor --quiet` was run after the change but did not pass. It reported pre-existing node-wide
findings including egress via `tailscale0`, a configured exit node, a busy default microphone,
untimed peer SSH, sole-path bypasses, and absence-as-negative sites. The invocation was then
stopped while waiting behind long-lived doctor/mic processes. No `[sense]` board post was made,
because the operator contract requires a clean `mesh-doctor` before posting one.

No commit was made.
