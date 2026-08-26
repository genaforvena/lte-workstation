# The shadow, not the decoy: a level is not a confirmation

**Live review, 2026-08-26 — enactivism & 4E cognition, from the angle the task asked for: a concrete
METRIC or EXPERIMENT the area uses to measure itself.**
Landed in `scripts/mesh-audio-active` (`--confirm`, report-only; uncommitted — steward lands from the tree).

---

## 1. Prior art, checked first

`memory/enactivism-4e-coverage.md` lists 20+ landings from this area. Read and passed over as already
ours: complexity matching / lead–lag (`mesh-cooscillate`, `mesh-leadlag`), CRQA laminarity
(`mesh-labor --crqa`), the matching condition (`mesh-cooscillate --sensitivity`), the sensorimotor
environment `s = g(m)` (`mesh-therm --response`), affordance effectivity (`mesh-load-gate`),
participatory coupling, precariousness, role cycling, agency-gated credit, hostile scaffolding — and
**reafference**, in both directions: SUBTRACTION (`mesh-audio-active source=self`, `mesh-room-sense`
self-playback discount) and CONFIRMATION (`mesh-audio-active --confirm`, landed 2026-07-30 from this
same lane).

MFDFA / interaction-dominant dynamics was already **discarded** on 2026-07-30 as hollow on our window
lengths, and I did not re-litigate it.

The gap I landed is not another coupling metric. It is the **control arm** the area uses to prove one.

## 2. The concept: the SHADOW

Auvray, Lenay & Stewart's **perceptual crossing** paradigm — *"Perceptual interaction in a minimalist
virtual environment"*, New Ideas in Psychology 27(1):32–47, 2009 — puts **three** objects in a
one-dimensional sensory field: a static **decoy**, the partner's **avatar**, and the avatar's
**shadow**. The shadow is dragged along the avatar's *exact* trajectory and **does not sense you back**.

That third object is the whole methodological point, and it is why the paradigm is still being built on
in 2026 rather than retired:

- the **static decoy** is trivially discriminated — you just find the thing that moves;
- the **shadow** is not, because at every instant it delivers the **identical sensory signature** as the
  real partner;
- what separates avatar from shadow is not the signal but its **contingency on your own action**. Only
  the avatar can mutually stabilise with you, because only the avatar responds.

