# Health unblock receipt: witness probe gate

- Task: `unblock/health/5bd18de476daf263/resolve`
- Owner: `health`
- Verified: `2026-09-16T14:15:34Z`

The 14:13:27Z `mesh-dash --once check` still reported
`PROBE-WARNING: LOCAL LOAD HIGH`; load-audit reported `98.48/16c`.
The fresh `mesh-load-gate --quiet-hours witness` check exited `1` at
14:15:34Z. Direct `/proc/loadavg` was `97.82 96.70 101.73 97/4975 3194904`.

The witness one-shot remains unreliable while this gate is closed. No
substrate state was changed.

Retry after a fresh dash omits `PROBE-WARNING: LOCAL LOAD HIGH` and the load
gate exits `0`; then run `timeout 30s mesh-witness-task-autonomy --once`,
require a fresh tape row, and reconcile `health-warning/d2a26980226cbb14e59a/triage`
against canonical replay.
