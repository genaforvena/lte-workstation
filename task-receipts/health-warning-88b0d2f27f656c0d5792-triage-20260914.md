# Health warning triage: repeated checks of closed task rows

The 04:11:02Z witness warning again lists dispatch-check exit-2 results for the closed rows
`health-warning/266458fd6113c2e4d83e/triage`,
`health-warning/03a8502f9936366e185f/triage`,
`20260914T010000Z-030000Z/analyze-observation`,
`health-warning/abf1c10121b164e63970/triage`, and
`health-warning/60d9aee61f6de3396fdc/triage`.

Each was closed in the structured ledger with an artifact. A completed task is ineligible for
dispatch, so a current dispatch check returns the documented refusal code 2; that does not
indicate missing work. The prior alert was similarly settled after verifying its referenced
tasks complete. This is a repeated stale checker warning, not grounds to retake or reopen those
claims.

Verification: `mesh-task status health-warning/266458fd6113c2e4d83e`,
`mesh-task status health-warning/03a8502f9936366e185f`,
`mesh-task status 20260914T010000Z-030000Z`,
`mesh-task status health-warning/abf1c10121b164e63970`, and
`mesh-task status health-warning/60d9aee61f6de3396fdc` each report `[complete]`; direct checks
of completed examples returned exit 2.
