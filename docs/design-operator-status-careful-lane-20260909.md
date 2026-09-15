# Careful/design lane — operator status model

**Decision date:** 2026-09-09 UTC  
**Scope:** important, non-urgent work that needs deliberate design or review  
**Status:** proposed durable contract; it does not itself change task state

## Purpose and boundary

`careful` is a work-class annotation, not a substitute workflow status. It makes deliberate
design/review work visible and protects it from being mistaken for either an incident or casual
conversation. The underlying task still has the ordinary lifecycle (`open`, `claimed`, `blocked`,
`done`) and must retain an owner, a concrete acceptance condition, and a durable artifact when
closed. A careful item is not human-gated merely because it is uncertain or deserves review.

Use this lane when all of the following are true:

1. The outcome matters beyond the current chat turn (a protocol, policy, architecture, safety
   boundary, or other decision that future work will rely on).
2. The work is non-urgent: no live incident, safety regression, or time-critical operator action
   requires incident priority.
3. A premature implementation would create material rework, compatibility risk, or an unsafe
   assumption; a written design/review checkpoint is cheaper than coding first.
4. The question is actionable and can name an owner, a decision boundary, and evidence that would
   make the result acceptable.

Do not use `careful` for an FYI observation, an ordinary implementation task with no design risk,
or an objectively external operator gate. Those remain FYI, ordinary workflow, or a typed
`human-gated` classification respectively.

## Priority ordering

Dispatch ordering is lexicographic:

1. `priority:incident` and other live safety/availability work always wins the next released slot.
2. Within non-incident work, explicit numeric priority is higher first.
3. Within equal priority, older careful work is first (`created_at`, then task ID as a stable tie
   breaker).
4. A careful label never bypasses the spend/pace hold and never outranks an incident by itself.

Recommended numeric bands are 80–89 for important cross-component or safety design, 60–79 for
ordinary architecture/policy review, and below 60 for useful but deferrable polish. The band is a
routing hint, not an acceptance decision.

## Required entry record

Before execution, create a canonical task/chain. The task description or linked design artifact
must state:

- the decision or question and why it matters;
- owner and priority, with `careful` as an explicit tag/class;
- alternatives and the chosen trade-off (including what is intentionally out of scope);
- acceptance/review evidence: artifact path, check/test, reviewer or acceptance role, and the
  condition for closing;
- aging protection: `created_at`, `next_update`/heartbeat expectation, and the escalation path if
  the owner cannot progress.

The claim sequence remains `[task]` → owner-authored `[taking]` → progress/evidence → `[done]`.
No work starts from a `[design]` chat line alone.

## Review and acceptance

The design is reviewable when its artifact lets another mind answer, without private context:

- what problem and non-goals were chosen;
- which current code/state was inspected;
- what alternatives were rejected and why;
- what observable test, command, or artifact distinguishes acceptance from a plausible story;
- what remains unresolved and the exact next action.

Acceptance requires a durable artifact plus the narrowest relevant verification. A reviewer may post
`[chat-review]` with a concrete defect; the owner revises the artifact and records the disposition.
`[done]` cites the artifact and verification, and closes the task only through the canonical task
ID/tag. A design may conclude “reject” or “defer” with evidence; that is a valid result, not a
failed implementation.

## Aging protection

Careful work must not become invisible because it is slow. On claim, record the next update and
keep the task's lease/progress current. If the next update expires, the dispatch/witness sweep
re-surfaces the task as aged; it does not silently convert it to `human-gated` or incident priority.
The owner must then either post evidence and a new next action, block it with a concrete machine or
dependency reason and retry path, or yield/reassign it. A repeated FYI is not progress and cannot
reset the task's acceptance clock without a task-linked progress record.

Suggested review checkpoints: initial framing within one dispatch window, an interim design update
after the first evidence pass, and a final artifact/decision before closure. These are liveness
guards, not fixed deadlines; an explicit dependency may extend them if the dependency and retry are
recorded.

## Relationship to ordinary FYI events

`[fyi]` is an append-only, typed event channel (`observation`, `ack`, `state-change`, `recovery`,
`receipt`, or `warning`), not a task, promise, claim, or completion record. It may provide evidence
to a careful task and may announce that a design artifact exists, but it cannot start, reprioritize,
block, review, or close that task. A task-citing FYI associates only through an explicit `task:`
tag; prose mentions do not create association.

If an FYI observation implies action, emit a separate canonical `[task]` with owner, priority,
acceptance, and (when appropriate) the `careful` class. Use `[design]` for a proposed approach,
`[chat-review]` for a concrete review finding, and `[done]` for the settled result. Repeated FYI is
retained/countable evidence and may trigger escalation only through a new task after its measured
threshold; it is never a hidden careful claim.

## Current-state check and non-regression

At design time, `mesh-task status operator-status-model-20260908` showed the parent chain open with
the audit step done and this design step open. The preceding audit artifact,
`docs/audits/operator-status-model-20260908.md`, establishes that uncertainty/review is not a human
gate and that FYI remains an event. The existing FYI policy,
`docs/superpowers/plans/2026-09-08-fyi-channel-policy.md`, independently requires FYI exclusion from
task lifecycle and promise semantics. This artifact therefore adds the missing careful-lane
contract without changing workflow code, live routing, or historical chat.

