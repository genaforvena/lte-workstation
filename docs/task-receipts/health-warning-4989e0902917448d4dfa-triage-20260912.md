# Health-warning triage: `health-warning/4989e0902917448d4dfa`

- Checked: `2026-09-12T04:38Z`
- Owner: `health` on `mesh-home`
- Task: `health-warning/4989e0902917448d4dfa/triage`
- Source warning: `2026-09-09T06:21:54Z`, `watchdog@phaedra` reported an
  imac-rozalia chronic-suppression roll-up for `100.121.88.110 — SSH unreachable`.
  The roll-up records 14 measured recurrences in a 351600s window and two
  suppressed cycles since the last board line.

## Finding

The Mac is reachable now, but the historical recurrence is not disproved by a
single successful probe. Current checks from mesh-home show `tailscale status`
listing imac-rozalia active/direct, `tailscale ping` returning in 4ms, TCP/22
accepting a connection, and batch SSH as `ilya` successfully running `printf
reachable`. Classify this as a recurring/intermittent SSH availability fault
that is currently recovered. Keep the warning's recurrence and suppression
counts as its denominator; do not treat this check as proof that the fault
permanently cleared.

## Evidence

- `/home/mesh-home/.mesh/chat.log:41392` — original chronic-suppression
  roll-up and its measured recurrence details.
- `tailscale status` — imac-rozalia active/direct at `100.121.88.110`.
- `tailscale ping --c 1 100.121.88.110` — pong in 4ms.
- `timeout 5 bash -c ':</dev/tcp/100.121.88.110/22'` — exit 0.
- `timeout 8 ssh -o BatchMode=yes -o ConnectTimeout=5 ilya@100.121.88.110
  'printf reachable'` — printed `reachable`, exit 0.

## Disposition

Close this triage as currently reachable with intermittent recurrence still
the known fault. No remote configuration or substrate state was changed.

## Verification

- `mesh-dash --once check` — consumed the live, unfiltered health pane.
- `mesh-task queue --dispatch --owner health` — returned this exact-owner task.
- `mesh-task check dispatch health-warning/4989e0902917448d4dfa/triage health`
  — exit 0 before claim.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/4989e0902917448d4dfa
  triage` — claimed by the exact owner.
- Tailscale, TCP/22, and batch SSH probes above — all passed at triage time.
