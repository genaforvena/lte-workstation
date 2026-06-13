# Phone body: FULL sensor matrix — every sensor read live (supersedes 2026-06-12)

Date: 2026-06-13
Node: Redmi 10 (the body) — `100.103.99.16:8022`, user **u0_a386**
Mind: capability-research (discover) on imozerov-IdeaPad-3-15IIL05

## What's new vs the 2026-06-12 inventory

The prior file enumerated `termux-sensor -l` (23 entries) but verified **only 2** sensors
with live values (light + proximity). This sweep **read every sensor once**
(`timeout N termux-sensor -s <name> -n 1`) and captured a real artifact for each — a full
verified matrix, not a list. 15 sensors return real continuous/cumulative data; 9 are
event-triggers that (correctly) returned `{}` on a stationary phone.

**SSH-user discrepancy (important):** the 2026-06-12 note declared `u0_a386` dead and
`u0_a380` current after an F-Droid reinstall. As of today **`u0_a386` is live again** and
returns full sensor data over SSH — the mission's `u0_a386` is correct, not stale. Whoever
wires organs: use **u0_a386** (confirmed working 2026-06-13). The UID evidently reverted
(another reinstall, or the prior note caught a transient state).

## Verified matrix — live artifacts (all read-only, side-effect-free)

| Sensor | Type | Live reading (2026-06-13) | Notes |
|--------|------|---------------------------|-------|
| `bma420` | accelerometer (m/s²) | `[0.078, -0.068, 9.861]` | Bosch BMA420; ~1g on Z = phone flat, face up |
| `GRAVITY` | gravity vector | `[0.078, -0.060, 9.806]` | fused; confirms flat-and-still |
| `LINEARACCEL` | accel minus gravity | `[-0.003, -0.004, -0.055]` | ~0 = no movement |
| `UNCALI_ACC` | uncalibrated accel | `[0.085, -0.073, 9.865, 0,0,0]` | + bias channels |
| `vl_gyro` | gyroscope (rad/s) | `[-1.4e-4, -4.1e-4, -0.061]` | near-zero = not rotating |
| `akm09918` | magnetometer (µT) | `[-15.36, -2.40, -48.0]` | AKM AK09918; compass / metal-presence |
| `ORIENTATION` | azimuth/pitch/roll | `[99.95, 0.27, 0.31]` | heading ~100° |
| `ROTATION_VECTOR` | quaternion+acc | `[-0.005, -1.1e-4, -0.772, 0.636, 0]` | fused 3D attitude |
| `GAME_ROTATION_VECTOR` | quaternion (no mag) | `[-0.005, -8.4e-5, -0.770, 0.639]` | drift-free short-term |
| `GEOMAGNETIC_ROTATION_VECTOR` | quaternion (mag) | `[-0.005, -2.5e-4, -0.755, 0.656, 0]` | low-power attitude |
| `tmd2755_l` | **ambient light (lux)** | `[2]` | AMS TMD2755; 2 lux = dark/face-down |
| `tmd2755_p` | **proximity** | `[5]` | nothing close (5 = far) |
| `STEP_COUNTER` | **pedometer (cumulative)** | `[81081]` | steps since boot — a REAL odometer artifact |
| `pickup  Wakeup` | pickup gesture state | `[2, 0×15]` | returns a state vector immediately |
| `adux1050` | **capacitive / grip (SAR)** | `[681, 21961, 21280, 6941, 19150, 12209, 0×10]` | Analog Devices ADUX1050; 6 live cap channels — grip/touch-near sensing |

## Event-triggers — returned `{}` (no event fired while parked, EXPECTED)

`SIGNIFICANT_MOTION`, `STEP_DETECTOR`, `STEP_DETECTOR_WAKEUP`, `TILT_DETECTOR`,
`GLANCE_GESTURE`, `DEVICE_ORIENTATION`, `STATIONARY_DETECT`, `MOTION_DETECT`, `Touch Sensor`.

`{}` here is **not a failure** — these are edge sensors that emit only on a physical event
(phone moved / picked up / tilted). For a stationary body node they are the *most valuable*
signal: a non-empty read = "the phone was physically disturbed" = tamper / presence /
human-interaction the mesh has no other way to sense. They need a *streaming* read
(`termux-sensor -s SIGNIFICANT_MOTION` without `-n 1`, watched) rather than a one-shot.

## Mesh-novel senses (no other node has these) — ranked by marginal value for a parked body

1. **Ambient light (lux)** `tmd2755_l` — the mesh has NO light sense. Room lit/dark,
   day/night *in the room*, coarse occupancy ("lights went on"). Edge-triggerable dark↔lit.
2. **Motion/tamper** `SIGNIFICANT_MOTION` / `STATIONARY_DETECT` / pickup — strongest signal
   for a stationary node: "the body was moved." Presence/tamper edge.
3. **Pedometer** `STEP_COUNTER` (81081 now) — if the body ever travels, a step delta =
   the phone is being carried (vs a static reading).
4. **Magnetometer** `akm09918` — compass heading + gross ferrous-object/field changes.
5. **Proximity** `tmd2755_p` — something near the phone face.
6. **Grip (capacitive)** `adux1050` — 6 cap channels; a held-vs-resting signal.

## Decision: OFFER, don't pre-build (doctrine reaffirmed)

The inventory IS the artifact. No consumer is asking for a light/motion sense yet, so wiring
`mesh-light` / `mesh-motion` pollers now is speculative churn ("wire on demand, don't
pre-build"). This stays a **declarable capability** on the phone's card: when a consumer
wants ambient-light or motion/tamper context, the read path is one SSH line, edge-triggerable
in the `mesh-body-power` / `mesh-therm-watch` pattern.

The two cleanest organ candidates *when demand appears*:
- **`mesh-light`** — edge-trigger `[room-dark]`/`[room-lit]` off `tmd2755_l` (threshold + hysteresis).
- **`mesh-tamper`** — watch `SIGNIFICANT_MOTION` stream; emit `[body-moved]` on any event
  for a node that is supposed to be parked.

## Read shape (for whoever wires it)

```bash
# one-shot continuous/cumulative sensor (safe, won't hang):
ssh -p 8022 u0_a386@100.103.99.16 "timeout 6 termux-sensor -s tmd2755_l -n 1"
# event-trigger (must STREAM and watch — -n 1 returns {} when idle):
ssh -p 8022 u0_a386@100.103.99.16 "timeout 30 termux-sensor -s SIGNIFICANT_MOTION"
```

`termux-sensor` streams until the `-n` count is met and **hangs if an event-sensor never
fires** — always wrap in `timeout`. Confirmed user: **u0_a386** (2026-06-13).
