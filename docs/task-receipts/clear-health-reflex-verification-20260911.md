# Clear health reflex verification — 2026-09-11

## Root cause

The new scheduled checker invoked `mesh-clear` by bare name. Cron's non-login environment does not
include `~/.local/bin`, so the real 22:40:01 run recorded `clear-command-missing` even though the
installed command existed at `~/.local/bin/mesh-clear`. The clear implementation itself still
correctly rejected a working Codex pane and left the reactor item pending.

## Change

`scripts/mesh-clear-health` now resolves `~/.local/bin/mesh-clear` by default, records a fresh
`~/.mesh/clear-health.state` heartbeat, validates the handoff-reactor state and freshness, and
checks that the reactor is cron-wired. Its regression test covers OK, clear-test failure, stale
reactor evidence, and a cron-like PATH without `~/.local/bin`.

The node-local desired set and live crontab now contain:

`*/5 * * * * $HOME/.local/bin/mesh-clear-health >> $HOME/.mesh/clear-health.log 2>&1`

## Verification

- `bash tests/test-mesh-clear-health.sh` — PASS.
- `bash -n scripts/mesh-clear-health tests/test-mesh-clear-health.sh` — PASS.
- `mesh-clear --test` and `mesh-handoff-reactor --test` — PASS.
- Source/deployed checker parity — PASS; deployed path is the repository symlink.
- Actual cron dispatch before fix — artifact `~/.mesh/clear-health.log`: `clear-command-missing` at
  22:40:01Z.
- Actual cron dispatch after fix — `~/.mesh/clear-health.state`: `22:45:02Z verdict=OK`.
- `mesh-reflexes --check` confirmed overall cron dispatch and the new reflex's presence; it also
  reported one unrelated pre-existing missing `mesh-load-gate ... mesh-diary` line.

## Remaining obligation

The new reflex is live and green. The unrelated missing desired reflex remains open for its owner;
it is outside this clear repair.
