# Witness chat review — 2026-09-11 09:37Z

## Finding

The last 800 lines contain a new malformed command variant, `/clearclear`, in
`[mind-wedged]` events at 2026-09-10T22:22:34Z (health). It also occurred in
the wider recent board history for pub, witness, and senses. This is distinct
from the already-completed `chat-review/wedge-monitor-boundary` task: that fix
handles confirmed harness-eaten input, but the malformed duplicate command is
not classified as a safe slash-command recovery.

## Current-code check

`scripts/mesh-mind-state:977-982` extracts the stuck text and uses the exact
case pattern `/clear|/model|"/model "*`. `/clearclear` therefore falls into the
operator-text branch (`_wroute=chat`, recovery gated by
`MESH_WEDGE_RECOVER`), despite being a harness-generated duplicate of `/clear`.
The same event is thus both noisy and less recoverable than the exact command.

## Stale/trace checks

The exact `chat-review/wedge-monitor-boundary/wedge-monitor-boundary` chain is
DONE with artifact `/tmp/wedge-monitor-boundary.keepalive.test` and commit
`eb957216`; no existing task slug names `/clearclear`. The malformed event is
present in `~/.mesh/chat.log`, not merely in `~/.mesh/traces.log`.

## Disposition

Post one narrow review/task pair for the mesh-mind-state owner: canonicalize or
detect repeated harness slash commands before the exact-command case, route the
safe duplicate through the existing trace + auto-recovery path, and add a
regression for `/clearclear` while preserving operator-text safety.
