# Witness pane charter checker receipt — 2026-09-14

Task: `chat-review/witness-pane-charter-contract-20260914/make-checker-enforce-charter`

Updated `scripts/mesh-window-check` so compact witness frames require at least
`min(20, unfinished)` visible task rows and `min(20, available chat lines)` actual raw tail
lines. Compact mode still requires its coverage label and omission count. Extended the focused
checker fixture to reject the renderer's 2+2 compact frame, reject a nominal 20-line label with
only two actual raw lines, and accept a complete 20+20 compact frame.

Verification:

- `rtk bash tests/test-mesh-window-check-witness-pane.sh` — PASS.
- `rtk bash tests/test-witness-pane-fit.sh` — PASS; normal 47-row output fits 20 task rows and
  20 raw lines, while the 80x11 compact renderer fixture still emits its 2+2 sample.
- `rtk scripts/mesh-window-check --test` — PASS (`16 windows in session mesh-home`).
- `rtk mesh-window-check` — exit 1, correctly reports `witness pane missing witness task heading`.
- Live `witness.0` viewport is 33x274. `tmux capture-pane -p` shows 33 lines, only 9 unfinished
  task rows and 20 raw chat lines; the task heading/count block is outside the visible viewport.
  A fresh `mesh-dash --once witness` emits 59 lines, so this live pane cannot display the full
  frame at its current height. The renderer's 80x11 compact fallback also remains below the
  enforced 20+20 charter.

Disposition: implementation and fixture are verified, but the parent task remains OPEN because
the current live witness pane cannot satisfy the visible-frame contract. Next action: change the
witness renderer/layout or pane allocation so its actual visible frame contains the heading,
freshness/count block, 20 unfinished task rows, and 20 raw chat lines; then rerun the focused
fixture, source smoke test, and deployed live checker. Do not certify the current underfilled pane.

Landing: not yet eligible at receipt time; the files are newly edited and MeshLand's 600-second
settle gate applies. `mesh-land --check` reported 929 existing bulk-backlog obligations; no
unrelated paths were selected.

## Followthrough — 2026-09-14

Changed the witness renderer to keep the complete authoritative 20-task + 20-raw-line frame even
when its pane is too short; it no longer labels a 2+2 sample as a compact witness frame. Updated
`mesh-restore` to reserve 19 rows for the witness mind pane, leaving a 48-row data pane on this
68-row terminal. Applied that allocation to the live `mesh-home:witness` window: pane 0 is now
274x48 and pane 1 is 274x19. The captured live frame contains the heading, source age, task counts,
20 unfinished task rows, and 20 raw chat lines.

Verification:

- `rtk bash tests/test-witness-pane-fit.sh` — PASS (normal viewport shows 20+20; short-pane render
  retains the full frame rather than claiming reduced coverage).
- `rtk bash tests/test-mesh-window-check-witness-pane.sh` — PASS (incomplete 2+2 and 20+2 frames
  fail; full 20+20 compact fixture passes).
- `rtk scripts/mesh-window-check` — PASS on the settled live frame; all 16 windows report OK after
  the witness allocation. One intervening run caught a partial redraw (missing witness labels and
  a separate discover-pane EOF); the next full check and direct pane capture were clean.
- `rtk scripts/mesh-dash --test` — exit 2 (honest n/a): all runnable legs passed; its fast-core
  benchmark was unmeasurable at load 32.96 on 16 cores against an 18s best-of-3 / 9s bar.
- `rtk scripts/mesh-restore --test` — FAIL in existing `chat`/`chat2` isolated collision checks
  and nested missing-session verdict checks. Those fixtures do not exercise witness sizing; the
  witness helper is called only for the `witness` window. This remains an unrelated restore-test
  obligation, not a passing verification.
- `~/.local/bin/mesh-dash` is a regular deployed copy and differs from `scripts/mesh-dash`; the
  source change will reach PATH through the steward's mesh-land deploy after review and settle.

Landing remains pending the 600-second settle interval measured from the latest source edits.
Next: path-limit `mesh-land` to `scripts/mesh-dash`, `scripts/mesh-restore`, and
`tests/test-witness-pane-fit.sh` plus this receipt, then verify the landed subject and live
deployment. Preserve the other dirty worktree paths.

## Stall recovery — 2026-09-14

