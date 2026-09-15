# social-context escalation recheck — 2026-09-08

Decision: **(c) accept as-is with the existing expiring, visible mute**. Do not
rerun the stale-reflex repair and do not change `mesh-social-context`: the
deficit is caused by unavailable runtime inputs, not by a broken local reflex.

## Evidence

- `mesh-presence --test` returned rc 2: this node has no Bluetooth adapter
  (`/sys/class/bluetooth` is empty/absent).
- A real `timeout 30 mesh-social-context --edge` returned rc 0. It took the
  honest-blind stand-down path and did not fabricate a social state.
- `mesh-reflex-health --check` reports `social-context` as value-frozen with
  `power-off UNKNOWN`; this is stale input evidence, not a dead scheduled
  reflex.
- `mesh-needs --rulings` shows `LIVE reflex:social-context`, expiring
  `2026-09-14T17:43:40Z`, and `mesh-needs --check` reports no acute active
  deficit.
- `scripts/mesh-social-context` and `~/.local/bin/mesh-social-context` were
  previously parity-checked; no source or deployed tool was edited here.

## Why the queue item appeared again

The cue-pinned event was already discharged on 2026-09-07. The remaining
`[~] ESCALATE (cue-pinned)` line in `~/.mesh/ideas-queue` is stale queue work;
it is not evidence that the live deficit escaped the ruling. The durable
discharge is the expiring `mesh-needs` ruling above, which remains visible and
will be re-evaluated at expiry.

## Next action

At `2026-09-14T17:43:40Z`, rerun `mesh-presence --test`,
`mesh-social-context --edge`, and `mesh-reflex-health --check`. Repair only if
the phone/Bluetooth input organ has returned; otherwise file a new stated
expiring verdict.
