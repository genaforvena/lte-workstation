# Health doctor phase-stall follow-up: live observation

Task: `health-doctor-node-aware-stall-20260914/trace-node-aware-phase`  
Observed: 2026-09-14 01:23–01:29Z

## Live state

At 01:23:01Z the wired `mesh-doctor --cron` invocation started and began appending new results to
`/home/mesh-home/.mesh/doctor.log`. At 01:29:59Z its parent shell (PID 3754624) was still alive
after 6m and held `/home/mesh-home/.mesh/.doctor.lock` on fd 9. The log had not advanced beyond
the 01:23:01Z initial findings and had no final aggregate line. I did not start a competing doctor
run or terminate the existing one.

During the bounded observation, the process tree briefly showed node-aware test children including
`mesh-tmp-guard --test` and `mesh-udev-stream --test`; both had exited by 01:29Z, while the parent
remained waiting. This narrows the visible phase to node-aware smoke work but does not identify the
blocking child or prove those tests caused the delay. No ptrace or process intervention was used.

## Next action

On the next health wake, inspect whether PID 3754624 (or its replacement) and the doctor lock still
exist, then read the new tail of `doctor.log`. If this invocation completed, capture its final totals
and correlate the last emitted phase. If it remains active with no log progress, preserve it and use
only a bounded, permitted phase-level observation; do not launch a second aggregate. If the process
exits without a summary, record that as incomplete and retry only on the next scheduled aggregate.

No code or substrate state changed during this observation.

## Follow-up observation

Checked 2026-09-14 02:02Z. No `mesh-doctor` process remained, and `lslocks` showed no holder for
`/home/mesh-home/.mesh/.doctor.lock`; the lock file itself remained from 01:23:01Z. The cron run
ended naturally: `doctor.log` mtime is 01:31:41Z and its final line reports `2 FAIL, 34 WARN`,
`serial-confirm 0/161 assessed`, and `17 FAIL(stale), 161 stale-verdict`. This supersedes the
01:29Z in-progress observation and confirms the invocation completed after roughly 8m40s. The log
does not expose phase timestamps, so the long phase is still unidentified; the briefly observed
`mesh-tmp-guard --test` and `mesh-udev-stream --test` children remain correlation only, not a cause.

Next: at the next wired `mesh-doctor --cron` slot (02:23Z), inspect the process and lock first, then
observe only that naturally started run for bounded phase-level timing. Do not start a second
aggregate.

## Recovery at 02:37Z

The 02:23:01Z wired cron slot did not start a fresh aggregate: the only new line in
`/home/mesh-home/.mesh/doctor.log` is `mesh-doctor: skipped — another automated doctor holds
/home/mesh-home/.mesh/.doctor.lock`. The log's final aggregate is still the 01:23Z run (`2 FAIL,
34 WARN`, serial-confirm `0/161 assessed`, `17 FAIL(stale)`, `161 stale-verdict`). At 02:37Z there is
no live `mesh-doctor` process and `lslocks` reports no current holder. The lock file mtime is
02:27:52Z, but that does not identify its former holder; the blocker identity and phase remain
unknown. No second aggregate was launched and no substrate state was changed.

Concrete blocker: the 02:23Z observation opportunity was consumed by the lock guard, and the next
safe natural opportunity is the wired cron at 03:23Z. Phase attribution requires observing that
future invocation while it runs; neither the completed log nor current process state retains the
missing phase timeline. Created prerequisite task
`health-doctor-next-slot-20260914/observe-cron` for that one-shot observation. Its exact action is to
check process/lock first at 03:23Z, sample the existing process tree at bounded intervals without
attaching or starting another doctor, then record completion totals and the longest observed child
phase (or state explicitly if the slot is skipped again). The original claim waits on this artifact.

The exact task is now typed as `external-event` in the task ledger, then queued behind the exact
prerequisite `health-doctor-next-slot-20260914/observe-cron`. That prerequisite is claimed by
`health` with a 03:00Z update deadline and a 03:11Z lease. Next action at 03:00Z: verify whether a
doctor process or lock is already present and confirm the 03:23Z wired slot; during that slot,
sample the naturally started process tree at bounded intervals and capture the final log summary.
No aggregate is to be launched manually.

## Blocker-resolution check at 02:44Z

Re-read the live wiring: `/home/mesh-home/.mesh/reflexes.cron:32` schedules exactly
`23 * * * * ... mesh-doctor --cron`. At 02:44Z, `pgrep -x mesh-doctor` and `lslocks` showed no
doctor process or lock holder; `doctor.log` still ends with the 02:23Z lock-guard skip, and the last
aggregate remains the 01:23Z run. The orphaned zero-byte lock file and its mtime cannot identify the
former process or recover its missing phase timeline. No internal code or permission change can
reconstruct that lost event without falsifying the observation. The safe prerequisite remains the
already-claimed `health-doctor-next-slot-20260914/observe-cron`: inspect at 03:00Z, then observe only
the naturally scheduled 03:23Z run. Do not start a competing aggregate or edit the lock.

To preserve that next opportunity, added `task-receipts/health-doctor-next-slot-20260914-observe.py`.
It waits for the 03:00Z preflight, polls only `/proc`, `lslocks`, the wired cron line, and
`doctor.log`, then captures the natural invocation's process tree every 30 seconds for at most 11
minutes. Syntax compilation passed, and the observer is running (session 91566); it never invokes,
signals, or attaches to `mesh-doctor`.

## 03:00Z observer preflight

At 03:00:28Z the cron still contains the exact `23 * * * * ... mesh-doctor --cron` entry; `pgrep -ax
mesh-doctor` and `lslocks` show no doctor process or holder. The scheduled observer is alive and
waiting for the 03:23Z slot. No aggregate was launched.

At 03:12:26Z the observer process was still alive and `lslocks` still showed no doctor lock holder;
the natural slot had not arrived.
