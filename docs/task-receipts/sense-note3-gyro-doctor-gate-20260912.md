# Note 3 gyroscope probe — doctor gate

Candidate signal: the Note 3's MPU6500 three-axis angular velocity (rad/s). Existing `mesh-gyro`
reads the Redmi body; the Note 3's orientation and acceleration are sensed, but no Note 3 tool read
this gyro. The new on-demand instrument is `scripts/mesh-note3-gyro`; it reports raw axes and the
Android HAL event tick without assigning a motion verdict. Its header declares `orphan-ok` until a
relation to other live axes is measured.

Evidence from 2026-09-12:

- `rtk scripts/mesh-note3-gyro --test` — PASS, including a real MPU6500 event
  `-0.00239685,-0.000266316,0.00798948`, HAL tick `29550114180299`.
- `rtk scripts/mesh-note3-gyro --json` — PASS with a second real read at
  `0.00186421,0.00213053,0.0082558`, HAL tick `29551732818009`.
- Full bounded `mesh-doctor --quiet` — exit 2: 2 FAIL, 33 WARN. Existing egress checks fail because
  traffic rides `tailscale0` and an exit node is set. Existing warnings include the default mic,
  timed peer SSH, stale/unassessed tests, and 92 stable orphans. The current orphan ledger does not
  contain `mesh-note3-gyro`; no new orphan warning was introduced.
- No `[sense]` line was posted because the requested doctor-clean gate did not pass. No network,
  routing, or unrelated doctor issue was changed.

Next action: after the node doctor blockers are resolved, rerun `mesh-doctor --quiet`; only if it
passes without a new orphan warning, post the `[sense]` line for this probe. Do not commit this work.
