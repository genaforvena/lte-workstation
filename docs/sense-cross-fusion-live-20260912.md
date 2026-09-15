# Cross-sense fusion live check — 2026-09-12

## Existing artifact and live read

The on-demand fusion tool is `scripts/mesh-social-fusion` (already executable and declared
`orphan-ok`). It derives occupancy from ambient sound × BLE presence × room activity, and operator
state from BLE presence × room activity × phone social context. Its output preserves each axis
status and reports joint coverage, so missing/stale axes do not become an empty room or all-clear.
No new tool or source change was needed for this request.

At `2026-09-12T18:45:33Z`, `mesh-social-fusion --json` performed a live read and returned exit 2:

```json
{"verdict":"UNCERTAIN","reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","relation":"UNKNOWN","coverage":"0/3","social_relation":"UNKNOWN","social_coverage":"0/4","occupancy":"UNKNOWN","occupancy_coverage":"0/3","occupancy_reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","operator_state":"UNKNOWN","operator_coverage":"0/3","operator_reason":"unavailable axis: presence=STALE activity=LIVE social=LIVE","coupling_audit":"COUPLING-DOMINANT-CANDIDATE","local_coverage":"2/3","coupling_recovery_s":"na","ambient":"MODERATE","ambient_status":"LIVE","ambient_age_s":"30","presence":"STALE","presence_observation":"UNKNOWN","devices":"UNKNOWN","presence_age_s":"1163296","activity":"UNCERTAIN","activity_status":"LIVE","activity_age_s":"572","social":"DEGRADED","social_status":"LIVE","social_age_s":"190","ts":"2026-09-12T18:45:33Z"}
```

The current observation is partial: ambient, activity, and social-context artifacts are live; BLE
presence is stale. The fused occupancy and operator-state outputs remain `UNKNOWN` with zero
overlap coverage instead of interpreting stale presence as zero devices.

## Verification

- `mesh-social-fusion --test` — PASS.
- `tests/test-mesh-social-fusion-occupancy.sh` — PASS.
- `tests/test-mesh-social-fusion-unreachable.sh` — PASS.
- `tests/test-mesh-social-fusion-coupling-audit.sh` — PASS.
- `mesh-autowire --test` — PASS.
- `mesh-doctor --quiet` — did not complete within its 180-second bound (exit 124). Partial findings:
  egress routed through `tailscale0` and an exit node is set (both FAIL); default mic is broken/busy,
  peer SSH to `mesh-load-audit` is untimed, plus unrelated sole-path and absence-as-negative WARNs.
- `mesh-doctor --test` — did not complete within its 45-second bound (exit 124).

The required clean full-doctor result is unverified and the partial scan is not clean. No `[sense]`
board post was made. The existing mesh fusion implementation and focused checks are ready; first
resolve or re-observe the node-wide doctor blockers under their respective owners, then rerun the
full doctor and post this artifact only after a clean pass with no new orphan WARN.

No commit was made.
