# Discover receipt: Note3 AudioFlinger dump — 2026-09-16

## Action

The canonical task-ledger create for `discover-note3-audioflinger-20260916/probe-note3-audioflinger`
was attempted before the probe but timed out after 25 seconds; no matching ledger line was found in
`~/.mesh/chat.log`. The bounded read-only probe was nevertheless executed because the attached device
was live and this was the one concrete frontier action for the wake.

Command:

```text
adb -s 4d00553d61ab90b7 shell dumpsys media.audio_flinger
```

## Material price and result

ADB device predicate: **1/1** (`SM_N900`, transport `usb:1-3`, state `device`).
Audio-flinger acceptance predicate: **1/1** — output is 2,120 bytes, includes clients, global
session refs, `Hardware status: 0`, an output thread, 48 kHz stereo PCM16 configuration, and four
parseable audio tracks. This is a proven read-only Note3 audio telemetry seam; no phone state was
mutated and no consumer was wired.

Raw capture: `/tmp/discover-note3-audioflinger-20260916.txt`

Raw capture SHA-256: `404a9395c637e8180d66870cd211a1ef3b0f0c3ebff9906950c12f852debc730`

Retry edge: rerun after ADB transport loss or a changed `media.audio_flinger` service/output.
