# Doctor next-slot observer progress

At 03:21:11Z the claimed `health-doctor-next-slot-20260914/observe-cron` task remained active for
`health`, but its structured lease had expired at 03:11:30Z. The exact `23 * * * *` cron entry is
still present. The one-shot observer
[`health-doctor-next-slot-20260914-observe.py`](health-doctor-next-slot-20260914-observe.py) is
running and has a 03:00Z preflight; its 03:12:26Z liveness check passed with no doctor process or
lock holder. No doctor aggregate has been started manually.

Next: capture only the naturally scheduled 03:23Z invocation, then write its final totals and
longest observed child phase (or record the precise lock-guard skip). Inspect the generated
`health-doctor-next-slot-20260914-observation.md` and validate it against `doctor.log` before
settling this task.

## Natural slot live phase at 03:25Z

The wired invocation did start: `doctor.log` gained lines stamped 03:23:01Z and its mtime advanced
to 03:24:03Z. At 03:25:28Z, PID 753706 (`bash ~/.local/bin/mesh-doctor --cron`) was still alive
with elapsed 02:27; a `/proc` ancestry scan found 152 matching `mesh-doctor --cron` processes under
one root. The log tail still had findings but no final aggregate summary. A `/proc/locks` sample
briefly named PID 754052 for `.doctor.lock`, but that PID exited before a follow-up lookup; the
observer continues bounded samples. No attach, signal, or competing aggregate was used.

At 03:29:01Z PID 753706 was still active at elapsed 05:59. `doctor.log` remained unchanged at
03:24:03Z (size 5,564,929 bytes), with no aggregate summary appended. This confirms the natural run
is still in a quiet phase after its initial findings; the exact child phase remains under sample.

## Completed natural observation

The observer finished at 03:32:13Z and wrote
[`health-doctor-next-slot-20260914-observation.md`](health-doctor-next-slot-20260914-observation.md).
The natural run began at 03:23:01Z and ended at 03:32:09Z (9m08s); it completed with
`2 FAIL, 34 WARN`, `serial-confirm 1/166 assessed`, `18 FAIL(stale)`, `164 stale-verdict`, and
`1 never-assessed`. No doctor process or lock holder remained after completion.

The sampled child-work phase was the aggregate's parallel smoke-test/census fanout: the process
tree peaked at 1,171 entries at 03:25:25Z (1,030 non-doctor descendants), with heavy fanout still
visible at 03:24:33Z (917 total). Individual `mesh-restore --test`, `mesh-tmp-guard --test`, and
`mesh-udev-stream --test` children recurred across adjacent samples; `mesh-social-context --test`
was present at 03:29:42Z and 03:30:12Z, then absent by 03:30:42Z. The doctor root remained alive
without sampled children through 03:31:43Z before the final summary. This bounds where time was
spent but does not prove one child caused the full 9m08s; the log has no phase markers. No competing
aggregate, process intervention, or substrate change occurred.
