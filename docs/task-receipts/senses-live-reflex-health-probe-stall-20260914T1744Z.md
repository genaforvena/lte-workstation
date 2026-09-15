# Senses live reflex-health probe stall — 2026-09-14 17:44Z

## Observation

`mesh-dash --once senses` completed at 17:44Z. Fused perception remained partial: perimeter
was `CALM (partial — 2/3 axes unreachable)`, several room and presence artifacts were stale, and
the sense-reflex-liveness row said `mesh-reflex-health unavailable — produced NO output`.

## Bounded diagnosis

The prior handoff recorded `mesh-reflex-health --check` timing out at 30 seconds with no output.
This turn ran `timeout -k 2s 10s bash -x scripts/mesh-reflex-health --check`. It exited 124 at
the 10-second bound. The trace reached the stale/missing `social-context` row and stopped inside
`organ_absence_probe`, at its nested command:

```text
timeout 30 /home/mesh-home/.local/bin/mesh-social-context --test
```

This localizes the observed stall to the organ-absence smoke-test probe. It does not establish
whether that probe would itself finish within 30 seconds; the overall check had not yet produced a
report when the outer 10-second bound fired. `mesh-social-context --test` includes a BLE
`mesh-presence --test` and three phone-dependent tests, so those are candidates for a narrower
bounded follow-up. No source, listener, or substrate was changed.

## Dispatch and wake state

`mesh-task queue --dispatch --owner senses` returned the owned
`health-device-churn-cross-namespace-join-20260914/investigate-cross-namespace-uevent-join` row,
but `mesh-task check dispatch … senses` exited 3 with no output. Per the dispatch gate, it was not
taken.

`mesh-wake-expect senses` now suppresses only the anchored refresh-header and pane-footer shapes
for 900 seconds. CPU and other readings remain wake-worthy.

## Next action

Inspect and individually time the dependencies of `mesh-social-context --test`, starting with
`mesh-presence --test`; then fix the boundedness or reporting path in `mesh-reflex-health` and
verify its `--check` plus sense-pane wiring. Keep the cross-namespace task queued until its dispatch
check exits 0.
