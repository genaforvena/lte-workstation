# Health-warning triage — witness-task-autonomy

Task: `health-warning/99acb378dd0574bb02cf/triage` (owner `health`).

Live evidence at 2026-09-16T11:54:55Z:

- `mesh-dash --once check` returned immediately and reported
  `PROBE-WARNING: LOCAL LOAD HIGH`, `CPU=MIND-LOAD`, `load1=52.73/16c`, and
  `GPU-IDLE`; this is a local resource warning, not evidence of a substrate
  path failure.
- `mesh-task queue --dispatch --owner health` succeeded and returned this
  task; `mesh-task check dispatch ... health` returned `0` for this task.
- `MESH_TASK_ACTOR=health mesh-task take ... triage` succeeded.
- `timeout 30s mesh-witness-task-autonomy --once` produced no result and its
  shell finalizer was not reached. A surviving child was then observed:
  `mesh-witness-task-autonomy --once`, elapsed `02:36`, CPU `0.0%`, with no
  new `/home/mesh-home/.mesh/witness-task-autonomy.log` row since 11:50:37Z.
- Only that exact orphaned mesh-owned one-shot probe was terminated (TERM,
  then KILL after one second if needed); no protected consumer or substrate
  process was touched. The log remains unchanged at 11:50:37Z.

Disposition: typed machine-owned capability block. Per mesh:2/3/5/8/9,
local-load contention and an unresponsive mesh-owned probe are recoverable
node conditions; no routing, DNS, firewall, VPN, or other substrate mutation
is justified.

Retry edge: after a fresh `mesh-dash --once check` omits
`PROBE-WARNING: LOCAL LOAD HIGH`, run `timeout 30s
mesh-witness-task-autonomy --once`; require a new tape row, reconcile the
named witness/adint task, and then settle this health-warning task.
