# UVC metadata stream organ

The UVCH metadata endpoint on `/dev/video1` is a separate diagnostic organ from the camera image
endpoint. The discovery artifact at
`/home/mesh-home/.mesh/knowledge/capability-uvc-metadata-stream-vid1871-0142-mesh-home-20260909.md`
records one accepted 5,874-byte capture (1/1) and sample SHA-256
`81aac71c51cb19921bf039bccfffd188d80a59eddab564c4eccc9d686b1dce94`.

`scripts/mesh-uvc-metadata` now validates the Linux `uvc_meta_buf` framing before replacing its raw
capture and publishes a sibling `latest.jsonl`. The parser reads the little-endian monotonic
nanosecond timestamp, USB frame number, header length, flags, and exact copied UVC payload header.
The timestamp remains explicitly monotonic; the organ does not label it UTC. For the supplied
sample, each 12-byte UVC header occupies a 22-byte driver record, so all 5,874 bytes parse as 267
complete records. The command `mesh-uvc-metadata --parse FILE` exposes the same validation/parser for
retained samples.

The `--test` path still performs a real bounded read from the selected device, then requires the
returned bytes to parse as at least one complete record. Runtime reads make up to ten individually
bounded attempts, reject malformed nonempty streams, and retain the prior raw/JSONL pair on read or
parse failure. The existing mesh wiring declares the physical metadata endpoint in `mesh-card`,
probes it through `mesh-organ-keepalive`, routes `uvc-metadata` and `camera-metadata` through
`mesh-organ`, and schedules the wrapper every ten minutes.

Verification on 2026-09-12:

- `bash -n scripts/mesh-uvc-metadata tests/test-mesh-uvc-metadata.sh` passed.
- `bash tests/test-mesh-uvc-metadata.sh` passed parser framing/truncation, transient retry,
  malformed-stream retention, the missing-device and bounded-hang gates, and a real `/dev/video1`
  capture: 968 bytes / 44 timestamped records.
- A separate runtime capture produced `/home/mesh-home/.mesh/uvc-metadata/latest.bin` (3,762 bytes,
  SHA-256 `a4192e74993d6252c77d4801e55545a6d68f5ec55ee57d837cbf08e83ca167d0`) and
  `/home/mesh-home/.mesh/uvc-metadata/latest.jsonl` (171 records).
- Parsing the supplied discovery sample returned 267 JSONL records.
- After landing, the installed copy passed its real-device `--test` at 6,556 bytes / 298 records.
  `mesh-organ --where uvc-metadata` resolved locally, and `mesh-organ uvc-metadata` captured 6,204
  bytes / 282 records through the router. An isolated `mesh-organ-keepalive --status` card containing
  only `uvc-metadata` reported `mesh-home:uvc-metadata — LIVE`. The existing ten-minute cron line
  remains singular.
- The latest routed capture is `/home/mesh-home/.mesh/uvc-metadata/latest.bin` (6,204 bytes,
  SHA-256 `32b7efedc8d0d84370ebf5fe60dc5c5cba28bf9323e118072d8c02c66eea7413`) with a paired
  282-record `latest.jsonl`.

The first deployment inspection found `~/.local/bin/mesh-uvc-metadata` was an older independent copy
without the retry or parser changes. `mesh-land` deployed the reviewed version; its SHA-256 now
matches `scripts/mesh-uvc-metadata`. The commits were pushed to `origin/main`, and the remote ref was
verified equal to the local landed head.
