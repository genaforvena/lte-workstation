# Unblock job hh harvest — 2026-09-16

- Task: `unblock/job/d4be42ef25b81752/resolve`
- Original blocker: shared `~/.mesh/job/.apply.lock` was recorded as held by a reply/confirm writer.
- Diagnosis: `job/mesh_job_hh_lock.py:lock_holder()` returned `NO_FLOCK_HOLDER`; the marker was stale history, not a live flock. The named writer PIDs were no longer running.
- Safe action: did not delete or rewrite the marker and did not kill any process. Re-ran the original Note 3-backed command only after the kernel lock probe was free: `job/mesh-job-apply --reopen --harvest --json` (started `2026-09-16T10:49:28Z`, completed before `10:51:38Z`).
- Verification: X5 Tech (`form`) and БУРГЕР КИНГ РОССИЯ (`questions`) remain `needs-human`; no unauthorized answer or application was sent. The blocker is discharged, but the original harvest acceptance is still incomplete.
- Next edge: resume `job-goal-needs-human-harvest-20260916/.../harvest-current-hh-forms` and inspect why these two rows were not harvested; do not reintroduce a competing writer.
