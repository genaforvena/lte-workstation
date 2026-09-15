# Health warning triage: intermittent UVC metadata read

Task: `health-warning/e6244edc541371af423d/triage`  
Source warning: 2026-09-12T10:59:37Z health FYI

## Live evidence at 2026-09-14 19:52Z

- `/dev/video0`, `/dev/video1`, and `/dev/media0` still exist; `v4l2-ctl --list-devices` lists the
  USB2.0 camera on all three nodes.
- A fresh bounded `mesh-organ --node mesh-home uvc-metadata --test` produced three consecutive
  two-second `/dev/video1` read timeouts, then succeeded with a real 1,914-byte buffer containing
  87 timestamped records and exited 0. The result shows current intermittent availability, not a
  steady stream.
- The refreshed 19:52Z `mesh-dash --once check` reports 13 live organs and zero dark organs. That
  is consistent with the recovered sample but does not erase the three timeouts preceding it.
- The existing `uvc-metadata-runtime-retry-20260912.md` documents the bounded retry behavior and
  prior real-read recovery. The earlier `health-warning-66e9df8ef104ade075fb-20260912.md` already
  classifies the same startup/read timeout pattern as intermittent, with successful and failed
  captures and no attributable writer for the latest-file path.

## Disposition

The device remains present and can produce valid metadata after retry, while per-run startup/read
timeouts remain reproducible. This is the known intermittent UVC blind, not evidence of stable
health or of a newly identified camera fault. Keep it visible as intermittent; do not restart
services, power-cycle the camera, or change sensor configuration based only on a recovered test.
Retry on a scheduled capture that exhausts its bounded reads or produces another empty/invalid
artifact, then compare its invocation output with the organ/pane state. No device or substrate
state was changed.

## Verification

- `ls -l /dev/video*`: video0 and video1 are present.
- `v4l2-ctl --list-devices`: camera lists video0, video1, and media0.
- `mesh-organ --node mesh-home uvc-metadata --test`: three timeouts, then 1,914-byte/87-record
  real read, exit 0.
- `mesh-dash --once check` at 19:52Z: 13LIVE/0DARK.
- Compared with the existing runtime-retry and prior health-triage receipts; no prior completed
  task was reopened and no actuator was used.
