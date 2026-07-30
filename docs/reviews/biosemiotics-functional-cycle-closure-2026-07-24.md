# Live-literature review — biosemiotics: closing the functional cycle on actuators

Date: 2026-07-24 · lane: genome (idea-queue LITERATURE task) · status: proposal, uncommitted

## Area

Biosemiotics — sign and meaning in living systems. Reviewed for an **operational**
mechanism (not philosophy) the mesh does not already embody. Searched the live literature
(Springer *Biosemiotics* vols 2025/2026, *Sign Systems Studies*, de Gruyter *Chinese
Semiotic Studies* 2025), read, and landed on one.

## The mechanism: von Uexküll's functional cycle (Funktionskreis) — the RETURN leg

Jakob von Uexküll's **functional cycle** models an organism's engagement with its Umwelt as a
*closed* loop of semiosis: a receptor organ (Merkorgan) extracts a perceptual sign
(Merkzeichen) → the inner world interprets it → an effector organ (Wirkorgan) acts, stamping
an **effect sign (Wirkzeichen)** onto the object → **that changed object is re-perceived by the
receptor, closing the loop**. The action is only meaningful once its effect returns to the
sense that predicted it. The loop — not the act — is the unit of meaning.

Live sources read:
- "Funktionskreis and the stratificational model of semiotic structures" — *Sign Systems
  Studies* 47(1-2), 2019 — https://ojs.utlib.ee/index.php/sss/article/view/SSS.2019.47.1-2.02
- "The circulation of meaning: a biosemiotic perspective on the functional circle" — 2024 —
  https://www.researchgate.net/publication/380319292
- Hoffmeyer, "semiotic causation": semiotic controls differ from deterministic ones by an
  **inbuilt anticipatory capacity** — action guided by an interpretation whose fulfilment is
  expected. Springer *Biosemiotics*, "Introduction: Semiotic Scaffolding" —
  https://link.springer.com/article/10.1007/s12304-015-9236-1
- 2025 reconciliation of code-biology with Deacon's interpretation — de Gruyter/Brill —
  https://www.degruyterbrill.com/document/doi/10.1515/css-2025-2003/html

## What we ALREADY embody (so this doesn't double-count)

The mesh already carries the *forward* half and one sophisticated adjunct:

- **Efference copy / reafference cancellation.** `scripts/mesh-audio-active` explicitly cites
  the motor-neuroscience literature (Straka/Simmons/Chagnaud, PMC6733654, 2019; efference copy)
  and uses the `~/.mesh/mesh-speaking` flag as the efference copy to subtract the mesh's own
  voice from its mic senses (`source=self` vs `source=external`). Every acoustic mic sense
  drains on that flag.
- **Verification doctrine.** "Every claimed capability must produce a real artifact" (CLAUDE.md)
  — but this is a *same-organ* artifact (camera → its own JPEG). It does not require the effect
  to be confirmed by a **different** sense.

## What we do NOT embody — the un-closed return leg

We emit the efference copy but use it only to **cancel**, never to **verify**. The
`mesh-speaking` flag says "I should be hearing my own voice in the room right now" — and nothing
ever checks that the room mic *actually* registered it. An actuator that acts on the world
through a channel a *different* sense would have to confirm is left **open-loop**: it declares
success from the near end of its own command, not from the effect returning to a receptor.

Canonical failure this leaves live — `scripts/mesh-note3-say`, line 136-138:

```
adb_sh "am start -a android.intent.action.VIEW -d file://$rpath -t audio/mpeg; input keyevent 126" \
  | grep -qiE 'Starting|cmp=' || { echo "...play intent did not launch"; return 1; }
echo "mesh-note3-say: spoke -> $rpath"
```

Success = the VIEW intent's stdout says `Starting|cmp=`. That is the intent **launching**, not
sound entering the room. Volume 0, audio routed to a disconnected BT sink, lost audio focus, a
muted speaker — every one of these yields `Starting` and a green `spoke ->` while the room stays
silent. This is exactly the recorded `Bose sink != speaker` trap (`off Bose rc=0, no sound`,
memory `bose-usb-sink-is-not-speaker-sounds`) and the silent-fallback doctrine, one modality up:
the Wirkzeichen was stamped but never re-perceived, so a non-effect reads as an effect.

## Concrete application (ONE, named file)

**File: `scripts/mesh-note3-say`.** Turn the `mesh-speaking` efference copy from a subtract-mask
into a **prediction whose fulfilment is verified** — the functional cycle's return leg:

1. After the play intent launches, the tool already computes the exact playback window
   `[now, until]` (line 112, `until = now + dur + 8`) and holds the self-mute flag over it.
2. Within that window, sample the **co-located room mic** (the room node feeding
   `mesh-overhear` / `mesh-room-transcript`; acoustic level via `mesh-room-sense`) and check the
   ambient level *rose above its pre-utterance floor* — a Merkzeichen confirming the Wirkzeichen.
3. Level rose → keep today's `spoke -> ...` success. Level did **not** rise → this is a real
   defect (`spoke but room stayed SILENT — effect unconfirmed`), `return 1`, the same class as
   Bose-rc0, instead of a false green.
4. **Honest degradation** (mesh doctrine): where no co-located ear is reachable, `exit 2`
   (honest n/a) — never a faked confirm — matching the tool's existing exit-2 contract and the
   no-faked-all-clear rule. A confirmation that cannot see the room says n/a, not "heard".

This closes the loop the efference-copy machinery already set up but left one-way, and it
generalises: the same pattern is the missing return leg for every *world-acting* actuator whose
effect only a different sense can confirm (`mesh-say` speaker path, room voice `mesh-voice-tx`).
Scope this landing to `mesh-note3-say` only.

## Not discarded — why it applies

It is operational (a mic-level threshold check inside an existing timing window, not a
philosophy), it names one real file, it degrades honestly, and it is genuinely un-embodied: we
have the efference copy but never verify the reafference it predicts. Landing point we have not
been: **the functional cycle's return leg — re-perceiving an actuator's effect through a
second sense to validate the act.**
