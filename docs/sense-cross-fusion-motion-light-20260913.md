# Motion/light cross-sense extension — 2026-09-13

Extended the existing `scripts/mesh-occupancy-kind` readout with a joint relation for its cached
body-motion and light-change inputs. It now reports `MOTION_AND_LIGHT`, `SINGLE_AXIS`,
`NO_ACTIVITY`, `PARTIAL`, or `UNKNOWN`, alongside overlap coverage (`2/2`, `1/2`, or `0/2`). The
occupancy label is unchanged. A fresh webcam light level without a light-change interval is
`UNKNOWN`; an offline motion/light input remains `OFFLINE`. Thus missing evidence cannot produce a
joint empty/no-activity relation.

The source is an existing executable with an `orphan-ok` header; no tool file or scheduler wiring was
added. The tool is a cached, read-only fold, so it writes no state and needs no liveness touch.

## Verification

- `bash -n scripts/mesh-occupancy-kind` — PASS.
- `scripts/mesh-occupancy-kind --test` — PASS, 25 assertions plus its real cached read.
- `tests/test-mesh-social-fusion-occupancy.sh` — PASS.
- Live `scripts/mesh-occupancy-kind --json`, `2026-09-13T02:52:12Z`, exit 2:

  ```json
  {"label":"DEGRADED","reason":"presence dark","activity_relation":"UNKNOWN","activity_coverage":"0/2","inputs":{"presence":"OFFLINE","motion":"OFFLINE","light":"UNKNOWN","room":"OFFLINE"},"ts":"2026-09-13T02:52:12Z"}
  ```

  This host had no live presence or motion input; the webcam supplied a fresh light level but no
  recent-change interval. The read therefore reports no joint activity relation and no occupancy
  verdict, rather than claiming an empty room.
- `mesh-doctor --test` — FAIL in the pre-existing sediment-parser assertion: `--sediment` expected
  the name-construction caveat to fire once `${!var}` is present.
- Full `mesh-doctor` — did not complete. It reported existing egress/exit-node failures, a busy
  default microphone warning, untimed peer SSH, funnel-bypass, and absence-as-negative warnings;
  after reaching node-aware smoke tests it made no further progress for 180 seconds and was
  interrupted. The orphan census was not reached, so a clean doctor result and no-new-orphan-WARN
  check remain unverified. No `[sense]` line was posted.

Next: rerun the full `mesh-doctor` after its smoke-test stall is resolved; post `[sense]` only after
it completes successfully with no new orphan warning.

## Recheck — 2026-09-13 14:00Z

The fused live read remains honestly partial on this node:

- `mesh-ambient-level --json`, `2026-09-13T14:03:24Z`, exit 0: `MODERATE`, `rms_db=-24.3`,
  source `overhear-tap@plughw:CARD=Camera,DEV=0`, coverage `0.986`, age 0s.
- `mesh-presence --has-radio` returned `no`; `mesh-presence --test` exited 2 and reported that
  `/sys/class/bluetooth` has no adapter.
- `mesh-social-fusion --json`, `2026-09-13T14:04:02Z`, exit 2: `occupancy=UNKNOWN`,
  `occupancy_coverage=0/3`, presence `STALE` (age 1,232,805s), ambient and activity `LIVE`.
  A stale presence cache is not accepted as a live empty census.
- `mesh-occupancy-kind --json`, `2026-09-13T14:05:10Z`, exit 2: `DEGRADED`, `presence dark`.
  Its `--test` passed (14 assertions plus a real cached read), the social-fusion occupancy and
  unreachable regression tests passed, and `mesh-social-fusion --test` passed.

The required full `mesh-doctor` was started, but remained in its node-aware smoke-test stage for
11m46s with no progress; at interruption the process was blocked in `pipe_read`, and its last child
had been `mesh-udev-stream --test`. The partial output included `all applicable --test smoke checks
pass`, but also the existing egress/exit-node FAILs and several unrelated WARNs. It reached the
orphan-check heading without printing its census and was interrupted (exit 143), so this is not a
doctor PASS and the no-new-orphan-WARN condition is unverified. No `[sense]` line was posted. No
tool file or scheduler wiring was created in this turn; the existing `mesh-occupancy-kind` source
already carries its `orphan-ok` header and is executable.

