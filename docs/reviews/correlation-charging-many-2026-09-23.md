# CORRELATION body_power-CHARGING × presence-MANY — DISCARDED (stale proxy, 2026-09-23)

Claim (idea-queue row 1764): when body_power reads CHARGING, presence tends to read MANY
(lift 1.92, 32 episodes, era-restricted; 8 occasions / 32 episodes of 539, window 1069.7h;
invariance UNSTABLE 0/4 envs: 1.64 / 0.66 / 1.51 / 1.00).

Verdict: DISCARD — no fused sense, no reflex. One line why: CHARGING is a genuine
battery state but MANY is a coarse BLE device-count proxy (>8 nearby devices incl.
appliances), and the overlap is environment-specific (0/4 stable) — fusing them would
turn an old availability-regime coincidence into a false presence reflex.

Evidence (live, 2026-09-23, read-only):

- `scripts/mesh-correlate --dry` rc=0: no CHARGING×MANY line; `--list` likewise empty.
  The pair does not surface on the current tape; the queued seed is stale.
- Prior full verdict (docs/correlation-investigation-body-power-charging-presence-many-spurious-20260908.md):
  era re-read (2259 rows, 577.7h) reproduces lift 1.99 but 0/4 environments clear the
  floor (best 1.64); joint rows concentrated in the old BLE observation era with only
  2 usable rows after the presence freshness boundary; MANY counts appliances and
  ambiguous devices, not human presence. Note: the raw BLE `presence.log` is fresh
  again today (2026-09-23T06:10Z tail) — but freshness of the raw scan log does not
  repair a 0/4-environment verdict or promote a device-count proxy to ground truth.
- Usefulness: nothing to fuse — a CHARGING→"room is full" reflex would fire on the
  household radio regime, not on people.

No tool edited. Receipt left uncommitted for steward landing.