Rechecked the actual visible pane after the stale 10:38 completion post. The checker initially
failed because the live witness window was manually constrained to 189x42 even though its attached
tmux client was 274x69. Merely increasing the pane height left the window too narrow; task rows
wrapped and pushed the charter heading above the viewport. Resized the live window to 274x68 and
the mind pane to 19 rows, yielding a 274x48 data pane. The visible capture now includes the heading,
freshness and task counts, 20 task rows, and the raw 20-line tail; `scripts/mesh-window-check`
reports all 16 windows OK.

Added a real isolated-tmux sizing fixture to `scripts/mesh-restore --test`. It first failed against
the old 67-row minimum at 54 rows (data=27, mind=26), then passed after `size_witness_window` began
reserving 48 data rows and allocating the mind the remaining 5 rows; the 68-row fixture preserves
data=48, mind=19. The production helper leaves windows below 54 rows untouched and emits the
allocation reason so the visible checker remains the final gate.

Fresh checks after the sizing change:

- `rtk bash -n scripts/mesh-restore`, `rtk bash -n scripts/mesh-dash`, and
  `rtk bash -n scripts/mesh-window-check` — PASS.
- `rtk bash tests/test-mesh-window-check-witness-pane.sh` — PASS.
- `rtk bash tests/test-witness-pane-fit.sh` — PASS.
- `rtk scripts/mesh-window-check --test` — PASS (16 windows).
- `rtk scripts/mesh-window-check` — PASS on the live 274x48 witness data pane; all 16 windows OK.
- `rtk scripts/mesh-restore --test` — FAIL overall on the existing nested node-condition precedence
  fixture (its injected block-1 code failure returned 2 instead of 1). Its new witness sizing
  fixture passed at both 54 and 68 rows, as did the isolated tmux teardown and collision fixtures.
- Source/deployed `mesh-dash` SHA-256 before landing: `78f3dc70887b7cfd153c25d3b7f0cd530a8f79e6b39b6e19602736a2c188db75` /
  `b58a94b61ec5b250e8815c5e9b176ff432474225594ecc5225e67ea6ea89333a` (different; source is not yet live on PATH).

No external prerequisite is needed: the current client provides enough rows, and the constrained
window was corrected locally. The exact genome task remains active with progress renewed; landing
is the only remaining gate. Because `scripts/mesh-restore` and its new fixture changed after the
earlier settle check, rerun the exact scoped MeshLand dry-run after 600 seconds from these edits,
then apply the listed six paths with subject `Allocate the witness pane to show its full 20-task,
20-line frame`; verify `git log -1 --format=%s`, deployed parity for `mesh-dash` and `mesh-restore`,
and the live checker before closing the task.

## Scoped landing and post-deploy verification — 2026-09-14

The six-path `mesh-land --apply` was refused (rc=2): one subject cannot describe six semantic
units. Followed the tool's instruction and landed each source/test unit separately, leaving the
237 unrelated staged paths untouched:

- `2b6a945c` — `Reject witness panes missing the full charter frame` (`mesh-window-check`).
- `3ea48c04` — `Cover the witness pane charter-frame contract` (focused checker fixture).
- `cfded58a` — `Render the complete witness task and chat frame` (`mesh-dash`).
- `89bd9cb2` — `Reserve the full witness frame on available terminals` (`mesh-restore`).
- `0ee2ed1c` — `Cover full witness rendering in short panes` (pane-fit fixture).

Each path-scoped dry-run admitted exactly one settled candidate, and each apply reported it landed
and deployed. Source/deployed parity now holds:

- `mesh-dash`: `78f3dc70887b7cfd153c25d3b7f0cd530a8f79e6b39b6e19602736a2c188db75`.
- `mesh-restore`: `7ef33f41d036ffc0b13821ff55e3b83032d7ae3b15ef2e10c4f05d3ce9d7f47e`.
- `mesh-window-check`: `4b97bfff1674666cea3bbb07987c3fcd6a922033f4f5707c08783aed8a663631`.

At 11:27Z the deployed live checker reported `witness ✓ ok` on the 274x48 data pane. That run
also reported an unrelated `haunt` pane-1 `No such file or directory`; the 11:19Z full run reported
all 16 windows OK. The witness contract itself passes in both live checks. The remaining local
artifact is this updated receipt; land it as one docs-only candidate after its own 600-second
settle interval, then close the structured genome task with the verified commit and deployment
evidence above.
