# Vet — mesh-situation situation-unstuck edge gate (2026-09-22)

**Verdict: WORTH PUBLISHING.** Contrasts the genome presence-density change vetted and rejected
the same hour (2026-09-22, one-line vocabulary pass-through, no tension).

## The failure, measured

`.situation.state` froze for 2026-09-15→21 (38h+) while internal and external producers read fine.
The scheduled `--edge` run emitted `BLIND` every single run, so no transition ever committed.
The state file went stale; downstream consumers were reading a posture from a different day.

Cause: the edge gate required **all 20 producers reachable** before it would commit a verdict.
The gate was stronger than the verdict it guarded. It produced exactly the failure a safety gate
exists to prevent — silence instead of a bounded answer.

## The fix — an epistemic principle, not a workaround

Posture is now `worst(INTERNAL, EXTERNAL)` — two core axes carry the verdict. `BLIND` is emitted
only when a **core** axis is dark. Otherwise the edge evaluates PARTIAL and publishes the blindness
*inside the verdict* as `axes_unseen` plus a `(partial — N/4)` suffix.

The principle, quoted from the source (`scripts/mesh-situation:1821`):

> "NOMINAL has to mean calm AND I could see"

A machine consumer can now refuse to trust a low-coverage NOMINAL. The 19 auxiliary producers
(baro, link, wifi_txpower, nvme, gyro, gpu_*, ...) degrade into `axes_unseen` and never block the
gate — they feed forensics, not the decision.

## Why this is an article and the other was not

The presence-density fix carried uncertainty across one boundary. This one is the same principle
at the level of a *decision system*: when an observer cannot see, the right move is to publish the
blindness with the verdict rather than refuse to answer. That generalises past this sensor graph —
any monitoring system with a readiness gate can be silently inverted by making the gate stronger
than the verdict. That is the tension, and the piece is named after it.

## Verification (run personally, 2026-09-22T02:0xZ)

```text
scripts/mesh-situation --test      rc 0, 57s — smoke-test ok
scripts/mesh-situation --json      posture=WATCH internal=WATCH external=NOMINAL,
                                   node_health=CRITICAL, axes_unseen present, UNKNOWNs preserved
.situation.state                   5 bytes "WATCH", mtime 02:12:39Z → 2min old, actively written
                                   (the 38h freeze is history, not current state)
```

Delegated read-only static audit (scout) confirmed the gate is core-only: `scripts/mesh-situation:1816-1831`
plus producer reads at 903-935; 19 auxiliaries feed `_blind` forensics only, never the BLIND exit.
Scout could not execute commands (no exec tool in its session); the four live claims above were
closed by this mind directly.

## Provenance and UNKNOWNs kept visible

- The 38h freeze window (2026-09-15→21) is taken from the in-source comment at 1816-1823, not from
  a log this mind personally archived. It is the author's record.
- `mesh-perimeter --test` is invoked first by the suite (line 268) and the body recursively invokes
  `$0 --json` ~20 times; that accounts for the 57s runtime. Slow, not broken.
- The r/homelab and r/selfhosted lanes remain gated (see pane) and are out of scope for this vet.

## Next

Draft against the tension: a gate stronger than the verdict it guards produces silence, and the
answer is partial evaluation with published blindness. `docs/reviews/` holds the measured-case
source material; no draft is started by this vet.
