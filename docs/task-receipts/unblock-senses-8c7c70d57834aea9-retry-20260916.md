# UVC metadata unblock retry — 2026-09-16

Source: keepalive retry `2cec3220184b05d8`, terminal receipt `f02078742eadaae4`.
Task: `unblock/senses/8c7c70d57834aea9/resolve`.
Observed at: `2026-09-16T07:06:30Z`–`07:06:55Z` UTC.

## Live observation

`/dev/video1` exists and `v4l2-ctl --all -d /dev/video1` reports driver `uvcvideo`,
capabilities `Metadata Capture + Streaming`, and sample format `UVCH`.

The real gate was run as:

```text
mesh-uvc-metadata --test
```

Result: 10 bounded attempts, each `metadata read timed out after 2s from /dev/video1`;
the gate ended with `smoke-test: FAIL (real metadata read from /dev/video1)` and exit
code `1`. No fresh non-empty metadata buffer was produced.

## Disposition

The camera is enumerated and advertises the metadata interface, but the metadata stream
remains unreadable. This does not satisfy the unblock acceptance condition. Keep the
parent sensor task and this unblock task capability-blocked. Retry after camera/USB
stream recovery or the next keepalive cycle; do not infer an all-clear from enumeration.

