# Cross-sense fusion live verification — 2026-09-11

The existing `scripts/mesh-social-fusion` was extended for cross-sense relations. It combines
ambient sound × BLE presence × activity for room occupancy, and BLE presence × activity × phone
social context for operator state. A real empty BLE census (`count=0`) is distinct from a missing or
stale BLE state; unavailable overlap yields `UNKNOWN`, never a silent all-clear.

## Gates

- `scripts/mesh-social-fusion --test` — PASS.
- `tests/test-mesh-social-fusion-occupancy.sh` — PASS.
- `tests/test-mesh-social-fusion-unreachable.sh` — PASS.
- `tests/test-mesh-social-fusion-coupling-audit.sh` — PASS.
- `mesh-autowire --test` — PASS.
- `mesh-doctor --test` — PASS.
- Source is executable: `-rwxr-xr-x scripts/mesh-social-fusion`.
- Existing tool header declares `orphan-ok`; no new tool file was created.

## Real read

At `2026-09-11T09:21:51Z`, `scripts/mesh-social-fusion --json` returned exit `2`:

```json
{"verdict":"UNCERTAIN","reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","relation":"UNKNOWN","coverage":"0/3","social_relation":"UNKNOWN","social_coverage":"0/4","occupancy":"UNKNOWN","occupancy_coverage":"0/3","occupancy_reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","operator_state":"UNKNOWN","operator_coverage":"0/3","operator_reason":"unavailable axis: presence=STALE activity=LIVE social=LIVE","coupling_audit":"COUPLING-DOMINANT-CANDIDATE","local_coverage":"2/3","coupling_recovery_s":"na","ambient":"MODERATE","ambient_status":"LIVE","ambient_age_s":"110","presence":"STALE","devices":"UNKNOWN","presence_age_s":"1043074","activity":"ACTIVE","activity_status":"LIVE","activity_age_s":"349","social":"DEGRADED","social_status":"LIVE","social_age_s":"269"}
```

This is the required visible distinction: the live ambient/activity axes cannot manufacture
occupancy while BLE presence is stale. The underlying presence artifact is
`~/.mesh/.presence-state`, last updated `2026-08-30T07:37:17Z`, and contains historical `count=9`;
it is not treated as a current observation.

## Doctor blocker

A full `mesh-doctor --quiet` run was started and stopped after it remained blocked by existing
long-lived live checks. Its reported node-wide findings were:

- FAIL: egress rides `tailscale0` (overlay/VPN) — should be LAN.
- FAIL: exit-node set — SPOF risk.
- WARN: mic default device broken/busy (the plughw path passed).
- WARN: untimed peer SSH to `mesh-load-audit`.
- WARN: pre-existing sole-path and absence-as-negative findings in unrelated tools.

No new `mesh-social-fusion` orphan warning appeared. Because the full doctor is not clean, the
required `[sense]` board post was intentionally withheld. No commit was made.
