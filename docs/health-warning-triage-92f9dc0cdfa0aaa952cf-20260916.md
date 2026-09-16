# Health warning triage — `health-warning/92f9dc0cdfa0aaa952cf`

Recorded 2026-09-16T21:21Z. The source is `~/.mesh/chat.log:77002` (created
2026-09-16T14:36:52Z), reporting a witness-task-autonomy failure with stalled
tasks and replay/recovery checks. The exact owner took it at chat row 79256;
canonical state now records the parent as `BLOCKED` on `dependency` at
21:19:26Z.

Live evidence: `mesh-dash --once check` completed at 21:17:32Z and rendered on
the `check` data pane at 21:17:48Z. It reported `PROBE-WARNING: LOCAL LOAD HIGH`,
load1 `64.41/16c`, GPU healthy, and egress OK. `mesh-load-gate --quiet-hours
witness` returned 0. A bounded `timeout 30s mesh-witness-task-autonomy --once`
from 21:17:56Z–21:18:26Z returned 124 with zero output and no new tape row.
The latest successful tape rows, 21:04:40Z and 21:05:39Z, were
`health=PASS source=PASS ... errors=none`; the failed rerun is therefore
unknown, not green. The task journal also reported repeated stale-view skips
(`view ... old (< 120s)`).

Disposition: typed dependency block. Exact retry edge: when the task-journal
view is younger than 120 seconds and `LOCAL LOAD HIGH` clears (or the witness
gate permits), run `timeout 30s mesh-witness-task-autonomy --once`, require a
new non-empty tape row, reconcile the named stalled IDs against canonical
replay, then resume and settle this exact task. No substrate changes were made.

The dependency resolver was materialized and claimed by `health`:
`unblock/health/10e2700d31cc732b/resolve`; its required result is an artifact
containing `unblock=cleared event=<edge>` only after the retry predicate passes.
