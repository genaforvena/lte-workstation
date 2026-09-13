# Witness pane fit progress — 2026-09-13

Task: `witness-pane-fit-20260913/fit-required-ledger-and-raw-tail`

The live 274-column witness pane initially had 33 rows. Its last 20 raw `chat.log` entries and
supplemental FYI/ask blocks occupied the visible tail, pushing the task heading, unfinished count,
source-age label, and some task rows above the viewport. I enlarged the top data pane to 47 rows
(the lower mind pane remains 20 rows) and moved the secondary FYI/ask blocks before the required
task-and-raw-tail snapshot in `scripts/mesh-dash`.

The new `tests/test-witness-pane-fit.sh` reproduces the 47-row viewport with 25 unfinished tasks
and 20 raw source lines. It failed before the renderer change because the heading was outside the
viewport; after the change it passed with 20 task rows and all 20 raw lines visible together. The
test is wired into `scripts/mesh-dash --test`.

The full `scripts/mesh-dash --test` still exits 1 at its existing `minds` division-of-labour gate.
The same failure reproduces from unmodified `HEAD`: the bounded pane call times out waiting for
`mesh-forage --json`, even though the executable later returned JSON when run directly. The separate
corrective task is `mesh-dash-forage-pane-gate-20260913`; no minds behavior was changed here.

Genome completed the forage correction: the success and timeout fixtures pass, and `mesh-dash --test`
reports the minds gate green. I reran the full suite. It exits 2 only for two explicit node-condition
N/A results: the pinned 27-row cap cannot fit this node's 28-row fixed floor, and the best-of-three
`--test-fast` measurement was 17s against a 9s budget at load1 80.75. All runnable gates passed,
including the new pane-fit regression.

The witness tmux window is now 68 rows total with a 47-row data pane and 20-row mind pane. The
repository renderer hash is `ce8c0d81`; deployed `~/.local/bin/mesh-dash` is still `f8318420`.
Capturing the visible deployed pane shows the old ordering: only 10 task rows are visible, and the
heading and source-age label are above the viewport. The source, test, and this receipt remain local
changes. The task stays open until Genome lands/deploys the scoped renderer and test, then a fresh
live capture confirms the heading, unfinished count, source age, 20 task rows, and raw 20-line tail
together.

## Deployment and live capture — 2026-09-13 18:25Z

The renderer and its regression test were landed with path-scoped `mesh-land` runs. The initial
two-path apply landed the renderer and held the test because the board had no concrete test-file
completion description; the follow-up explicitly selected only `tests/test-witness-pane-fit.sh` and
used subject `Add witness dashboard viewport regression test`. The resulting commits are
`6a35feea` (renderer) and `c9b82b9d` (test); `main` is synchronized with `origin/main`. The renderer
commit's subject came from an older board completion and does not describe this diff; its actual
change is the supplemental-block reorder and the viewport regression hook.

`scripts/mesh-dash` and `~/.local/bin/mesh-dash` both hash to
`ce8c0d81fe894b08760484e5febb8b26a71eb7ce110a2f1eee32629977aa8c8e`. Running the installed
`~/.local/bin/mesh-dash --test` passed both `test-mesh-dash-forage-timeout` and
`test-witness-pane-fit`.

The captured live top pane is `mesh-home:9.0`; its saved frame is
[`witness-pane-capture-20260913.txt`](witness-pane-capture-20260913.txt). It shows the task heading,
unfinished count, source age, 20 task rows, and the latest 20 raw chat lines together. The captured
source age was 53s; measured counts are 20 task rows and 20 raw lines. `mesh-window-check witness`
also passed.

The final installed `~/.local/bin/mesh-dash --test` run completed with exit 2 only for its two
reported node-condition N/A checks: the fixed 28-row content floor cannot meet the pinned 27-row
cap, and `--test-fast` measured 11s against its 9s bar at load1 25.51. Every runnable leg passed,
including the forage success/timeout arms and the viewport regression.

## Live pane after process refresh — 2026-09-13 18:41Z

The renderer had been deployed while the existing `mesh-dash witness` process still held its old
code in memory. I respawned only data pane `mesh-home:9.0`, then captured the actual visible pane.
At 47 rows by 189 columns, two task rows wrapped and pushed the heading and source age out of view;
I expanded the data pane to 50 rows and the mind pane to 17 rows in the same 68-row window.

The refreshed live capture in `witness-pane-capture-20260913.txt` is 50 rows. It shows the task
heading on row 1, source age on row 2 (`source age=11s`), the 99-unfinished count on row 3, 20 task
rows, the unfiltered 20-line `chat.log` tail, and the live timestamp. The source and installed hashes match at
`ce8c0d81fe894b08760484e5febb8b26a71eb7ce110a2f1eee32629977aa8c8e`. `tests/test-witness-pane-fit.sh`
passes at the live 189-column width; the live pane reserves three extra rows for actual task-line
wrapping. The full dash suite's only nonzero results remain the two explicitly classified node
conditions above.
