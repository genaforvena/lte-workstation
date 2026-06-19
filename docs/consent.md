# Consent & recording indicator

The project's single non-negotiable rule:

> only things you own or are authorized for, no effect on anyone who didn't consent, everything auditable.

This document turns that prose into implementation boundaries that every sensing script must enforce.

## What this covers

Any script that captures sensor data from a space where a person other than the operator may be present — microphone, camera, webcam, or any ambient sensor that can identify or track people. This includes:

- `mesh-blessyou` — always-on mic, energy-detection loop
- `mesh-ear` — always-on mic, wake-word reflex (opt-in consent already built in)
- `mesh-converse` — on-demand mic, voice conversation
- `mesh-eye` — consent-gated camera/mic ambient sense; reduces each capture to abstract signals
  (light/sound/motion) and keeps **no** raw frame or audio. The dedicated still-camera organ is
  `mesh-camera`.

## Consent file: `~/.mesh/consent`

A simple key=value file, one key per sensor class. Default is **off** for always-on capture; one-shot capture requires a `--consent` flag or a file entry.

```
mic = yes                  # on-demand mic use (mesh-converse, genius-loci phone mic)
mic_always = yes           # always-on mic (mesh-blessyou, mesh-ear --listen)
camera = yes               # camera/webcam capture (genius-loci)
scope = room               # what is being sensed and why (human-readable)
```

- A script that provides `--listen` (always-on) **must** refuse unless `mic_always = yes` is present.
- A script that provides `--once` or single-use capture **must** refuse unless `mic = yes` or `camera = yes` is present (or an explicit flag overrides).
- `mesh-ear --consent` shows the current consent state.

## Announce on start

When any sensing script starts (or begins capturing after idle), it **must**:

1. Speak a short announcement via `mesh-say` (e.g. "mic is listening in this room") if `mesh-say` is available.
2. Write a start event to `mesh-trace` (see Audit below).
3. If a phone body is available, flash the **torch** 3 times (`termux-torch on` / `termux-torch off` with 0.5s gaps) as a visible indicator.

## Recording indicator

While actively capturing:

- **Phone body**: torch stays on during capture; turns off when capture ends.
- **Laptop/node**: `mesh-trace` marks every capture cycle start/stop.
- Log to console with the local time so anyone with access to the terminal can see the script is live.

## Audit trace

Every sensing script must write structured marks to `mesh-trace`:

```
[start] <script> began capturing <sensor> on <host> at <time>
[stop]  <script> stopped capturing <sensor> on <host> at <time>
```

Capture-loop scripts write a start mark on launch and regular heartbeat marks (`[running] <script> alive N min`). One-shot scripts write both start and stop.

The audit trail already covers speech (`mesh-say`, `mesh-tts`); this closes the gap on the capture side.

## Boundary

Scripts must enforce the boundary at the code level (not only in comments):

- Never identify, profile, or track people.
- Refer to anyone present only as abstract presence (e.g. "someone is in the room").
- Sanitise transcription text before passing to an LLM — strip names, identifying context.
- Retain no raw audio or images beyond the current capture cycle.

## Enforcement

| Script | Consent | Announce | Indicator | Trace |
|--------|---------|----------|-----------|-------|
| `mesh-blessyou` | ✅ `mic_always` gate (genome; not cron-wired) | ✅ | ✅ torch | ✅ start/stop/heartbeat |
| `mesh-ear` | ✅ `mic` / `mic_always` (built-in) | ✅ | ✅ torch | ✅ start/stop/heartbeat |
| `mesh-converse` | ✅ `mic` gate | ✅ | ✅ torch | ✅ start/stop |
| `mesh-hear` | ✅ `mic_always` gate | ✅ | ✅ torch for phone | ✅ start/stop |
| `mesh-eye` | ✅ `camera`/`mic` gate — STRUCTURAL, refuses `rc=3` (sandbox-tested in `--test`) | ✖ no `mesh-say` | abstract signals only, **no raw frame kept** | → `~/.mesh/eye.log` (not `mesh-trace`) |
| `genius-loci` | ✅ `camera` gate (+`mic` when using phone mic) — STRUCTURAL, refuses `rc=3` | ✅ `mesh-say` ("this room is being watched by the mesh") | ✅ torch (phone, 3 flashes) | ✅ `[sense]` start/stop via `mesh-trace` |
| `mesh-transcribe-organ` | n/a (processes caller-provided WAV) | n/a | n/a | n/a |
