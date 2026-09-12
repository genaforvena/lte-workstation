# Health warning triage: intermittent UVC metadata capture

Task: `health-warning/9acbe26cce46544962c3/triage`

## Current evidence

- The warning describes the UVC metadata source as currently healthy, while noting intermittent
  V4L2 stream-start timeouts. It cites a prior fresh 10,120-byte sample dated 2026-09-10.
- `mesh-uvc-metadata --test` exited 0 on 2026-09-12 and read a real one-buffer sample of 7,524
  bytes, parsed into 342 timestamped records from `/dev/video1`. The script uses a private temp
  file in test mode, so this result does not forge the durable capture log.
- A separate normal `mesh-uvc-metadata` invocation exited 1: two reads timed out after 2 seconds,
  then eight attempts returned empty metadata buffers. This confirms the intermittent failure is
  still live, rather than only historical.
- The canonical artifact was independently parseable afterward: `latest.bin` was 1,936 bytes,
  mtime `2026-09-12 13:14:10 UTC`, SHA-256
  `e9cea6c27ab8fc49c2b8ffb30e922bed76bdd75f99a83dd3a6e17344797b8885`, and
  `mesh-uvc-metadata --parse` produced 88 timestamped records.
- `~/.mesh/reflexes.cron` contains the live `*/10 * * * * ... mesh-uvc-metadata` schedule. During
  this check a separate `mesh-uvc-metadata` process was visible while the manual invocation was
  reporting empty buffers, and the canonical artifact mtime advanced at 13:14:10. Its successful
  output recorded a capture after retries. This establishes concurrent activity, but the available
  log does not attribute the resulting artifact to a specific invocation or prove that concurrency
  caused the manual failure.

## Verdict

The organ is wired and can produce parse-valid timestamped records, but startup/read failures still
occur. Current health is therefore **intermittently live with a known attribution blind**: the
manual read failed while another reader was active, and a fresh canonical file alone cannot identify
which invocation produced it. No camera, routing, or other substrate state was changed. Do not claim
the timeouts are fixed. If overlapping invocation failures recur, add per-run attribution or
single-writer locking at the capture boundary before inferring device failure from the final file.

## Verification

Recomputed the canonical artifact hash, checked its byte count and mtime, independently parsed it
into 88 records, inspected the real-read test implementation (private temporary artifact), and
confirmed the reflex schedule in `~/.mesh/reflexes.cron`. The normal capture's exit code was 1; the
test probe's exit code was 0.
