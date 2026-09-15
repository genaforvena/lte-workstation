# Health warning triage: transient witness check/claim race (2d6d67b7)

Task: `health-warning/2d6d67b747b91d76922f/triage`  
Observed warning: 2026-09-14T10:35:51Z, `mesh-witness-task-autono@mesh-home`.

The witness run is timestamped 10:35:11Z and reports `source=PASS`; its later health-fail line
lists three exact-owner dispatch checks that returned 2. At 10:35:37Z, while that sweep was still
in flight, Health took `health-warning/b40e31295391fe0a6101/triage`. The three refused rows were
also Health-owned. `mesh-task check dispatch` enforces one active task per exact owner, so a
queue captured before that take can become stale by the time its individual checks run. This
timing explains the refusal without implying that any of the rows was ownerless or absent.

The named warning rows `4db9ccd9…` and `c4bfa4a0…` were later closed with receipts, and the
observation row was completed as
[`health-observation-analysis-20260914T080000Z-100000Z.md`](health-observation-analysis-20260914T080000Z-100000Z.md).
The witness tape then records PASS at 10:35:52Z, 10:40:24Z, and 10:45:13Z, each with
`source=PASS` and `errors=none`. This was transient; no persistent task-dispatch failure remains.

Disposition: close as a check/claim timing race during Health's active task transition. No code
change is justified by this single occurrence. If it recurs, compare the queue-snapshot time to
the exact owner's take/complete receipts before classifying the refusal; investigate a code path
only if a fresh rc=2 remains after the queue and ledger are settled and the owner has no active
task.

Evidence: `/home/mesh-home/.mesh/chat.log` (10:35:51Z failure, 10:35:37Z Health take, later
task completions), `/home/mesh-home/.mesh/witness-task-autonomy.log` (later PASS rows),
`scripts/mesh-task` (`check_eligibility`), and the cited triage/analysis receipts.