Next: resolve the `mesh-doctor` smoke-stage stall and the node's existing doctor failures, rerun the
full doctor through the completed orphan census, then post `[sense]` only if it passes without a new
orphan WARN.

## Recheck — 2026-09-13 18:12Z

The joint relation is still visible on a real invocation, and unavailable inputs remain distinct
from measured no-activity:

- `scripts/mesh-occupancy-kind --json`, `2026-09-13T18:01:15Z`, exit 2:
  `label=DEGRADED`, `activity_relation=UNKNOWN`, `activity_coverage=0/2`, presence and motion
  `OFFLINE`, light `UNKNOWN`. No `EMPTY` or `NO_ACTIVITY` verdict was emitted.
- `scripts/mesh-occupancy-kind --test` — PASS (25 assertions and the real cached read).
- `tests/test-mesh-social-fusion-occupancy.sh` and
  `tests/test-mesh-social-fusion-unreachable.sh` — PASS.
- `mesh-activity-light --test` — PASS (existing 3-axis fusion tool; no source changes here).
- `mesh-doctor --test` — PASS.
- Full `mesh-doctor --quiet` — timed out at the 600-second cap before its orphan census or final
  summary. Its emitted checks include hard FAILs for egress over `tailscale0` and an exit node,
  `mesh-report` real smoke-test FAIL, and unrelated warnings for the default microphone, untimed
  peer SSH, funnel bypasses, absence-as-negative sites, temporary-file leaks, and incomplete
  serial-confirm coverage. Thus this is not a full doctor PASS and no-new-orphan-WARN is unverified.

No `[sense]` line was posted because the required full doctor gate did not pass. No new tool file,
state artifact, scheduler wiring, or commit was made. Next action: resolve the full-doctor blockers,
rerun `mesh-doctor` through its orphan census with no FAIL and no new orphan WARN, then post this
verified fusion result as `[sense]`.

## Recheck — 2026-09-14 10:20Z

The derived motion × recent-light-change relation remains explicit and distinguishes unavailable
evidence from a measured quiet pair:

- `scripts/mesh-occupancy-kind --test` — PASS (25 assertions and real cached read).
- `tests/test-mesh-social-fusion-occupancy.sh` and
  `tests/test-mesh-social-fusion-unreachable.sh` — PASS.
- `scripts/mesh-social-fusion --test` — PASS (6 assertions and joint relation/coverage contract).
- `scripts/mesh-occupancy-kind --json`, `2026-09-14T10:19:34Z`, exit 2:
  `label=DEGRADED`, `activity_relation=UNKNOWN`, `activity_coverage=0/2`, presence and motion
  `OFFLINE`, light `UNKNOWN`. This is a real partial read, not `NO_ACTIVITY` or an empty-room claim.
- `scripts/mesh-doctor --test` — PASS after making its FAIL(real) fixture pin healthy meminfo and
  low PSI inputs; the fixture no longer depends on this host's exhausted swap. The installed
  `~/.local/bin/mesh-doctor` remains an older copy and its `--test` still fails with `got 'na'`.
- Full `scripts/mesh-doctor --quiet` — timed out at 620 seconds (exit 124). It reported hard FAILs
  for egress over `tailscale0` and an exit-node setting, plus unrelated microphone, peer-SSH,
  sole-path, absence-as-negative, temp-leak, stale-confirm and unassessed warnings. It did not
  complete the orphan census, so no clean doctor result or no-new-orphan-WARN result is available.
  Captured output: `task-receipts/mesh-doctor-cross-fusion-20260914.log`.

No `[sense]` post was made because the required full doctor PASS and orphan census are still absent.
No tool file or scheduler wiring was created and nothing was committed. Next: resolve the owned
doctor blockers and smoke-sweep stall, bring the installed doctor in sync through the normal landing
path, rerun the full doctor through its orphan census, then post this artifact only if it passes with
no new orphan WARN.
