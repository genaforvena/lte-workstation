# Predictive processing / Bayesian brain — live review: a fusion organ must be compared against BOTH baselines, and ours *is* one of them

## `mesh-audio-mode` is a forced-fusion model with `p_common` hard-wired to 1 — the field's own null model, shipped as the verdict.

**Area:** predictive processing & the Bayesian brain · **Angle:** a concrete METRIC/EXPERIMENT the
area uses to measure itself
**Arm:** treated (assigned) · target organ drawn by coin at p=0.20 from the 568 never-reviewed
tools, not chosen by me or by the lane · **Window:** genome · **Date:** 2026-08-24
**Landed:** `scripts/mesh-audio-mode` (`--causal`, report-only + header note) — **uncommitted in the
tree, not deployed.** Steward lands.

---

## 1. Where we had already been (checked before landing, so this does not double-count)

This is the mesh's most-saturated review area — **20 prior reviews** under `docs/reviews/`. Confirmed
already embodied before searching:

- **precision-weighting**, conformal coverage, Bayesian model reduction, model recovery →
  `scripts/mesh-precision`
- **prediction error / Bayesian vs Shannon surprise, HGF volatility, local-global two-timescale,
  feature-specific PE, uncertainty-driven boundaries, the genuine-MMN matched control** →
  `scripts/mesh-novelty`
- **the omission response and its learned WHEN** → `scripts/mesh-novelty --when`
  (`predictive-processing-when-expectation-time-locked-omission-novelty-2026-08-15.md`, off the same
  Yaron et al. 2026 EJN paper). My first candidate this session *was* the omission/due-time-locking
  metric; it is **already served**, and I discarded it rather than re-serve it.
- **corollary discharge timing** → `scripts/mesh-audio-active --cd`
- **metacognitive sensitivity `meta-I₂ᵣ`** → `scripts/mesh-room-sense`

