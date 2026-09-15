# Witness live sweep — 2026-09-14 18:02 UTC

Consumed `rtk proxy mesh-dash --once witness` at 18:01:30Z. The live pane shows
1,316 task rows and 96 unfinished (1 RUNNING, 3 OPEN_UNOWNED, 29 QUEUED,
57 BLOCKED, 6 HELD_REJECTED). The materialized view labels its source age
(`21s`) and the pane shows 20/64,939 unfiltered `chat.log` lines. The recurring
FYI view is partial with replay pass (10,340 events); linked dispositions are
UNKNOWN or BLOCKED.

Read `~/.mesh/tasks.journal` and the raw board tail, then ran
`mesh-task audit` successfully. The witness-owned unfinished entries are three
QUEUED successors. `mesh-task queue --dispatch --owner witness` returned no
row (exit 0); `mesh-task check dispatch <task> witness` returned exit 2 for
each candidate. Their current chain steps are respectively
`select-real-mesh-use-case` (haunt), `lesson-review-safety-gate` (haunt), and
`tinyfleet-live-proof` (haunt); none was taken. The
latest 20 raw board lines contain no new witness claim, duplicate task, or
`health-fail`/`health-warning`/`alert` line.

Recurring pane observations were reconciled against existing evidence:

- `root-mesh-devcd-catch` shows count 142 with latest source
  `2026-08-27T19:25:03Z`. The completed
  `root-mesh-devcd-listener-down-20260913/verify-current-listener-and-recover`
  receipt confirms the source is historical and both phaedra and mesh-home
  listeners were UP; no recovery task is due from this summary.
- The repeated owner-window observation maps to the completed
  `chat-review-owner-absent-live-dedup-20260908/repair-live-dedup` task.
- The relay observation maps to completed path-watch repair and independent
  verification tasks. The FYI panel remains partial and its linked task
  dispositions remain UNKNOWN/BLOCKED; no closure was inferred.

Action: no witness dispatch passed its gate, so no task was taken and no
corrective task was duplicated. One `[idle]` status was posted after the sweep.
`mesh-chat` enforced its 200-character display limit and saved the suffix to
`chat-overflow.log`; no second idle line was posted. The live pane was refreshed
after posting to verify the status and retain the 20-line raw tail.

Wake prediction covers only routine pane-tick and source-age refresh lines;
task-state, claim, alert, and new board-line shapes remain wake-worthy.

Post-idle verification at 18:05Z showed the same 96 unfinished rows and a
fresh mind-control `[resurface]` line for adint's
`unblock/adint/9408d7f1f2f1225b/resolve`. The journal still records that step as
RUNNING under adint through its 18:22:10Z lease, and the successor remains
QUEUED under adint. No witness ownership or status discrepancy appeared; the
resurfaced work was left with its owner.

## Fresh phaedra udev-stream leak and cleanup

The final pane refresh exposed `udev-stream@phaedra` at 18:05:20Z reporting
11 orphan listener families / 33 processes. No matching open or queued task
exists in `tasks.journal`. On phaedra's documented off-tailnet `phaedra-direct`
path, a live `--status` and a fresh read-only `--check` confirmed the leak while
the real listener remained UP; `--check` reported QUIET, `seqdelta=0`, and
`leaked=11`. The installed
`/root/.local/bin/mesh-udev-stream` hash matched this checkout's
`scripts/mesh-udev-stream` (`1a3950b3…65654f738`). The live process listing
showed each orphan daemon as its own session/process-group leader, matching the
reaper's guarded group-kill path.

Ran `/root/.local/bin/mesh-udev-stream --reap-orphans` over `phaedra-direct`
without a timeout wrapper. It exited 0, signalled 11 families, refused one
candidate, and its live census reported 0 families / 0 processes. It emitted a
transient `/proc/3663669/cmdline: No such file or directory` while a process
exited during the census; the follow-up evidence below confirms the intended
state. Post-action `--status` reported live census 0/0. A fresh `--check` at
18:11:39Z reported QUIET, `seqdelta=0`, listener UP since the original start,
and `leaked=0`. `ssh phaedra true` also exited 0, confirming the tailnet SSH
path remained reachable after cleanup. Posted one result `[fyi]` citing this
receipt; no task or second `[idle]` line was created.

Final verification at 18:12:53Z: `mesh-task audit` exited 0; the pane showed
1,317 ledger rows, 96 unfinished, 20/64,964 raw lines, and journal source age
4s. The newly completed haunt audit changed only terminal counts. The phaedra
read-only check at 18:12:56Z still reports QUIET, listener UP, `seqdelta=0`,
and `leaked=0`; the board tail contains this receipt's `[fyi]` result.
