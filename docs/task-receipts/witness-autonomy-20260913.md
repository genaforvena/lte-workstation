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

- `python3 tests/test-mesh-task-blocked-self-unblock.py` (19 tests, including preserved local cases)
- `python3 tests/test-mesh-witness-task-autonomy.py`
- `python3 tests/test-mesh-gpu-lease.py`
- `scripts/mesh-task --test`
- `scripts/mesh-task-unblock-sweep --test`
- `scripts/mesh-heavy-run --test`
- `scripts/mesh-manifest --check`
- `scripts/mesh-autowire --test`
- `scripts/mesh-autowire --check` (only wire candidate: `mesh-gpu-lease --sweep`)
- Bash syntax checks for the changed shell scripts

Landing and install verification:

- Original source commit `a09b9c2acd674c75dd84b3d45b8f83a5b432acf3` was cherry-picked onto current
  main as `ec96272f055865ffc7c699d2f16bc4df3da950a7` (`Add witness prerequisite and GPU autonomy
  reflexes`) and pushed with `mesh-land --push-heal`. The canonical checkout fast-forwarded to it.
- The root had 1,260 unrelated dirty paths. Only
  `tests/test-mesh-task-blocked-self-unblock.py` overlapped; its original local diff was saved,
  checked on the landed tree, and reapplied without loss. That preserved test diff remains dirty;
  this receipt is also intentionally modified as the task's completion artifact.
- Source/install SHA-256 matched for `mesh-task`, `mesh-task-unblock-sweep`, `mesh-gpu-lease`, and
  `mesh-witness-task-autonomy`. The prior `mesh-task` install was backed up to
  `~/.mesh/tools-backup/mesh-task.pre-witness-autonomy-20260913` before replacement. The sweep,
  `mesh-heavy-run`, and `mesh-study-launch` installs resolve to the canonical source checkout.
- Deployed `mesh-task --test`, `mesh-task-unblock-sweep --test`,
  `mesh-witness-task-autonomy --test`, and `mesh-gpu-lease --test` all passed. The manifest check
  passed with 1,339 complete rows and no duplicate basenames. Python AST and changed shell-script
  syntax checks passed.
- `mesh-autowire --check` reported exactly one wire candidate:
  `* * * * * $HOME/.local/bin/mesh-gpu-lease --sweep >> $HOME/.mesh/gpu-lease.log 2>&1`.
  No unscoped apply was run. The existing 30-minute autowire reflex completed at 15:01:05Z,
  reported `applied 1 new reflex(es) to crontab`, and added the one-minute GPU lease sweep to both
  `~/.mesh/reflexes.cron` and live crontab. A prior five-minute tick, before deployment, logged the
  expected `mesh-witness-task-autonomy: command not found`; the 15:00:15Z tick after install
  reported `RUN health=PASS source=PASS ... checks=1 errors=none` in
  `~/.mesh/task-unblock-sweep.log`, confirming the installed resolver and witness check ran.
- Resource decision for verification: at start, load average was `167.14, 102.84, 61.90` on 16
  CPUs, available memory was 21,246,528 kB, free swap 1,489,916 kB, and the GPU was idle but had
  8,816 MiB of 12,288 MiB in use. Tests therefore ran serially with CPU-only fakes; no GPU service
  was stopped or workload scheduled.

Haunt's comparison remains gated. The resolver recovery created exact-owner prerequisite work, but
no generative registration, behavioral preflight, external-label artifact, or cross-repository
analysis was produced here; do not run the Haunt comparison until those prerequisites are artifact
backed. The separate `autoland/witness-autonomy-followups-20260913/land-followup-autonomy-fixes`
task remains queued to genome after this task settles. Close the claimed
`autoland/witness-autonomy-reflex-20260913/land-and-verify` task against this receipt.
