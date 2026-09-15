# Idle-turn follow-through mislanding finding — 2026-09-11

## Finding

Commit `8c0481eb4250946308835ab5e11e3e9cfed4fee5` was pushed under the subject
`mesh-land: land idle-turn correction regression tests`, but its only path is
`tests/test-mesh-task-no-expiry.py`. That file was already a tracked dirty path outside the reviewed
idle-turn correction scope. Its content adds resolver-completion/parent-resume tests, not pane-consume
idle-turn tests, and the landing also changed its mode from `100644` to `100755`.

The reviewed correction test is instead
`tests/test-mesh-pane-consume-task-aware-idle-gate.sh`, already landed separately as commit
`025ef766c7fd80fa17d1510502bc5470a29a215e`.

## Required recovery

Do not rewrite pushed history and do not discard the underlying resolver-test edits. Create a normal
revert of `8c0481e`, then restore exactly its content delta to the working tree as uncommitted mode
`100644` work so its real owner can reconcile it under the correct task. Verify the revert commit,
restored dirty diff, mode, and unchanged correction artifacts independently before resuming the
idle-turn correction.

