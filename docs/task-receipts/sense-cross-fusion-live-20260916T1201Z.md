# Cross-sense fusion live receipt — 2026-09-16T12:01Z

## Result

Used the existing executable `scripts/mesh-social-fusion`, which fuses five existing axes:
ambient level, BLE presence, activity, phone social context, and audio path. Its derived relations
are occupancy, operator/social state, and media context; they require live overlap and are not a
worst-of fold. A measured BLE `count=0` is `presence_observation=EMPTY`; absent/stale/malformed
BLE is `UNREACHABLE`/`STALE`/`HOLLOW`, with the derived relation `UNKNOWN` and zero coverage.

## Verification

- `scripts/mesh-social-fusion --test` — PASS, rc 0.
- `tests/test-mesh-social-fusion-occupancy.sh` — PASS, rc 0.
- `tests/test-mesh-social-fusion-unreachable.sh` — PASS, rc 0.
- `tests/test-mesh-social-fusion-media.sh` — PASS, rc 0.
- `tests/test-mesh-social-fusion-coupling-audit.sh` — PASS, rc 0.
- `mesh-autowire --test` — PASS, rc 0.
- Source is executable (`755`) and already carries `# orphan-ok:`; no new tool file was created.
- No commit was made.

## Fresh real read

At `2026-09-16T12:01:40Z`, `scripts/mesh-social-fusion --json` returned rc 0:

```json
{"verdict":"SOCIAL_PASSIVE","relation":"NO_JOINT_PATTERN","coverage":"3/3","occupancy":"UNRESOLVED","occupancy_coverage":"3/3","operator_state":"UNRESOLVED","operator_coverage":"3/3","media_relation":"MEDIA_IDLE","media_coverage":"3/3","ambient":"QUIET","ambient_status":"LIVE","presence":"LIVE","presence_observation":"PRESENT","devices":"10","activity":"AMBIENT","activity_status":"LIVE","social":"DEGRADED","social_status":"LIVE","audio_path":"IDLE","audio_status":"LIVE"}
```

This is a genuine live partial semantic result: all five inputs were live, but the current tuple
does not meet the occupied/operator-active thresholds, so it reports `UNRESOLVED` rather than
inventing `EMPTY` or active operator state.

## Doctor gate

`mesh-doctor --quiet` was retried after the lock-holder exited. The completed scan was not clean:

```text
WARN mic DEFAULT device broken/busy (use -D plughw:N,M)
FAIL dispatch.log: 2 recent error-lines (UP but broken?)
```

The scan also retains unrelated node-wide failed-unit/topology findings in
`~/.mesh/doctor.log`. No fusion orphan warning was present in the captured run. Per the operator
request, the `[sense]` post is intentionally withheld until a complete doctor run is clean with
no new orphan WARN.

## Next action

Resolve or clear the node-wide doctor findings, then rerun `mesh-doctor`, the focused fusion tests,
and the real JSON read; post this artifact as `[sense]` only after the doctor gate passes.
