# Correlation investigation: `body_motion=STILL` ↔ `presence=MANY` — spurious, 2026-09-07

**Disposition:** discard. No fused sense and no reflex.

## Reproduction

`bash scripts/mesh-correlate --dry` reproduced the queued candidate: corrected/hour-stratified
lift **3.01**, 60 episodes, 27 occasions, and 344 usable rows in the 1305-hour window. The
uncorrected full-window lift is **2.1** and is explicitly confounded; the hour-shadow alone
scores **1.15**, leaving only the narrow 3.01-vs-1.8 margin. `bash scripts/mesh-correlate
--stable` reports **UNSTABLE**: the floor clears in **0/4** environments (env20 0.00, env25
1.00, env28 0.98, env29 0.98).

## Reality check

`body_motion=STILL` is a phone-motion classification: the phone is stationary, not proof that
the person is stationary or that anyone else is present. `presence=MANY` is the BLE scan count
bucket from `scripts/mesh-sensor-tape` (`n > 8`), not a person count.

The live source artifacts make the failure concrete. In `~/.mesh/presence.log`, the 2026-08-26
13:00–16:00 run contains `n=9–14` scans while the tape repeatedly reads `body_motion=STILL`.
Those scans contain the persistent Bose speaker, Samsung TV, Quest, and Bluetooth/DV8235
identities alongside rotating `?` MACs. For example, the 14:20 scan has 14 devices, including
the Bose, Samsung TV, Quest, and ten unidentified/random entries; its attribution is
`personal:11,appliance:2,ambiguous:1`, which is an attribution of BLE identities, not a census
of eleven people. Across the current presence log, 688 `MANY` scans sum to 1,410 appliance and
1,405 ambiguous attributions plus 3,757 random unidentified entries; the count is therefore
highly exposed to radio visibility, MAC rotation, and nearby electronics.

The current tape's 84 direct `STILL`/`MANY` rows are clustered rather than broadly distributed:
29 on Aug 26, 14 on Aug 28, 19 on Aug 29, and 9 on Aug 30 (the remainder are isolated). This
is compatible with one local BLE-population regime and does not establish a causal relation
from phone stillness to room occupancy.

## Verdict

The association is an environment-specific BLE-count/phone-placement coincidence. It fails the
invariance test and `MANY` does not identify people, so promoting it would turn an unstable,
confounded proxy into an operational belief; **discard**.

## Evidence and verification

- `bash scripts/mesh-correlate --dry`
- `bash scripts/mesh-correlate --stable`
- `~/.mesh/sensor-tape.tsv` (live tape; schema and bucket source: `scripts/mesh-sensor-tape`)
- `~/.mesh/presence.log` (the matching BLE device lists and attribution fields)

No source tool was edited; no deployment or commit is required.
