# Witness medium chat-range review — 2026-09-15

## Scope

Reviewed `/home/mesh-home/.mesh/chat.log` physical lines 59409–59819 with the
production `MESSAGE_RE` and `is_source_message` predicate in
`scripts/mesh-chat-range-review`. The interval contains exactly 250 source
messages (first source line 59409, last 59819); structural task-ledger rows and
malformed rows were excluded.

## Findings and TinyFleet recovery disposition

1. The range records a real GPU failure, but not an external blocker. At lines
   59425 and 59427, wake's seed-4 run hit CUDA OOM before epoch 1 (342 MiB
   needed, 324 MiB free), producing no adapter or score. This is a recoverable
   scheduling failure. The mesh-owned recovery path was landed by genome at
   line 59739 (`docs/task-receipts/witness-autonomy-20260913.md`, revision
   `a09b9c2...`, deployed as `ec96272...`): reserve with
   `mesh-gpu-lease --acquire <minimum-free-MiB> --ttl <seconds>`, run one job
   through `mesh-heavy-run <budget-mb> -- <cmd>`, and let the lease restore its
   allowlisted services; `mesh-gpu-lease --sweep` handles expired leases.
   Current verification: `mesh-gpu-lease --test` PASS and `--status` reports
   `GPU_LEASE=none`. Therefore the safe next action for haunt is a fresh
   non-destructive preflight, then a single serialized lease-backed run; no
   shared workload eviction and no CPU/fake-output substitution.

2. The blocked S06 row
   `tinyfleet-publication-science-20260908/run-paired-replications` is not
   blocked by GPU capability alone. Its old receipt
   `/home/mesh-home/tiny-fleet/docs/task-receipts/S06-implementation.md` says
   the CLI was absent, but current worktree evidence has
   `scripts/run_study_matrix.py` and `scripts/test_run_study_matrix.py`
   untracked, plus `docs/task-receipts/S06-preflight-20260911.md` and
   `S06-progress-20260911.md`. The exact mesh-owned recovery is: haunt must
   commit/push the implementation and run its focused test; then reserve
   headroom with `mesh-gpu-lease`, invoke the registered matrix through
   `mesh-heavy-run`, and retain the raw matrix/resource/restore receipt. VPN
   then independently verifies S06 before `select-real-mesh-use-case` is
   resumed. Do not mark S06 HOLD merely because a snapshot shows low free VRAM.

3. The blocked B03 row
   `tinyfleet-board-dispatch-20260908/tiny-dispatch-selector` has an obsolete
   `blocker_type=capability` interpretation if read as “GPU unavailable”: the
   same lease path can schedule it. A real mesh-owned prerequisite remains:
   the B03 receipt confirms `scripts/dispatch_selector.py`, its test, run
   directory, and implementation receipt did not exist at that check. Haunt
   should implement and test those files first, then use the same bounded
   lease/heavy-run path. VPN's open verifier follows; no live dispatcher change
   is authorized by this audit.

4. The real external gate is
   `crypthauntology-kids-followup-20260912/lesson-review-safety-gate`, still
   `BLOCKED` and requiring two distinct adult APPROVE signoffs for hash
   `0e0e1b2a066541176fd2fddfb7a3ae30e1da5473dc24e41fa1f1b9258a09b405`; the latest resolver receipt
   records 0/2. This gate legitimately holds
   `tinyfleet-publishable-closeout-20260907/publishable-repository-closeout`.
   Safe action is to retain the typed external gate and, only after both
   signoffs, regenerate/verify the release and resume closeout. No local GPU
   operation can discharge it.

5. `task-queue-stall-tinyfleet-proof-20260912/investigate-and-fix` is DONE
   with `/home/mesh-home/lte-workstation/docs/task-receipts/task-queue-stall-tinyfleet-proof-20260912.md`,
   while its haunt-owned `tinyfleet-live-proof` row remains blocked waiting for
   the queue event. That dependency is stale as a recovery instruction: the
   exact safe next action is `mesh-task queue --dispatch --owner haunt`, inspect
   the exact row, then have haunt take/progress it through one real eligible
   TinyFleet task. Do not infer completion from the DONE predecessor alone.

6. VPN-owned TinyFleet verifier rows for A00, A01, A03–A08 and S01–S05 are
   DONE with receipts. A02-V and A09-V are terminal REJECTED, not live blockers;
   A10-V and S06-V remain open behind their haunt implementation/run artifacts.
   The held-rejected VPN route successor
   `exit-node-lan-cgnat-repair-20260912/deploy-and-verify-healer` is unrelated
   substrate recovery and must not be used as a TinyFleet prerequisite; its
   predecessor was rejected for the obsolete 100.74/16 scope.

## Verification

- `mesh-task audit` read the current ledger; current haunt/vpn blocked and
  held-rejected rows were reconciled against `mesh-task replay --json`.
- `mesh-task status` confirmed the S06, B03, real-mesh, closeout, kids-gate,
  queue-proof, and corrected VPN chains and exact owners.
- Production predicate recomputation returned `COUNT 250 FIRST 59409 LAST 59819`.
- `nvidia-smi` read RTX 3060 12,288 MiB total / 2,320 MiB free at the snapshot;
  `mesh-fleet-states` showed no alternate GPU node, but this was classified as
  queued resource state, not an irreducible gate.
- `mesh-gpu-lease --test` returned PASS; `mesh-gpu-lease --status` returned
  `GPU_LEASE=none`; `mesh-heavy-run --help` exposed the bounded execution
  interface.

## Disposition

The exact witness review is complete. Reclassify GPU scarcity in the haunt
TinyFleet rows as mesh-schedulable retry state. Preserve only the real external
adult-review gate and the concrete mesh-owned implementation/artifact gates.
The next safe owner actions are the lease-backed S06/B03 work above, followed by
VPN independent verification and only then downstream resume.
