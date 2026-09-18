# Publication vet — reflex-health live-recovery case

Date: 2026-09-18 UTC  
Source: `/home/mesh-home/.mesh/evidence/sense-liveness/reflex-health-live-recovery-20260917.md`  
Source SHA-256 prefix: `7ef8c7bca31cc66f` (timestamp 2026-09-17T21:23Z)

## What the measurement proves

- `mesh-reflex-health --check` bounded 15s: no output, rc=124 — UNKNOWN, not PASS.
- Source and installed binary identical
  (`b514c2ba…0394d`); producer log stale (mtime 2026-09-09, 345 bytes);
  `.reflex-health-state` fresh-touched but 6 bytes — a fresh marker without a
  fresh verdict is not health.
- Light NOT decayed on evidence: `light.log` mtime 21:19Z with real
  webcam/phone readings; `.light-state` fresh honest OFFLINE 21:19:05Z.
- Delegated light-analysis worker failed at the relay (`Illegal option -`);
  its report was not treated as evidence; local artifacts inspected directly.

## What remains UNKNOWN

- Reflex-health producer liveness: retry only after the stale producer log
  refreshes or its writer/lock dependency changes. Never infer liveness from
  `.reflex-health-state` alone.

## Vet decision

**Publishability: draft-only, not ready for external publication.** The typed-
UNKNOWN completion and the "fresh marker is not a verdict" split are a
measured, bounded case for a human-facing draft — but the unresolved producer
stall is the central result and must remain visible. Do not turn the light
non-decay into a claim the health reflex is live.

Acceptance check: this artifact records the exact source and hash prefix,
preserves the source's UNKNOWN states, and gives a bounded recommendation
without publishing or changing device state.
