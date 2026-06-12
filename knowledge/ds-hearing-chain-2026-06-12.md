# ds hearing chain brought live: whisper.cpp planted + strongest-model probe

Date: 2026-06-12
Tools: ds organ install (no genome change) + `scripts/mesh-transcribe-organ` (genome fix)

## What was dead

ds had the full audio tool stack deployed (mesh-ear/hear/transcribe/transcribe-organ) and —
after the mic-detector fix (see [[mic-device-enumeration-2026-06-12]]) — a declared, working
USB mic. But two smoke FAILs kept the chain dead:

1. `mesh-ear`: no whisper.cpp at `~/.mesh/whispercpp/main` — dependency never planted.
2. `mesh-transcribe-organ`: hardcoded `ggml-large-v3-turbo.bin` (1.6GB) as its default
   model despite its own header saying "uses the strongest **installed** model". A node
   with only base.bin was dead-by-default on a model it never had.

## What was done

- **Planted whisper.cpp on ds by copying from IdeaPad** (both x86_64; binary deps are only
  libstdc++/libm/libc): `main` (1.1MB) + `for-tests-ggml-tiny.bin` (spot model) +
  `ggml-base.bin` (148MB) + `samples/jfk.wav`. No compile needed.
- **Genome fix** in mesh-transcribe-organ: `strongest_model()` probes
  turbo → base → base.en → tiny and uses the first present; `MESH_TRANSCRIBE_MODEL`
  still overrides; nothing-installed falls through to the canonical turbo path so the
  smoke error names the right ask.

## Verification (real artifacts, both nodes)

- ds raw whisper: jfk.wav → "And so, my fellow Americans, ask not what your country can
  do for you, ask what you can do for your country." rc=0 (also proves no CPU
  instruction-set mismatch from the IdeaPad-built binary).
- ds `mesh-ear --test`: ok, rc=0 (was FAIL).
- ds `mesh-transcribe-organ --test`: ok; real run on jfk.wav → full correct sentence
  via ggml-base.bin.
- IdeaPad no-regression: smoke ok; real run picks turbo and transcribes correctly.
- ds `mesh-doctor`: "all applicable --test smoke checks pass" (was 2 smoke FAILs).
  Remaining ds FAILs are the unrelated log error-line triage (chat-sync/doctor/mind-watch).

## ds capability delta (one tick)

Before: card said `senses: ble wifi`, no transcription possible.
After: card says `senses: ble wifi mic`; capture (plughw:1,0) + whisper transcription
verified end-to-end. ds can hear and transcribe. Continuous listening stays
consent/operator-gated as before — this is capability, not activation.
