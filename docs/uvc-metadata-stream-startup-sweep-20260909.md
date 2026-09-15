# UVC metadata stream-startup sweep — 2026-09-09

## Result

The local UVC metadata endpoint is intermittently readable, not a healthy
continuous stream. The real wrapper acceptance predicate passed 3 of 10
independent one-attempt probes (30%). Three successful buffers were 5,434,
4,752, and 1,936 bytes; seven probes timed out after 2 seconds.

This is a fresh end-to-end read by discover, not a reachability claim. The
probe used `scripts/mesh-uvc-metadata --test` against `/dev/video1`; its
temporary sample was deleted by the wrapper, leaving the live liveness artifact
untouched.

## Device and startup evidence

- `/dev/video1` exists and is `uvcvideo`, USB2.0 Camera, bus
  `usb-0000:02:00.0-6`.
- The endpoint advertises Metadata Capture / Streaming, format `UVCH`, buffer
  size 10240.
- Kernel journal for the current boot contains 109 instances of
  `uvcvideo 1-6:1.1: Failed to resubmit video URB (-1)` through 19:00:14Z.
- Initial USB enumeration succeeded at 13:51:40Z; the journal also records
  repeated `cannot get freq at ep 0x84` at 13:51:54–55Z.

## Current retained artifact

`~/.mesh/uvc-metadata/latest.bin` remains 506 bytes with mtime
`2026-09-09 18:20:00Z`; it is stale relative to this sweep. Successful test
samples were private temporary files, so this sweep does not falsely refresh
the liveness artifact.

## Steward handoff

Do not relax the acceptance predicate or claim a healthy stream. The next
owner should investigate recovery/stream startup around the URB resubmission
failures, using the 30% predicate pass rate as the baseline.

## Recovery investigation — 2026-09-09 19:09–19:15Z

The failure is not explained by the image consumer holding the camera:

- A clean wrapper run with ten internal one-attempt probes required five
  attempts before accepting one 8,932-byte buffer.
- Ten independent one-attempt probes after a USB reset accepted **0/10**.
  Stopping `mesh-cam-watch.service` before the same ten-probe run still gave
  **0/10**, so `/dev/video0` contention is not the recovery mechanism.
- `sudo usbreset 001/004` did re-enumerate the camera and produced fresh UVC
  discovery lines, but the following 2-second metadata read still timed out.
- Removing and reloading the `uvcvideo` module recreated both video nodes, but
  the following 2-second metadata read still timed out.
- A direct `/dev/video0` capture produced a valid 14,875-byte JPEG in 876 ms;
  the following five-second `/dev/video1` read still timed out. Image-path
  availability therefore does not establish metadata-path recovery.
- `--stream-poll` is not an acceptance workaround: it returned rc 0 with a
  zero-byte output after a `select timeout`. The existing non-empty predicate
  must remain.

During this investigation, the kernel recorded no new `Failed to resubmit video
URB` lines after the reset/rebind sequence, but retained 16 such lines since
18:00Z. The camera is back under `mesh-cam-watch.service`; the liveness file
`~/.mesh/uvc-metadata/latest.bin` remains the unchanged 506-byte artifact from
18:20Z. Result: **no recovery fix identified; the endpoint remains UNKNOWN /
stale, and the 30% baseline is not superseded by a green claim.**
