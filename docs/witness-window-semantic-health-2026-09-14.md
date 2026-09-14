# Witness pane semantic health check

Date: 2026-09-14

`mesh-window-check` now validates the visible `witness` pane 0 frame against the current task
journal and board log. It reports an issue unless the same frame contains the unfinished count,
the labelled task-journal source age, up to 20 unfinished task rows, and up to 20 raw unfiltered
board-tail lines. The regression covers a complete frame, short backlogs, and each missing-frame
case.

Verification on mesh-home:

```text
rtk bash -n scripts/mesh-window-check
# exit 0
rtk bash tests/test-mesh-window-check-witness-pane.sh
test-mesh-window-check-witness-pane: PASS (visible witness frame contract and failure diagnostics)
rtk ./scripts/mesh-window-check
witness  ISSUE: witness pane missing labelled source age
```

The live pane is `mesh-home:witness.0`, 80x11. Its captured visible frame contains only recent raw
board lines and the pane-live footer; it does not show the task view or source-age label. The checker
therefore raises the expected issue against the actual pane. This identifies a live layout failure;
the checker change does not resize or rewrite the witness pane.

MeshLand committed and pushed the checker as `7e295125` (`Make mesh-window-check flag incomplete
witness pane views`) and the regression as `365723ee` (`Add regression coverage for witness pane
semantic requirements`). The deployed `~/.local/bin/mesh-window-check` matches the repository source
byte-for-byte. Its live run exits 1 and reports the same expected witness-pane issue shown above.
