# MCC link: `mesh-note3-field-motion` → `mesh-situation`

Selected the live-but-under-consumed branch. Before the change, `rg -l` over the five named fusions
(`mesh-situation`, `mesh-sensorium`, `mesh-stress`, `mesh-ambient-clock`, `mesh-operator-state`)
found no reader for `mesh-note3-field-motion`, `field_motion`, or `magnetic_field_uT`. A fresh read
from its Note 3 sensorcat HAL types 2+4 then returned a real, aligned AK09911C magnetometer × MPU6500
gyroscope pair.

`mesh-situation` now calls that producer live, validates the paired numeric fields and HAL ticks,
preserves the producer JSON, and reports `field_motion_status` plus `field_motion_coverage`. A missing,
malformed, or unreachable producer remains `UNKNOWN` with `0/1` coverage and makes the fusion return
exit 2. No novelty or fitness score, new label, or state artifact was added. The existing
`mesh-situation` cadence and executable symlink are unchanged; the producer source was already
executable and declared `orphan-ok`. No new tool file was created.

## Verification

- RED: `scripts/mesh-situation --test` failed at the new assertion because the fusion output lacked
  `field_motion_status`.
- GREEN: `rtk scripts/mesh-situation --test` — pass, including a fixture with the real paired shape,
  and an unreachable case asserting `UNKNOWN`, `0/1`, and exit 2.
- `rtk bash -n scripts/mesh-situation` — pass.
- `rtk scripts/mesh-note3-field-motion --test` — pass; it required a real paired HAL read:

  ```json
  {"magnetic_field_uT":{"x":1.14,"y":30.3,"z":47.22,"magnitude":56.117002770996244},"angular_velocity_rad_s":{"x":0.0,"y":0.00133158,"z":0.0111853,"magnitude":0.01126428166313325},"coverage":"1/1 paired sample","pair_skew_ms":4.227,"pair_age_ms":20.464,"hal_ticks_ns":{"magnetometer":177621275309091,"gyroscope":177621279536341},"source":"Note 3 sensorcat HAL types 2+4"}
  ```

- Fresh direct `rtk scripts/mesh-note3-field-motion --json` — exit 0:

  ```json
  {"magnetic_field_uT":{"x":0.78,"y":30.72,"z":46.92,"magnitude":56.08754942052648},"angular_velocity_rad_s":{"x":-0.00133158,"y":0.00399474,"z":0.00958738,"magnitude":0.01047133746129882},"coverage":"1/1 paired sample","pair_skew_ms":4.25,"pair_age_ms":25.298,"hal_ticks_ns":{"magnetometer":177646900452103,"gyroscope":177646904702144},"source":"Note 3 sensorcat HAL types 2+4"}
  ```

- Fresh `rtk scripts/mesh-situation --json` — exit 0; the live fusion called the producer and emitted
  this real nested artifact with full overlap:

  ```json
  {"magnetic_field_uT":{"x":0.66,"y":30.72,"z":46.74,"magnitude":55.93551286973241},"angular_velocity_rad_s":{"x":0.000266316,"y":0.00399474,"z":0.00932106,"magnitude":0.01014450744999756},"coverage":"1/1 paired sample","pair_skew_ms":0.0,"pair_age_ms":33.014,"hal_ticks_ns":{"magnetometer":177635876985973,"gyroscope":177635876985973},"source":"Note 3 sensorcat HAL types 2+4"}
  ```

- `~/.local/bin/mesh-situation` resolves to the edited `scripts/mesh-situation`, so the verified
  consumer is on the live local invocation path.
- Post-change `rtk mesh-doctor --quiet` — **exit 2**, `2 FAIL, 33 WARN`; hard FAILs remain
  `egress rides tailscale0` and `exit-node set (n2sbt7yy6t11CNTRL)`. The orphan census remained at
  `94 unwired+non-canon, confirmed 2+ checks`; no new orphan warning named this link. Doctor did not
  pass cleanly, so no `[sense]` line was posted.
- No commit was made.

## Next action

The substrate owner clears the two routing FAILs, then reruns `mesh-doctor --quiet`. Only after it
exits 0 with no new orphan WARN, post:

`[sense] mesh-note3-field-motion <-> mesh-situation: live Note 3 magnetic-field × gyroscope artifact consumed (1/1)`
