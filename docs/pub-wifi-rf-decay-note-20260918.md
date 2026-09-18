# wifi-rf decay: absent organ, not false empty (draft, not for publication)

Date measured: 2026-09-18 UTC. Evidence: `docs/pub-vet-wifi-rf-decay-20260918.md`
(source `~/.mesh/evidence/artifacts/sense-liveness-wifi-rf-20260918.md`,
SHA-256 prefix `9137bbde82f8bca8`). Not published externally.

## What we measured

- Bounded 24h: 246 timestamped CRON dispatches (syslog 2026-09-17T08:06:01Z →
  2026-09-18T08:01:00Z), 0% fresh-artifact coverage; 7d: 1158 dispatches, same.
- Live probe exits `2`, `no associated wireless interface`; no
  `.wifi-rf.state` ever present — an absent organ, not a false wireless-empty.
- Action: source header `# reflex-cadence: off`; `mesh-reflexes --apply`
  converted the schedule to a preserved `DECLINED-BY-HEADER` tombstone.
- `mesh-reflex-health --check` reports explicit `organ-absent: wifi-rf`
  before and after — no stale positive.

Verify: `sha256sum docs/pub-vet-wifi-rf-decay-20260918.md`;
re-run `scripts/mesh-wifi-rf --json; echo rc=$?` (expect rc=2).

## What we do not know

- `wifi-rf.log` holds 5,062 un-timestamped lines: result history cannot be
  assigned to either bounded window. Missing per-attempt result timestamps
  are UNKNOWN, not calm.

## Limits

The decay proves the schedule is tombstoned and the probe is honest about
absence. It says nothing about radio health. Publication waits for a node
with an associated wireless interface and timestamped result evidence.
