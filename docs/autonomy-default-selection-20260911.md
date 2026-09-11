# Autonomy default and experiment-selection receipt — 2026-09-11

The mesh's research/reflection reflexes now choose their own work by default when the local
`claude` distiller is available. `MESH_AUTONOMY=0` is the explicit global opt-out; the narrower
`MESH_STUDY_AUTO` and `MESH_REFLECT_AUTO` variables still override one lane independently.

The study bridge prompt and task boundary now make full experiment-parameter ownership explicit. For
parameters not already preregistered, the worker selects and freezes them from repository/runtime
evidence, records the rationale, and does not ask the operator to choose. The reproducibility record
covers model revision, corpus/dataset manifests (including CSV/JSON/TSV inputs), dataset split and
sample budget, cross-validation folds/repeats when applicable, arms/ranges/order, seeds, training
hyperparameters and step budget, metrics and decision thresholds, stopping rule, and resource and
wall-time caps. If a frozen registration has no CV field, the worker records `not applicable`; it does
not invent a field or ask an operator. Existing frozen registrations must be preserved exactly; resource
contention causes a retry, never silent parameter renegotiation.

The durable `mesh-task create` boundary now enforces the same contract for every new task whose
description names an experiment, study, parameter, benchmark, ablation, or replication. This catches
plans emitted by other producers, not only the study bridge. For the Tiny Fleet pilot, the worker owns
the complete experiment decision record; operator input is not a normal selection path.
The Tiny Fleet matrix runner now rejects manifest, seed, and case-subset overrides during real
execution; those switches are reserved for verification-only smokes, so a human cannot accidentally
turn the real pilot into a favorable subset run.
`mesh-study-launch` also writes an atomic `autonomy-decision.json` before queueing, recording
`operator_required: false`, the frozen registration hash, corpus manifest, and full-arm/full-seed
selection policy. The runner explicitly permits that receipt as an input artifact.

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
contention. `scripts/mesh-study-autowake` is the readiness reflex: it records an atomic waiting receipt
while frozen adapter artifacts are absent, then invokes the launcher automatically once the complete
registered matrix is runnable. It never asks an operator to choose parameters, subsets, or a start time.

- `tests/test-autonomy-defaults.sh` exercises default autonomous selection, global opt-out, and
  per-lane override with real script execution and hermetic local fixtures.
- `scripts/mesh-study --test`, `scripts/mesh-reflect --test`, and `scripts/mesh-study-bridge --test`
  pass; the study test also completed its live-read gate with 20 current hits.
- After expanding the parameter prompt, `mesh-study-bridge --gate-live` passed both live arms:
  off-topic SKIP 8/8 (floor 3/8) and on-topic APPLY 7/8 (floor 5/8), using the live mesh relay.
- `mesh-task --test` now asserts the full reproducibility contract is added at task creation;
  `mesh-study-bridge --test` captures the actual distiller prompt and asserts it carries autonomous
  parameter selection and frozen-registration preservation.
- `tests/test-mesh-task-autonomy-detection.py` exercises the common benchmark/ablation/replication
  labels and passes against the real task-description boundary.
- `tests/test-primary-compute-selection.sh` passes after `MESH_PRIMARY_COMPUTE=mesh-home` was added
  to the live node registry; a refreshed card advertises `capabilities: compute: primary`.
- Tiny Fleet `scripts/test_run_study_matrix.py` passes 10 tests, including rejection of real-execution
  manifest, seed, and case-subset overrides; verification-only bounded overrides remain supported.
- `tests/test-mesh-study-launch.sh` passes with the autonomy receipt present, and
  `mesh-study-launch --test` passes.
- The real runner guard is exercised before GPU admission, so an invalid human subset cannot sit in a
  24-hour resource wait; the normal launch path remains registration-driven and non-interactive.
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
- `tests/test-mesh-study-autowake.sh` verifies the readiness reflex waits autonomously and launches
  when all registered adapter artifacts become available.
- Installed command paths resolve to the repository scripts:
  `~/.local/bin/mesh-study`, `mesh-reflect`, `mesh-study-bridge`, and `mesh-heavy-run` resolve into
  this worktree. `mesh-heavy-drain` is autowired at `*/2 * * * *` in the live crontab and logs to
  `~/.mesh/heavy-drain.log`.

Unresolved by design: operator-owned substrate/safety gates and genuinely unavailable external
inputs remain blocked and visible; this change removes routine choice-waiting, not those physical
or governance constraints. The live ledger's remaining `operator-input` rows are typed examples of
that boundary: missing physical exports/dictionary source material, or an external node coming back
online. The mesh must not invent those facts just to make a task green.
