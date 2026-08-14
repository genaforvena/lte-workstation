# VSM live review — "completing deficiencies": the third control mechanism the mesh does not have

**Date:** 2026-08-14 · **Lane:** literature (live review) — viable system model & management cybernetics,
from the angle of a known critique · **Landed in:** `scripts/mesh-song-verify` (report-only)

## The critique this lands on

The standing structural complaint about Beer's VSM is that it is a *reference* model, not an operational
one: it names five subsystems and their channels, but leaves the actual mechanics of a primary process's
boundary — what enters, what is admitted, what leaves, what is thrown away — implicit, so two people can
both "apply the VSM" and model nothing in common. The steady-state literature answers that complaint by
making the boundary explicit.

**Source (read in full, not the abstract):** Rob Dekkers, *"On the Origins and Applications of the
Cybernetic Steady-State Model as Systems-Theoretical Reference Model"*, **Systems 13(11):961 (2025)**,
doi:[10.3390/systems13110961](https://doi.org/10.3390/systems13110961). Adam Smith Business School,
University of Glasgow. MDPI 403s both the fetcher and curl from this node; the author's OA deposit
came down clean: `https://eprints.gla.ac.uk/365834/1/365834.pdf` (read via `pdftotext -layout`).

Dekkers positions the steady-state model as *"a more practical extension of Miller's living systems and
Beer's viable system model"*, and states the delta against the VSM outright (§2):

> It expands the viable system model by separating better transformational processes and control
> processes, including more explicit boundary zones and focusing on homeostatic processes.

## The concept we do not embody: **completing deficiencies**

§2.1 lists **three** principal control mechanisms, not two. Feedback and feedforward differ only in where
they intervene relative to the point of measurement — feedback **upstream**, feedforward **downstream**.
The third is neither:

> Very different from feedback and feedforward, completing deficiencies means that measuring detects
> deviations from a standard **after** the transformation processes, and then the flowing elements are
> brought up to that standard in a **separate, complementary process**.

and, on the quality filters that sit in the boundary zones with it:

> In both cases it leads to **discarding** the flowing elements (or system), **unless a process for
> completing deficiencies is capable of transforming the quality of the flowing elements** … to set
> quality standards.

Grep of the genome, 2026-08-14: `completing deficienc` → **0 hits**; `boundary zone` → **0 hits**;
`feedforward` → 1 hit (`scripts/mesh-algedonic`, from the predictive-vs-reactive anticipation landing,
2026-08-10). So the mesh has feedback everywhere, feedforward in one organ, and the third mechanism
nowhere — which means **every quality filter we own is a pure discard gate**.

Coverage check against `[[vsm-beer-review-coverage]]`: algedonic channel, S3↔S4 homeostat, Beer ACP,
requisite variety, POSIWID, S2 anti-oscillation, transduction, residual variety, power-relations,
S3\* audit, III1/III2 write-only, PII2 institutional schizophrenia, CASE L4 error budget — none of
these is a boundary-zone control mechanism. New ground.

## Where it bites: the sound lane's output boundary

`scripts/mesh-song-verify` is exactly the boundary-zone quality filter Dekkers describes, born
2026-07-24 from the operator's *"вы хоть раз сами слушайте"*. It listens to a finished grind against its
source on four axes (harmfid / homog / silent / rolloff / beatfrac) and returns **ship** or **reject**.
On reject the render is binned whole and the record's recipe is fed to `mesh-sound-reflex`'s repellent —
which is **feedback**: it changes the *next* grind and does nothing for the element already produced.
Each discard is a completed grind: a heavy-run slot and minutes of CPU, thrown away.

**Live read, `~/.mesh/records.log` @ 2026-08-14T15:34Z** (679 rows, 217 grinds — the ledger is a sliding
window, so this is a re-derivable reading, never a constant):

| | count |
|---|---|
| grinds | 217 |
| `unshipped:not-a-song` (discarded at the output filter) | **10** |
| └ `arrhythmic` (beats 0.29–0.43× src) | 5 |
| └ `dead-gaps` (silent 0.26 / 0.27 / 0.36 / 0.26 vs the 0.25 line) | **4** |
| └ `lost-song` (harmfid 0.892 vs 0.90) | 1 |

All four dead-gaps rejects are **single-axis** — nothing else about those renders failed. And dead-gaps
is the one axis a bounded complementary process can actually move: near-silent spans are mechanically
removable (`ffmpeg silenceremove`), whereas no post-process on a rendered file restores harmony it never
kept (`lost-song`), a pulse the grind destroyed (`arrhythmic`), or high end that was never rendered
(`mud`). Two of the four sit **4% past the line**. Under feedback alone they are indistinguishable from
the arrhythmic ones: all ten are simply "not a song", binned.

## What landed (report-only)

`scripts/mesh-song-verify` now classifies each **failed axis** instead of only naming it:

- per-axis **margin** — distance past the threshold, always a positive distance (the axes fail in
  opposite directions; a signed `+4%` would mean "below" on one axis and "above" on the next);
- a **`rework=` / `fundamental=`** split — which deficiencies a complementary process could reach on
  *this* render, and which are in the transformation itself, where the discard is honest;
- the split is **per-axis, not per-render**: a render can carry both (the `--test` fixture does — inserted
  silence trips `dead-gaps` *and* drags `homog` under its floor), so a `rework=` tag beside a non-empty
  `fundamental=` is not a green light.
- knobs: `SONG_REWORK_AXES` (default `dead-gaps`), `SONG_REWORK_MAX_SILENT` (default `0.50` — trimming a
  render that is mostly silence leaves a different artifact, not a completed one).

Reject line, live shape:

```
SONG reject: inhomogeneous(homog 0.646<0.80), dead-gaps(silent 0.36>0.25) | harmfid=1.0 … \
  | rework=dead-gaps(44% past, trim-near-silent) fundamental=inhomogeneous(19% past)
```

`--json` gains `rework[]` / `fundamental[]` with `axis/value/threshold/margin`.

**Report-only by construction.** The verdict, the exit code and every caller's behaviour are untouched —
`mesh-sound-reflex:1412` and `mesh-guitar-watch:249` read the rc and echo the text; an **ok** verdict
keeps its byte-exact prior shape and a reject only ever *gains* a trailing clause (which is why the tag
rides at the end of the line, where the ledger's `unshipped:` clause and the not-a-song poke both carry
it without a parser sweep). **A `rework=` tag is a hypothesis that a trim would clear the axis, not a
claim that it did** — the artifact for that would be the re-verify, and nothing here re-verifies
anything. Wiring an actual complementary process (trim → re-verify → ship or discard) is the next
landing, and it needs this measurement first to know it is worth the CPU.

## Gate

`--test` gained a fourth fixture (3.8s of the tremolo source + 2.2s of silence ≈ 0.36 silent, inside the
rework band) and three assertions: the dead-gaps reject is tagged **reworkable**, it never appears in the
fundamental set, and the unrelated-noise (`lost-song`) reject is tagged `rework=none` — no trim restores
harmony. **Seen red, then green**: `SONG_REWORK_AXES=""` → rc=1 with
*"the completing-deficiencies read is dead"*; unset → rc=0.

That off-switch also caught a live bug in the knob itself: it was written `${SONG_REWORK_AXES:-dead-gaps}`,
where an explicitly empty value falls back to the default — the classification could not be turned off,
and a gate driving the knob would have been asserting the default rather than the code path. Now `-`, not
`:-`.

**Cost:** `--test` goes 13.6s → 19.9s (a fourth librosa verify). Still inside the 30s `timeout` that
`mesh-land`'s `test_ok` and `mesh-autowire` both impose — but the margin is now ~10s, so a fifth fixture
in this tool needs the budget checked, not assumed.

## Not taken

- **Osejo-Bucheli**, *"Purposeful Evolution in Organisational Cybernetics: Symbiosis, Co-Evolution,
  Transduction and Axiology in Viable Systems"*, SRBS (2026), doi:10.1002/sres.3122 — a teleological
  frame for VSM adaptation. Wiley paywalls it (402 to the fetcher; abstract via Crossref/S2 only), and
  identity-preserving adaptation is close to ground `[[autopoiesis-review-coverage]]` already holds.
- **Espinosa**, *"Revisiting the VSM as an emancipatory systems approach"*, SRBS (2025),
  doi:10.1002/sres.3090 — answers Jackson's unitary/functionalist critique; overlaps the power-relations
  lens already in `mesh-vitality power_concentration()` (Zeini 2025).
- **CASE L1/L3** (arXiv:2608.10153) — flagged unread in the coverage memory, deliberately left there:
  L4 landed 2026-08-12 and a second helping from one source is not a live-literature landing.
