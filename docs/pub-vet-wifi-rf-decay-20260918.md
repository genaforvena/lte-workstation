# Publication vet — wifi-rf decay case

Date: 2026-09-18 UTC  
Source: `/home/mesh-home/.mesh/evidence/artifacts/sense-liveness-wifi-rf-20260918.md`  
Source SHA-256 prefix: `9137bbde82f8bca8`

## What the measurement proves

- Absent organ, not false-empty: live probe exits `2`,
  `no associated wireless interface`; no `.wifi-rf.state` ever present.
- Bounded 24h: 246 timestamped CRON dispatches (syslog 2026-09-17T08:06:01Z →
  2026-09-18T08:01:00Z), 0% fresh-artifact coverage; 7d: 1158 dispatches, same.
- Action: source header `# reflex-cadence: off`; `mesh-reflexes --apply`
  converted the schedule to a preserved `DECLINED-BY-HEADER` tombstone.
- `mesh-reflex-health --check` reports explicit `organ-absent: wifi-rf`
  before and after — no stale positive.

## What remains UNKNOWN

- `wifi-rf.log` holds 5,062 un-timestamped lines: result history cannot be
  assigned to either bounded window — scheduler history is timestamped,
  result history is not. Missing per-attempt result timestamps are UNKNOWN,
  not calm.

## Vet decision

**Publishability: draft-only, not ready for external publication.** The decay
with its honest exit-2 probe and tombstoned schedule is a measured, bounded
case for a human-facing draft — the "absent organ vs false empty" split is the
angle — but the un-timestamped result history stays UNKNOWN and visible.
Do not turn the decay into a claim about radio health.

Acceptance check: this artifact records the exact source and hash prefix,
preserves the source's UNKNOWN states, and gives a bounded recommendation
without publishing or changing device state.
