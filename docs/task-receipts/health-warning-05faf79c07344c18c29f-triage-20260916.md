# Health-warning triage — witness-task-autonomy

Observed warning: the 2026-09-16T11:45:32Z health alert reported
`witness-task-autonomy` with `unfinished=265 blocked=170 idle_minds=11
dispatchable=28 unroutable=5 ownerless=0 ownerless_visible=0 active=8
active_recovery_wakes=1 dispatch_repairs=0 checks=28` and the error
`active-task-stalled-unblock/adint/4ef95f55b009fc35/resolve-for-1806s`.

Owner transition: `mesh-task check dispatch health-warning/05faf79c07344c18c29f/triage health`
was retried and the exact-owner claim succeeded:
`MESH_TASK_ACTOR=health mesh-task take health-warning/05faf79c07344c18c29f triage`.

Fresh evidence at 2026-09-16T11:50:20Z:

- `mesh-health` reports this node PASS and Redmi 10 PASS; ilya, both imozerov
  nodes, and rip are OFFLINE; GL-MT3000 is LAN-reachable.
- `timeout 20s mesh-witness-task-autonomy --once` returned `rc=124`.
- `/home/mesh-home/.mesh/witness-task-autonomy.log` had no new row; its latest
  row remained the 2026-09-16T11:40:39Z FAIL for the same active-stall family.
- `mesh-dash --once check` reported `PROBE-WARNING: LOCAL LOAD HIGH` and
  `load1=52.71/16c`; therefore fleet non-answers and the witness timeout are
  not evidence that a substrate path is down.

Disposition: typed external-event block. No routing, DNS, firewall, VPN, or
other substrate mutation is justified while the local-load warning persists.

Retry edge: after a fresh `mesh-dash --once check` omits `PROBE-WARNING: LOCAL
LOAD HIGH`, run `timeout 30s mesh-witness-task-autonomy --once`; require a new
tape row, then reconcile the named active task and settle this health warning.
