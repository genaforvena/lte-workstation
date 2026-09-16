# unblock/adint/43a6d0cff44e1fc4/resolve — 2026-09-16

## Result

BLOCKED: the real UVC metadata endpoint is intermittently readable, but the
production refresh did not obtain a fresh buffer.

## Evidence

- `mesh-uvc-metadata --test` at 2026-09-16T07:48Z exited 0 after three timeout
  messages and reported one real buffer: 3410 bytes and 155 timestamped records
  from `/dev/video1`.
- The immediately following `mesh-uvc-metadata` production refresh exited 1
  after 10/10 reads timed out; it did not replace the retained artifacts.
- Retained files were explicitly not treated as LIVE: `latest.bin` mtime
  2026-09-16 07:46:18Z, 6116 bytes, SHA-256
  `c2b9f2c9fba0e73c801e5e0864eca760b49030f79a5ab5cbb5a8a40d8e645626`;
  `latest.jsonl` mtime 2026-09-16 07:46:18Z, SHA-256
  `9af3b1a0e695134d7aee04300f5d63fc43afa846ef182704699045c0a5cdd41a`.

## Exact retry edge

After camera/USB stream recovery or the next keepalive cycle, run
`mesh-uvc-metadata --test`; only if that real read passes, run
`mesh-uvc-metadata` and verify fresh timestamps and non-empty `latest.bin` plus
`latest.jsonl` before resuming the parent.
