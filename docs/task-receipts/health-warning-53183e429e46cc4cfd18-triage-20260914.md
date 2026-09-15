# Reconcile historical pane and warning-queue gap

At 2026-09-14T19:18Z, triaged
`health-warning/53183e429e46cc4cfd18/triage`, sourced from the 2026-09-12T05:01:55Z
roll-call FYI.

The route marker in the source is retired, as already documented in
`task-receipts/health-warning-3ea960d7c6438f1a59e7-triage-20260912.md`. The
reported pane/queue consumption and warning-dispatch gap is not present in this
pass: `mesh-dash --once check` returned a complete current pane with exit 0;
`mesh-task queue --dispatch --owner health` returned this exact row;
`mesh-task check dispatch health-warning/53183e429e46cc4cfd18/triage health`
returned 0; and owner-authored `mesh-task take` succeeded. This is direct wiring
evidence for pane read, canonical dispatch, eligibility, and owner claim today.

The live pane did surface a separate current observation at 19:18: egress was
`UNATTRIB(hop1-unknown) loss=20%` (35-second sample age), while the 24-hour line
still reports unattributed samples. That is unresolved attribution, not evidence
for changing route or VPN state. Keep it named as a visibility limit; retry on a
fresh sample with a resolved hop or sufficient attribution evidence. The
historical route proposal stays retired and no substrate state changed here.

Result: the old unconsumed-pane/failed-dispatch report is cleared by the observed
current pass; the new egress attribution sample remains explicitly unknown.
