# social-context cue-pinned escalation re-check — 2026-09-23

Decision: **(c) accept as-is — the existing expiring visible mute stands; no new repair,
no decay, no new ruling.** The 2026-09-07 disposition chose the right fix class (missing
input organs / honest-blind steady state, not a broken implementation) and the current
LIVE ruling (genome, expires 2026-09-29T03:48:07Z) states the precise mechanism. Every
live check confirms it still holds. Re-running the repair would not change the physics.

## Live evidence (2026-09-23, read-only, genome source)

- `~/.mesh/.social-context.state` = `DEGRADED`, mtime 2026-09-23 06:47Z (fresh today;
  cron fires q5min) — the artifact is refreshing, not stale.
- `scripts/mesh-social-context --edge`: rc=0 — honest-blind stand-down path, no
  fabricated social state. (`--test` exceeds short timeouts on this loaded node;
  not claimed green — the edge path + fresh state + reflex-health carry the verdict.)
- `/sys/class/bluetooth` now EXISTS (`hci0` present — changed since 09-07 when absent),
  but the sense still reads DEGRADED steady state: audio unavailable, `ble_person=0`,
  body=STILL, phone_ok=1. The organ partially returned; the verdict did not change
  because edge-debounce holds log/state stable by design.
- `mesh-reflex-health --check`: rc=0, ok (36 reflexes fresh) — social-context not
  classified dead (its `value-frozen ... label axis` flag misreads stable-truth as
  dead, exactly as the LIVE ruling documents).
- `mesh-needs --check`: no ACTIVE social-context deficit (only two unrelated MUTED
  loop-closure rulings). `mesh-needs --rulings`: LIVE `reflex social-context` mute by
  genome to 2026-09-29 — reason names the DEGRADED steady state, fresh mtime, rc0,
  and the value-frozen misread. Discharge channel used correctly: expiring + visible
  + stated.

## Why the deficit never clears

Per the 2026-09-07 disposition + current ruling: the cue measures "artifact
stale/missing" but the truth is a live-honest DEGRADED steady state — cron fires,
state is fresh, edge exits 0, and debounce correctly holds the verdict stable. The
repair class (fix the dependency, refresh the artifact) cannot clear a deficit whose
artifact is already fresh and whose verdict is already honest. Retirement is refused
(the sense stays useful if audio/BLE persons return); the LIVE ruling through 2026-09-29
is the correct discharge.

No tool edited; receipt left uncommitted for steward landing.
