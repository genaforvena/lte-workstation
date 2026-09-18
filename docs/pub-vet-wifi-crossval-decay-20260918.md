# Publication vet — wifi-crossval decay case

Date: 2026-09-18 UTC  
Source: `/home/mesh-home/.mesh/evidence/sense-liveness/wifi-crossval-20260917.md`  
Source SHA-256 prefix: `4b16e45de6de2c12` (timestamp 2026-09-17T21:09:18Z)

## What the measurement proves

- Bounded 24h window: 96 scheduled scans, 0 real AP reads, 96 honest-empty;
  7d window: 829 scheduled, 0 real, 829 empty, 0 crossval transitions.
- Crossval transition history absent since 2026-08-30; peer 192.168.8.214
  unreachable; local vantage past horizon.
- Post-action probe `mesh-wifi-crossval --json` at 21:09Z returns `rc=2`
  explicit `cannot cross-validate`, not an all-clear; cron scheduling removed,
  source retained with `reflex-cadence: off`.

## What remains UNKNOWN

- Post-change `mesh-reflex-health --check` bounded run timed out (rc=124):
  UNKNOWN, not green.
- Post-action scanner freshness UNKNOWN: standalone wifiscan retry at 21:12:52Z
  timed out (rc=124); the 21:06:01Z 0-AP record predates the decay action.
- `mesh-wifi-crossval --test` rc=0 is fixture coverage only.

## Vet decision

**Publishability: draft-only, not ready for external publication.** The decay
action and its honest rc=2 post-artifact are a measured, bounded case suitable
for a human-facing draft, but the scanner-freshness UNKNOWN and the absent
transition history are central results and must remain visible. Do not turn the
explicit rc=2 into a claim about radio health.

Acceptance check: this artifact records the exact source and hash prefix,
preserves the source's UNKNOWN states, and gives a bounded recommendation
without publishing or changing device state.
