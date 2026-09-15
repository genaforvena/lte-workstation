# Witness blocker resolution check — 2026-09-13

The assigned unblock task is live and was taken by witness. Its named prerequisite,
`mesh-dash-forage-pane-gate-20260913/make-forage-pane-timeout-explicit`, is already `DONE`
under Genome with artifact `docs/reviews/mesh-dash-forage-pane-timeout-20260913.md`. That
artifact records bounded `mesh-forage --json` handling and explicit `UNKNOWN` output on
timeout/unavailable data. The original `witness-pane-fit-20260913/fit-required-ledger-and-raw-tail`
step is also already `DONE` with its receipt and live capture.

Verification on this run:

- The forage success and timeout arms passed.
- `test-witness-pane-fit` passed with 20 task rows and 20 raw lines visible together.
- The full `mesh-dash --test` completed with exit 2 / `n/a`, not a green verdict. All runnable
  legs passed; its fast-core timing was 11 seconds best-of-three against a 9-second limit while
  load1 was 18.51 on 16 cores. The script identifies this as an unmeasurable busy-node condition.
- No dash source, deployment, or network substrate was changed during this check.

The remaining gate is a full dash test on a quiet node. Retry `rtk mesh-dash --test` when load1 is
at or below 8 on this 16-core node; only close the unblock task after the full command exits 0.

Read-only mesh-home substrate inventory at 2026-09-13 19:24 UTC:

- `mesh-dms --list`: no dead-man switches armed.
- `mesh-claim --check routing` and `mesh-claim --check 100.76.0.0/16`: both unclaimed.
- `enp42s0` has the connected `100.76.0.0/16` route and default via `100.76.0.1`; no throw route
  is installed. `ip route get 100.76.0.2` selects `tailscale0` in table 52. No route or rule was
  changed.
- The old `exit-node-lan-cgnat-repair-20260912` live-route step is `REJECTED` for the former
  `100.74.0.0/16` scope. Its healer, deploy, and independent-verification successors remain
  held/recover-required. The router read-only access task is open under the operator; Wi-Fi
  root-cause access is blocked on that input and repair/verify remains queued.
- Operator hold acknowledged in the witness board at 19:20:03 UTC. No routing, exit-node, DNS,
  firewall, WireGuard, LAN-healer, or deployment change was made.

## Follow-up at 2026-09-13 20:01 UTC

The exact unblock task was rechecked and `mesh-task take` confirmed it is already active under witness. The required quiet-node gate still fails: `uptime` reported load averages 18.12 / 23.88 / 30.87 on the 16-core mesh-home host, above the recorded load1 <= 8 threshold. A contemporaneous process snapshot showed several Python/Bash workers each using about one CPU; I did not terminate or alter them. The full `mesh-dash --test` remains unsafe to interpret under this measured contention. Next action: rerun `rtk mesh-dash --test` only after load1 <= 8, then settle this exact task only on exit 0. Recheck load at 2026-09-13 20:11 UTC.

## Follow-up at 2026-09-13 20:30 UTC

The live load gate remains closed: `uptime` reports load averages 39.30 / 49.74 / 40.00, so load1 is well above the required <= 8. I did not run the full dash suite under this load. `mesh-dash --once witness` showed 96 unfinished tasks, a six-second source age, task rows, and the unfiltered 20-line chat tail; `mesh-window-check witness` reports all windows OK. The blocker prerequisites remain completed, but the final quiet-node full-suite gate is not yet satisfied. Keep this task active; next action is to recheck load and run `rtk mesh-dash --test` only once load1 <= 8. Recheck at 2026-09-13 20:40 UTC.

## Follow-up at 2026-09-13 20:40 UTC

At the scheduled retry check, `uptime` reports load averages 11.35 / 37.41 / 39.20. The 1-minute
load is still above the <= 8 gate, so I did not run `rtk mesh-dash --test`. Keep the exact resolver
active and retry only after a later load1 <= 8 observation; settle only on exit 0. Recheck at
2026-09-13 20:50 UTC.

## Follow-up at 2026-09-13 21:00 UTC

The scheduled retry check is still closed: `/proc/loadavg` reports `16.15 45.41 49.19` on
the 16-core host, above the required load1 <= 8. I did not run `rtk mesh-dash --test`.
The one-shot pane reports 94 unfinished tasks and this resolver remains RUNNING under
witness. `mesh-task audit` shows the exact task with its active lease through 21:10:48Z;
the board tail has no new witness-owned duplicate or unclaimed correction. Keep this exact
task active and retry at 21:10 UTC; run the full dash test only if load1 <= 8, settling
only on exit 0.
