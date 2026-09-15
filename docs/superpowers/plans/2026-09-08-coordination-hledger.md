# Coordination and useful hledger Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn observed coordination, execution, background delivery, communication and accounting gaps into owned repairs with evidence of recovery.

**Architecture:** Keep chat.log authoritative and materialize task and hledger views from explicit identities. Repair existing lifecycle paths before adding views. Every accounting addition must answer a named operational question and have a consumer, coverage report and independent source reconciliation.

**Tech Stack:** Existing Bash/Python mesh tools, mesh-task, hledger, tmux, cron, append-only board.

## Global Constraints

- This requested deliverable is the plan and registered ledger tasks; implementation completion is a later acceptance gate.
- Preserve unrelated work and historical board records. Correct records through supported task transitions.
- Use bare live window names in mesh-task TSV owner fields; slash-qualified tool/window board conventions are not valid mesh-task owner arguments.
- Each task begins by checking whether its evidence has already been superseded. Reuse existing repair IDs; never redo completed work from a stale summary.
- A timeout means observation unavailable, not process death. Verify PID plus start identity or live session/job handle before restart.
- Substrate edits require the existing single-writer, peer/tmux and mesh-dms protocol.
- Token usage remains observation-only as specified by token-usage-accounting-implementation-20260908. Do not add budget enforcement, routing scores or alerts from token usage.
- USD is imputed value, not cash expenditure. A historical maximum multiplied by 1.2 is not evidence that a cap solves a mesh problem.
- hledger balance alone cannot prove completeness, delivery, task execution or outcome quality.
- Every implementation receipt records source revision, deployed identity, meaningful failure test, actual wiring, live outcome and unresolved coverage.
- Use rtk for shell commands. Read current mesh-task help before changing lifecycle state.

## Evidence and corrections to the previous audit

At the current read, the board ends around 2026-09-08 22:30 UTC.
The previous snapshot is docs/coordination-hledger-live-audit-20260908.md.

1. The queue still contains two parked-autostash repair aliases with owners land and mesh-land/genome. Yet witness-live-unattended-followup-owner-correction2-20260908/repair-parked-autostash-strand is done. This proves inconsistent lifecycle representation, not that the actual stash is repaired.
2. Sound's 22:29:24 completion uses task:min-beats-material-cost. The full sound-experiments-20260908/min-beats-material-cost remains in the dispatch queue. Completion prose and canonical state disagree.
3. witness-mesh-chat-delivery-attempts-correction-20260908/fix-attempts-field is complete. Reverify its deployed behavior; do not recreate that fix.
4. ask-answer-funnel-implementation-20260907 has unit-4 done, unit-5 blocked and final verification open. Determine whether the named dependency is now satisfied.
5. Background manifests currently show 356 delivered, 45 done-nodeliver, 3 crashed, zero running/done-undelivered. This is a census, not proof of recovery across crash or reset. mesh-bg-register stores PPID only; test PID reuse before trusting crash detection.
6. The prior hledger checks show 81 PROMISE, 135 CLAIM, 58 HOLD, 63 ASK and three unrouted promises. TURN journal=5635 versus input tape=6009 is only an upper-bound check: 374 TURN need an explained partition, accounting for feed watermark, retained history and documented corrections.
7. FYI experiment is complete, with 952 events, 34 explicit task tags versus 278 prose mentions. No production FYI materializer was established by that scratch experiment.
8. Correct the previous health count: six OFFLINE nodes plus one SSH-unreachable node = seven, not eight. Egress FAIL is a board-reported condition; the most recent completed doctor evidence was stale, so it is not a fresh verified diagnosis.

## Task 1: Reconcile task identity, routing and closure (witness, priority 95)

**Files:** inspect scripts/mesh-task, scripts/mesh_task_log.py, scripts/mesh-dispatch, scripts/mesh-promises; receipt docs/task-receipts/coordination-hledger-identity-20260908.md.
**Consumes:** canonical replay and existing repair receipts.
**Produces:** per-ID disposition table: canonical ID, aliases, owner, state, evidence, next action.

