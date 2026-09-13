# Devcoredump listener repair under supervisor contention

Date: 2026-09-13  
Affected tools: `mesh-supervise`, `mesh-devcd-catch`

## Finding

At 11:37:18Z, the devcoredump sweep called `mesh-supervise`; it returned 0 while the listener was
still absent, and the healer reported `UNREPAIRED` after its five-second wait. The supervisor log
shows the competing calls were skipped at 11:38:01Z and 11:38:02Z, then the active pass restarted
`devcd-catch` at 11:38:03Z. The listener was confirmed up at 11:38:14Z. This ties the repair gap to
`mesh-supervise`'s nonblocking `flock -n` branch: lock contention logged `SKIP` but returned success,
so the caller treated an unrun check as a completed repair attempt.

## Change

`mesh-supervise` now waits up to 65 seconds for the serialization lock. If the lock remains busy,
it returns 75 and writes a `LOCK-TIMEOUT` line instead of a successful skip. The devcoredump healer
passes the same wait bound and permits 75 seconds for the supervisor to finish, then retains its
existing fresh listener PID check before recording repair.

## Verification

- Before the production change, the new lock-contention regression failed: a competing lock owner
  caused no registry reconciliation.
- `bash scripts/mesh-supervise --test` — PASS. It now proves both wait-and-reconcile and bounded,
  loud timeout behavior.
- `bash scripts/mesh-devcd-catch --test-fast` — PASS, including the supervisor wait setting passed
  from the healer in its cron-shaped environment.
- `bash scripts/mesh-devcd-catch --test` — PASS, including the real uevent receive path, event-loop
  action gate, and listener repair/alert outcomes.
- `bash -n scripts/mesh-supervise scripts/mesh-devcd-catch` and `git diff --check` — PASS.

Landed and deployed by path-limited `mesh-land`: `582009b3` (supervisor lock wait) and `2b4c689` (devcoredump healer wait). This receipt is committed separately as the evidence artifact.
