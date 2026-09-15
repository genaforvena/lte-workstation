# Decision: minds select work from the ledger

Date: 2026-09-12. Author: witness. Request: evaluate pushing tasks to minds versus
inviting minds to find their own ledger work, and record task-distribution decisions.

**Decision: prefer event-driven invitations followed by mind-selected, atomic claims.**
This is the selected architectural direction from this review, not a deployed scheduler
change. Keep the existing dispatcher until the replacement demonstrates claim safety,
recovery, and useful work under the live wiring. No scheduler, charter, or runtime
configuration was changed by this review.

The invitation should mean: “Eligible work may be available; read your current ledger
view, select a suitable task, and claim it before acting.” It must not start another
paid turn just to discover an unchanged empty queue. A cheap deterministic process
detects relevant work and admits a wake; the mind chooses within its authority.

## Current mesh: already partly pull-based

| Stage | Observed implementation | Consequence |
|---|---|---|
| Intake and authority | `mesh-task` replays structured task records from `chat.log`; journals and JSON are derived. `create` publishes the first step; `done` publishes its successor. | Keep one task identity and one lifecycle. Hledger is an accounting projection, not a second queue. |
| Task selection | `mesh-dispatch` reads `mesh-task queue --dispatch`, then uses `mesh-mind-control` to choose/deliver work. | A task-specific prompt still says “Board task assigned to you.” |
| Independent pickup | `mesh-pane-consume` already asks the receiving mind to query `queue --dispatch --owner <mind>`, check, and take. | The operator's idea already exists for owned work. It excludes unassigned rows. |
| Claims | `mesh-task take` serializes transitions with a local `flock`, assigns an unowned step to the actor, checks exact ownership, dependencies and ordinary one-active-task limits. | There is a usable claim primitive. Unblock resolver chains explicitly bypass the ordinary active-task limit. |
| Delivery | `mesh-mind-control` checks canonical state and uses `mesh-tell --ack`, normally with `--fresh`; pane consumption has its own wake gates. | Delivery, selection and ownership are spread across paths. Delivery acknowledgment is not task acceptance. |
| Completion | `mesh-task done` requires an active owner and an existing file, records its hash, advances the chain and requests landing. | File existence/hash establishes evidence identity, not that the result meets the acceptance criterion. Verification must remain explicit. |

Code reviewed: `scripts/mesh-task` (`take`, `done`, `coordinator_lock`,
`dispatch_queue`); `scripts/mesh_task_log.py` (`eligibility`);
`scripts/mesh-dispatch` (canonical queue, pace gate and dispatch framing);
`scripts/mesh-mind-control` (canonical delivery gate and acknowledged send);
`scripts/mesh-pane-consume` (`wake_msg`, `task_candidate`, `consume_once`).
Source and installed hashes matched for the four executable tools at capture.

The doctrine already says idle agents pull tasks, while later rules describe automatic
allocation. Older dispatch comments/docs say priority/FIFO. Current `dispatch_queue`
uses incident, numeric priority, then **newest first**, following the September 12
operator instruction. Preserve that ordering during migration; do not silently
restore FIFO based on historical prose.

## Evidence and limits

The [captured journal](task-receipts/ledger-pull-coordination-review-20260912/tasks.journal)
reports 907 rows, 108 unfinished: 61 `BLOCKED`, 39 `QUEUED`, 4 `OPEN_UNOWNED`,
3 `HELD_REJECTED`, and 1 `RUNNING`. Its source timestamp is 09:50:19Z;
capture was 09:51:53Z. These are journal categories, **not 108 ready jobs** and
not a census of busy minds. `OPEN_UNOWNED` can still name an assigned owner;
it is not a reliable test for availability to another mind.

The [dispatch tail](task-receipts/ledger-pull-coordination-review-20260912/dispatch.log)
shows repeated busy/unhealthy-owner holds, a later genome delivery, and suppression
of an already dispatched task. The
[pane-consume tail](task-receipts/ledger-pull-coordination-review-20260912/pane-consume.log)
separately records genome waking and other minds held busy. This establishes two
active delivery paths; it does not prove the same task executed twice.

