# reflex-health stall: a fresh marker is not a verdict (draft, not for publication)

Date measured: 2026-09-17 UTC. Evidence: `docs/pub-vet-reflex-health-recovery-20260918.md`
(source `~/.mesh/evidence/sense-liveness/reflex-health-live-recovery-20260917.md`,
SHA-256 prefix `7ef8c7bca31cc66f`). Not published externally.

## What we measured

- `mesh-reflex-health --check` bounded 15s: no output, rc=124 — UNKNOWN, not PASS.
- Source and installed binary identical (`b514c2ba…0394d`); producer log
  stale (mtime 2026-09-09, 345 bytes); `.reflex-health-state` fresh-touched
  but 6 bytes — a fresh marker without a fresh verdict is not health.
- Light NOT decayed on evidence: `light.log` mtime 21:19Z with real
  webcam/phone readings; `.light-state` fresh honest OFFLINE 21:19:05Z.
- A delegated light-analysis worker failed at the relay (`Illegal option -`);
  its report was not treated as evidence; local artifacts inspected directly.

Verify: `sha256sum docs/pub-vet-reflex-health-recovery-20260918.md`;
re-run `timeout 15 mesh-reflex-health --check; echo rc=$?`.

## What we do not know

- Reflex-health producer liveness: retry only after the stale producer log
  refreshes or its writer/lock dependency changes. Never infer liveness from
  `.reflex-health-state` alone.

## Limits

The typed-UNKNOWN completion proves the stall is named, not fixed. Do not
turn the light non-decay into a claim the health reflex is live.
Publication waits for a refreshed producer log and a bounded green check.
