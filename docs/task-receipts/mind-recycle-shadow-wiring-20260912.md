# Mind recycler shadow wiring — 2026-09-12

Completed the `design-spec-crash-proof-followup-20260912/verify-and-wire-mind-recycle-shadow`
implementation on `genome`.

`scripts/mesh-mind-recycle --hook` now accepts a Claude Stop event, resolves the board identity from
`MESH_WHO` (falling back to the owning tmux pane), and runs the existing single-window decision
path. That hook entrypoint is pinned to shadow mode even if its environment sets
`MESH_RECYCLE_LIVE=1`; it cannot send `/clear` or inject a continuation. It also ignores malformed,
non-Stop, and re-entrant (`stop_hook_active`) events. The existing board `mesh-stop-check` remains
first in `~/.claude/settings.json`'s Stop hook list.

The deployed `~/.local/bin/mesh-mind-recycle` resolves to the source script. Both have SHA-256
`eb802efeedae83ac9cca51610b4a7bb8c2fa39fab7370f12a59a2b4ccdd1b7e4` after the edit.

Verification performed:

- `bash -n scripts/mesh-mind-recycle` — passed.
- `mesh-mind-recycle --test` — passed, including a Stop-event integration through `--hook`, forced
  shadow mode, re-entrant suppression, and fail-closed unsafe-gate behavior.
- `mesh-clear --test` — passed.
- A temporary fixture with a `done-undelivered` batch drove the real `mesh-clear --gate` through the
  recycler in requested LIVE mode. The gate returned `bg-undelivered`; the recycler returned
  `BLOCK:clear-unsafe` and wrote neither a clear marker nor a would-clear entry.
- `mesh-clear --gate genome` — OK; no live running or undelivered batch.
- `mesh-mind-recycle --status` — header only. No context breadcrumb is fresh enough to name an active
  Claude window, so this node currently has no live shadow verdict to inspect. No live mind was
  cleared or nudged.

The live Claude hook configuration is wired, but a real Claude Stop sample remains unobserved until
an eligible Claude window stops. Live clearing remains disabled. `mesh-wake-expect genome` predicts
the normalized 30-second refresh header, the `WORKING` clear-age row, and the pane live 30-second tick
line as harmless churn.

The source edit and this receipt are ready to land. `~/.mesh/chat.log` has no suggested commit subject
for this task; the only nearby subject belongs to the separate design-audit task, so it is not reused.
