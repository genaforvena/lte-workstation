# Health-warning triage: witness-task-autonomy

Task: `health-warning/d2c264da18ff7e026b55/triage`

## Finding

The 2026-09-16T01:29:19Z warning reported `source=PASS` but an exit-15
missing-prerequisite recovery error for the already referenced task
`health-warning/ea6220a35ca3e4238da1/triage`. That prerequisite is now
`complete`, owned by `health`, with its receipt present and hash-verified.
This warning is therefore stale/report-only; no rejection, reassignment, or
substrate mutation is justified. A distinct later warning at 01:31:57Z has
its own queued task and remains separate work.

## Live verification

- `mesh-dash --once check` at 2026-09-16T01:37:30Z returned local egress OK,
  all organs LIVE, but load 27.96/16, 4 fleet nodes down, 6 peers offline,
  degraded WG client handshakes, and `mesh-model-swap` as the real doctor
  smoke-test failure.
- `mesh-task status health-warning/ea6220a35ca3e4238da1` reports
  `[complete]` / `done` with artifact
  `docs/task-receipts/health-warning-ea6220a35ca3e4238da1-triage-20260916.md`.
  Its SHA-256 is
  `36b59e5657a127fa7c8b20b01c73ffceca41b60ed1c02f0d2d1419f825456757`.
- `mesh-task status health-warning/d2c264da18ff7e026b55` was active after
  the owner-authored take. `mesh-task-journal` was not refreshed because its
  view was 108 seconds old (<120s); this is recorded as a freshness limit,
  not treated as a pass.

## Independent delegated audit

The read-only `health-modelswap-audit` worker inspected the model-swap
failure. I personally inspected its cited files and reproduced both paths:

- `~/.mesh/.doctor-fails` records `smoke-test FAIL (real): mesh-model-swap`
  at 01:35:51Z.
- `scripts/mesh-model-swap:61` copies `$ROOT/scripts/mesh-voice-rx`.
  The deployed symlink resolves to the same script, with matching SHA-256
  `902e018517de3ecea45646e73e64fb1622e367b610fb2d5474cf235d5314c5d6`, but
  `$ROOT` becomes `/home/mesh-home/.local`; that fixture path does not exist.
- `bash scripts/mesh-model-swap --test` passed (`source_rc=0`), while
  `/home/mesh-home/.local/bin/mesh-model-swap --test` failed with
  `cp: cannot stat '/home/mesh-home/.local/scripts/mesh-voice-rx'` and
  `deployed_rc=1`.

The model-swap defect belongs to the owning code lane for a separate fix;
this health triage does not edit it. The worker made no file, substrate, or
task-state changes.

## Decision

Close this warning as stale/report-only. Retry only on a fresh
`witness-task-autonomy` warning or a new owner task; separately route the
deployed model-swap path-resolution defect to its code owner.

## Delegation and verification

Delegated `health-modelswap-audit` for the independent read-only model-swap
analysis. Personally inspected the worker's transcript, the failure marker,
the source line, symlink/hash metadata, and both test invocations above.
Receipt creation, task closure, board voice, and final verification stayed
local because they are tightly coupled ownership work.
