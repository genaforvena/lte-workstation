# UVC metadata recovery — 2026-09-16

## Result

**BLOCKED: live UVC stream-start/read unavailable at this probe window.**

At 2026-09-16T06:01Z, the exact deployed real probe

```text
timeout 35s env MESH_UVC_METADATA_TEST_ATTEMPTS=10 /home/mesh-home/.local/bin/mesh-uvc-metadata --test
```

ran all 10 bounded attempts and exited 1. Every attempt reported a 2-second
metadata read timeout from `/dev/video1`; no fresh buffer was accepted.

## What remains live

`/dev/video1` exists with mode `crw-rw----`, owner `root:video`, and the
`uvcvideo` driver advertises `Metadata Capture`, `Streaming`, format `UVCH`,
and 10240-byte buffers. The retained artifact `/home/mesh-home/.mesh/uvc-metadata/latest.bin`
is 8932 bytes, mtime 2026-09-16T05:58:18Z, and parses into 406 records, but
it predates this failed probe and therefore is not evidence of current liveness.

The keepalive tape records a prior `DARK`/`DOWN-edge` followed by a debounced
recovery indication. `dmesg` was unreadable without kernel-buffer permission;
no permission or hardware repair was attempted. Existing mesh-owned readers
were the only processes stopped, to clear diagnostic lock contention.

## Retry edge

Retry the same bounded real probe when `/dev/video1` becomes stream-readable
again (camera/USB driver recovery or a new keepalive cycle). Acceptance remains
a `--test` exit 0 reporting nonzero bytes and timestamped records, followed by
an organ refresh; do not infer LIVE from the retained artifact alone.
