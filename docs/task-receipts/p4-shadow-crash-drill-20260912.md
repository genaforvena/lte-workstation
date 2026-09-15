# P4 shadow crash drill — 2026-09-12

Task: `design-spec-crash-proof-followup-20260912/p4-shadow-crash-drill`.

Ran the drill in a separate tmux server (`p4pub`, session `shadow`) and a fresh clone at
`/tmp/mesh-p4-pub.JMJRUM/repo`, with an isolated `HOME`, `CODEX_HOME`, task ledger, and handoff
directory. The production mesh panes and repository worktree were not used for the drill. The test
worktree held exactly two synthetic dirty paths: a tracked README line and an untracked marker file.
No manual handoff was written; P2 used only `mesh-handoff --snapshot` auto-snapshots.

P1 snapshot: `refs/wip/drill` → `e0b581684bd8590a5ad3bd25f7a64842f19aeb91`. Its tree contains:

- `README.md`: `P4_SHADOW_DIRTY_SENTINEL=pub-20260912-9f31`
- `p4-untracked-marker.txt`: `P4_SHADOW_UNTRACKED_SENTINEL=pub-20260912-9f31`

P2 wrote an auto-snapshot in `/dev/shm/mesh-p4-pub.JMJRUM/drill.md`; it named the WIP ref and
recovery command. The final snapshot was taken from a separate control pane so the measurement
commands did not displace the test mind's own scrollback.

For the engine-kill case, Codex session `01a09395-5e1c-7aa0-abd8-3a84723da672` was running in the
isolated `drill` pane when its process was killed with `SIGKILL` (PID 3844200). The tracked and
untracked working-tree copies were then removed while `.git` and the auto-handoff remained. Fresh
Codex session `01a0939a-27ba-7fe3-832c-217980783b94` restored the handoff and read `refs/wip/drill`;
its recovered response named both sentinels and `mesh-wip-commit --restore drill`. That command
reconstructed the two files, and a fresh `rg` plus `git status --short` confirmed their values and
dirty paths.

For the `/clear` case, `mesh-clear drill` exercised the real path and reported
`/clear → shadow:drill.0 (handoff written)`. The fresh Codex context (session
`01a0939e-650b-7643-b936-d61c7bd6cb8d`) read the preserved WIP ref and returned both sentinel values
plus the same exact recovery command. No edits occurred during this recovery check.

For the simulated-reboot case, the Codex process was killed, the two working-tree copies were
removed again, and `/dev/shm/mesh-p4-pub.JMJRUM/drill.md` was deleted. The test `.git` directory and
`refs/wip/drill` remained intact; the handoff directory was verified empty. Fresh Codex session
`01a0939f-cee0-7830-82d2-79fad760833f` independently found the ref, reported both sentinels, and
named `mesh-wip-commit --restore drill`. Running that command restored both paths; `rg` confirmed
the exact marker values and `git status --short` showed `M README.md` and
`?? p4-untracked-marker.txt`.

The first isolated SessionStart attempt failed because the fixture had no isolated `chat.log` for
`mesh-task reconcile`. After creating that empty test-only file, reconciliation returned zero
canonical pointers and subsequent SessionStart hooks completed; the active recovery sessions above
were genuine fresh Codex sessions. The first WIP attempt also exposed the clone's missing Git author
identity; rerunning with test-only author/committer values produced the ref recorded above.

This verifies engine death, `/clear`, and the task's simulated-reboot definition (fresh session,
cleared tmpfs handoff, intact `.git`). It does not claim a physical host reboot. The shadow Codex
sessions are preserved in the isolated Codex session index under `/tmp/mesh-p4-pub.JMJRUM/codex`.
