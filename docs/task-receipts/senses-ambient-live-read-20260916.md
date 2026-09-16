# Senses ambient live-read verification — 2026-09-16

Task: `senses-ambient-live-read-20260915/repair-ambient-live-read`.

The live pane showed `ROOM ambient=DATA-STALE|...|fixture=CYCLING (STALE)`. I checked the
underlying producers separately rather than treating that derived state as a dead microphone:

- `scripts/mesh-ambient-level --test` — PASS (`floor gate: DEAF at rms<=-85dB, real signal passes`).
- `scripts/mesh-ambient-level --json` at `2026-09-15T23:57:25Z` — exit 0, real current read:
  `label=MODERATE`, `rms_db=-27.6`, `peak_db=-2.9`, `duration=120.0`, `coverage=0.982`,
  `dev=overhear-tap@plughw:CARD=Camera,DEV=0`.
- `scripts/mesh-ambient-clock --json` at the same time — exit 2 with explicit `DATA-STALE`:
  `presence.log 24047min old > adaptive 20min threshold — BLE data unavailable`.

Acceptance is met by the existing honest split: the acoustic producer exposes a fresh measured
artifact, while the dependent household clock refuses to manufacture a current fixture when its BLE
input is stale. No production change was needed.
