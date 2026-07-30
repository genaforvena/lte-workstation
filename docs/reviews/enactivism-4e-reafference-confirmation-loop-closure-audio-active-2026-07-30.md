# Enactivism/4E live review — reafference CONFIRMATION (the loop-closure half we left out)

**Date:** 2026-07-30 · **Area:** enactivism & 4E cognition · **Angle:** a foundational idea applied
TOO LOOSELY · **Landed in:** `scripts/mesh-audio-active` (`--confirm`, uncommitted — steward lands).

## The idea, and where we read it too loosely

The mesh already cites the reafference principle in `mesh-audio-active`: separate sensory input the
agent's OWN action caused (**reafference**) from input the world caused (**exafference**) via a copy of
the motor command (the **efference copy**). But we used it in ONE direction only — **subtract** our own
sound so it doesn't masquerade as room activity (`source=self|external`). Von Holst & Mittelstaedt's
principle (1950) and sensorimotor-contingency **mastery** (O'Regan & Noë 2001; the sensorimotor-approach
review arXiv:2510.14227, 2025; *Toward Enactive AI* arXiv:2605.24238, 2026) are constitutively about a
**prediction that must be CONFIRMED**: the efference copy predicts a sensory consequence, and perceptual
mastery *is* that consequence reliably arriving. The other half of "subtract your own sound" is
"…and if your own predicted sound is **missing**, your actuator is hollow." We never used it.

Sources:
- [Efference copy / reafference principle — von Holst & Mittelstaedt 1950 (overview)](https://plato.stanford.edu/entries/action-perception/)
- [Pak, Sensorimotor Contingencies and the Sensorimotor Approach to Cognition, arXiv:2510.14227 (2025)](https://arxiv.org/abs/2510.14227)
- [Toward Enactive Artificial Intelligence, arXiv:2605.24238 (2026)](https://arxiv.org/abs/2605.24238)
- [Straka/Simmons/Chagnaud, Predictive Sensing, PMC6733654 (2019)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6733654/)

## The concrete gap in the genome

`mesh-audio-active` trusts `/proc/asound … state: RUNNING` as proof sound is emitting — but RUNNING is
the record that the mesh **commanded** playback (the efference copy itself), not that sound left the
speaker. `mesh-sink-health` closes the loop for exactly **one** fault — the PipeWire broken-pipe wedge —
**by log signature**, and its header EXPLICITLY refuses acoustic confirmation ("never by
absence-of-sound", the never-touch-a-working-sink rule). So the whole **silent-speaker fault class** —
muted sink, disconnected/misrouted Bose, zero volume, dead Note3 adb audio (see memories
[[bose-usb-sink-is-not-speaker-sounds]], [[mesh-home-audio-stack-down-note3-ear]]) — leaves the
substream RUNNING, emits no wedge log, and reads `PLAYING source=self` here + HEALTHY there while the
room is dead silent. **Nobody checks the predicted reafference actually arrived.**

## The mechanism landed (`--confirm`, report-only, reuses the calibrated ear)

When a `source=self` stream is RUNNING, sample the room mic through the existing calibrated ear
(`mesh-ambient-level`, RMS→SILENCE/QUIET/MODERATE/LOUD, exit 2 honest) and close the loop:

```
confirm=heard    predicted reafference arrived (mic QUIET/MODERATE/LOUD) → actuator VERIFIED
confirm=unheard  sink RUNNING yet the room is SILENT → HOLLOW actuator (silent-speaker fault; a
                 working speaker mid-TTS/-music is never dead-silent)
confirm=n/a      not self-emitting, nothing running, or mic unreachable — nothing to / cannot confirm
```

It is **report-only** (no heal/kill/post): silence is normal, so `unheard` is a FLAG for a human eye,
never an auto-action — respecting `mesh-sink-health`'s never-touch rule. Only `source=self` is
confirmable (an external stream has no efference copy predicting a level → `n/a`, so a quiet human video
is never mis-flagged). This is the mesh's own **Verification Principle** in acoustic form: `PLAYING` is a
claim; *the mic heard it* is the artifact.

## Verification (RED→GREEN, mutation-verified)

`mesh-audio-active --test` gains 7 assertions (`confirm_of` + `read_mic_level`, 20 total). The
load-bearing pair: self+RUNNING splits on the mic alone. Seen RED, both live:
- Mutate `confirm_of` to ignore the mic (always `heard`) → fixture (m) `self+SILENCE` no longer reads
  `unheard` → RED (exit 1). Restored → GREEN.
- Delete the `self=1` guard → fixture (o) `external+SILENCE` reads `unheard` instead of `na` → RED
  (exit 1). Restored → GREEN.

Both `self_emitting` (efference copy) and `read_mic_level` (the ear) are injectable via env
(`MESH_AUDIO_ACTIVE_SELF` / `MESH_AUDIO_ACTIVE_MIC`), so the classifier is falsifiable without hardware;
the live `--confirm` path does the real /proc read + mic sample (verified live: nothing playing →
`confirm=n/a`, mic SILENCE −48 dB on this node's webcam mic).

## Why this file, not a new organ

The confirmation reuses `mesh-audio-active`'s own substream read and its `source=self` verdict — the
efference copy is already computed here; `--confirm` just adds the sensory-consequence check against a
mic the node already exposes. A separate organ would duplicate the /proc parse and split the
reafference story across two tools. Report-only, opt-in verb — the fast default `/proc` path is
untouched.
