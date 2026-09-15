# MCC sense closure: `mesh-io-contention` → `mesh-stress`

Date: 2026-09-10

Closed producer↔consumer link: `scripts/mesh-io-contention` → `scripts/mesh-stress`.

The producer is a live relational sense over `/proc/stat` CPU iowait and `/proc/diskstats`
block-device ticks. `mesh-stress` now reads its fresh `.mesh/.io-contention.state` artifact and
publishes `io_contention_state`, both deltas, and `io_contention_joint`. The consumer raises only
the joint `IO_CONTENTION + heavy local load` pattern to WARM; IDLE/one-sided activity, absent,
stale, malformed, or unreachable input cannot raise pressure and remains `?` where applicable.

Evidence:

- `scripts/mesh-io-contention --test`: PASS; real procfs read `iowait=5 disk_ticks=8`.
- `tests/test-mesh-io-contention.sh`: PASS; missing kernel inputs return rc=2.
- `scripts/mesh-stress --test`: PASS, including fresh producer-only, joint, and stale-artifact
  consumer cases.
- Live producer run at 2026-09-10T15:50:49Z: `IDLE`, `iowait_delta=0`, `disk_io_ticks_delta=0`.
- Live consumer run immediately afterward: `io_contention_state=IDLE`,
  `io_contention_joint=no`, `level=WARM` (the level is independently elevated by existing axes).
- `scripts/mesh-stress` and `scripts/mesh-io-contention` are executable; source syntax check passed.
- Before this change, `rg` found `mesh-io-contention` only in itself and its test; after it is read
  by `mesh-stress`.

Doctor gate: NOT CLEAN. `mesh-doctor` reports pre-existing egress FAILs (`egress rides tailscale0`,
`exit-node set`) and existing WARNs (busy default mic, untimed peer SSH). Its `--test` passes, and
no new orphan warning names this change. No `[sense]` board post was made because the contract
requires a clean live `mesh-doctor` first.

Uncommitted by request. Next action: repair or explicitly clear the pre-existing egress doctor
failures, rerun live `mesh-doctor`, then post:

`[sense] closed producer↔consumer: mesh-io-contention → mesh-stress (IO contention × heavy load)`
