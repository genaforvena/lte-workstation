---
name: mesh-task-recovery
description: Diagnose and recover unattended mesh operator work by joining source asks, canonical task state, dispatch, owner progress, and delivery receipts. Use for forgotten requests or stalled task flow.
---

Read `mesh-task audit`, `mesh-task queue --dispatch`, and the relevant source range in
`~/.mesh/chat.log`. Canonical task-ledger records are authority; JSON caches, a handoff,
dispatch messages, and board `[done]` prose are not substitutes. Retain source line
numbers and timestamps in evidence. Read failures and timeouts mean unknown.

This is an adjustable workflow, not a fixed ritual. Adapt and improve the shared skill
when evidence shows a better procedure; record the reason and verify the change.
Follow the living-skill guidance in mesh-window-turn. Do not weaken authorization,
ownership, privacy, or receipt/verification requirements through a skill edit.

Join each suspected request to its immutable ask key and exact `chain/step`. Distinguish:

- No chain: verify that the ask is actionable and still unmet; create a scoped chain
  with its original source key. Do not resurrect already-delivered work or duplicate
  an existing chain because its wording differs.
- Queued: inspect owner eligibility, live window, dispatch reason and actual scheduler
  wiring. Correct routing or delivery failures; do not equate a queued row with a start.
- Active: inspect last progress, deadline, lease, artifact and current owner activity.
  An elapsed lease alone is not proof of abandonment. Never claim as the old owner.
- Blocked: verify the exact retry event and prerequisite. Internal design choices
  belong to the mesh. Keep real external blockers explicit; do not auto-resume them
  because time passed. Use the existing resolver before creating another.
- Done/rejected: verify the artifact or reason against the original acceptance
  condition. If delivery was requested, inspect the delivery receipt separately.

Repair a demonstrated cause, with a failing regression test for code defects. Existing
task commands enforce transitions and ownership: use them rather than editing chain
JSON, chat.log, or caches. Reassign only through the designated coordinator authority.
Batch evidence and deduplicate corrective tasks so the audit does not become its own
unbounded backlog. Do not change unrelated tasks or send outside the authorized scope.

Report what was measured, what changed, and which exact obligation/event remains.
Verify both executable behavior and its live caller; a self-test does not prove dispatch.
