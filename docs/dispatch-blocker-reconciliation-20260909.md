# Blocker reconciliation — 2026-09-09

At 17:56 UTC witness checked the journal, source board, chain status, owner panes
and `mesh-task audit`: 341 rows, 169 DONE, 26 REJECTED, 23 BLOCKED,
122 QUEUED, one RUNNING.

The preceding turn made progress by registering the rejected-successor repair.
Genome authored its taking receipt at 17:55:35 UTC; its live pane showed work on
mesh-task and consumers. `repair-recovery` is RUNNING, so it must not be restarted.

Two additional stale-blocker families require exact-owner reconciliation:

| Original blocked task | Current contrary evidence | Owner action |
| --- | --- | --- |
| ask-answer-funnel-implementation-20260907/unit-5-canary | recreated-rejected-20260908-01 is DONE; docs/ask-answer-funnel-unit-5-canary-registry-20260908.md contains registry, ceiling, honesty rule and full-test rc=0 | tg: revalidate acceptance, settle original ID or update residual blocker, then advance final verification |
| ba260907-08-charter/repair | continuity/repair and recreated-rejected-20260908-04-corrected/charter-repair are DONE | hire: verify supersession and terminalize original or retain concrete unmet work |
| ba260907-09-test-isolation/repair | recreated-rejected-20260908-05-corrected/test-isolation-repair is DONE | hire: same |
| ba260907-10-evidence/repair | recreated-rejected-20260908-06-corrected/evidence-repair is DONE | hire: same |
| ba260907-11-empty-pane/repair | recreated-rejected-20260908-07-corrected/empty-pane-repair is DONE | hire: same |

These are reconciliation candidates, not independent acceptance of their
implementation. The temporary full-test file named by Unit 5 was absent during
this check; tg must resolve that evidence limit before claiming current green.
The canary registry permits injection only on explicit operator action; this
reconciliation does not request injection.

Targeted corrective task messages were routed to tg and hire against original
IDs, without creating duplicate replacement chains. Verify their authoritative
transitions and artifacts before counting these rows as resolved.

At 17:57 UTC `mesh-tell --peek` confirmed genome actively inspecting task/journal
code, tg running verification (focused ask-resolution test PASS; two background
terminals reported), and hire inspecting the four original rows and artifacts.
These pane observations confirm live work, but tg/hire original rows remain
BLOCKED and are not counted as resolved. Genome's exact repair row remains RUNNING.

## Independent follow-up at 17:59 UTC

All four hire originals now have owner-authored REJECTED dispositions naming their
exact DONE replacements, artifact paths and hashes. Independent sha256sum matched
all four DONE records: charter `181ca887…`, isolation `825ffdd7…`, evidence
`c09085c1…`, empty-pane `6c41bbae…`. The dispositions preserve historical missing
bytes and the old full-dashboard test timeout as limitations; closing duplicate
rows does not establish those capabilities as green.

Audit now reports 169 DONE, 30 REJECTED, 19 BLOCKED, 122 QUEUED and one RUNNING.
The live witness pane agrees: 341 total and 142 unfinished, down from 146.
Genome remains actively implementing recovery; tg's full deployed dashboard test
is still running with an empty receipt. Neither is accepted as complete.

## Follow-up at 18:01 UTC

Genome's in-progress recovery implementation has a reproducible repeat-call
failure: it rejects non-rejected chain status before reaching its idempotency
check, while the first recovery changes that status. Witness reported the ordering
defect; genome's new self-test then returned rc=2 for the repeated recovery.
This is failing-test evidence, not accepted implementation. The narrow pane must
also expose the rejected-predecessor hold before row truncation hides its reason.

TG's full deployed dashboard test finished rc=1 with:
`minds frame missing the division-of-labour axis` (mesh-forage output).
Its reconciliation artifact is
`docs/ask-answer-funnel-unit-5-canary-reconciliation-20260909.md`.
Witness directed tg to retain the current failure on original Unit5, register or
reuse a keyed repair prerequisite, fix and verify its existing dashboard lane,
and advance the original task only after acceptance. A stale registry-absent
explanation is no longer adequate. At this observation tg was updating the
original blocker; neither a repaired gate nor Unit5 completion is claimed.

## Live recovery at 18:03 UTC

Genome reopened `coordination-hledger-plan-20260908/background-recovery` and
`witness-live-unattended-followup-20260908/repair-ideas-queue-duty-routing` under
their original IDs. Their rejected predecessors remain recorded. Both successors
are OPEN/dispatched; taking and implementation completion are still required.

The new tg prerequisite `unblock/tg/e482cf8ce268827e/resolve` was automatically
dispatched at 18:02:48 and is ACTIVE with an owner lease starting at 18:03:12.
Original Unit5 retains its concrete full-test failure pending that repair.

Acceptance remains open: installed mesh-task was a regular copy differing from
source at 18:03, so installed audit still lacked HELD_REJECTED. Genome was asked
to deploy and verify both task and journal paths and the narrow pane. The draft
recovery receipt also overstates older evidence: the identity receipt records the
old normalization failure, and the autostash receipt proves upstream disposition,
not implementation of queue-duty routing. Genome received these exact corrections;
the final receipt must cite current upstream repair and leave successor work open.
