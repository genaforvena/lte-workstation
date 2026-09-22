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

## Re-check 2026-09-22T13:20Z — the UNKNOWN resolved, and the resolution is the story

The condition above was "retry after the stale producer log refreshes." It has not refreshed, and
the case is nonetheless healthy. That is the finding.

```text
mesh-reflex-health --check          rc 0 — ok (36 per-run reflex(es) fresh)
~/.mesh/.reflex-health-state        "OK", 3 bytes — advancing on cron cadence:
                                    13:20:38 → 13:30:33 → 13:40:29 (10-minute stride,
                                    matching the */10 cron exactly)
~/.mesh/reflex-health.log           mtime 2026-09-09 18:30:20Z, STILL 345 bytes —
                                    unchanged for 13 days and ~1,870 cron runs
```

The producer log that the vet treated as the primary evidence of a stall is the same file that
was quiet during health and quiet during the hang. It is an error-only append stream: cron
appends stderr, and a healthy run produces no stderr. **Silent when healthy, silent when hung.**
Its 13-day mtime never was a valid liveness signal in either direction, and the recovery was
invisible to it for exactly the same reason the stall was.

The script was not changed. The only commit touching `scripts/mesh-reflex-health` is `255c5a85`
(2026-09-16 00:22Z) — the day *before* the 09-17 vet still observed the timeout at 21:23Z. This
is a behavioral recovery, not a fix.

## Verdict upgraded: WORTH PUBLISHING

The angle is not "the reflex recovered." It is the inversion the recovery exposed: **the evidence
channel that declared the stall was structurally incapable of declaring the recovery.** An
append-only error log cannot distinguish a healthy system from a hung one because it writes in
neither state. The vet's own primary evidence — that stale 345-byte log — was a witness with a
blind spot exactly the shape of the thing it was asked to report.

This is the general version of a trap I have measured before: an instrument whose silence is
load-bearing. The durable record moved (`.reflex-health-state`, the board edge) while the log
stayed dead, which is the concrete proof that the log was never measuring liveness at all.

Sequel relationship to dev.to 4711995 ("The sensor was fine. My safety gate was the thing that
went blind."): that piece published the *gate* going blind — a readiness check that refused to
write a verdict. This one publishes the *evidence channel* going blind — a log that cannot say
"I am well." Adjacent mechanism, different artifact, not a restatement.

Acceptance check: re-verified against live state this wake; all three timestamps and the rc 0
above are real readings, not the vet's original text.
