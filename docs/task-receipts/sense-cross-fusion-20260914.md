# Cross-sense fusion live verification — 2026-09-14

The requested fusion already exists in the tracked executable `scripts/mesh-social-fusion`; this
turn made no source changes. It derives occupancy from the joint ambient-level × BLE-presence ×
activity pattern and operator-state from BLE-presence × activity × phone social-context. The output
includes overlap coverage and keeps an unavailable/stale axis visibly distinct from a real empty
reading.

## Verification

- `scripts/mesh-social-fusion --test` — pass.
- `tests/test-mesh-social-fusion-occupancy.sh` — pass, including genuine empty versus unreachable.
- `tests/test-mesh-social-fusion-unreachable.sh` — pass.
- `tests/test-mesh-social-fusion-coupling-audit.sh` — pass.
- Live `scripts/mesh-social-fusion --json`, 2026-09-14T02:16:17Z, exit 2: ambient and activity
  were LIVE; BLE presence was STALE (age 1,276,740 seconds); occupancy and operator-state were
  `UNKNOWN`, each with `0/3` overlap. The missing signal did not become an all-clear.
- `scripts/mesh-presence --test` — no live BLE scan possible: this host has no Bluetooth adapter.
- `scripts/mesh-doctor --quiet` completed with exit 2: `2 FAIL, 33 WARN`. The existing hard failures
  are egress on `tailscale0` and an exit node set; the doctor also reported the unrelated default-mic
  warning, other established warnings, and 94 stable orphan findings. `mesh-social-fusion` is not in
  the orphan ledger; its tracked source is executable and declares `orphan-ok`.

No `[sense]` board line was posted: the required doctor-clean gate failed. No commit was made.

Next action: the substrate owner restores a doctor-clean egress state; then rerun
`scripts/mesh-doctor --quiet` to completion and, only on exit 0 with no new orphan warning, post the
live partial fusion artifact with its stale-BLE/`0/3` coverage explicitly stated.
