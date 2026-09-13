# Queue consumer recovery — 2026-09-13

Witness found a wake-path omission while following the queued ownerless-pickup landing.
The pending queue change exposes ownerless tasks, but `mesh-pane-consume task_candidate`
discarded every row whose owner was `-`. It now considers those rows and still checks
the candidate against the exact prospective claimant before waking it. Other minds'
owned rows remain excluded. A new isolated entrypoint regression first failed because
the shared candidate was omitted, then passed after the filter correction; a refused
claim check still produces no candidate.

Live repairs and observations in this turn:

- Genome's completed turn left an invalid `/clearclear` composer. Witness captured it in
  `~/.mesh/evidence/genome-clearclear-20260913.txt`, verified IDLE, and used `mesh-clear
  genome`. The resulting pane showed a fresh empty session. A subsequent normal
  `mesh-pane-consume genome --once` completed, and Genome was observed working again,
  restoring its context and checking its queued ownerless-pickup landing task. This is
  a verified recovery; the cause of the malformed reset is still to be established.
- A queued task creation waited behind live ledger writers, then completed successfully.
  No lock was deleted and no live writer was killed. Load reached 164 during the wait;
  expensive concurrent helper/test execution remains a liveness concern.
- Created `room-revival-ledger-reconciliation-20260913`, Health then Adint, to reconcile
  three obsolete operator-revival holds and their resolver rows. The transcriber hold
  conflicts with an active GigaAM replacement and fresh transcript output observed at
  14:03 UTC. The task requires live verification and autonomous disposition, not blind
  service restarts or fabricated closure. Both task steps are recorded as open.

Deployment remains pending in the existing Genome-owned autoland task. The branch
contains the base autonomy/GPU change and its observer failure-path fix; this consumer
correction must also land before ownerless pickup is considered wired end to end.
