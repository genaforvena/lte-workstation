# Witness pane compact viewport — 2026-09-14

The witness data pane can shrink to 80×11 or 80×12 when its tmux window is split. The prior renderer placed
the task summary above a 20-line raw board tail, so the visible frame contained only board lines and
the liveness footer. `mesh-window-check` correctly reported the missing labelled source age.

At 11 rows the renderer now shows the task heading, labelled materialized-view age, exact task
totals, the two highest-priority unfinished rows, an explicit count of hidden unfinished rows, and
the newest two unfiltered `chat.log` lines with their coverage label. At 12 rows the same compact
frame also fits above tmux's cursor row. The compact source label carries the task-journal mtime,
so `mesh-window-check` can distinguish a journal generation that advanced after paint from a bad
task count. Taller panes retain the existing 20-task/20-line view. The checker reads the live pane
height and validates the appropriate visible-frame contract.

The regressions are `tests/test-witness-pane-fit.sh` (full-height, 80×11, 80×12, and a two-digit source-age
frame) and `tests/test-mesh-window-check-witness-pane.sh` (full and compact checker frames,
board/task-ledger churn, missing-heading diagnostics, and failure cases). Both pass. `scripts/mesh-dash
--test` passed all runnable gates and exited 2 only for its existing node-load N/A: the best-of-three
fast check measured 33s against its 9s budget at load1 96.39.

After MeshLand deployment, the live witness pane was resized 80×11 → 80×12 → 80×11. The captured
frames retain the heading, source age and generation, exact counts, task sample, omission count, and
two raw board lines. `mesh-window-check witness` exited 0 at both sizes, with all 16 windows OK. The
full capture is in [`witness-pane-small-viewport-live-20260914.txt`](witness-pane-small-viewport-live-20260914.txt).

Repository and deployed hashes match: `mesh-dash` `b58a94b6…ea89333a`; `mesh-window-check`
`39661a48…2549bc23e`.