- [ ] Run `rtk mesh-task replay --json` and `rtk mesh-task queue --dispatch`; freeze the relevant IDs and board cutoff in the receipt.
- [ ] Read the completed owner-correction2 autostash receipt and both remaining aliases. Resolve aliases through supported rejection/supersession transitions with reasons; if repair remains unperformed retain exactly one valid live owner task.
- [ ] Have sound settle the full min-beats-material-cost ID against its receipt after checking acceptance, including the held reflex test. Do not claim completion on the owner's behalf.
- [ ] Resolve the three unrouted promises from the prior snapshot against their original events. Keep offline-dependent obligations visible with a named owner and retry edge; do not discard them because the node is offline.
- [ ] Run `rtk proxy bash tests/test-mesh-task-source-coverage.sh` and `rtk proxy bash tests/test-mesh-task-dispatch-receipt.sh`. Use same-suffix/different-chain fixtures to show that an alias cannot close unrelated work if a parser repair is needed.
- [ ] Compare source replay, queue and promise accounts at one cutoff. Acceptance: no duplicate runnable repair, no silent owner substitution, all retained obligations have a live owner or explicit blocked disposition.

## Task 2: Make long-running completion and recovery verifiable (genome, priority 90)

**Files:** scripts/mesh-bg-register, scripts/mesh-bg-done, scripts/mesh-bg-retry, scripts/mesh-clear, scripts/mesh-task; new tests/test-mesh-bg-lifecycle.sh; receipt docs/task-receipts/coordination-hledger-background-20260908.md.
**Consumes:** existing manifest contract and task progress/next-update fields.
**Produces:** run-to-task correlation, reliable liveness and one durable delivery receipt per completed run.

- [ ] Census current manifests and launchers, distinguishing task-associated runs from anonymous runs and deliberate no-output completion.
- [ ] In an isolated MESH_DIR, exercise a real short-lived child through register, output creation and completion into a local file sink. Exercise owner absence, child death before completion, delivery failure followed by retry, repeated completion and PID reuse.
- [ ] Patch only demonstrated gaps. A reused PID must not make a dead run appear live; an observation timeout must not trigger a second launch. Delivery retry must retain the original run/message identity.
- [ ] Record explicit task ID, run identity, artifact hash and next-update when missing; retain compatibility with historical manifests with an unknown identity verdict.
- [ ] Run `rtk proxy bash tests/test-mesh-bg-lifecycle.sh` plus register/done/retry self-tests. Before running any clear-related test ensure it uses an isolated fixture session, never a live mind.
- [ ] Verify actual launcher calls and retry cron from the current config, then one bounded canary to a local sink. Acceptance: owner absence does not strand completion; one artifact produces one receipt; crashes and no-output are distinct; no test writes human liveness tapes.
- [ ] Price whether a new hledger run commodity adds a decision beyond existing task debt. Prefer explicit task/run tags in existing obligations; create a new view only with a demonstrated unanswered query.

## Task 3: Close communication and ask receipt gaps (tg, priority 85)

**Files:** scripts/mesh-chat-deliver, scripts/mesh-textin, scripts/mesh-task; tests/test-mesh-chat-deliver.sh, tests/test-mesh-chat-deliver-attempts.py; receipt docs/task-receipts/coordination-hledger-communication-20260908.md.
**Consumes:** completed delivery correction and existing ask-answer-funnel chain.
**Produces:** source-message to answer/artifact/board receipt mapping with unresolved cases explicit.

