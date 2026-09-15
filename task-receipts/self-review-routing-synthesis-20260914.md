# Self-review and shared-task routing synthesis — 2026-09-14

Task: `tg-self-review-timeseries-20260914/synthesize-routing-design`

## Decision

Run two read-only shadow experiments before changing any mind-review cadence or task assignment:

1. A per-mind, bounded self-review of canonical task outcomes and timestamped board activity, with a six-hour maximum interval and an earlier trigger after 50 new source messages. Keep at least one hour between reviews. Each review emits an evidence-linked no-action, update, or narrowly scoped task recommendation.
2. A capability-constrained load recommendation for genuinely shared, unowned tasks. Preserve exact-owner assignments and all existing incident, dependency, resolver, and priority behavior. Do not move any task during the shadow period.

The current evidence supports testing those proposals, not adopting either as a runtime policy. The review-input price is 25/25 (100%) for the most recent canonical completion records tested in the predecessor audit. That predicate establishes ledger-outcome-summary coverage only; per-mind transcript completeness and acceptability remain unpriced. The first experiment can therefore use ledger and board evidence without reading raw conversations.

## Evidence from the three predecessor artifacts

| Source | Measured evidence | Routing/review implication |
|---|---|---|
| `task-receipts/discover-self-review-timeseries-20260914.md` | In the 24 hours ending 09:10Z, 165 steps were queued and 146 completed. Health completed 73/146 (50%), including 36 warning triages, 11 unblock resolvers, and 18 observation analyses. Of the 25 most recent completion records tested, 25 (100%) had description, start/finish, result, and a resolvable artifact. Only 316/9,892 TURN rows (3.2%) were task-attributed. At the live capture there were three active claims and seven claimable rows, with assignments already producer/owner-directed. | Completion concentration is not evidence of unfair assignment among interchangeable tasks. Ledger outcomes are currently reviewable; TURN effort and raw transcripts are not sound primary inputs. |
| `task-receipts/senses-self-state-timeseries-20260914.md` | The 24-hour board sample had 124 Senses-authored tagged records; 58 handoffs plus 28 idle lines were 86/124 (69%). Canonical replay showed 2 queued and 2 completed Senses steps. Reported reach changed from 3/11 to 4/11, then remained 4/11 in the sampled frames, while several phone reads and routing-dependent checks remained unavailable. | Raw message count overweights status churn. A review must exclude routine status-only traffic as an early trigger and preserve unknown/stale sensor state. Event-gated review is more useful than message volume alone. |
| `task-receipts/health-self-state-timeseries-20260914.md` | Health recorded 89 queue events and 97 completions over its interval; completions included 53 warning triages, 17 unblock resolvers, and 17 observation analyses. Repeated blocked resolver attempts did not improve evidence until the external reachability condition changed; a later probe warning made the path unreliable again. | Health's high task share reflects distinct owner-specific duties. Reviews should compare task state and retry conditions, avoid time-only duplicate work, and keep blocked work gated on its recorded event. |

These are adjacent but not perfectly synchronized samples, and queue/completion counts are event totals rather than matched cohorts or labor hours. No predecessor measures the volume or outcomes of a capability-matched shared-task pool. The evidence does not establish that load balancing would have changed any assignment.

## Proposed self-review protocol

- Trigger a review after six elapsed hours or 50 new source messages, whichever comes first, subject to a one-hour minimum interval. Review at most the latest 50 source messages from the latest six hours and 20 canonical task transitions. If neither messages nor task state changed, record a bounded no-action result rather than manufacture a task.
- For the first implementation, use canonical task transitions, retained task receipts, and timestamped board lines. Exclude the review's own output and routine `[handoff]`/`[idle]` churn from early triggers. Treat stale, absent, or unreachable measurements as unknown, never as zero or recovered.
- Before any side effect, persist the source cursor and exact task IDs examined. Resolve an existing task or equivalent active work before recommending an update or new task. Emit exactly one of: evidence-linked no-action, update to an existing task, or a narrowly scoped new task. A review may not reassign another mind's task or change substrate/routing state.
- Before any later transcript-driven implementation, price a stratified sample of 25 latest candidate records across available mind windows using the predecessor's complete-record predicate plus stable source identity, timestamps, and retrievable content. Publish pass rate and missing/stale counts. Until that price is published, raw transcripts are out of scope.

This is a proposed shadow discipline, not a production cadence. The predecessor's proposed six-hour/50-message bounds are supported by the 69% Senses status-only share and by the already existing 50-source-message board-review scale; Health's two-hour observation stream is a separate health duty and should not be imposed on every mind.

## Proposed shared-task routing rule

For each new task explicitly identified as shared and unowned:

