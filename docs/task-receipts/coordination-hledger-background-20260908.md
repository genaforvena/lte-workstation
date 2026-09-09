# coordination-hledger-plan-20260908/background-recovery

Recorded 2026-09-09. The task was live at inspection: canonical chain was
`open`, step 2/7 was `background-recovery`, owner `genome`, with no existing
lifecycle receipt or integration test.

## Repair

Background manifests now record `pid_start_ticks`, the Linux process start
identity paired with `pid`. `mesh-clear` reaps a stale manifest when the
recorded identity is dead or has been replaced, while historical manifests
without the field remain conservatively blocking. `mesh-bg-retry` refuses a
matching live process and retries a dead/replaced identity. Completion remains
terminal and idempotent after delivery.

## Verification artifact

`tests/test-mesh-bg-lifecycle.sh` drives a real detached child and local file
sinks. It verifies one receipt after repeated completion, failed delivery
followed by retry, PID reuse, and that a live matching child is not restarted
when observation is delayed.

Passed:

- `tests/test-mesh-bg-lifecycle.sh`
- `scripts/mesh-bg-register --test`
- `scripts/mesh-bg-done --test`
- `scripts/mesh-bg-retry --test`
- `scripts/mesh-clear --test`
- `bash -n` for all changed shell tools and test
- `git diff --check`

The changed tools are deployed to `~/.local/bin/mesh-bg-register`,
`mesh-bg-retry`, and `mesh-clear` by the landing step. No live mind was
cleared and no external delivery was sent; all delivery assertions used the
isolated local sink.
