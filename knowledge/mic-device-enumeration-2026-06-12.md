# mic detector: enumerate capture devices, don't hardcode plughw:0,0

Date: 2026-06-12
Tools: `scripts/mesh-card` (mic_real), `scripts/mesh-doctor` (mic organ probe)

## The bug

Both mirrored mic probes hardcoded `-D plughw:0,0`. On ds the only working capture
device is the USB card at index 1 (`plughw:1,0`, verified 13:11 rotation: real 64KB WAV),
while card 0 is absent/dummy — so `mic_real` failed and the card declared
`senses: ble wifi` on a node that can hear. A capability the mesh HAS but hides:
the inverse of a hollow organ, equally wrong (consumers opt in by reading the card).

## The fix

Enumerate every capture device from `arecord -l`:

```bash
devs=$(arecord -l 2>/dev/null | sed -n 's/^card \([0-9]\+\): .*device \([0-9]\+\):.*/\1,\2/p')
```

and probe each `plughw:$dev` until one yields a frame OR a busy error (busy = real,
a voice agent holds it). Doctor's `mic_cap` accumulates stderr across devices
(`: >"$mic_err"` then `2>>`) so the busy→WARN branch still sees a busy error from an
earlier device. Doctor now reports WHICH device passed: `mic captures (plughw:1,0)`.

## Verification (both nodes, live)

- `bash -n` both tools: clean.
- IdeaPad (no regression, busy branch): card 0 held by live mesh-converse →
  `Subdevices: 0/1`; refreshed card still declares `mic`. invariant-check OK.
- ds (the fix target): sed parse → `1,0`; raw capture rc=0, 32044 bytes
  (exactly 1s @ 16k mono S16 + 44B header — real frame, not a stub);
  card refreshed: `senses: ble wifi mic` (was `ble wifi`, stale since 04:04).
  invariant-check OK. Live `mesh-doctor` run: `PASS mic captures (plughw:1,0)`.

## Gotchas found on the way

- **Non-login ssh PATH ate the first refresh silently**: `ssh ds "mesh-card --refresh"`
  failed with command-not-found, but stderr was discarded → looked like the fix didn't
  work when actually the card was never refreshed. Use `~/.local/bin/mesh-card` full
  path over raw ssh (same class as the 12:59 "claude missing" false alarm on ds).
- ds `mesh-ear --test` FAIL is UNRELATED: missing whisper.cpp at
  `~/.mesh/whispercpp/main` (dependency gap, not device). Left open.
- Doctor's secondary check ("DEFAULT device broken") still WARNs on ds — correct:
  ALSA default there genuinely doesn't capture; tools should pass explicit `-D`.
