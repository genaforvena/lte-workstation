# Operator task lifecycle

`mesh-task` is the durable lifecycle for long-running operator work in every lane, including
`adint`, tiny-fleet chains, and `job`. A chain step's canonical identity is `task:<chain>/<step>`;
an operator intake additionally carries one immutable `ask:<key>` supplied at creation.

```text
mesh-task create <chain> <plan.tsv> <ask-key>
MESH_TASK_ACTOR=<exact-owner> mesh-task take <chain> <step>
MESH_TASK_ACTOR=<exact-owner> mesh-task progress <chain> <step> <artifact> <next-action> <next-update-ISO>
MESH_TASK_ACTOR=<exact-owner> mesh-task block <chain> <step> <type> <needs> <retry-edge>
MESH_TASK_ACTOR=<exact-owner> mesh-task resume <chain> <step> <event>
MESH_TASK_ACTOR=<exact-owner> mesh-task done <chain> <step> <artifact> [result]
mesh-task audit
```

The accepted block types are `operator-input`, `external-event`, `dependency`, `capability`, and
`safety`. A block remains open and queryable and cannot be dispatched until an exact-owner resume.
Progress renews the lease and persists artifact, next action, and update deadline in both the chain
and owner context. `audit` distinguishes a live owner's `EXPIRED` lease from an absent owner's
`ABANDONED` lease. Closure requires a file, stores its SHA-256, repeats the task and ask keys on the
board, and is idempotent only for the same path and digest.

Dependency blocks automatically materialize one `unblock/<owner>/<digest>/resolve` task. When its
owner closes that resolver with an artifact-backed result containing the exact tokens
`unblock=cleared event=<edge>`, `mesh-task done` resumes the one matching blocked parent and records
the edge as `resume_event`; this is the recurring lifecycle path, not a witness-only repair. A
resolver result without `unblock=cleared` is terminal evidence that the parent must remain blocked.
The `mesh-task-unblock-sweep` reflex runs every five minutes to backfill missing resolver tasks; it
never impersonates an owner or resumes a parent without the owner's cleared result.

## Work the dependency frontier first

At the start of a turn, read the complete `mesh-task queue --dispatch --owner <owner>` result. It is
a candidate list, not an assignment: choose a runnable task using its context and the work it
unlocks, and check eligibility before taking it. Prefer a runnable resolver or prerequisite before
its dependent work; keep external-event/operator-input rows blocked until their exact condition is
met. Runnable age advances in daily bands by default (the interval is configurable with
`MESH_TASK_QUEUE_AGING_SECONDS`): older bands rank first, then incidents and `unblock/` resolvers,
numeric priority, and FIFO. Redelivery retains the first `queued_at`; a task released from
`waiting_for` starts aging when its prerequisite completes. `mesh-task audit` uses the same ordering
as dispatch. Age is a fairness backstop, not a fixed assignment. If the queue is empty, run
`mesh-task audit` and `mesh-task unblock-sweep`. An owner may use
`mesh-task independent <chain> <step> <reason>` only after attesting that the later step can proceed
without weakening that dependency. Treat age as a fairness signal when choosing, not as a reason to
ignore what a task unblocks.

An open runnable step with no owner is a shared pool item, not an operator assignment request.
Every idle mind can see it in its owner-scoped queue and choose it; the first successful `take`
atomically records that mind as owner, after which the task is reserved. A queue result is therefore
a set of claimable choices. `queued` means runnable work is awaiting a mind, while a successor
behind `waiting_for` or a blocked chain head is not runnable and needs its prerequisite resolved.

Internal design and planning choices belong to the mesh. Choose among alternatives from accepted
task scope, repository evidence, protocol, and runtime constraints; record the rationale and
alternatives in an artifact. Use `operator-input` only for a genuinely external authority or
missing input, not to defer a machine-owned decision.

An expired active lease is not an available queue slot: active claims count toward the configured
owner capacity (`MESH_TASK_MAX_ACTIVE`, default three). Prefer parallel subagents for independent
work within that capacity; never impose a one-active-task rule by habit. At capacity, the exact
owner must settle or renew its current claims by
recording artifact-backed progress with a real update deadline, or by blocking/rejecting it with a
concrete reason. Witness routes and verifies this recovery but never impersonates the owner. Once
capacity becomes available, take the already-routed corrective task; do not create a duplicate. If there
are no runnable candidates and no missing resolvers, preserve the explicit blockers and report the
exact event needed to reopen the frontier instead of manufacturing work.

Case mapping:

- adint device export: block with `operator-input`, name the CSV/path in `needs`, and resume on its
  arrival; never close a missing-input block as done.
- tiny-fleet: the current chain step is the sole task identity; `status` exposes owner, lease,
  blocker/retry, and artifact without reconstructing them from board prose.
- job: create each actionable operator ask with its ask key; progress cites the job artifact, and
  completion requires that artifact before the keyed board close can discharge the ask.
