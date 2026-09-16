# Redmi trigger/interaction sensor frontier — 2026-09-16

## Live probe

The Redmi SSH body lane answered at `100.103.99.16:8022` as `u0_a380`, model `21061119DG`.
The following bounded commands were run with `termux-sensor -s <name> -n 1`:

| requested sensor | result | verdict |
|---|---|---|
| `TILT_DETECTOR` | exit 0, returned a `GEOMAGNETIC_ROTATION_VECTOR` quaternion-like 5-vector | alias/driver mismatch; not promoted as tilt evidence |
| `GLANCE_GESTURE` | no output, timeout 124 | event not observed in this window; unknown |
| `pickup Wakeup` | exit 0, `No valid sensors were registered!` | declared by list but not readable under this name |
| `STATIONARY_DETECT` | no output, timeout 124 | event not observed in this window; unknown |
| `MOTION_DETECT` | no output, timeout 124 | event not observed in this window; unknown |
| `Touch Sensor` | no output, timeout 124 | event not observed in this window; unknown |
| `GEOMAGNETIC_ROTATION_VECTOR` | no output, timeout 124 | event/driver did not emit within bound; unknown |

The raw command outputs and exit classifications are preserved in this document's live probe
record above. No phone state, touch input, or outward actuator was changed. The result is useful
negative evidence: the API's list is not equivalent to a producing sensor, and partial-name
matching can return a different sensor. Future probes must pin the exact returned key and keep a
timeout as `unknown`, never `quiet` or `false`.

## Literature application

The event-triggered sensing survey [Ge et al.](https://doi.org/10.1109/TCYB.2019.2917179) and
[SmartON](https://arxiv.org/abs/2103.00749) motivate event-driven wakeups, but they do not justify
assuming Android trigger sensors will emit on demand. The mesh-specific application is a
trigger-probe organ that records requested name, returned key, event count, timeout, coverage, and
power/battery context; it can then decide whether a trigger is usable as a wake source.

## Disposition

This is a frontier result, not a new verified organ. Ordinary Redmi motion/light/step paths already
exist and were intentionally not duplicated. The next exact-owner task should test whether a
controlled physical movement or screen interaction causes each event sensor to emit, using a
separate operator-facing physical-action boundary; absent that event, retain `unknown`.
