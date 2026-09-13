# Active-claim recovery

On 2026-09-13, `mesh-witness-task-autonomy` gained a bounded recovery action for
an active claim whose owner and lease remain unchanged for 30 minutes.  The
witness tape records the exact stalled task and sends its exact owner a
`mesh-tell --origin` continuation prompt.  The prompt requires the owner to
continue, or to record a concrete block and create or take the prerequisite
that unblocks it.  The observer never reassigns or silently expires a claim.

The per-task recovery timestamp is durable in
`~/.mesh/.witness-task-autonomy.json`; a retry occurs no more often than the
existing 30-minute health-alert cadence, and a changed owner or lease resets
the observation.

Verification passed on the deployed executable: source/install SHA-256
`8b0637cafc918a2dbd458ad1a92d31caa51b67a39c3f00f2dd0308c4aa24838e`,
`~/.local/bin/mesh-witness-task-autonomy --test`,
`scripts/mesh-task-unblock-sweep --test`, and
`python3 tests/test-mesh-witness-task-autonomy.py`.  The fixture advances an
unchanged active claim beyond the threshold and asserts both the durable
failure row and one exact-owner recovery wake.  Commit `2c5dc663` is pushed to
`main`.
