# UVC metadata unblock receipt — 2026-09-16

Task: `unblock/senses/0a7d7bac216001ed/resolve`
Owner: `senses`
Observed: 2026-09-16T06:49–06:50Z UTC

## Result

`BLOCKED` — the live UVC metadata stream remains unreadable in this window.

- `timeout -k 2s 12s scripts/mesh-uvc-metadata --test` — rc 124; emitted
  `mesh-uvc-metadata: metadata read timed out after 2s from /dev/video1` before the bounded process ended.
- Retained `/home/mesh-home/.mesh/uvc-metadata/latest.bin` exists at 8448 bytes,
  and `latest.jsonl` exists at 46080 bytes, but these are retained artifacts from
  2026-09-16T06:41Z and do not prove a fresh hardware read.

No software-only repair or substrate change was attempted. The missing capability
is a stream-readable `/dev/video1` UVC metadata source; the current evidence does
not establish whether the cause is camera/USB/driver state or external contention.

## Bounded retry — 2026-09-16T06:53Z

- `/dev/video1` is present and readable as a UVC device (`uvcvideo`, USB2.0 Camera,
  Metadata Capture, Streaming, `UVCH`, buffer size 10240); bounded `v4l2-ctl --all`
  completed with rc 0.
- `timeout -k 2s 12s scripts/mesh-uvc-metadata --test` completed with rc 124 and
  emitted no fresh-read success. The blocked predicate therefore remains: the
  metadata stream is not readable by the organ test despite the device being
  enumerated and exposing metadata capabilities.

## Retry edge

Retry `scripts/mesh-uvc-metadata --test` after `/dev/video1` becomes stream-readable,
on camera/USB driver recovery or the next keepalive cycle. Accept only a fresh
nonzero-byte, timestamped read and subsequent organ refresh; do not infer LIVE from
the retained files.
