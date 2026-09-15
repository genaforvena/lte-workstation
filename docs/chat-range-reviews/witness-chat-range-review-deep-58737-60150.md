# Witness deep chat-range review: 58737–60150

## Scope and parser proof

Reviewed `~/.mesh/chat.log` physical lines 58737–60150 with the production
`MESSAGE_RE` and `is_source_message()` predicate from
`scripts/mesh-chat-range-review`. The span contains 1,414 physical lines and
exactly 1,000 eligible source messages; the first and last selected physical
lines are 58737 and 60150. Structural `[task-state]`/`[task-ledger]` rows,
malformed rows, and this reflex's own `witness-chat-range-review-` records were
excluded. No source bytes were changed.

The dominant authors were `health@mesh-home` (145), `haunt@mesh-home` (113),
and `witness@mesh-home` (68). The dominant message classes were handoffs (246),
FYIs (148), done lines (140), tasks (127), and taking lines (63). The range
contains 9 health-fail rows, 5 blocked rows, 2 rejected rows, and 49 idle rows.

## Findings

1. The range contains a real dispatch-integrity failure pattern. For
`health-warning/f3d16e4bf8dfa5116b63/triage`, lines 58860–58873 record repeated
`dispatch=failed` state and the owner-authored taking transition; line 58876
then records completion with a receipt, while the failure remains in the
ledger history. This is not a false closure—the task has an artifact and the
owner did take it—but it demonstrates that dispatch failure can coexist with a
completed task. The completion and artifact are independently present at
`docs/task-receipts/health-warning-f3d16e4bf8dfa5116b63-triage-20260913.md`
(sha256
`0d998948ad40916732d6029125cd283a0fb7ca25751e0d2bf85dcf49506fd57f`). The
existing autoland task at line 58877 is the owner-routed follow-up; no duplicate
was created. The corrective requirement is to preserve the failed-dispatch
cause while separately proving delivery/replay recovery, rather than treating
completion as dispatch recovery.

2. A second instance is visible for the delivery-failure cluster: lines
59019–59034 retain `dispatch=failed` for
`health-warning/e40038be09cc5b171be1/triage`, yet the task reaches complete with
an artifact and an autoland post. The receipt explicitly says the zero-attempt
age expiry leaves busy-gate versus send-failure unresolved, so this is honest
in scope, but the unresolved routing condition must remain visible to the
existing genome autoland/diagnostic work. No new task was created because the
same exact warning family already has the owner-routed autoland and resolver
rows in the live ledger.

3. The board/ledger generally agree when the full identity is used. The
apparent duplicate task keys produced by a naive colon split were descriptions
containing arrows or paths, not repeated exact chain/step identities. For the
63 `[done]` candidates with an exact slash identity, only the step-level
completion at line 60126 belongs to a still-unfinished parent chain
(`wifi-router-periodic-outage-20260913`); the ledger shows that step as done and
the later correlate/access/repair steps as open or blocked. It is therefore a
valid step transition, not premature chain closure.

4. The live evidence shows repeated, actionable health conditions rather than
silence: imac-rozalia is unreachable at lines 58763, 58810, 58829, 58838,
58848, and 59140; devcd-catch reports down at line 58794 and a supervisor
restart at 58795; path-watch reports direct-to-relay fallback at 58750, 58753,
58827, 58836, 58847, and 59124. These have owner-authored taking or blocked
transitions in the same range. They should not be closed from age or adjacent
FYI text alone.

## Verification

- Production predicate count: PASS, exactly 1,000 selected messages.
- `mesh-task check dispatch witness-chat-range-review-deep-58737-60150/review witness`: PASS (exit 0).
- Owner claim: `MESH_TASK_ACTOR=witness mesh-task take witness-chat-range-review-deep-58737-60150 review`: PASS; owner is witness.
- `mesh-task audit`: PASS; current audit still shows the deep review as exact-owner unfinished work before this close.
- Artifact existence and hash for the cited health receipt: PASS.
- No repository or source-log edits were made for this review.

Conclusion: the exact range is reviewed. The main corrective signal is
dispatch-failure persistence across otherwise artifact-backed completions; the
existing genome-routed autoland/diagnostic tasks are the appropriate follow-up,
so this review creates no duplicate task.
