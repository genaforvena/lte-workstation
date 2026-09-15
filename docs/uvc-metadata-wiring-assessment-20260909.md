# UVC metadata wiring assessment — 2026-09-09

## Verdict

The discovered UVC metadata capability is wired on `mesh-home`, but the live
sensor is currently blind. The wiring must not be reported as a healthy stream.

## Evidence

- `/dev/video1` is the local `uvcvideo` metadata-capture endpoint for
  `USB2.0 Camera`, format `UVCH`, buffer size 10240.
- `~/.local/bin/mesh-uvc-metadata` resolves to
  `lte-workstation/scripts/mesh-uvc-metadata`; both copies have SHA-256
  `5369fc99c51775f0b0e52898b9b0bffdf7784022c1f8fb14148f976e9bdf5039`.
- `~/.mesh/reflexes.cron` and the live crontab each contain one
  `*/10 * * * * mesh-uvc-metadata` entry writing
  `~/.mesh/uvc-metadata/latest.bin`.
- `mesh-organ --where uvc-metadata` and `mesh-organ --why uvc-metadata`
  resolve the sole local offerer, `mesh-home`.
- `tests/test-mesh-uvc-metadata.sh` was run against the real device; ten
  attempts returned empty data or timed out, so the gate exited 1.
- The current runtime artifact is 506 bytes and timestamped 18:20:00Z,
  therefore stale at assessment time. The discovery artifact is a separate,
  fresh 5,874-byte sample from 10:41Z and does not prove current liveness.
- A paired `/dev/video0` image stream did not make `/dev/video1` produce a
  metadata buffer.

## Unresolved

The camera driver/USB path is intermittently failing UVC probe control with
`-110` in the node's hardware-fault observations. Investigate stream startup
and device recovery before changing the wrapper's acceptance predicate.
