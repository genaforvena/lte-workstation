# Health-warning triage: `health-warning/3df6a8f98b0e495cd109`

- Checked: `2026-09-12T04:41:44Z`
- Owner: `health` on `mesh-home`
- Task: `health-warning/3df6a8f98b0e495cd109/triage`
- Source warning: `2026-09-09T06:15:45Z`, `watchdog@mesh-home` reported
  imac-rozalia chronic suppression for `100.121.88.110 — SSH unreachable`.
  The roll-up records 9 measured recurrences in a 652162s window and two
  suppressed cycles since the last board line.

## Finding

The Mac is reachable now over SSH, but this does not clear its measured
intermittent recurrence. Current Tailscale status lists it active via DERP
relay `hel`; `tailscale ping --c 1` returned a pong in 282ms but exited 1
because a direct connection was not established. TCP/22 accepted a connection
and batch SSH as `ilya` successfully printed `reachable`. Keep the historical
recurrence and suppression counts as the denominator. Current reachability is
recovery evidence, not proof the fault permanently cleared.

## Evidence

- `mesh-dash --once check` — live pane listed `imac-rozalia(NOSSH icmp3.7ms)`.
- `tailscale status | rg 'imac-rozalia|100.121.88.110'` — active via
  DERP relay `hel`.
- `tailscale ping --c 1 100.121.88.110` — pong in 282ms via DERP; exit 1,
  `direct connection not established`.
- `timeout 5 bash -c ':</dev/tcp/100.121.88.110/22'` — exit 0.
- `timeout 8 ssh -o BatchMode=yes -o ConnectTimeout=5 ilya@100.121.88.110
  'printf reachable'` — printed `reachable`, exit 0.

## Disposition

Close this triage as currently reachable over relayed Tailscale, with
intermittent SSH availability and loss of the direct path still visible.
No remote configuration or substrate state was changed.

## Verification

- `mesh-dash --once check` — consumed the live, unfiltered health pane.
- `mesh-task queue --dispatch --owner health` — returned this exact-owner task.
- `mesh-task check dispatch health-warning/3df6a8f98b0e495cd109/triage health`
  — exit 0 before claim.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/3df6a8f98b0e495cd109
  triage` — task status confirmed `[active] owner=health`.
- Tailscale status, ping, TCP/22, and batch SSH probes above — ping used a
  relay and did not establish direct connectivity; TCP and SSH succeeded.
