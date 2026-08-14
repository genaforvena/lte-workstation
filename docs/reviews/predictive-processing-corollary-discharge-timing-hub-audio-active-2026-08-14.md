# Predictive processing / Bayesian brain — live review: the corollary discharge has a CLOCK, and it is recalibrated at ONE hub

**Date:** 2026-08-14 · **Area:** predictive processing & the Bayesian brain · **Angle:** cross-domain
transfer into a distributed sensor mesh · **Landed in:** `scripts/mesh-audio-active` (`--cd`, plus a
behaviour fix to `self_emitting()`; uncommitted — steward lands).

## The source (live, current)

**Martin W. Jarzyna & Bruce A. Carlson, "Developmental and evolutionary changes in sensorimotor
integration to maintain coordination of corollary discharge and afferent input in electric fish",
*Current Biology*, published 11 June 2026, doi:[10.1016/j.cub.2026.04.068](https://doi.org/10.1016/j.cub.2026.04.068)**
(NSF IOS-2203122, NIH F31NS139904).

Found via a live web sweep of 2026 predictive-processing publications; read through the WashU and
phys.org write-ups (the Elsevier full text is paywalled — cited claims below are the ones both
write-ups state, not inferred detail):

- [WashU — "New research reveals how brains update their predictions" (2026-06)](https://source.washu.edu/2026/06/new-research-reveals-how-brains-update-their-predictions/)
- [phys.org — "Brains update sensory predictions through single timing hub, electric fish study finds" (2026-06)](https://phys.org/news/2026-06-brains-sensory-hub-electric-fish.html)
- [Scientific Frontline — study details, funding](https://www.sflorg.com/2026/06/ns06142602.html)

## The concept we did not embody

Corollary discharge — the copy of a motor command sent to sensory areas so predicted self-caused input
is cancelled — is the canonical predictive-processing primitive, and the mesh already has it
(`mesh-audio-active`'s reafference/exafference split, and its `--confirm` loop closure, 2026-07-30).
What we had NOT taken from the literature is that **the corollary discharge is not a flag, it is a
TIMED prediction whose duration must track a self-signal that keeps changing** — and the paper's
finding about *where* that retiming happens:

- Mormyrid electric pulses change duration hormonally (testosterone, over days), developmentally
  (aging), and evolutionarily (across species). The cancellation must be re-coordinated each time.
- Recording **every stage of the corollary discharge pathway within individual fish** ("never before
  has anybody recorded from each area within an individual animal"), the timing shift for *all three*
  kinds of change **first appears at one structure** — the mesencephalic command-associated nucleus
  (MCA), which branches to the three downstream pathways (communication, sensing, signal production).
- So the animal does **not** recalibrate each pathway independently: **one hub is retimed and the
  pathways inherit it.** Fail to retime and self-generated signal swamps the sense, so external input
  cannot be detected at all.

No quantitative timing values are given in the accessible write-ups; the claim transferred here is
structural (one hub, inherited by pathways), not numeric.

## The transfer, and the mesh's actual state

`~/.mesh/mesh-speaking` **is** this mesh's corollary discharge: one shared mark, held while a speech
organ emits, read by the room ear (`mesh-overhear` capture loop, `_self_playing`, `_self_emitting_now`),
`mesh-soundscape`, `mesh-room-music`, `mesh-tuner`/`-metronome`/`-changes` (`MUTE_FLAG`), and by
`self_emitting()` in `mesh-audio-active`. The hub exists. **The recalibration happened at a pathway.**

`mesh-note3-say` learned the timing lesson the expensive way (2026-07-14, comment in-file): a bare
`touch` … `rm` cannot span a duration, so two overlapping speaks let the *shorter* clip's release
unmute the mic over the *longer* one's voice — "observed in room-transcript.txt at 23:41:22 and
23:41:40 — two of 'his' lines were verbatim MY speech." Its fix was exactly the MCA move: put a
**deadline epoch** in the mark and only ever **extend** it (monotone max). That fix never reached the
hub. Verified in the tree today:

| writer | dialect | release |
|---|---|---|
| `mesh-note3-say:107-118` | deadline epoch, monotone-max | reaper, only past the latest deadline |
| `mesh-say:296-298` | empty touch | `trap 'rm -f' EXIT` — **unconditional** |
| `mesh-voice-tx:406,409` | empty touch | `rm -f` — **unconditional** |
| `mesh-overhear:978,996` | empty touch (`open(…,"w")`) | `os.remove` — **unconditional** |

So a `mesh-say` finishing at t+3 deletes a note3-say deadline that runs to t+20: **one pathway's
release cancels another pathway's live corollary discharge**, which is the same fault note3-say already
paid for, resurrected at the level above it.

And the **readers diverge on the same mark**:

- `mesh-overhear:161-171` `_self_emitting_now()` — honours the deadline, and treats a stale
  touch-mark as *not speaking* (fails OPEN, "deafness is never the safe default").
- `mesh-overhear:775` `_self_playing()` and `:1055` the capture loop — bare `os.path.exists`. A leaked
  mark leaves capture **permanently deaf**.
- `mesh-audio-active` was a **third** dialect: a bare `[ -f ]`, so a leaked or expired mark pinned
  `source=self` forever and masked genuine **exafference** from `mesh-room-sense`'s presence fusion
  (`mesh-room-sense:1192-1195` consumes exactly that field).

One mark, three answers. That is the pathology the fish avoids.

## The mechanism landed (`--cd`, report-only)

`scripts/mesh-audio-active` gains **one canonical reading of the hub mark** and an axis that measures
whether the corollary discharge actually *spans* the emission:

- `cd_mark <present> <content> <age> <now> <stale>` — the only place in the tool that knows both live
  dialects: deadline epoch → `held` | `expired`; empty touch → `held` | `stale` by mtime against
  `MESH_SELF_EMIT_STALE` (**the same env knob `mesh-overhear` reads** — one hub, one calibration).
  Staleness fails **open**, matching `_self_emitting_now`.
- `player_alive` — emission evidence *independent* of the mark (`pw-play`/`aplay`/`paplay`). Splitting
  it out of `self_emitting()` is what lets the mark and the emission be seen to come apart.
- `cd_of <player> <mark>` →

```
cd=aligned    mark held while a local player emits — self-sound cancelled at the ear
cd=uncovered  a player is EMITTING with no live mark → the ear is live on our OWN voice
              (self-transcription → the false-wake class). The fish's "swamped by self" fault.
cd=overhang   mark held, no local player — NORMAL for off-node speech (voice-tx on the Bose,
              note3-say over adb), or a writer over-holding. Not a fault.
cd=expired    deadline passed, mark still on disk → the READER DIVERGENCE is live:
              deadline-aware readers fail open, bare-exists readers stay DEAF
cd=stale      touch-dialect mark past the stale window — same divergence
cd=n/a        nothing emitting, no mark
```

**Behaviour fix in the same file (not report-only):** `self_emitting()` now reads the mark through
`cd_mark()` instead of `[ -f ]`. An expired/stale mark no longer pins `source=self`. Direction of
change is fail-open (more willing to report `external`), aligning this tool with
`_self_emitting_now` rather than with the deaf readers.

`--cd` deliberately does **not** read `/proc/asound` and does not inherit its `exit 2`: measured on
this node today, `aplay` runs with every hw substream reading `closed` (PipeWire holds no hardware
sink here), so an ALSA gate would blind the axis exactly where the mesh speaks — through PipeWire and
through remote sinks.

**No write, no reap.** The mark is shared substrate: a wrong release makes the mesh transcribe itself,
a wrong hold makes it deaf. This axis measures the coordination; the hub fix it is evidence for is
below.

## Verification

`mesh-audio-active --test` → **39 assertions, rc=0** (was 20). All six `cd` classes were then driven
**live** against real mark files in a throwaway `MESH_DIR` — the live `~/.mesh/mesh-speaking` was never
written (a test that writes the artifact forges it; here it would also have muted the room ear for
real, and it is confirmed absent after the run):

```
deadline +30s + player      → cd=aligned    (mark=deadline remaining=30s)
deadline +30s, no player    → cd=overhang
deadline −5s,  no player    → cd=expired
deadline −5s,  + player     → cd=uncovered
touch mark, mtime now       → cd=overhang
touch mark, mtime −1h       → cd=stale      (age=3600s stale_window=300s)
touch mark −1h + REAL aplay → cd=uncovered  (live pgrep, not injected)
```

**8 mutants, each seen RED for its own reason:** cd_mark ignores the clock → (s); stale reads held
(fail closed) → (u); stale window ignored → (u); cd_mark ignores mark presence → (u2); overhang
mislabelled aligned → (x); emitting+expired not uncovered → (w); absent+player not uncovered → (w);
`self_emitting` reverted to bare `[ -f ]` → (aa) **and** (ab). The (ab) leg drives a **real on-disk
expired mark**, not the injected class — an injected class alone is satisfied by a reader that never
parses the mark.

Downstream consumers re-run green: `mesh-audio-mode --test` (which does a REAL playback read of this
tool), `mesh-say --test` (which asserts the `mesh-speaking` contract). Output vocabulary unchanged —
`--cd` is a new subcommand, the `PLAYING|SILENT` first token and the `source=` field are untouched.

## The proposal this is evidence for (NOT landed — needs the operator / a substrate-owner)

Give the hub the MCA's job: **one hold/release primitive** (`mesh-speaking hold <secs>` / `--release`)
with note3-say's monotone-max deadline semantics, and migrate `mesh-say`, `mesh-voice-tx` and
`mesh-overhear`'s pwplay path off unconditional `rm -f` onto it; then canonicalize the two Python
readers (`_self_playing`, the capture loop) onto the deadline+staleness reading that
`_self_emitting_now` already uses. That is a multi-organ change to the mesh's deafness path — the
failure mode of getting it wrong is a permanently deaf node — so it wants a deliberate hand, and it
wants `--cd` running first so the fault classes it claims to remove are visible before and after.

## The generalizable rule

**A shared signal with two dialects is two signals.** The mesh's corollary discharge was fixed once,
correctly, inside one pathway — and the fix stayed there, so the hub kept the old semantics and every
other pathway kept re-deriving them differently. Biology's answer (Jarzyna & Carlson 2026) is that the
retiming lives at the hub and the pathways inherit it. Sibling of
`two-renderings-of-a-value-must-be-canonicalized` and `a-rule-asserted-at-one-call-site-is-not-asserted`.

**Sources:**
- [Jarzyna & Carlson, *Current Biology*, 11 Jun 2026, doi:10.1016/j.cub.2026.04.068](https://doi.org/10.1016/j.cub.2026.04.068)
- [WashU: New research reveals how brains update their predictions](https://source.washu.edu/2026/06/new-research-reveals-how-brains-update-their-predictions/)
- [phys.org: Brains update sensory predictions through single timing hub](https://phys.org/news/2026-06-brains-sensory-hub-electric-fish.html)
- [Scientific Frontline: Brain Predictions & Corollary Discharge](https://www.sflorg.com/2026/06/ns06142602.html)
