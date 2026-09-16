# UVC metadata retry receipt — 2026-09-16

Task: `unblock/senses/0a7d7bac216001ed/resolve`
Owner: `senses`
Observed: 2026-09-16T06:53:34Z–06:53:56Z UTC

## Result

`BLOCKED` — the live UVC metadata stream remains unreadable in this window.

- `scripts/mesh-uvc-metadata --test` — exit 1.
- The command emitted ten real-read failures: `metadata read timed out after 2s
  from /dev/video1`, then `smoke-test: FAIL (real metadata read from /dev/video1)`.
- `/dev/video1` is present (`crw-rw---- root:video`), but device presence does not
  establish stream readability.
- Retained metadata artifacts were not treated as fresh evidence.

## Retry edge

Retry `scripts/mesh-uvc-metadata --test` after `/dev/video1` becomes stream-readable,
on camera/USB driver recovery or the next keepalive cycle. Accept only a fresh
nonzero-byte, timestamped read and subsequent organ refresh; do not infer `LIVE` from
retained files.

No software-only repair or substrate change was attempted.

## Verification

The command and device inspection were run live from `/home/mesh-home/lte-workstation`.

## Retry after keepalive

At `2026-09-16T06:55:37Z` the requested keepalive receipt was acknowledged as
`ack:8f16522619a29fdc`. `/dev/video1` remained present as `crw-rw---- root:video`
(`char device`, mode `660`). The retry was then run live at approximately
`2026-09-16T06:56Z`:

```text
scripts/mesh-uvc-metadata --test
```

It exited `1`, again producing ten real-read failures (`metadata read timed out
after 2s from /dev/video1`) and `smoke-test: FAIL (real metadata read from
/dev/video1)`. No nonzero-byte fresh buffer or organ refresh was produced.

The blocker remains `capability`; retry after a camera/USB stream recovery or
the next keepalive cycle. Retained files remain excluded from LIVE evidence.

## Retry after senses consume

At approximately `2026-09-16T07:14Z`, a fresh bounded retry was run live:

```text
scripts/mesh-uvc-metadata --test
```

It exited `1` after ten real metadata-read timeouts from `/dev/video1`, followed by
`smoke-test: FAIL (real metadata read from /dev/video1)`. No fresh nonzero-byte
metadata buffer or organ refresh was produced. The captured command output was
`/tmp/senses-uvc-retry-20260916T0714Z.log`.

The capability blocker is unchanged; retry only after stream recovery or the next
keepalive cycle.

## Retry after exact-owner unblock dispatch — 2026-09-16T07:33Z

The exact-owner task `unblock/senses/ac92903dd430ba20/resolve` was checked eligible
and taken by `senses`. A fresh live retry was then run from this node:

```text
timeout 30s mesh-uvc-metadata --test
```

It exited `1`: all ten bounded reads timed out after 2 seconds from `/dev/video1`,
ending with `smoke-test: FAIL (real metadata read from /dev/video1)`. A bounded
production refresh (`timeout 45s mesh-uvc-metadata`) also exited `1` after repeated
timeouts. No fresh production organ artifact was produced; the retained files remain
excluded from LIVE evidence. The captured production output is `/tmp/uvc-diagnosis.out`.

Typed block: `capability`; needs a stream-readable `/dev/video1` or camera/USB
recovery; retry edge is `mesh-uvc-metadata --test` after the next keepalive or stream
recovery, followed by a production refresh and timestamp inspection.

## Retry after senses consume — smoke pass, organ refresh blocked

At approximately `2026-09-16T07:22Z`, the fresh test-only probe passed:

```text
scripts/mesh-uvc-metadata --test
smoke-test: ok (real one-buffer metadata read: 3410 bytes, 155 timestamped records from /dev/video1)
```

The subsequent production refresh was attempted with `timeout 15s mesh-uvc-metadata`.
It timed out (`rc=124`) after visible metadata-read timeouts; the existing organ files
remained at their earlier `2026-09-16T07:20:19Z` timestamps (`latest.bin` 594 bytes,
`latest.jsonl` 3294 bytes). Therefore the test-only success does not establish a fresh
production organ refresh, and the resolver remains capability-blocked.
