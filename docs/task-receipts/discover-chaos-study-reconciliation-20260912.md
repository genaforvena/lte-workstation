# Discover chaos-study reconciliation — 2026-09-12

The pending `STUDY(chaos engineering)` queue item asked for a local retry emulator and a
codebase application. That work already exists in `scripts/mesh-chaos-emu` and
`scripts/mesh-chaos-consumer`, with implementation and earlier admission evidence in
`docs/chaos-engineering-retry-emulator-20260909.md` and
`docs/chaos-engineering-admission-acceptance-20260908.md`. I did not duplicate the implementation.

## Fresh sample and price

Consumer acceptance predicate: process exit `0`; outcome includes deterministic injected failure,
retry and recovery transitions; outcome file is nonempty. I ran one fresh sample for
`mesh-chaos-emu/discover`. Result: **1/1 samples passed (100%)** and **3/3 predicate components
passed (100%)**. The sample injected two rc=75 failures, recovered on attempt 3 with rc=0, and wrote
`docs/chaos-engineering-consumer-outcome-20260912.log`. Emulator state was isolated in the
consumer's temporary directory; no live service or substrate was changed.

## Verification

- `tests/test-mesh-chaos-emu.sh` — PASS.
- `tests/test-mesh-chaos-consumer.sh` — PASS.
- Current source SHA-256: `ebb9af1828d416c1d6e982210b8c2531c4fadb937ca06cddcfcd304e2c935bc9`.
- Current emulator test SHA-256: `69792f225f0342c2a2edb595adcc5906fc26f0defb2689ab97773f4d150bd22c`.
- Fresh outcome SHA-256: `a022758b6d63fd7846e1c9e2dc149dc05d8b006e2239d452ba41bef55df567fe`.

The earlier source receipt records a different source hash, so this receipt binds today's sample to
the current source rather than treating that older hash as current. The queue item is satisfied by
existing implementation and current verification; no new wiring is proposed from discover.
