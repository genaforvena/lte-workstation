# Health warning triage: stale doctor observer alert

The 03:21:13Z witness warning reports
`health-doctor-next-slot-20260914/observe-cron` stalled for 2,133 seconds. That exact task is
now done in the structured ledger. It completed the naturally scheduled 03:23Z observation and
points to
[`health-doctor-next-slot-20260914-observation.md`](health-doctor-next-slot-20260914-observation.md).
The report records the doctor run from 03:23:01Z to 03:32:09Z, its 9m08s runtime, the sampled
parallel test/census fanout, and final totals of 2 FAIL / 34 WARN.

This warning was raised before its claimed observer's next scheduled event and became stale
once that task completed. No new prerequisite or competing doctor invocation is needed. The
exact phase remains unproven because the doctor has no phase markers.

Verification: `mesh-task status health-doctor-next-slot-20260914` reports complete with the
observation artifact above.