- [ ] Inspect the completed attempts correction and deployed script identity. Run `rtk proxy bash tests/test-mesh-chat-deliver.sh` and `rtk proxy python3 tests/test-mesh-chat-deliver-attempts.py`; inspect test entrypoint first if it requires a runner.
- [ ] Reassess unit-5-canary's stated dependency against unit-4's actual receipt. Resume the existing chain only when that evidence satisfies the dependency; do not create a replacement funnel.
- [ ] Use the existing canary registry, rate ceiling and recognisable test policy. Check exact inbound ID, target owner, processing acknowledgement, answer artifact and delivery receipt. ACK alone cannot settle the operator's question.
- [ ] Exercise unavailable receiver, failed delivery, delayed receiver and duplicate input in fixtures; sample current real receipts without sending unsolicited external messages.
- [ ] Acceptance: all sampled asks have a delivered answer or owned, aged, actionable pending state; exact-ID replay survives reset; terminal delivery failure preserves actual attempt count and failure reason.

## Task 4: Reconcile hledger coverage and task attribution (genome, priority 80)

**Files:** scripts/mesh-labor, scripts/mesh-ledger, scripts/mesh-promises, scripts/mesh-codex-lifecycle; new tests/test-mesh-labor-reconciliation.sh; receipt docs/task-receipts/coordination-hledger-accounting-20260908.md.
**Consumes:** spend.log, journal feed windows/watermarks, explicit task IDs and documented correction entries.
**Produces:** independent source-to-journal reconciliation and task cost coverage with unknowns.

- [ ] Partition the observed 374 TURN difference using a frozen source cutoff: not-yet-fed, pre-retention/pre-inception, documented correction, duplicate and unexplained. Recompute current counts; never force equality by booking historical guesses.
- [ ] Test a missing feed, duplicate feed, overlapping concurrent feeders, and a delayed completion timestamp behind the watermark. A balanced but missing transaction must fail completeness validation or report explicit partial coverage.
- [ ] Add the narrow reconciliation/locking fix warranted by the fixtures. Validate per-window and explicit task-tag totals, not just total journal <= log.
- [ ] Keep branch interval estimates visibly separate from explicit task attribution. Reuse the existing observation-only token recorder, and retain unknown/missing counts.
- [ ] Run `rtk proxy bash tests/test-mesh-labor-reconciliation.sh`, `rtk mesh-labor --check`, `rtk mesh-ledger --check` and `rtk mesh-promises --check`.
- [ ] Acceptance: all differences explained with source evidence or reported as failures; query of one completed and one open task yields attributable TURN plus unknown coverage; removal of a balanced feed is detected.
- [ ] Publish which decision this helps: spotting repeated work, missing completions and unattributed labor. Do not arm the earlier $10039 proposal.

### Operator-requested reconciliation extension

The follow-up chain `coordination-hledger-reconciliation-extension-20260909` makes
the next questions explicit rather than silently expanding Task 4:

- establish a recurring cadence and frozen-cutoff protocol for ledger↔source reconciliation;
- classify and record adjustments with reasons, source evidence and UNKNOWN coverage;
- test whether a synthetic effort commodity answers a useful question that unit counts do not,
  while keeping it separate from cash, quality and routing;
- expose mind/load reports with volume, effort, age, rework, completion and attribution coverage
  as separate axes, then use them to inform (not automatically decide) balancing;
- independently verify missing/delayed/balanced-incomplete feeds and actual cadence wiring.

## Task 5: Give FYI accounting an operational consumer (genome, priority 70)

**Files:** existing docs/superpowers/plans/2026-09-08-fyi-channel-policy.md; create scripts/mesh-fyi-ledger and tests/test-mesh-fyi-ledger.sh; consumer scripts/mesh-dash; receipt docs/task-receipts/coordination-hledger-fyi-20260908.md.
**Consumes:** bounded raw FYI board events and explicit task tags from the completed experiment.
**Produces:** separate FYI journal and witness view answering which recurring events consume communication without an actionable disposition.

