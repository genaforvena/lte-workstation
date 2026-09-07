# social-context escalation disposition — 2026-09-07

Decision: **(c) accept as-is with an expiring, visible mute**. No source repair is
warranted on this node because the missing input organs are physical/runtime
dependencies, not a broken `mesh-social-context` implementation.

## Evidence

- `mesh-presence --test` returned rc 2: no Bluetooth adapter; `/sys/class/bluetooth`
  is empty/absent.
- The live crontab contains `2-59/5 * * * * ... mesh-social-context --edge`.
- `cmp scripts/mesh-social-context ~/.local/bin/mesh-social-context` returned rc 0.
- `mesh-reflexes --check` reported `dispatch OK`: 2,787 dispatch lines and 217
  reflexes verified in the 3,600-second window.
- A real `timeout 30 mesh-social-context --edge` returned rc 0, with no state file
  created because the current run has neither a reachable phone nor a BLE reading;
  this is the script's honest-blind stand-down path, not a fabricated social state.
- `~/.mesh/needs.log` records the earlier repeated classes: stale-reflex repair
  injections on 2026-08-27 and 2026-08-30, followed by the cue-pinned escalation
  at `2026-08-30T08:45:06Z` (`n=4`). Later verdict experiments on 2026-09-06
  distinguished honest blindness, scheduler divergence, and edge-triggered steady
  state; none can create the absent phone/BLE organs.

## Discharge

The existing ruling is `reflex:social-context`, filed by `genome@mesh-home`,
expiring **2026-09-14T17:43:40Z**. It is visible in `mesh-needs --rulings` and
renders the deficit as `MUTED`, not absent. It must be re-evaluated at expiry;
if the phone or Bluetooth organ has returned, repair the sensing path then.

No source edit and no commit were made.
