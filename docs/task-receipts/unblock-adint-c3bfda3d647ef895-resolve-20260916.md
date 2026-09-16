# UVC metadata unblock receipt — 2026-09-16

Task: `unblock/adint/c3bfda3d647ef895/resolve`
Owner: `adint`
Observed: `2026-09-16T07:40:13Z–07:41:53Z UTC`

## Result

`BLOCKED` — the live UVC metadata stream remains unreadable after the exact-owner retry.

- `mesh-uvc-metadata --test` — exit `1`.
- The test emitted ten real-read failures: `metadata read timed out after 2s
  from /dev/video1`, followed by `smoke-test: FAIL (real metadata read from /dev/video1)`.
- `/dev/video1` is present as `crw-rw---- root:video`; `v4l2-ctl --all` confirms the
  `uvcvideo` device advertises Metadata Capture, Streaming, `UVCH`, and a 10240-byte
  metadata buffer. Enumeration does not establish stream readability.
- No fresh nonzero-byte metadata buffer or production organ refresh was produced.

## Retry edge

Retry `mesh-uvc-metadata --test` after `/dev/video1` becomes stream-readable, on camera/USB
driver recovery or the next keepalive cycle. Accept only a fresh nonzero-byte, timestamped
read and then a successful production refresh; retained files remain excluded from LIVE evidence.
No software-only repair or substrate change was attempted.

## Verification

The retry and device inspection were run live from `/home/mesh-home/lte-workstation`.
Captured smoke-test output was `/tmp/adint-uvc-test.out` during this turn.
