# unblock/adint/4bd98af1cbbf602f/resolve — 2026-09-16

## Result

BLOCKED: the `/dev/video1` UVC metadata endpoint remained stream-unreadable on
the fresh retry. No production refresh was attempted because the test-only
real read did not pass.

## Evidence

- `timeout 40s mesh-uvc-metadata --test` at 2026-09-16T07:52Z exited 1 after
  10/10 real metadata reads timed out after 2 seconds.
- Read-only `v4l2-ctl --device=/dev/video1 --all` confirms `uvcvideo`, Metadata
  Capture + Streaming, and `UVCH` with a 10240-byte buffer; capability exists,
  but this does not prove a readable stream.
- `/dev/video1` mtime: 2026-09-16 05:47:33Z. Retained `latest.bin` is 6116
  bytes, and `latest.jsonl` is 33916 bytes; both remain mtime 2026-09-16
  07:46:18Z and were not treated as fresh.

## Exact retry edge

Retry `mesh-uvc-metadata --test` after camera/USB stream recovery or the next
keepalive cycle. Only if it returns a real non-empty buffer, run
`mesh-uvc-metadata` and verify fresh timestamps plus non-empty `latest.bin` and
`latest.jsonl`; otherwise retain this block and do not infer LIVE state.
