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

Case mapping:

- adint device export: block with `operator-input`, name the CSV/path in `needs`, and resume on its
  arrival; never close a missing-input block as done.
- tiny-fleet: the current chain step is the sole task identity; `status` exposes owner, lease,
  blocker/retry, and artifact without reconstructing them from board prose.
- job: create each actionable operator ask with its ask key; progress cites the job artifact, and
  completion requires that artifact before the keyed board close can discharge the ask.
