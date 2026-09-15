# Witness pane-fit unblock verification — 2026-09-13

Task: `unblock/witness/86f189a3979ccf1c/resolve`

Genome's named prerequisite is present and deployed. The source and installed renderer both hash to
`ce8c0d81fe894b08760484e5febb8b26a71eb7ce110a2f1eee32629977aa8c8e`. The live witness data pane
`mesh-home:9.0` is 50x189; the extra rows cover actual task-line wrapping observed at this width.

Evidence captured for this resolution:

- `tests/test-witness-pane-fit.sh` — PASS: 20 task rows and 20 raw lines visible together.
- `mesh-window-check witness` — PASS; all windows look fine.
- Live pane capture: [`unblock-witness-pane-live-20260913.txt`](unblock-witness-pane-live-20260913.txt).
  It shows the task heading, unfinished count (102), source age (15s), 20 task rows, and the
  unfiltered `chat.log` tail (20 of 60,785 lines) together. The capture has 20 task rows and 20 raw
  chat lines.
- `scripts/mesh-dash` and `~/.local/bin/mesh-dash` hashes match at the value above.

The installed renderer's broader `--test` started and passed its forage-timeout and pane-fit tests,
then was stopped after it continued into unrelated environment-dependent smoke checks. The focused
regression and live pane checks required by this unblock completed successfully.

Resolution: the renderer deployment prerequisite is satisfied, the live pane meets the original
heading/count/source-age/20-task-row/20-raw-line criteria, and the parent pane-fit task is complete.
