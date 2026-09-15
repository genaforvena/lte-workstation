# Cross-sense fusion live recheck — 2026-09-14 18:01Z

The existing executable `scripts/mesh-social-fusion` already derives room occupancy from the
ambient-level × BLE-presence × activity relation and operator state from BLE-presence × activity ×
phone social-context. This recheck made no source change. It confirms an unavailable/stale input
remains visibly `UNKNOWN`, distinct from a live empty BLE census (`count=0`). The on-demand tool is
exempted with an `orphan-ok` header; its change-gated edge path calls `mesh-state-touch "$STATE"` on
successful evaluations.

## Verification

- `scripts/mesh-social-fusion --test` — pass.
- `tests/test-mesh-social-fusion-occupancy.sh` — pass.
- `tests/test-mesh-social-fusion-unreachable.sh` — pass.
- `tests/test-mesh-social-fusion-coupling-audit.sh` — pass.
- Live `scripts/mesh-social-fusion --json`, `2026-09-14T18:01:11Z`, exit 2:

  ```json
  {"verdict":"UNCERTAIN","reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","relation":"UNKNOWN","coverage":"0/3","social_relation":"UNKNOWN","social_coverage":"0/4","occupancy":"UNKNOWN","occupancy_coverage":"0/3","occupancy_reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","operator_state":"UNKNOWN","operator_coverage":"0/3","operator_reason":"unavailable axis: presence=STALE activity=LIVE social=UNREACHABLE","coupling_audit":"NOT-CANDIDATE","local_coverage":"2/3","coupling_recovery_s":"na","ambient":"MODERATE","ambient_status":"LIVE","ambient_age_s":"68","presence":"STALE","presence_observation":"UNKNOWN","devices":"UNKNOWN","presence_age_s":"1333434","activity":"UNCERTAIN","activity_status":"LIVE","activity_age_s":"310","social":"UNKNOWN","social_status":"UNREACHABLE","social_age_s":"na","ts":"2026-09-14T18:01:11Z"}
  ```

- `mesh-doctor --quiet` was attempted first with a 180-second bound and again with a 360-second
  bound. Both ended before a completed doctor summary; the longer run returned exit 124. Its partial
  output included existing warnings (default microphone, untimed peer SSH, sole-path and absence
  findings), but partial output is not a clean pass. No `[sense]` board post was made.
- No new tool file was created and no commit was made.

## Next action

Rerun `mesh-doctor --quiet` to completion. Only after exit 0 and confirmation that the orphan scan
adds no new warning should the active senses mind post `[sense]` with this live `UNKNOWN`/`0/3`
artifact. The current blocker is doctor runtime; do not alter routing or other substrate state from
this senses window.
