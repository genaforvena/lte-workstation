# Live capability census extension — 2026-09-16

This extension updates the earlier census with fresh direct reads after Redmi SSH became
available. Commands were run from mesh-home at approximately 2026-09-16T14:10Z.

## Redmi 10 — newly verified body surface

SSH `u0_a380@100.103.99.16:8022` succeeded. Direct outputs:

- `getprop ro.product.model` → `21061119DG`.
- `termux-battery-status` → present, Li-poly, GOOD, AC charging, 87%, 30.4 C, 4315 mV.
- `termux-sensor -l` → 24 named sensor interfaces, including accelerometer (`bma420`), magnetic
  field (`akm09918`), gyro, proximity, gravity, linear acceleration, rotation vectors, significant
  motion, step detector/counter, tilt, pickup, stationary/motion detection, touch sensor, and
  wakeup variants.
- `termux-sensor -s bma420 -n 1` → real sample `[0.36105, 7.54095, 5.88705]`.
- `termux-telephony-deviceinfo` → dual-SIM GSM body, SIM ready, MTS RUS, RU, data enabled.
- command presence: `termux-camera-photo`, `termux-location`, and
  `termux-microphone-record` all resolved on the device.

The first attempted generic sensor command (`termux-sensor -n 1`) returned `Unknown command: null`;
this is recorded as a tool invocation error, not hidden. The named-sensor invocation succeeded.
No camera, microphone, location, SMS, or call-control side effect was performed in this pass.

## iMac-Rozalia — newly verified physical I/O

SSH `ilya@100.121.88.110` succeeded. `system_profiler` reported:

- FaceTime HD built-in camera (UVC, vendor/product identity present).
- Built-in microphone, two input channels, 44.1 kHz default.
- Built-in output, two channels, 44.1 kHz, plus Soundflower/Corel/Movavi virtual audio devices.
- Two active displays: internal 1920x1080 and Cintiq 27QHD 2560x1440.
- `/usr/bin/say` exists from the prior probe.

These establish declared/reachable hardware and a speech actuator, but not a produced camera frame,
audio recording, or notification artifact. Keep those as `unverified`.

## phaedra — service evidence

SSH `root@100.94.116.17` succeeded. `mesh-loc-collector.service` is `active/running` with
`ExecStart=/usr/bin/python3 /root/.mesh/loc-collector.py`, and the node also runs the Tailscale
agent and port-80 fallback service. The service and file presence are verified; the collector's
actual fresh output was not consumed in this pass, so its sensing value remains `wired/unverified`.

## Candidate upgrades changed by this pass

1. Redmi is no longer merely a sleepy/reachable body: it now has a verified real IMU sample and a
   broad Termux sensor/API surface. It is a strong candidate for event-triggered body-context
   sensing, with battery percentage and charging state available for admission control.
2. iMac is a real second camera/microphone/display/speech vantage, not just a `say` binary. The next
   safe probes should produce one bounded camera/audio artifact and inspect existing notification
   paths, each with separate privacy and actuator gates.
3. A three-tier capability state is necessary: hardware/API existence, live read, and produced
   artifact. This prevents `termux-camera-photo` or a running collector from being promoted to a
   verified mesh sense without actually producing a valid artifact.
