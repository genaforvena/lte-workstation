# Live version-aware consumer verification — 2026-09-11

## Verdict

REJECTED. Content-SHA stamping works, but process discovery is unsafe and caused live driver loss.

## Reproduction

After landed commits `160517fa` and `2c866b70`, source/deployed parity and both self-tests passed.
An independent `/proc` audit initially saw one current-SHA process per 15 configured channels.
During a later audit, verification command lines themselves contained strings such as
`mesh-pane-consume tg-roz --interval`. The supervisor's unanchored
`pgrep -f "mesh-pane-consume $ch --interval"` admitted those non-driver processes.

At `15:11:54Z`–`15:11:56Z`, `~/.mesh/consume-all.log` records both verifier/decoy PIDs and the real
loaded-SHA PIDs as duplicate respawns for `tg-roz`, `job`, and `haunt`. Immediately afterward,
`mesh-consume-all --status` reported all three `DOWN` despite live two-pane mesh-dash windows.

## Required correction

Discover drivers by exact argv structure from `/proc/<pid>/cmdline` (interpreter, deployed
`mesh-pane-consume` path, exact channel argument, exact `--interval` position), not substring/regex
matching. Add a regression with a decoy command line containing the old substring and prove it is
never returned or killed. Serialize simultaneous supervisor passes with a single-writer lock so two
ensure invocations cannot both observe absence and spawn duplicates. Restore the three down drivers,
then independently prove exactly one current-SHA process per eligible channel and stable PIDs across
an idempotent pass.

