# Cross-sense fusion live verification — 2026-09-10

Existing artifact: `scripts/mesh-social-fusion` (executable, `orphan-ok` header).

Focused gates passed:

- `tests/test-mesh-social-fusion-occupancy.sh`
- `tests/test-mesh-social-fusion-unreachable.sh`
- `tests/test-mesh-social-fusion-coupling-audit.sh`
- `scripts/mesh-social-fusion --test`

Live read at 2026-09-10T13:32:13Z:

```json
{"verdict":"UNCERTAIN","reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","relation":"UNKNOWN","coverage":"0/3","occupancy":"UNKNOWN","occupancy_coverage":"0/3","operator_state":"UNKNOWN","operator_coverage":"0/3","ambient":"LOUD","ambient_status":"LIVE","presence":"STALE","devices":"UNKNOWN","presence_age_s":"971697","activity":"MODERATE","activity_status":"LIVE","social":"DEGRADED","social_status":"LIVE"}
```

The BLE input is visibly stale, not an empty reading; the derived relations therefore remain
`UNKNOWN` with zero overlap and the tool exits 2. A separate live-enough `count=0` fixture derives
`occupancy=EMPTY` in the focused test.

`mesh-doctor` was run, but is not clean on this node: it reports pre-existing egress FAILs for
`tailscale0` and the configured exit node. No `[sense]` board post was made because the operator
contract forbids posting until `mesh-doctor` passes with no new orphan warning.

## Recheck — 2026-09-10T17:17Z

Fresh real read:

```json
{"verdict":"UNCERTAIN","reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","relation":"UNKNOWN","coverage":"0/3","occupancy":"UNKNOWN","occupancy_coverage":"0/3","operator_state":"UNKNOWN","operator_coverage":"0/3","coupling_audit":"COUPLING-DOMINANT-CANDIDATE","local_coverage":"2/3","ambient":"QUIET","ambient_status":"LIVE","presence":"STALE","presence_age_s":"985213","activity":"UNCERTAIN","activity_status":"LIVE","social":"DEGRADED","social_status":"LIVE"}
```

Fresh focused results: all three fusion tests and `scripts/mesh-social-fusion --test` passed;
`mesh-autowire --test` returned 0. `mesh-doctor` was run with a 180-second bound and returned
124 before completing its smoke-test phase. Its completed sections still showed the pre-existing
egress FAILs (`tailscale0` and configured exit node), and existing non-orphan WARNs. No new orphan
warning was observed, but the required clean doctor gate was not met, so no `[sense]` post was made.
