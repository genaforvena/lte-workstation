# Organ exercise — IdeaPad mic, signal + concurrency (2026-06-12T20:54Z)

NOTE: a concurrent agent wrote organ-exercise-mic-2026-06-12.md (format-only check, 2s WAV).
This pass adds what that one didn't: live-signal verification and the busy-vs-exclusive finding.
Not a duplicate — complementary.

## mic (arecord, ALC236 card 0) — ✅ LIVE, signal-verified

- Concurrent 3s capture while converse held the device: `/tmp/mic-organ-*.wav`,
  RIFF/WAVE PCM 16-bit mono 44100Hz, 264644 bytes, 132300 frames.
- **Signal is real, not silence: peak=852, rms=263** (quiet ambient room). A dark mic reads
  peak=0 (cf. default-string's deaf Zoran in docs/organ-verification). The other agent's note
  confirmed format but not that the capture carries actual audio — this closes that gap.

## Finding: "mic busy" WARN means shared, not unavailable

The mic was held by converse (PID 1772470) + its `arecord -D default -r 16000` (PID 1772477)
on `/dev/snd/pcmC0D0c`, yet a second reader still got a live stream — ALSA default does
shared capture (dmix/dsnoop). So mesh-doctor's persistent "mic busy" WARN is correctly
cautious but, on this node, the mic is simultaneously usable. Recording the fact; not
proposing a doctor change (the WARN can't assume sharing is configured everywhere).

## Declared-sense sweep complete (today)

All 6 artifact-verified: ble (9-dev scan), camera (640×480 JPEG), wifi (23 APs),
lid (ACPI open), power (AC 95%), mic (this, signal-verified). Zero declared-but-dark.

Tree: artifact in /tmp only; no genome change. Steward lands the knowledge note.
