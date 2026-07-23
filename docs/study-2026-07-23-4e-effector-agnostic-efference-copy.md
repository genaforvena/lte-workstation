# Study finding — effector-agnostic efference copy (enactivism / 4E cognition)

**Source:** auto idea-queue task — LITERATURE (live review): enactivism & 4E cognition, from the angle of
a RECENT result (2023–2026) (2026-07-23).
**Verdict:** Finding + concrete proposal for `scripts/mesh-overhear` (+ `mesh-note3-say` emission mark).
**BUILT 2026-07-23** (same day, genome baton turn): the emission mark already existed — EVERY speech organ
(`mesh-note3-say` deadline-epoch flag, `mesh-voice-tx`/`mesh-say`/room-music touch-style) writes
`~/.mesh/mesh-speaking`; the one missing wire was the wake-mint gate. `_self_emitting_now()` added to
`_wake_should_mint` (RED-first: fresh mark vetoes the mint, expired/stale mark fails OPEN so a leaked
flag can never make the mint permanently deaf). The `~/.mesh/self-emitting` mark proposed below was
therefore NOT created — `mesh-speaking` IS that mark; adding a second one would be a duplicate contract.
**Date:** 2026-07-23 · owner: genome

## The concept, and what's recent

Sensorimotor / enactive perception: perceiving is constituted by mastery of **sensorimotor contingencies**
— the lawful way sensation changes as a function of the agent's OWN action — which requires the agent to
hold an *efference copy* and cancel self-caused (reafferent) sensory change so only world-caused
(exafferent) change drives perception. Live 2025 sources:

- *Sensorimotor Contingencies and the Sensorimotor Approach to Cognition*, arXiv 2510.14227 (Oct 2025) —
  <https://arxiv.org/pdf/2510.14227>: reaffirms perception as a skill-laden, action-coupled relationship;
  notably still *conceptual* — it does not ship an algorithm, which sharpens rather than weakens the
  transfer: the operational move is ours to make.
- *G-systems and 4E Cognitive Science*, arXiv 2501.04125 (Jan 2025) — <https://arxiv.org/pdf/2501.04125>.
- *Mechanisms of skillful interaction: sensorimotor enactivism & mechanistic explanation*, Philosophical
  Psychology 38(5), 2024/25 — <https://www.tandfonline.com/doi/abs/10.1080/09515089.2024.2302509>.

## Why the core idea is MOSTLY embodied — and where the real residual gap is

Honest check first: the mesh already embodies the SMC principle substantially. `mesh-overhear` explicitly
does NOT classify its own TTS as speech, mutes the ambient classifier during our own playback, and gates
wake-minting on `_bose_foreign_now` (`scripts/mesh-overhear:152,743,782,1635`). That IS reafference
cancellation. So this is not a wholesale new concept — it is the ONE residual the recent framing exposes.

**The residual gap:** the efference copy is tied to a single EFFECTOR CHANNEL, not to the agent's emission
ACT. `_bose_foreign_now` / `_self_playing` consult the Bose pipewire sink only (they scan `wpctl status`
for the Bose sink and the local `pw-play` pid). But the mesh also speaks in the same room through
**`mesh-note3-say`** — a physically separate Note3 speaker driven over adb, NOT on the pipewire Bose sink —
and through clone-voice routed to non-Bose sinks. Those emissions are **invisible** to the self-emission
gate, so the room ear can hear the mesh's OWN Note3 voice as world-caused speech. Memory corroborates the
hazard is live (the room false-wake storm; "never wrap note3-say in touch/rm").

## Concrete proposal — `scripts/mesh-overhear` + `scripts/mesh-note3-say`

Make the efference copy effector-agnostic (perceive-around the agent's action, not around one sink):

- **Emission mark:** every speech organ (`mesh-note3-say`, `mesh-voice-say`/clone, plus the existing Bose
  path) writes `~/.mesh/self-emitting` with an expiry = utterance duration + slack on start.
- **Generalize the gate:** replace `_bose_foreign_now`'s Bose-only check with `_self_emitting_now()` =
  Bose-sink-playing OR a fresh `~/.mesh/self-emitting` mark. Wake-minting and the ambient classifier
  consult the ACT, so self-speech through ANY effector is canceled — the exafference/reafference split the
  literature makes central.
- **Test:** with the mark fresh, a "меш"-containing chunk must NOT mint a wake; with it expired, it must.
  (RED-first: today a Note3-emitted wake word passes.)

## Disposition

Filed as a proposal, not landed. It is a two-file contract (emitter writes the mark, ear reads it) in a
129KB load-bearing organ; correct move is to define the mark contract and the RED-first test before code.
Cited to current (2025) sources, concrete, and a genuine residual — not the already-embodied Bose gate.