- [ ] Implement the already-decided separate FYI view using `events:fyi:<producer> 1 FYI` and `equity:fyi -1 FYI`, with stable event identity, explicit task tags, source cutoff/hash and replay count.
- [ ] Test 952-row baseline where available, quoted task slugs versus explicit tags, malformed input, replay duplication and truncated source. Maintain unknown/partial coverage when input history is incomplete.
- [ ] Add a bounded witness query for producer/event recurrence and explicitly linked tasks. Show one measured recurring owner-absent or path-watch episode and its linked disposition; no automatic task creation from prose.
- [ ] Run `rtk proxy bash tests/test-mesh-fyi-ledger.sh`; require hledger parity, independent count by identity, and unchanged PROMISE/CLAIM/HOLD/ASK balances for FYI-only input.
- [ ] Wire the view through the existing dashboard refresh path, with evidence age and a loud unavailable state. A scratch journal alone is insufficient.
- [ ] Acceptance: a witness can find a repeat without manually rereading hundreds of lines; repeat suppression retains counts; event count does not imply work completion. Defer wider ingress policy to the existing FYI plan rather than imposing an unreviewed grammar here.

## Task 6: Resolve stale health evidence and operational dependencies (health, priority 85)

**Files:** scripts/mesh-doctor, scripts/mesh-health, docs/coordination.md; receipt docs/task-receipts/coordination-hledger-health-20260908.md.
**Consumes:** board egress report, doctor process/lock and exact existing health tasks.
**Produces:** fresh health evidence and a disposition for each dependency affecting coordination.

- [ ] Check actual doctor process and lock owner; a lock file by itself is not proof of life. Poll the existing live invocation; record result or observation unavailable.
- [ ] Run `rtk mesh-health` and inspect the current node card/egress evidence in tmux. Classify six historically offline nodes and the SSH-unreachable node by expected status and active obligations.
- [ ] Reuse current health-warning tasks for recurring incidents. If egress remediation is required, follow the substrate protocol and measure reachability before/after from an independent peer.
- [ ] Acceptance: no stale doctor result is shown as current; offline dependencies have owner/retry/impact; routing findings have a current measured disposition. Never use an unrelated offline phone to declare all task coordination broken.

## Task 7: Prove the full loop and publish acceptance (witness, priority 60)

**Files:** create docs/task-receipts/coordination-hledger-acceptance-20260908.md; inspect all receipts above and scripts/mesh-task-journal.
**Consumes:** tasks 1–6 plus existing operator-status-model-20260908/design-careful-lane and hire idle-edge work.
**Produces:** requirement matrix with source evidence, failure arms, deployed wiring and unresolved obligations.

- [ ] Verify each prior receipt and re-read the live board. Keep existing design-careful-lane and hire idle-edge obligations linked; do not launch duplicates.
- [ ] Use a bounded canary to exercise create, owner take, progress, wait, completion, delivery and successor dispatch. Include a real process handle for wait, not a lease alone.
- [ ] Verify replay from raw chat.log reconstructs all tasks including queued successors. Run `rtk proxy bash tests/test-mesh-task-audit-complete.sh` and the source coverage test.
- [ ] Query obligations, task labor and FYI views at the same cutoff. Require independent source agreement; verify a deliberately corrupted fixture fails.
- [ ] Inspect two scheduled observation cycles and record actual callback/cron receipts. Repeated input must not multiply claims, deliveries or spend records.
- [ ] Publish PASS/FAIL/UNKNOWN separately for coordination, execution, background completion, operator communication, obligation coverage, labor attribution and FYI usefulness. Do not declare global health from narrow tests.

## Ledger registration and handoff

Chain: coordination-hledger-plan-20260908.
TSV: docs/plans/2026-09-08-coordination-hledger.tsv.
The chain deliberately serializes changes to shared coordination writers; existing independently owned tasks continue.
Each owner uses `rtk mesh-task take coordination-hledger-plan-20260908 <step>`, records progress with artifact/next-action/next-update, then uses the matching canonical ID for settlement.
If an existing dependency is still pending, record it with mesh-task wait-for/block and a precise retry edge; do not let generic completion prose advance the chain.

Planning acceptance: all seven steps must be reconstructed from chat.log with valid owners, priorities and this plan pointer; first dispatch must be visible; task summary must include queued successors. Implementation acceptance remains open until Task 7's evidence is complete.