Installed `reflexes.cron` includes dispatch every five minutes and an fsnotify
dispatch trigger, plus journal refresh/watch and unblock sweep backstops.
`restore.env` explicitly sets `MESH_DISPATCH_NO_PACE=1`, documented there as a
temporary operator override; the captured dispatcher logs confirm the bypass was
effective. Pane consumption also bypasses its refractory window for exact-owner
task candidates. Therefore this review cannot credit the current mesh with a
single effective paid-work throttle. The override was observed, not changed.

One concrete predicate discrepancy was reproduced:
[`eligibility(..., dispatch, alpha)` returns 0 for an open step with `waiting_for`](task-receipts/ledger-pull-coordination-review-20260912/eligibility-probe.txt).
The queue and `take` separately reject that dependency. This is a review finding,
not proof of forbidden execution: the final take guard remains. A unified eligible
view must also consider the actor's existing active work, capability, admission,
and any retry holds; today's `check dispatch` alone does not prove all of those.

No comparative throughput or token-cost experiment was run. Lower interruption
and stale-prompt cost are expected benefits, not measured savings.

## Why this direction

| Option | Benefit | Failure mode / decision |
|---|---|---|
| Push a selected task into a mind | Direct routing and urgency are easy to express. | Sender may use stale availability or bind general work to a busy specialist. Keep explicit ownership where it matters. |
| Periodically ask every mind whether it has work | Simple mental model. | Empty paid turns, simultaneous scans and duplicate selection attempts. Reject as the default. |
| Notify an eligible idle mind, let it select and claim | Selection uses current ledger state and the mind's actual context; immutable task details stay external. | Needs unified eligibility, atomic claims and wake deduplication. Choose this approach. |

Pull cannot create missing capacity, unblock external dependencies, or make a
specialist's work safe for arbitrary minds. Most unfinished rows in this snapshot
are blocked or queued; changing the prompt alone will not drain them.

## Task creation and distribution decisions

1. **Record the ask before distributing it.** Store origin/deduplication key,
   intended outcome, next action, expected artifact and acceptance criterion.
   Separate required dependency steps from optional ideas. Explicitly reject an
   unsuitable ask with a reason; never silently lose it or declare age a success.

2. **Separate eligibility from ownership.** Describe required capability, repository,
   permissions, resource constraints and role. General work starts unassigned.
   Set a hard owner only for operator direction, specialist authority, private
   context, an existing commitment, or a contended resource. A suggested role is
   not an exclusive owner. Substrate ownership remains separately coordinated.

3. **Give each mind one suitable view.** Resume its own active task first; otherwise
   expose its owned ready tasks plus compatible unassigned tasks. Exclude other
   owners, unmet dependencies, blocked/terminal work and unavailable capabilities.
   Respect declared `minds:` opt-in. Rank by the current incident/priority/newest
   policy. A mind can decline an unsuitable candidate with a concrete reason;
   selecting a different candidate is not permission to rewrite its priority.

4. **Centralize admission, leave selection to the mind.** A cheap watcher computes
   eligibility and available capacity. It sends a short invitation when eligible
   work appears, an owner becomes free, a prerequisite clears, or recovery makes
   a retry due. Coalesce triggers into one outstanding invitation per mind.
   Keep any candidate ID advisory; re-read the ledger after waking. Empty or
   unreadable queues must produce distinguishable outcomes.

5. **Claim one task transactionally before effects.** Within the authority's lock,
   re-read current state, check eligibility, assign owner and commit the accepted
   claim. A losing claimant does no work. Keep owner-authored acceptance distinct
   from invitation and delivery receipts. Preserve the one-active-task rule;
   resolver exceptions must remain explicit, not become general parallelism.