Live restatements read this pass, all reachable and current:
[Froese, Iizuka & Ikegami, *Sci. Rep.* 3:3672](https://www.nature.com/articles/srep03672) (embodied
interaction constitutes social cognition — the shadow is the control that makes that claim testable);
[Deschamps, Lenay et al., *Front. Psychol.* 7:1059](https://www.frontiersin.org/articles/10.3389/fpsyg.2016.01059/full)
(joint perception of a shared object);
[Behav. Res. Methods (2020) adolescent PCE](https://link.springer.com/article/10.3758/s13428-020-01378-4);
[an open-source perceptual-crossing rig, PMC11164400 (2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11164400/);
and, on the metric side of the same field,
[Bremer et al., *Front. Virtual Real.* 6:1619710 (2025)](https://www.frontiersin.org/journals/virtual-reality/articles/10.3389/frvir.2025.1619710/full),
which computes net transfer entropy against surrogate dyads — the same instinct, one abstraction up.

**The transferable rule: the negative arm of a coupling test must match the positive arm in every
measured property EXCEPT reciprocity.** Every mesh null I could find is a *shuffle*, a *permutation* or
an *absence* — a static decoy. Nothing in the genome carries a shadow.

## 3. Where it bites, in a real organ

`scripts/mesh-audio-active --confirm` (landed 2026-07-30 out of this lane) closes the action→perception
loop: when a `source=self` stream is RUNNING, sample the room mic and ask whether the predicted
reafference arrived. Its classifier split on the mic **class**:

```
SILENCE              -> unheard      # hollow actuator
QUIET|MODERATE|LOUD  -> heard        # "the mic corroborates the self-sound -> VERIFIED"
```

That is proved against the **static decoy only**. **The room's own floor is the shadow.** A fan, an open
window, the operator's iMac, a human talking — all deliver QUIET or louder, all mint `confirm=heard`
for a stone-dead sink. And that is exactly the fault class the axis exists to catch
(`bose-usb-sink-is-not-speaker-sounds`, `mesh-home-audio-stack-down-note3-ear`), in exactly the
condition — an occupied room — where it is *most likely to be asked*.

## 4. What landed

The paradigm's own discriminator, in dB: **require a LIFT above the room's own floor, not a level.**

- `ambient_floor()` — floor = **p20 of the trailing 6h** of `~/.mesh/ambient-db-tape.tsv`
  (`mesh-ambient-tape`, 2-min cadence, 16 870 clean rows 2026-07-14 → 2026-08-26).
- `read_mic_db()` / `lift_of()` — the current `rms_db` behind the class, and the one subtraction that
  is the whole discrimination.
- `confirm_of` gains a 4th argument and one new verdict word:
  `lift >= threshold -> heard` · `lift < threshold -> shadowed` · **`lift UNKNOWN -> the pre-2026-08-26
  verdict verbatim`**.
- The **evidence travels with the verdict** (`floor_db`, `floor_n`, `floor_age_s`, `mic_db`, `lift_db`,
  `lift_thr`, and the JSON fields) — a bare `heard` cannot say whether it was earned or defaulted.

Three design choices that are each a mesh rule, not a preference:

**p20, not the median.** The tape records whatever is sounding, our own playback included. A median
would drift toward our own output and erase the very lift it measures. A low quantile still estimates
the room's quiet floor as long as we are not emitting for most of the window.

**Per-window, never a constant.** Across this node's 111 six-hour windows the p20 floor has **sd 15.6
dB** (the tape pools capture devices at different gains). Measured live during this review the room's
own 6h floor was **−27.7 dB** while the corpus-wide 6h-window median floor is **−46.8 dB** — a pinned
constant would have read the live room's pure ambient noise as a **+20.9 dB lift** and shouted HEARD.
The fossil-constant trap ([[a-constant-outlives-its-reader]],
[[calibrate-a-derived-axis-against-the-live-corpus]]) is not hypothetical here; it was one line away.

**The threshold is the corpus's own p75.** Default `5.0` dB = the 75th percentile of the lift that
ordinary ambient samples already ride above their own window's p20 (p50 +1.7, p75 +5.0, p90 +10.9).
The header carries the re-derivation script; the claim is the gate, not the quoted number.

**The new word is safe.** `grep -rn 'confirm=' scripts/` finds no consumer in the genome
(`mesh-room-sense` parses `source=`, not `confirm=`), `shadowed` only ever appears where the old code
said `heard`, and it **weakens** that claim — it never converts a `heard` into an alarm
([[a-new-verdict-word-must-be-in-the-consumers-alphabet]]). An UNKNOWN floor reproduces the old verdict
exactly, so absent evidence mints nothing ([[na-must-be-a-claim-about-the-node]]).

## 5. The live artifact

Real tape, real mic, one instant (2026-08-26T15:40Z), a self stream injected as RUNNING:

```
ambient_floor -> -27.7|150|67          # floor −27.7 dB, 150 rows in the 6h window, newest 67 s old
mic now: MODERATE, rms_db −25.9        # lift = +1.8 dB

OLD (deployed ~/.local/bin)  confirm_of(1,1,MODERATE)      -> heard
NEW (genome)                 confirm_of(1,1,MODERATE,+1.8) -> shadowed
```

```
[audio-active] confirm=shadowed — source=self stream RUNNING and the mic is not silent (mic=MODERATE),
but the level is fully explained by the room's OWN floor (floor_db=-27.7 floor_n=150 floor_age_s=67
mic_db=-25.9 lift_db=1.8 lift_thr=5.0) → the sound is a SHADOW (exafference), the actuator is
UNCONFIRMED. A level is not a confirmation; only a lift is.
```

The room at that moment was a **shadow**: MODERATE, and explained without us.

**Honest bound on this artifact:** no speaker was driven. This shows the discrimination on the room's
real floor and the real mic, not a red-then-green against a physically dead sink. The end-to-end `--test`
legs drive the real script both ways; the *hardware* half of the claim is still owed.

## 6. Test

`--test` 39 → **63 assertions**, 0.2 s. Load-bearing pair **(r1)/(r2)**: same mic class, same source,
same running count, **opposite verdict on the lift alone** — a classifier that ignores the lift cannot
pass both. **(r7)** proves the staleness gate by the **clock** on a present, well-formed, long-enough
tape, not by absence. **(r9)** drives the real script end-to-end.

Five mutants, all RED, restore green:

| mutant | dies on |
|---|---|
| `confirm_of` ignores the lift (any non-silence → heard) | (r2) ×6 |
| `ambient_floor` drops its staleness gate | (r7) ×2 |
| `lift_of` returns `0` instead of `""` for an unknown side | (r6)+(r9) ×6 |
| UNKNOWN floor falls back to `shadowed` instead of `heard` | (r3) ×5 |
| the lift is computed in `--confirm` and `""` passed to `confirm_of` | (r9) ×2, every pure leg green |

That last one is the **computed-then-discarded wiring bug** — the failure that survived mesh-load-gate's
first fully-green pass. It is why (r9) exists.

## 7. Found while building it — a live forgery hazard in `--test`

The first (r9) run went green against the **deployed** binary. `"$0"` inside `--test` is the bare string
`mesh-audio-active` when invoked as `bash mesh-audio-active --test` from the genome, and bash resolves
that child **via PATH** → `~/.local/bin/`. A genome-only edit would have tested green against the old
copy — the drift-clobber leak wearing a test's clothes. Fixed in the new legs by resolving
`${BASH_SOURCE[0]}` to an absolute path. **Other `"$0"` re-execs across the genome's `--test` blocks
carry the same hazard and were NOT swept** — flagged, not claimed.

## 8. Discarded this pass

- **Net transfer entropy** (Bremer et al. 2025, KSG estimator, netTE = TE(L→F) − TE(F→L)) — the directed
  half is already ours in `mesh-leadlag` (lagged prediction, autocorrelation baseline, permutation null
  on the global max, its own asymmetry margin, and a 2026-08-19 Basak et al. review already cited in its
  header). Would be a second estimator for a question we already answer.
- **Allostasis / anticipatory regulation** — still open in the coverage map, still a review rather than a
  result. Left where it is.