1. Derive required capabilities from the task description/type and a capability registry backed by current charters or verified artifacts. Record `unknown` when the match cannot be established; do not infer skill from historical task counts.
2. Exclude minds that lack a required capability, are unavailable, already hold an active claim, or are protected by their charter. If no eligible mind remains, leave the task visibly unassigned or use its established steward path.
3. Among eligible minds, choose the one with the fewest active plus queued runnable claims. Break ties by the longest-waiting eligible task, then least-recent assignment. Preserve task age and priority.
4. Keep exact-owner work, incidents, dependency/resolver steps, and tasks with unavailable capability evidence outside the balancing pool. Do not reassign work already owned or claimed.

This policy addresses only the opportunity the measurements leave open: shared work for which more than one qualified mind is eligible. Equal round-robin risks sending work to an unqualified mind; global task-count balancing would misread Health's owner-specific production; keeping producer-fixed ownership everywhere leaves the shared pool unbalanced. The capability filter plus least-load choice avoids those failure modes without overriding current ownership.

## Evaluation plan and decision gates

### Self-review shadow

Run read-only for 14 days. Freeze the starting cursor, eligible source definitions, and six-hour/50-message/20-transition bounds before the first report. Record, per mind and review, source counts, task IDs, source/artifact coverage, proposed disposition, duplicate-task matches, and reviewer time/cost. Do not read or infer private conversation content. At day 14, report trigger count, duplicate recommendations prevented, actionable/no-action split, missing evidence, and whether any review made an unsupported claim. Any unsupported claim or duplicate task creation is a fail requiring redesign; missing source data remains `unknown` and does not count as a clean review.

### Routing shadow

Freeze a per-task baseline from dispatch/ledger records before the shadow starts. Pair each actual assignment with a shadow recommendation using only the capabilities and load visible at that task's queue time. Run for 14 days and at least 100 shared, unowned tasks; stop at 30 days if fewer than 100 accrue and report the trial as inconclusive. Exact-owner, incident, resolver/dependency, unavailable-capability, and human/operator tasks are excluded and counted separately.

Report capability-match coverage, eligible-set sizes, recommendation/actual-owner disagreement, override/refusal and unassigned rates, same-capability owner concentration, and p50/p95 queue-to-start time. Use evidence-backed completion (a done result plus retrievable artifact) as the outcome measure. Compare like-for-like tasks within the same eligible capability set; do not compare raw per-mind completion totals.

The shadow passes only if every recommendation has a verified capability match, there are zero recommendations for protected/exact-owner work, p95 wait and evidence-backed completion do not regress against the frozen baseline, and maximum owner share within comparable eligible sets falls by at least 20% relative to baseline. The 20% concentration threshold is a predeclared material-effect bar, not a value inferred from the current unequal-duty counts. A pass authorizes a separate review and implementation proposal; it does not itself change production routing. A failure or underpowered sample retains current routing and records the evidence.

No model training or randomized treatment is required: model revision, seed, train/test split, CV folds, and training hyperparameters are not applicable. The shadow is paired, read-only evaluation over live task events; the arm order is actual dispatch first, shadow scoring second, so no recommendation can affect the observed assignment. Stop at 14 days and 100 eligible tasks, or at 30 days if the minimum sample is not reached. CPU-only read-only processing is sufficient; no GPU or separate node reservation is needed.

## Exact follow-up work

1. `genome`: pre-file audit `scripts/`, `docs/`, and the task ledger for an existing per-mind review source/runner; price the stratified 25-record transcript sample if a transcript path is proposed; publish an acceptance artifact before any transcript-based wiring.
2. `genome`: implement a read-only self-review shadow report over canonical task transitions and retained artifacts with durable cursors, exact-task deduplication, explicit no-action output, the frozen bounds above, and a separate non-liveness log. No runtime trigger or dispatch side effect in this task.
3. `genome`: implement read-only paired routing-shadow scoring for shared/unowned task candidates, including the capability evidence, queue-time active/queued load, exclusions, baseline, and evaluation metrics above. Leave production owner selection unchanged.
4. `witness`: independently audit both shadow artifacts and the day-14 comparison against the frozen definitions and gates; publish pass/fail/inconclusive with raw source paths. Only after that review should the steward decide whether to file a separate production-change task.

## Verification and limits

- Read and compared all three predecessor receipts named in the task.
- Rechecked the task chain: the three predecessor steps are `done`; this synthesis step is active under `discover`.
- The predecessor discover audit reports successful `mesh-task replay --json`, load report, and 25/25 ledger-record acceptance sample. I did not rerun those analyses; this artifact synthesizes their retained evidence.
- No repository runtime code, dispatch policy, or substrate state was changed.
- Unresolved: transcript source acceptance; quality/completeness of the capability registry; number of future shared unowned tasks; matched wait/outcome baseline; whether reducing within-pool concentration improves outcomes. These are gates for the listed shadow work, not assumptions treated as findings.
