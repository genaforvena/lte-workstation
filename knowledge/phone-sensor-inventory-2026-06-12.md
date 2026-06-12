# Phone body: full sensor inventory + two mesh-novel senses VERIFIED

Date: 2026-06-12
Node: Redmi 10 (the body) — 100.103.99.16:8022, user **u0_a380** (post-F-Droid-reinstall;
the old u0_a386 is dead — Termux UID changed on reinstall).

## Why this tick

PLAN listed "25 sensors AVAILABLE (not yet wired)" but only mic/camera/location/battery were
ever exercised. Node-level capability sweeps were exhausted today, but the phone's full
hardware **sensor manager** had never been enumerated — a genuine, read-only, side-effect-free
discovery. `termux-sensor -l` over SSH gives the real list.

## Full sensor list (`termux-sensor -l`)

```
bma420 (accelerometer)      akm09918 (magnetometer/compass)   vl_gyro (gyroscope)
ORIENTATION  GRAVITY  LINEARACCEL  ROTATION_VECTOR  GAME_ROTATION_VECTOR
GEOMAGNETIC_ROTATION_VECTOR  DEVICE_ORIENTATION  UNCALI_ACC
tmd2755_l (AMBIENT LIGHT)   tmd2755_p (PROXIMITY)
STEP_DETECTOR  STEP_COUNTER  (pedometer)
SIGNIFICANT_MOTION  MOTION_DETECT  STATIONARY_DETECT  TILT_DETECTOR  pickup Wakeup
GLANCE_GESTURE  adux1050 (capacitive)  Touch Sensor
```

## VERIFIED real artifacts (not just "listed")

Per the verification principle — listed ≠ real. Read live, side-effect-free:

- **Ambient light** `termux-sensor -s tmd2755_l -n 1` → `{"tmd2755_l":{"values":[26]}}`
  — 26 lux, a dim indoor room (consistent with evening). A REAL reading.
- **Proximity** `termux-sensor -s tmd2755_p -n 1` → `{"tmd2755_p":{"values":[5]}}` — nothing close.

## Mesh-novel senses (no other node has these)

1. **Ambient light (lux)** — the mesh has NO light sense. Real value: room lit/dark,
   day/night *in the room* (vs the body's clock), ambient context for the embodied agent,
   coarse occupancy ("lights went on"). Edge-triggerable (dark↔lit).
2. **Proximity** — something near the phone.
3. **SIGNIFICANT_MOTION / STATIONARY_DETECT** — for a STATIONARY body node this is the
   strongest signal: a motion event = "the phone was physically moved/picked up" = a
   tamper / human-interaction / presence event the mesh can't sense any other way.
4. Pedometer, orientation, magnetometer — lower marginal value while the body is parked.

## Decision: OFFER, don't pre-build (doctrine)

"A node declares what it offers; consumers read the card and opt in" + "wire on demand,
don't pre-build" (reaffirmed today re mesh-relay). No consumer is asking for a light sense
yet, so wiring a `mesh-light` poller now would be churn. This is a **declarable capability**:
when a consumer wants ambient-light/motion context, the read path is one SSH line
(`termux-sensor -s <name> -n 1`), edge-triggerable in the body-power/therm pattern. Until
then it stays a verified, documented affordance — the inventory is the artifact.

## Note for whoever wires it later

Use **u0_a380** (not the stale u0_a386 in old docs). `termux-sensor` needs a `timeout` wrapper
over SSH — it streams until `-n` count is met and can hang if a sensor never fires; the
one-shot `-s <name> -n 1` with `timeout 12` is the safe read shape.