Unclaimed, verified by grep over `scripts/` + `docs/`: **`p_common`, "Bayesian causal inference",
"forced fusion", "protected exceedance"** — zero hits. (`mesh-pace`/`mesh-convexity` carry
"exceedance" in the *extreme-value-theory* sense; `mesh-load-gate`/`mesh-cooscillate` carry "common
cause" in the *does-A-cause-B* sense. Neither is this.)

## 2. The source (live, current, read first-hand)

**Günaydın G, Moran JK, Rohe T, Senkowski D — "Causal inference shapes crossmodal postdiction in
multisensory integration." *Scientific Reports*, 2026, doi:
[10.1038/s41598-026-36884-6](https://doi.org/10.1038/s41598-026-36884-6)**, first published
**2026-02-21**, open access.

How it was obtained, honestly: `nature.com` 303s this node into an `idp.nature.com` authorize
redirect. The **full text** was read from the Europe PMC REST API
(`ebi.ac.uk/europepmc/webservices/rest/PMC12929559/fullTextXML`, 126 KB); the record and abstract
from the same API's `search?query=TITLE:...&resultType=core`. Everything quoted below is from that
full text. The bioRxiv preprint (doi:10.1101/2025.07.02.662778, 2025-07-03) is the same work.

Found by walking the live 2026 predictive-processing surface: a first sweep landed on the omission
literature (Yaron et al., EJN 63(10):e70566) — **already served here**, see §1 — so I moved along the
causal-inference branch instead.

### The metric, verbatim

> "Our generative BCI model assumed that common (C = 1) or independent (C = 2) causes were determined
> by sampling from a binomial distribution with the causal prior p(C = 1) = p common."

> "In the 'model averaging' strategy of the BCI model, the observer weighs the estimates in
> proportion to the posterior probabilities of their underlying causal structures."

And — the sentence this review turns on — their **null model**:

> "a classical forced-fusion model that mandatorily assumes a common cause (i.e., **p common = 1**),
> thus always selecting the fusion estimate."

### The experiment, and what makes it a measurement

They fit **four** competing models to 32 participants — **BCI, forced-fusion (FF),
forced-segregation (FS), and non-postdictive BCI (BCI-NP)** — and compared them by **BIC, AIC, R²**,
plus Bayesian model selection: *"the BCI model best explained the group data, with a **protected
exceedance probability of 0.96**. FF and FS had negligible probabilities, and BCI-NP model had a
probability of 0.04."*

**That is the transferable discipline, and it is not the model — it is the comparison.** The field
does not permit a fusing model to assert itself. It must beat *both* degenerate baselines: the one
that always fuses and the one that never does. A model that was never compared against them has not
been measured, only asserted.

## 3. What we did not embody

`classify()` (`scripts/mesh-audio-mode:79-87`) crosses mic-class × playback into six verdicts. Every
cell names **one activity**. There is no cell — and no representable value — for *"these two axes are
being driven by two separate causes."*

By the paper's own definition, that is **forced fusion with `p_common` = 1**: the mesh shipped the
field's null model as its verdict, and named it a fusion.

The truth table is in fact **both** baselines hard-coded, cell by cell, with nothing deciding which:

| cell | what it does | which baseline |
|---|---|---|
| `FOREIGN + PLAYING → CALL` | fuses two streams into one activity | **FF** (`p_common`=1) |
| `MESH + PLAYING → MESH-SENSING` | discards the playback axis entirely | **FS** (`p_common`=0) |

The concrete failure: a dictation app holding the mic while an unrelated player emits audio reads
**CALL**, with exactly the confidence of a real call.

**The mesh already felt this joint and patched it by hand.** The `net_note` block bolted onto the
CALL cell reads `mesh-netrate` and appends *"(uplink quiet for a live call — corroboration weak, not
disqualifying)"*. That is a disparity cue — evidence bearing on whether the two axes share a cause —
but it is prose, on **one** cell, and explicitly **cannot change the verdict**. The organ gathers the
evidence and throws it away. That is a hand-rolled, single-cell, non-actionable `p_common`.

**And the identifying information never reaches the fusion at all — both inputs drop it one layer
down.** The kernel states who owns each substream and when it started, in the very files these tools
read:

- `mesh-capture-inuse` resolves holder PIDs internally (`:118-120`) and emits only
  `"pcmC2D0c:arecord(MESH)"` — **the PID is dropped from the JSON.**
- `mesh-audio-active` counts `state: RUNNING` and carries `owner_pid` in its own test fixture text
  (`:251`) **without ever reading it.**
- `trigger_time` is read by exactly one tool mesh-wide, `mesh-pcm-motion`, and only as a
  *stream-instance key* for hw_ptr delta continuity (`:306,:337`) — never as an **onset** for
  cross-stream disparity. No duplication.

So the fusion organ could not distinguish one cause from two **even in principle**.

## 4. The instrument — `mesh-audio-mode --causal` (report-only, additive, opt-in)

Reads `/proc/asound/card*/pcm*{c,p}/sub*/status` directly to recover what the two inputs discard —
`owner_pid`, `trigger_time` (CLOCK_MONOTONIC, so a *difference* is meaningful though the absolute is
not), and the owner's `comm` — then prints **all three readings the field demands**:

- **FF** — the shipped verdict (`p_common` = 1), unchanged.
- **FS** — the segregated baseline, naming the two axes as two causes.
- **BCI-cue** — which the kernel actually supports, with published coverage.

`causal_class()` is **structural only** — every branch is a fact the kernel states, never a tuned
threshold:

| cue | verdict |
|---|---|
| capture pid == playback pid | `COMMON` (`p_common`~1) — one process does both: the definition of a call |
| same `comm`, different pid | `WEAK-COMMON` — fusion plausible, unproven |
| distinct processes | `INDEPENDENT` (`p_common`~0) — the fused verdict asserts a cause the kernel does not show |
| either side dark | `UNKNOWN` — **never** a defaulted 0.5 |

**Two deliberate refusals, both doctrine:**

1. **No fitted `p_common`.** There is no labelled corpus here; a fitted number would be a claim whose
   value lives only in an echo string. The cue is graded and named, not scored.
2. **The temporal axis is measured, not thresholded.** `onset_dt` prints the onset asynchrony in
   seconds marked **UNCALIBRATED**. The paper's temporal window is *"several hundred milliseconds"* —
   a **human perceptual** constant. Transferring it here as a threshold would be a constant with no
   reader on this node.

`UNKNOWN` on a dark side, and `onset_dt` propagating `na` rather than `0`, are the same rule: a
missing stamp rendered as 0 would read as **perfect synchrony** — the strongest possible
common-cause evidence — manufactured out of absence.

### Live artifact (both sides driven, this session)

Driven against a real second stream: 20 s of digital silence to `hw:0,3`, an HDMI pin whose every
`eld#0.*` reads `monitor_present 0` — a RUNNING playback substream that is inaudible anywhere.

```
[audio-mode causal] FF=MESH-SENSING | FS=mesh-capture + playback | BCI-cue=INDEPENDENT
  p_common~0 (distinct processes: 'arecord'#3198391 vs 'aplay'#3196844 — the fused verdict
  asserts a cause the kernel does not show)
  streams: capture=1 playback=1  onset-dt=2.2s (UNCALIBRATED)  coverage=cap:3198391/arecord play:3196844/aplay
```

The shipped verdict at that instant: `MESH-SENSING … (mic=MESH play=PLAYING)` — the FS-hard-coded
cell, discarding a live playback stream, visible in the same breath.

## 5. Verification

- `--test`: **ok** — 9 classify + json-resolve + **13 new causal-cue fixtures** + REAL mic-capture
  read + REAL playback read + **REAL `pcm_streams` parse** against live `/proc/asound`.
- **Report-only, proved not claimed**: default and `--json` output **byte-identical** to
  `git show HEAD:scripts/mesh-audio-mode` (ts field normalised); `--causal` leaves
  `~/.mesh/.audio-mode-state` mtime+size untouched; an unknown flag still falls through to the
  read-only render.
- **Every new gate seen RED** (7 mutants, one per gate):

| mutant | gate that caught it |
|---|---|
| `na` guard dropped from `causal_class` | dark capture side → expected UNKNOWN |
| WEAK-COMMON → COMMON | same comm, two pids |
| same-pid branch dropped | one pid holding both |
| `onset_dt` na → 0 | must propagate na, never 0 |
| `onset_dt` abs dropped | must be symmetric |
| `fs_reading` collapsed to one cause | FS reading of FOREIGN+PLAYING |
| `pcm_streams` trigger_time blanked | caught against **live** data, pid 3230873 |

## 6. What this does not claim

`--causal` is report-only and changes no verdict. Making `p_common` *actuate* — a seventh verdict for
the INDEPENDENT case, or demoting CALL to a two-cause reading — is a contract change for the
consumers of `[audio-mode]`, and the field's own answer (model averaging vs model selection vs
probability matching, which the paper compares explicitly) is a decision the mesh has not made. The
measurement comes first; the actuator is a separate, arguable step.

The **postdiction** half of the paper — that input arriving *after* a stimulus revises it, isolated
by their BCI-NP control — is a second unclaimed axis and a natural follow-on: this organ commits to a
verdict from one instantaneous sample and never revises it. Not built here; recorded as an open lead.

---

**Sources**
- Günaydın, Moran, Rohe & Senkowski, *Sci Rep* 2026, doi:10.1038/s41598-026-36884-6 — full text via
  Europe PMC `PMC12929559`.
- Preprint: doi:10.1101/2025.07.02.662778 (bioRxiv, 2025-07-03).
- Swept and **set aside as already-served**: Yaron, Shiramatsu, Takahashi & Chao, *Eur J Neurosci*
  63(10):e70566 (2026), doi:10.1111/ejn.70566 — the omission response; embodied in
  `mesh-novelty --when` since 2026-08-15.
