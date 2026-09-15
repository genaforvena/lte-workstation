# Health doctor aggregate audit: help fallthrough and long run

Task: `health-doctor-aggregate-20260914/audit-help-recursion`  
Checked: 2026-09-14 UTC

## Finding

The current `mesh-doctor` source had no `--help`/`-h` argument branch. An invocation such as
`mesh-doctor --help` therefore fell through to the normal aggregate path; prior health receipts
record that this produced a full scan. This was an accidental CLI fallthrough, not a recursive
self-invocation: a literal-source search found no `mesh-doctor --help` call in `scripts/mesh-doctor`,
and the deployed file matched the source before the fix.

The already-running `mesh-doctor --cron` was still active when inspected, held the doctor lock, and
had not yet emitted its final summary. I did not start a competing aggregate. It completed naturally
by 00:31:43Z; its final line was `2 FAIL, 33 WARN`, with serial-confirm coverage `1/165 assessed`,
`17 FAIL(stale)`, `163 stale-verdict`, and `1 never-assessed`. Thus this observation did not show a
current infinite stall. The run is long (roughly eight to nine minutes), while its logged
serial-confirm phase is explicitly capped at 60 seconds. Existing instrumentation does not identify
which remaining aggregate phase accounts for the whole-run duration, so no more specific timing cause
is claimed. A bounded `strace` attach was attempted but the host denied ptrace; no tracing or process
termination was used.

## Change

Added an early `--help`/`-h` usage path to `scripts/mesh-doctor` and synchronized that exact script to
`~/.local/bin/mesh-doctor`. The previous deployed bytes were backed up at
`~/.mesh/tools-backup/mesh-doctor.pre-help-20260914`. Help now exits before touching the doctor log
or lock.

## Verification

- `tests/test-mesh-doctor-help.sh` failed before the change as expected: `--help` entered the
  aggregate path and hit its 3-second timeout (`rc=124`). The fixture used a temporary HOME.
- The same test passes against both the repository source and deployed `~/.local/bin/mesh-doctor`;
  it asserts usage output, exit 0, and no doctor log/lock creation.
- `bash -n` passes for both copies; `cmp` confirms deployed bytes match the repository source.
- The existing cron aggregate completed with the fresh totals above. No routes, DNS, firewall, VPN,
  or service state changed, and no second aggregate was started.

## Remaining observation

The fresh total still reports two failures and 33 warnings. The health pane's earlier cached totals
are superseded by this completed 00:23Z-stamped cron result. A phase-level timing trace would be the
next diagnostic only if a future run again fails to finish; the safe check is to first inspect the
doctor lock and current `--cron` process, then observe the existing run for a bounded interval rather
than start a second aggregate.
