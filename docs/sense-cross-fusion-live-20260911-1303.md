# Cross-sense fusion live verification — 2026-09-11

Existing tool: `scripts/mesh-social-fusion` (executable, declared `orphan-ok`; no new tool
file or wiring was created).

Verification:

- `scripts/mesh-social-fusion --test` — PASS.
- `tests/test-mesh-social-fusion-occupancy.sh` — PASS.
- `tests/test-mesh-social-fusion-unreachable.sh` — PASS.
- `tests/test-mesh-social-fusion-coupling-audit.sh` — PASS.
- Source mode: `-rwxr-xr-x scripts/mesh-social-fusion`.

Live read at `2026-09-11T13:02:38Z` (`scripts/mesh-social-fusion --json`, exit 2):

```json
{"verdict":"UNCERTAIN","reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","relation":"UNKNOWN","coverage":"0/3","social_relation":"UNKNOWN","social_coverage":"0/4","occupancy":"UNKNOWN","occupancy_coverage":"0/3","occupancy_reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","operator_state":"UNKNOWN","operator_coverage":"0/3","operator_reason":"unavailable axis: presence=STALE activity=LIVE social=LIVE","coupling_audit":"COUPLING-DOMINANT-CANDIDATE","local_coverage":"2/3","coupling_recovery_s":"na","ambient":"LOUD","ambient_status":"LIVE","ambient_age_s":"23","presence":"STALE","devices":"UNKNOWN","presence_age_s":"1056321","activity":"UNCERTAIN","activity_status":"LIVE","activity_age_s":"397","social":"DEGRADED","social_status":"LIVE","social_age_s":"16","ts":"2026-09-11T13:02:38Z"}
```

This demonstrates the joint relation does not collapse stale BLE into an empty room or all-clear:
the required three-axis relations remain `UNKNOWN` with zero overlap coverage and a non-zero exit.

`mesh-doctor --quiet` found no orphan warning, but the doctor is not clean: it reports the known
pre-existing `egress rides tailscale0` and `exit-node set` failures, plus the known default-mic
warning. Therefore no `[sense]` board post was made; the contract requires a clean doctor before
that post. The exact next action is to repair or explicitly clear those substrate doctor failures,
then rerun `mesh-doctor --quiet` and post this fusion artifact as `[sense]`.

Uncommitted by request.
