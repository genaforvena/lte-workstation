# Witness task and GPU autonomy reflex

## Outcome

Make a recurring witness-side reflex verify that runnable ledger work is actually visible and
claimable to idle minds, and have blocker recovery materialize the next exact prerequisite, including
recent tasks rejected because internal prerequisites were missing. For
bounded GPU tasks on mesh-home, provide a short exclusive resource lease that can pause mesh-managed
GPU services when measured capacity is insufficient, then restore exactly the services that were
active before the task.

## Steps

1. Add focused tests for GPU lease acquisition, selective quiescing, rollback, expiry, and restore.
2. Implement a node-local lease with a bounded dead-man expiry; only touch the allowlisted mesh GPU
   services and preserve prior active state.
3. Integrate opt-in lease use into the existing heavy-job admission/queue path so deferred jobs can
   obtain declared headroom, run within their existing budget, and restore services on completion.
4. Add witness task-ledger checks after the scheduled unblock sweep: rebuild the journal, audit the
   source, inspect global and exact-owner queues, and verify ownerless runnable work is visible to
   idle minds and passes `check dispatch`.
5. Wire the checks through the already scheduled unblock reflex; document the changed resource
   policy and add regression tests for idempotent rejection recovery and the full reflex contract.
6. Verify source behavior, scheduler wiring, live task observations, and deployed source parity after
   the isolated branch is landed.

## Boundaries

Keep task priority and scope mind-selected. Make protocol registration and execution decisions from
mesh evidence without permission waits. If a required external datum cannot be sourced or honestly
substituted, leave an exact retryable blocker while completing independent internal prerequisites.
GPU preemption is limited to mesh-owned allowlisted services, uses a declared threshold and deadline,
and must restore prior active state on normal completion or sweep expiry. If freeing those services
does not establish headroom, restore immediately and keep the task queued.
