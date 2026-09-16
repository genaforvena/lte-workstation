# Cross-sense fusion live receipt — 2026-09-16

## Result

The existing executable `scripts/mesh-social-fusion` is the cross-sense implementation. It
derives occupancy from ambient sound × BLE presence × activity, operator state from BLE × activity
× phone social context, and media state from BLE × activity × audio path. These are joint relations,
not a max/worst-of selector; each publishes overlap coverage.

Its input contract visibly distinguishes a measured empty census (`count=0`, `presence_observation=EMPTY`)
from absent, stale, or malformed input (`presence_status=UNREACHABLE|STALE|HOLLOW`). Missing axes
produce `UNKNOWN` relations and zero overlap rather than an all-clear.

## Verification

- `bash -n scripts/mesh-social-fusion` — PASS, rc 0.
- `scripts/mesh-social-fusion --test` — PASS, rc 0.
- `tests/test-mesh-social-fusion-occupancy.sh` — PASS, rc 0.
- `tests/test-mesh-social-fusion-unreachable.sh` — PASS, rc 0.
- `tests/test-mesh-social-fusion-media.sh` — PASS, rc 0.
- `tests/test-mesh-social-fusion-coupling-audit.sh` — PASS, rc 0.
- `mesh-autowire --test` — PASS, rc 0.
- Source mode is `755`; existing header declares `# orphan-ok:`. No new tool file was created.
- No commit was made.

## Fresh real read

At `2026-09-16T07:50:56Z`, `scripts/mesh-social-fusion --json` returned rc 0:

```json
{"verdict":"SOCIAL_ACTIVE","relation":"NO_JOINT_PATTERN","coverage":"3/3","occupancy":"UNRESOLVED","occupancy_coverage":"3/3","operator_state":"UNRESOLVED","operator_coverage":"3/3","media_relation":"MEDIA_IDLE","media_coverage":"3/3","ambient":"MODERATE","ambient_status":"LIVE","presence":"LIVE","presence_observation":"PRESENT","devices":"7","activity":"AMBIENT","activity_status":"LIVE","social":"DEGRADED","social_status":"LIVE","audio_path":"IDLE","audio_status":"LIVE"}
```

This is a live partial semantic result, not a fabricated occupied/empty state: the three core
axes are live, but activity does not meet the occupied relation's active threshold; the degraded
social context remains visible; media is measured idle across the live 3-axis overlap.

## Doctor gate disposition

The required clean `mesh-doctor` gate was not achieved, so no `[sense]` board post was made.
A bounded `mesh-doctor --quiet` run emitted:

```text
2026-09-16T07:48:17Z WARN mic DEFAULT device broken/busy (use -D plughw:N,M)
2026-09-16T07:48:17Z FAIL dispatch.log: 1 recent error-lines (UP but broken?)
```

The scan did not complete within its bound, and the later `mesh-doctor --test` also did not
complete within its bound (it reached the long `--sediment` smoke output). These are node-wide
pre-existing doctor findings, not a fusion orphan warning; the artifact remains intentionally
unpublished until a complete doctor run returns clean with no new orphan WARN.

## Next action

After the doctor lock is released and the node-wide mic/dispatch findings are resolved or cleared,
rerun `mesh-doctor`, then rerun the focused fusion tests and the real JSON read; post `[sense]` only
if that doctor result is clean.
