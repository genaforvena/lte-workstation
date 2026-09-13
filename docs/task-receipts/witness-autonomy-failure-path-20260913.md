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

This supplements commit a09b9c2a in the same isolated branch. It is not deployed yet.
Genome's existing `autoland/witness-autonomy-reflex-20260913/land-and-verify` must land
both commits, verify installed parity, and observe the scheduled execution and lease
sweep. Full queue self-maintenance remains unproven until live wiring and corrective
outcomes are checked.
