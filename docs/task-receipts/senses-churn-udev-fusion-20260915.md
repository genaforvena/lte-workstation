# Device-churn × udev attribution receipt

- **Task:** `senses-churn-udev-fusion-20260915/correlate-churn-attribution`
- **Completed:** 2026-09-15T20:34:35Z
- **Producer:** `scripts/mesh-device-churn`
- **Consumer:** the device-churn artifact's joint verdict and triage route

## Change

`mesh-device-churn` now correlates its bounded churn interval with the
source-signed `mesh-udev-stream` interval and emits an explicit `joint` verdict
plus the overlap denominator. Complete overlap with any unsigned or otherwise
possible non-probe event becomes `TRIAGE_UNATTRIBUTED`; partial or unknown
overlap remains `UNKNOWN_UNATTRIBUTED`. A complete quiet interval with no
possible non-probe is `QUIET_CORROBORATED`. No unreachable input is converted
to an all-clear.

## Live evidence

`mesh-device-churn --check` produced a real reading:

```text
CHURN delta=5 ... joint=TRIAGE_UNATTRIBUTED joint-coverage=5/5
... source-attribution=complete observed=5/5 probes=mesh-udev-stream:3
unsigned=2 ... possible-nonprobe=2
```

The command returned rc=1 because the live verdict was `CHURN`; that is the
honest sensor result, not a smoke-test failure. The fused denominator is the
five-event overlap, with three source-signed probe events excluded and two
remaining events routed to explicit triage.

## Verification

```text
scripts/mesh-device-churn --test: rc=0
```

The test covers complete, partial, quiet, and unreadable overlap fixtures and
retains the real counter, boot-id, and USB hardware-read assertions.
