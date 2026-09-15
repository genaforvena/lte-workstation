# Health warning triage: witness task audit timeout

At 2026-09-13T22:25:40Z, `mesh-witness-task-autonomy` recorded
`health=FAIL source=PASS ... errors=audit-rc-124`. The row's `unfinished=0`,
`blocked=0`, and `active=0` are empty audit-derived counters: in
`scripts/mesh-witness-task-autonomy`, they remain at their initialization values
when the audit subprocess returns nonzero. They do not describe an empty task
ledger.

The observer's `command()` wrapper uses a 60-second default and converts
`subprocess.TimeoutExpired` to return code 124 with empty stdout and stderr.
`run_once()` invokes `mesh-task audit` through that default. So the evidence
establishes that this audit invocation did not finish inside 60 seconds; it does
not expose how long it ran, partial output, or why it stalled.

The immediately subsequent scheduled observations recovered: 22:30:15Z was
`health=PASS source=PASS`, with 94 unfinished rows and two dispatchable tasks;
22:36:12Z was also PASS, with 95 unfinished and three dispatchable tasks. A
fresh `mesh-task audit` at 22:40 UTC exited 0 in 2.76 seconds. Its output is
captured at `/tmp/health-warning-audit-47efd3a73e356a062d8b.tsv`; the refreshed
`~/.mesh/tasks.journal` reports `task_source=PASS`, 1,159 rows, and 95 unfinished.
No persistent audit or ledger failure reproduced.

Disposition: one transient audit timeout, now recovered. The cause is unknown:
the observer does not preserve timeout duration/partial output, and no
time-aligned load or lock evidence was available for 22:25Z. Treat a future
`audit-rc-124` as a real health warning and correlate it with the audit's runtime,
host load, and task-state input size before changing the 60-second bound. No
mesh behavior or substrate was changed during this triage.
