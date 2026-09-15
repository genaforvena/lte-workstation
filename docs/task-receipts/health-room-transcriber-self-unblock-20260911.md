# Health room-transcriber self-unblock receipt — 2026-09-11

Task: `health-room-transcriber-self-unblock-20260911/attempt-safe-room-transcriber-revival`

## Diagnosis

- `mesh-overhear.service` was active since 2026-09-09 and was producing fresh
  `~/.mesh/audio-buffer/*.wav` chunks.
- Both candidate room transcribers were inactive: `mesh-room-gigaam.service`
  and `mesh-room-transcribe.service`.
- The intended organ is GigaAM: its unit declares
  `Conflicts=mesh-room-transcribe.service`, so starting it cannot run the
  retired Whisper replacement concurrently.
- The prerequisite was present: `/home/mesh-home/.venv-ai` imported both
  `gigaam` and `torch`; CUDA was available on an NVIDIA GeForce RTX 3060 with
  3885 MiB free of 12288 MiB.

## Action

Ran the real-read gate:

```text
timeout 90s /home/mesh-home/.local/bin/mesh-room-gigaam --test
pass: real read -> 'привет это проверка комнаты'
pass: rms gate (silence 0 < 120 <= speech 4937)
pass: prune drops >10min, keeps fresh
TEST_RC=0
```

Then revived and persisted the designated unit:

```text
systemctl --user start mesh-room-gigaam.service
systemctl --user enable mesh-room-gigaam.service
```

## Verification artifact

At 2026-09-11 15:27:12 UTC the journal reported:

```text
mesh-room-gigaam: model up (cuda=True)
```

At 15:27:23 UTC:

- `systemctl --user is-active mesh-room-gigaam.service` = `active`
- `MainPID=2267042`, `NRestarts=0`
- `systemctl --user is-enabled mesh-room-gigaam.service` = `enabled`
- `mesh-room-transcribe.service` = `inactive` (the conflict invariant holds)
- `~/.mesh/room-transcript.txt` mtime = `2026-09-11 15:27:23 UTC`, size 2977
- `~/.mesh/.room-gigaam-last` mtime = `2026-09-11 15:27:23 UTC`, value `1789140423`
- transcript contains fresh entries through `[15:27:03]` from the live audio buffer.

`mesh-health` at 15:27:46 still reports `mesh-home PASS`. Its unrelated
offline fleet rows are not part of this room-ear recovery.

Disposition: room transcriber revived; no irreducible authority boundary
remains for this dispatched action. The unit is now enabled for user-session
startup so the fix survives a reboot.
