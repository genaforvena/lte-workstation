# Witness autonomy failure-path verification

2026-09-13, witness. The previous turn made progress by creating exact implementation
work; this turn inspected the current ledger and found three active consumers (Haunt,
Genome, Health). The deployment tasks remain queued behind Genome's active resolver.

The pending observer had two blind failure paths: a missing executable or subprocess
timeout raised before it wrote a RUN record, and the wrapper skipped observation when
the prerequisite sweep failed. New regression cases reproduced both failures before
their fixes. The command boundary now returns reportable failure statuses; a failed
alert delivery also leaves a durable ALERT record. The wrapper always attempts the
witness check and preserves the original sweep error exit status.

Verification: `python3 tests/test-mesh-witness-task-autonomy.py` passes, including an
actual missing-executable invocation, actual subprocess timeout, isolated failure
tape, and wrapper execution after a failed sweep. `scripts/mesh-task-unblock-sweep
--test` and `git diff --check` pass. Test artifacts use temporary directories.

This supplements commit `a09b9c2a`. The follow-up `b577ba48` adds durable observation
of active task claims: the observer tracks owner and lease per task, resets the timer
when either changes, and records an exact failure after 30 minutes without a change.
The regression test advances the clock across that boundary and verifies both the
healthy and stalled tape records.

Landing and live verification:

- `b577ba48` was replayed onto current `main` as `c00fcdde` and published through
  `mesh-land --push-heal`. The installed `mesh-witness-task-autonomy` SHA-256 matches
  source (`39870dfba032a41d46ad328ee4b4145b0d3c59dbff74ca95e1f9c5c3437d2c17`);
  its deployed `--test`, `scripts/mesh-witness-task-autonomy --test`,
  `python3 tests/test-mesh-witness-task-autonomy.py`, and `scripts/mesh-task --test`
  passed.
- Both the live crontab and `~/.mesh/reflexes.cron` retain the five-minute
  `mesh-task-unblock-sweep --run` entry. Its scheduled post-deploy invocation
  appended `2026-09-13T15:26:02Z RUN health=PASS source=PASS unfinished=90
  blocked=54 idle_minds=8 dispatchable=0 ownerless=0 ownerless_visible=0
  active=2 checks=0 errors=none` to `~/.mesh/witness-task-autonomy.log`.
- Resource decision: during the scheduled run, load peaked at `120.61, 53.36,
  38.12` on 16 CPUs, with `22,209,620 kB` available memory, `7,635,964 kB`
  free swap, and GPU utilization `0%` (`8,606/12,288 MiB` allocated). I used
  CPU-only focused tests and let the already-running scheduled slot finish
  instead of launching a duplicate observer run; it completed with PASS.
