# wifi-crossval decay: honest empties, no peer, explicit rc=2 (draft, not for publication)

Date measured: 2026-09-17 UTC. Evidence: `docs/pub-vet-wifi-crossval-decay-20260918.md`
(source `~/.mesh/evidence/sense-liveness/wifi-crossval-20260917.md`,
SHA-256 prefix `4b16e45de6de2c12`). Not published externally.

## What we measured

- Bounded 24h: 96 scheduled scans, 0 real AP reads, 96 honest-empty; 7d:
  829 scheduled, 0 real, 829 empty, 0 crossval transitions.
- Crossval transition history absent since 2026-08-30; peer 192.168.8.214
  unreachable; local vantage past horizon.
- Action: `wifi-crossval` marked decayed on mesh-home, cron scheduling
  removed, source retained with `reflex-cadence: off` for a future
  radio-bearing node with a reachable peer.
- Post-action probe `mesh-wifi-crossval --json` at 21:09Z returns `rc=2`
  explicit `cannot cross-validate` — not an all-clear.

Verify: `sha256sum docs/pub-vet-wifi-crossval-decay-20260918.md`;
re-run `mesh-wifi-crossval --json; echo rc=$?` (expect rc=2, unreachable).

## What we do not know

- Post-action scanner freshness UNKNOWN: the 21:06:01Z 0-AP record predates
  the decay action; the standalone retry at 21:12:52Z timed out (rc=124).
- `mesh-wifi-crossval --test` rc=0 is fixture coverage only.

## Limits

The rc=2 proves the tool says it cannot testify. It says nothing about radio
health. Publication waits for a radio-bearing node with a reachable peer and
timestamped launch/outcome evidence.
