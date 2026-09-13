# Witness autonomy and Haunt prerequisite recovery — 2026-09-13

Haunt's `tinyfleet-architecture-drift-review-20260907/run-cross-repository-analysis` was rejected at
13:16:25Z because its behavioral preflight, generative-input registration, and external-label
artifacts were absent. The scheduled blocker reflex did not inspect terminal rejections, so the work
had no owned path to create those prerequisites.

Witness ran the updated sweep against the canonical ledger. It created
`unblock/haunt/bdf0bd563436ad74/resolve`, assigned it to Haunt, and verified the owner-authored
`[taking]` transition at 13:28:41Z. Witness also clarified that registration and execution choices
are mesh-owned and that `mesh-task recover` cannot reopen the rejected step. Haunt must create a
fresh exact-owner comparison task linked to its rejection and gate artifacts once the prerequisites
are satisfied. No comparison ran as part of this recovery dispatch.

The source change adds recent prerequisite-rejection detection and idempotent exact-owner recovery
to `mesh-task unblock-sweep`, which already runs from the five-minute cron reflex. It adds a durable
task-description rule to inspect existing work, create and implement missing mesh-owned
prerequisites, and avoid permission waits. The reflex then runs the witness checks for journal
integrity, queue visibility, exact-owner eligibility, and ownerless self-pick.

GPU jobs opt in to a bounded `mesh-gpu-lease`: it may pause only the three mesh-managed GPU services,
restores their prior active state at job exit or expiry, and queues the job if it cannot establish
the requested headroom. Verification used fakes; live GPU services were not stopped.

Verification passed:

- `python3 tests/test-mesh-task-blocked-self-unblock.py` (12 tests)
- `python3 tests/test-mesh-witness-task-autonomy.py`
- `python3 tests/test-mesh-gpu-lease.py`
- `scripts/mesh-task --test`
- `scripts/mesh-task-unblock-sweep --test`
- `scripts/mesh-heavy-run --test`
- `scripts/mesh-manifest --check`
- `scripts/mesh-autowire --test`
- Bash syntax checks for the changed shell scripts

Remaining delivery obligation: land this isolated branch so the already scheduled reflex runs the
updated source. Then compare installed and source hashes and confirm Haunt's resolver has produced
artifact-backed prerequisite work.