6. **Keep the authority on one node for now.** The current `flock` protects processes
   sharing this node's ledger/lock, not independent replicated boards. A future
   remote worker must obtain a claim from this authority before acting. During a
   partition it cannot start shared unclaimed work. Do not describe log replication
   or matching local locks as distributed mutual exclusion.

7. **Recover unfinished work without duplicating effects.** Persist progress,
   artifact references and the exact next action. A missed progress deadline
   triggers inspection, not automatic theft or completion. Before transferring
   an active task, establish the former executor is stopped or fence its effects;
   reconcile previously performed external actions. Keep blocked reasons and
   retry events queryable. Release successor work only through the ledger.

8. **Close against the acceptance criterion.** DONE includes result, artifact,
   verification and any landing obligation. Use an independent verifier when the
   task requires one. The witness audits missing intake, unaccepted invitations,
   overdue progress, unresolved blockers and false closure; it should not pick
   every next task for every mind.

9. **Make fairness and cost observable.** Preserve newest-first selection but show
   oldest-ready age and repeated bypasses so starvation is visible. Budget all
   non-operator wakes through one admission path with explicit operator overrides.
   Queue changes caused only by receipts, timestamps or a mind's own idle post
   must not cause another empty turn. Keep the algorithmic recovery cadence across
   restarts and reset context only at the completed-turn boundary.

## Migration and acceptance

Implement in this order, with the current dispatcher retained for rollback:

1. Share one readiness predicate between queue/check/take; add an eligible-for-mind
   view including compatible unassigned work. Preserve current CLI behavior for
   existing callers. Validate rejected dependency, wrong owner, busy owner,
   malformed source and simultaneous unassigned-claim cases.
2. Run a read-only shadow selector against live ledger revisions. Record what it
   would offer and why; compare to existing routing without waking any minds.
3. Canary one opted-in window with invitation-only routing. Disable the competing
   task-push path for that window in the same coordinated change; keep telemetry
   and operator events distinct but deduplicate task invitations at the receiver.
4. Exercise arrival while busy, becoming idle without new arrivals, lost wake,
   crash before/after claim commit, cache loss, prerequisite completion and restart.
   Verify the real watcher process and actual owner-authored claim/result, not
   merely a configured cron line or a successful send.
5. Compare matched workloads: useful completions, eligibility-to-claim and
   claim-to-completion latency, empty paid turns, tokens per verified completion,
   duplicate invitations, competing claims, unaccepted invitations, and oldest
   ready age. Record task mix and budget overrides. Expand only with zero
   cross-owner/dependency violations or duplicate effects, no lost ready work,
   and lower empty-turn cost without worse comparable completion latency.

**Next implementation action:** unify the readiness predicate in
`scripts/mesh_task_log.py` and `scripts/mesh-task`, starting with the reproduced
dependency mismatch and a failing regression test. Full deployment remains future
work; this review does not assert the new distribution mechanism is operational.

## Verification performed for this review

- Read live `mesh-task audit`, journal and board; inspected source paths and wiring.
- Compared installed/source hashes; captured journal and log excerpts with
  [timestamp, hashes and repository revision](task-receipts/ledger-pull-coordination-review-20260912/manifest.txt).
- `python3 tests/test-mesh-task-log.py`: 26 tests passed
  ([output](task-receipts/ledger-pull-coordination-review-20260912/task-log-test.txt)).
- `python3 tests/test-mesh-task-optional-owner.py`: passed owner exclusion,
  optional-owner lifecycle, failed receipt and cache-loss/write-failure recovery
  ([output](task-receipts/ledger-pull-coordination-review-20260912/optional-owner-test.txt)).
- Reproduced the dependency eligibility discrepancy with an isolated in-memory
  record. No test or probe claimed live work on behalf of another mind.

These checks establish existing primitives and the stated finding. They do not
prove a simultaneous cross-process claim race, cross-node safety, or the proposed
scheduler's performance. All unrelated dirty worktree changes were preserved.
