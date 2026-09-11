# Autonomy default and experiment-selection receipt — 2026-09-11

The mesh's research/reflection reflexes now choose their own work by default when the local
`claude` distiller is available. `MESH_AUTONOMY=0` is the explicit global opt-out; the narrower
`MESH_STUDY_AUTO` and `MESH_REFLECT_AUTO` variables still override one lane independently.

The study bridge prompt also makes parameter ownership explicit: a worker must choose and record
the seed, ranges, and arm ordering from repository/runtime evidence, and must not ask the operator
to pick or freeze experiment parameters. This covers experiment setup without pretending that
irreducible physical access, credentials, or safety decisions are machine-owned.

The durable `mesh-task create` boundary now enforces the same contract for every new task whose
description names an experiment, study, parameter, or params. This catches plans emitted by other
producers, not only the study bridge.

Resource ownership follows the same rule. `mesh-heavy-run` now records a content-addressed queued job
when its live memory/pressure admission gate returns `EX_TEMPFAIL`; `mesh-heavy-drain` periodically
rechecks the live gate and retries queued work. Queue records retain the original budget, command
arguments, working directory, enqueue time, and latest headroom evidence, so “GPU/CPU/memory busy right
now” is a retry state rather than an operator question or an impossible claim. Malformed legacy entries
are quarantined, and repeated non-resource failures are retained as `.failed` evidence rather than
retried forever or silently discarded. Real heavy consumers retain deferred inputs until the drain can
replay them. GPU consumers may additionally declare `MESH_HEAVY_GPU_MIN_FREE_MB`; the drain persists
that threshold and the `nvidia-smi` probe, so a busy GPU is treated as recoverable capacity pressure.

Evidence:

The Tiny Fleet matrix runner now applies the same principle at its real-execution boundary: it selects
a 2048 MiB free-VRAM default, waits for recovery within the frozen 24-hour wall cap, and writes
`resource-preflight.json` before loading adapters. A live telemetry failure or wait expiry is reported
as `deferred` and does not start a partial study; verification-only smokes remain GPU-free by design.
The node-local `mesh-study-launch` command wraps that exact frozen matrix in `mesh-heavy-run`'s durable
queue, limits each inner VRAM wait to 60 seconds, then relies on the existing two-minute drain to retry
contention. It is on-demand rather than scheduled, so enabling autonomous resource/parameter selection
does not silently start a multi-hour experiment without an open study task.

- `tests/test-autonomy-defaults.sh` exercises default autonomous selection, global opt-out, and
  per-lane override with real script execution and hermetic local fixtures.
- `scripts/mesh-study --test`, `scripts/mesh-reflect --test`, and `scripts/mesh-study-bridge --test`
  pass; the study test also completed its live-read gate with 20 current hits.
- `scripts/mesh-task --test` passes, including creation of an experiment task and inspection of its
  persisted description for the machine-owned parameter contract.
- `scripts/mesh-heavy-run --test` passes, including transient-pressure enqueue and recovery drain;
  `scripts/mesh-heavy-drain --test` passes for the recurring drain contract.
- Tiny Fleet `scripts/test_run_study_matrix.py` passes 8 tests, including a subprocess fixture that
  observes GPU-busy then GPU-recovered admission; an unavailable-GPU run returned 75 and wrote a
  `deferred` `resource-preflight.json` before adapter/backend access.
- `tests/test-mesh-study-launch.sh` verifies the launcher selects only the frozen registration and
  queues the run with the declared RAM/VRAM gates and short retry window; installed command resolves
  to this repository's `scripts/mesh-study-launch`.
- Installed command paths resolve to the repository scripts:
  `~/.local/bin/mesh-study`, `mesh-reflect`, `mesh-study-bridge`, and `mesh-heavy-run` resolve into
  this worktree. `mesh-heavy-drain` is autowired at `*/2 * * * *` in the live crontab and logs to
  `~/.mesh/heavy-drain.log`.

Unresolved by design: operator-owned substrate/safety gates and genuinely unavailable external
inputs remain blocked and visible; this change removes routine choice-waiting, not those physical
or governance constraints.
