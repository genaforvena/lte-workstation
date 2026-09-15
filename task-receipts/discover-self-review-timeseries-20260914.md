# Per-mind self-review and routing audit — 2026-09-14

Task: `tg-self-review-timeseries-20260914/design-and-load-audit`

## Finding

The assignment concern is visible in task counts, but the current sample does not establish
unfair routing among interchangeable minds. Over the 24 hours ending 2026-09-14 09:10 UTC,
the canonical replay contained 165 steps queued and 146 completed. Health completed 73/146
(50.0%), genome 18 (12.3%), and haunt 16 (11.0%). Health's volume is concentrated in
health-owned work: 36 warning triages, 11 unblock resolvers, and 18 two-hour observation
analyses. Those are distinct health duties and recurring producers, not evidence that arbitrary
work was steered to health.

| Owner | Queued | Completed | Share of 146 completions |
|---|---:|---:|---:|
| health | 76 | 73 | 50.0% |
| genome | 23 | 18 | 12.3% |
| haunt | 22 | 16 | 11.0% |
| vpn | 11 | 11 | 7.5% |
| adint | 11 | 10 | 6.8% |
| witness | 5 | 5 | 3.4% |
| job | 4 | 4 | 2.7% |
| hire | 3 | 3 | 2.1% |
| senses | 2 | 2 | 1.4% |
| pub | 2 | 2 | 1.4% |
| sound | 2 | 2 | 1.4% |
| all other owners | 4 | 0 | 0.0% |

The all-time mind-load report has 1,230 task steps, but only 316 of 9,892 TURN rows are
task-attributed (3.2%). It reports volume and a small tagged-effort subset, not comparable labor
hours. Completion counts also combine routine generated work, incident response, research, and
implementation. Neither metric should drive reassignment by itself.

## Material price

Before proposing a context-review trigger, I tested whether recent canonical completion records
can support an outcome review. Predicate: each record has a description, start and finish times,
a nonempty result, and an artifact path that currently resolves to a file. All 25 most recent
completed records in the 24-hour sample passed: **25/25 (100%) reviewable for ledger outcome
summaries**. This prices the task-ledger material only. It does not establish that per-mind raw
conversation transcripts are available, complete, or acceptable review inputs; that must be
priced before any transcript-driven wiring.

Replay source: `mesh-task replay --json`, 927 chains / 1,230 steps, SHA-256
`7934bff09a97dc3bcfc2779a69f5c6cf4402aae04d96d64a12722db65da97234`. The sampled time window
was `2026-09-13T09:10:00Z` through `2026-09-14T09:10:00Z`; assignment counts use `queued_at`,
and completion counts require `status=done` plus `finished` in that window.

## Existing mechanisms and overlap

- `scripts/mesh-task` already enforces one active task per owner and emits owner-scoped claimable
  queues. Queue aging is a fairness backstop within a queue; it does not redistribute an
  explicitly owned task.
- `scripts/mesh-dispatch` reads the ledger candidate list, respects owner-direct delivery, and
  makes at most one real mind wake per pass. The producer/owner choice precedes that wake.
- `scripts/mesh-chat-range-review` already reviews board ranges at 50, 250, and 1,000 source
  messages and excludes its own generated task records. `scripts/mesh-chat-review` has a time-plus-
  new-lines throttle for a live review window. These are board/system reviews, not individual
  minds' bounded action-and-outcome reflections.
- `scripts/mesh-mind-state` classifies pane state; it does not review actions. `mesh-mind-stamp`
  is explicitly decayed. `scripts/mesh-hledger-mind-load` is read-only, but the 3.2% effort
  attribution coverage makes its TURN measure unsuitable as a primary balancing signal.

The live audit had three active claims (health, haunt, discover), and the global claimable queue
had seven rows, all currently assigned to genome, operator, phaedra, or steward. The 24-hour
table therefore describes producer-assigned demand, not a central scheduler choosing among all
available minds.

## Proposed policy and cadence

Prefer capability-constrained least-load routing for new **unowned/shared-pool** tasks. First
derive a small, explicit required-capability set from the task's declared type and evidence-backed
capability registry. Filter out minds that lack that capability, are unavailable, or already hold
an active claim. Within the eligible set, minimize active claims plus queued runnable claims;
break ties by longest-waiting eligible task and then least-recent assignment. Preserve task age,
incident priority, dependency/resolver ordering, and exact-owner assignments. Do not infer skill
from task volume or completion count. Use tagged TURN effort only as a reported secondary signal
until attribution coverage is materially higher.

Candidate review trigger: per mind, start a review after **50 new source messages or six elapsed
hours**, whichever comes first, with a one-hour minimum interval between reviews. Bound each input
to the most recent 50 source messages / six hours and at most 20 task transitions. This reuses the
existing near-range size and adds a maximum staleness bound; transcript material must pass its own
sample acceptance test before that trigger is wired. Advance a durable cursor before any review
side effect so a crash cannot duplicate already emitted tasks.

Each review should emit an evidence-linked summary and exactly one of: no action, update an
existing task, or open a new narrowly scoped task. Resolve exact task IDs and active equivalent
work first; exclude the review's own generated records from its next input. Never make the
reviewer reassign another mind's task or change routing/runtime state. Preserve an explicit
no-action result so silence cannot masquerade as a successful review.

## Alternatives

- **Equal round-robin:** easy to count, but can send hardware, privacy, or steward work to an
  unqualified mind and can overload a mind with long-running tasks despite equal task counts.
- **Global task-count balancing:** would react to the measured health concentration, but it
  mistakes required health triage for freely movable demand and treats unlike tasks as equal.
- **Keep producer-fixed ownership:** preserves expertise and authority, but gives no fair choice
  for genuinely shared, unowned work. The capability-constrained rule handles that narrower pool.

## Narrow implementation and evaluation sequence

1. Price the actual per-mind transcript source with the same complete-record predicate; record
   missing/stale rows as unknown and publish its pass rate. If the source fails, use only the
   25/25-supported task-ledger recap, not a transcript claim.
2. Add a read-only shadow report for candidate task capability, eligible minds, active/queued
   load, and chosen owner; do not alter dispatch. Run it for 14 days across at least 100
   unowned tasks and publish capability coverage, concentration within each eligible set, p50/p95
   wait, completion/evidence rates, and override/refusal counts.
3. Adopt only if every routed task has a capability match, p95 wait and evidence-backed completion
   do not regress against the frozen baseline, and same-capability assignment concentration falls.
   Keep exact-owner, incident, resolver, and unavailable-capability cases out of the balancing
   comparison; route exceptions to their existing owner or leave them visibly unassigned.
4. If the shadow report passes, hand the change to the `mesh-task`/dispatch steward for a separate
   implementation task. This audit makes no runtime or wiring changes.

## Verification and limits

- `mesh-task replay --json`: PASS; 927 chain records / 1,230 steps.
- `scripts/mesh-hledger-mind-load --cutoff 2026-09-14T09:10:00Z`: PASS; report produced with
  `task_owner=1230/1230`, `effort_task_attribution=316/9892`, and `outcome_evidence=1010/1028`.
- 25-record material acceptance sample: PASS, 25/25.
- `mesh-task audit` and `mesh-task queue --dispatch`: read-only live snapshots; three active
  claims and seven claimable rows at capture time.

The 24-hour sample is dominated by recurring owner-specific health production. It proves task
count concentration, not that comparable free work is being unfairly distributed. Transcript
availability and task-to-capability matching quality remain unmeasured and are explicit gates in
the proposed sequence.
