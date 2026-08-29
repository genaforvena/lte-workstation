# Predictive processing / the Bayesian brain — a prediction error is only worth acting on in proportion to its PRECISION, and the tuner page was handing the operator raw error at full authority

**Date:** 2026-08-29 · **Channel:** genome
**Area:** predictive processing & the Bayesian brain
**Angle:** a concrete METRIC the area measures itself with
**Arm:** treated (assigned) · target organ `scripts/mesh-tuner-web` drawn uniformly by coin at
p=0.20 from the 563 never-reviewed tools in the lane's own denominator — not chosen by me, not
chosen by the lane.
**Verdict:** APPLIES. Landed on the assigned organ.
**Landed:** `scripts/mesh-tuner-web` — **uncommitted in the tree, not deployed** (steward lands).

---

## What was already ours, checked before searching so this could not re-land

The PP/FEP shelf here is 40+ files deep and *precision* appears in five of their filenames already:
`fep-interoceptive-precision-allocation-need-alignment-precision`,
`fep-channel-knowledge-map-context-conditioned-observation-noise-precision`,
`fep-bayesian-model-expansion-structure-learning-precision`,
`predictive-processing-conformal-distribution-free-coverage-precision`,
`second-order-cyb-non-trivial-informational-closure-precision`. Also already embodied: Bayesian
surprise vs Shannon, the genuine MMN with its matched control, omission responses, Bayesian model
reduction, model recovery, volatility vs stochasticity, forced fusion / Bayesian causal inference.

**Not on the shelf, and it is the whole of one live sub-literature: sensorimotor synchronization.**
Nothing here measures a prediction error's precision *from the dispersion of a short run of repeated
readings*, and nothing here turns that dispersion into a **gain on the correction shown to a human
in the loop**. That is where this lands.

## The literature, live

Three sources, read this session:

1. **Palmer & Demos (2022), "Are we in time? How predictive coding and dynamical systems explain
   musical synchrony", *Current Directions in Psychological Science* 31(2):147–153** —
   [PMC8988459](https://pmc.ncbi.nlm.nih.gov/articles/PMC8988459/). The paper's metric pair is the
   one I took: **mean asynchrony** (the bias) and **variance of asynchrony** (the precision), and
   its load-bearing sentence is that only *"prediction errors with small variances cause the
   higher-level predictions to be adjusted."* Precision is not a nicety in the model — it is the
   gate on whether the error is allowed to change anything. Concrete numbers it quotes: musicians
   anticipate the beat by 30–50 ms, non-musicians by 50–80 ms.

2. **arXiv:2411.05971 (Nov 2024), "A Kalman Filter model for synchronization in musical
   ensembles"** — [arxiv.org/html/2411.05971v1](https://arxiv.org/html/2411.05971v1). This is the
   *metric* paper: the phase-correction gain α — the fraction of the observed error a player
   actually absorbs — is treated as a **time-varying quantity estimated from the performance**, not
   a constant. Initialized at the theoretical optimum 0.25 for a quartet, the fitted α "promptly
   deviate[s]" from it in every one of three conditions (Normal, Speed, Deadpan) on Haydn Op. 74
   No. 1. The point I carry over is exactly that: **the gain that ought to be applied to an error is
   a function of the noise you are currently in, so a constant gain is wrong the moment the noise
   moves.**

3. **Lagarde (2021), "The classical mean negative asynchrony in sensorimotor synchronization is not
   universal in humans. A cross-cultural study"** — [arXiv:2107.03971](https://arxiv.org/pdf/2107.03971).
   15 French and 15 Indian participants, tapping to a beat swept 1→6.1 Hz, finger angle at 5 kHz,
   relative phase from the Hilbert transform at each stimulus onset, N = 9720 relative-phase values,
   KS test on the cumulative distributions significant: the French distribution sits on one side of
   zero and the Indian on the **other**. The field's most-cited constant does not merely vary in
   magnitude across populations — **its sign flips.** That is the mesh's own
   `calibrate-a-derived-axis-against-the-live-corpus` rule arriving from the outside, and it is why
   nothing below imports a dispersion figure as a constant.

## The organ, and the defect

`scripts/mesh-tuner-web` is the bass-clef practice page: `mesh-tuner` runs YIN on the room mic and
writes `{ts,name,octave,midi,freq,cents,status}` to `~/.mesh/tuner-state.json`; the page polls
`/state` every 150 ms and draws the note on a staff with a cents needle.

Its verdict was one line:

```js
const inTune = Math.abs(s.cents) <= 6;
```

**One YIN frame, judged against a fixed ±6 cent band, rendered as a state.** Three things are wrong
with that and only the third is obvious:

- the page has no idea how noisy the reading it just got was;
- it has only two words, so the case "this reading cannot answer the question" is served as one of
  the two confident ones;
- the correction it prints (`подтяни ВВЕРХ (−7¢)`) is the **raw single-frame error**, i.e. the
  operator — whose entire practice is minimizing his own prediction error — is being handed the
  microphone's noise at exactly the same visual authority as his own intonation.

### The dispersion is not a constant, measured on this detector

I lifted `detect_pitch` **verbatim** out of `scripts/mesh-tuner` (sliced between its own `def`
lines, not reimplemented) and ran it over synthesized bowed-string tones — an 8-partial harmonic
stack at the page's own `RATE=16000`, at the tool's own two window lengths, over an SNR sweep.
40 frames per cell, sample SD (ddof=1) of the cents reading:

| note | window | 40 dB | 20 dB | 12 dB | 6 dB |
|---|---|---|---|---|---|
| C2 (65.4) | 0.40 s | **0.005** | 0.261 | 1.322 | **5.147** |
| C2 (65.4) | 0.18 s | 0.010 | 0.487 | 3.018 | **5.927** |
| G2 (98.0) | 0.40 s | 0.004 | 0.166 | 1.057 | 4.541 |
| G2 (98.0) | 0.18 s | 0.008 | 0.270 | 1.830 | 5.669 |
| D3 (146.8) | 0.40 s | 0.003 | 0.087 | 0.592 | 2.301 |
| A3 (220) | 0.40 s | 0.002 | 0.076 | 0.474 | 1.328 |

σ in cents. And separately, with the noise held at 30 dB and a **vibrato** added at 5 Hz with a
random vibrato phase per frame (60 frames, G2):

| vibrato width | σ @ 0.40 s | σ @ 0.18 s |
|---|---|---|
| ±0 c | 0.020 | 0.036 |
| ±10 c | 0.143 | 1.295 |
| ±20 c | 0.279 | 2.582 |
| ±30 c | 0.418 | **3.889** |

Read against the fixed ±6 c band, that is a **1200× span in the estimator's own precision**, and
the constant is wrong at *both* ends:

- **At the clean end the band is vacuous.** σ = 0.005 c against a 6 c band: the instrument can
  resolve intonation a thousandfold finer than the verdict it is allowed to give, so a real,
  audible, easily-correctable 5 c flat is reported as `✓ чисто`.
- **At the noisy end the band is a coin flip.** σ ≈ 5–6 c at C2/G2 at 6 dB, individual frames
  measured out to **13.4 c** on a tone that is *exactly* in tune. The old page renders those frames
  as a confident `♯ выше — опусти ВНИЗ (+13¢)`, i.e. it instructs the operator to detune a correct
  note — and it does so **worst in the low register the page exists for**: σ at C2/G2 runs 3–4×
  that at A3.
- **The window matters as much as the SNR.** A perfectly ordinary ±30 c cello vibrato contributes
  σ = 3.9 c at the 0.18 s frame and 0.42 c at 0.40 s — 9×, from the analysis window alone.

So there is no single number that is the right band, because σ is a joint function of SNR, register,
window and bowing technique, none of which the page can know in advance. That is Lagarde's lesson
one ring out.

## What landed

The page keeps a short window of tuner samples and replaces the one-line two-way test with a
precision-weighted verdict. The whole of the new logic is one pure function, delimited in the page
source by `// ---- PRECISION BLOCK` markers:

```js
const alpha = (band*band)/(band*band + se*se);   // this problem's Kalman gain
const shown = alpha*m;                           // the precision-WEIGHTED prediction error
const lo = m-1.96*se, hi = m+1.96*se;
if (hi < -band || lo > band)      state='off';        // decisively outside
else if (lo > -band && hi < band) state='in';         // decisively inside
else                              state='undecided';  // this reading cannot resolve it
```

Four things, each with a source in the papers above:

1. **A third word.** `не разобрать` — the reading's own 95 % interval straddles the band edge. Before
   this the case existed and was served as a confident verdict. (Two abstentions, not one:
   `набираю…` — fewer than 4 samples, *play longer* — is typed apart from `не разобрать` — *the
   reading is too noisy*, which no amount of playing longer at this SNR will fix. Different
   remedies, different words.)
2. **The displayed correction is shrunk by α**, the ratio of the target band's variance to the
   window mean's standard error. Palmer & Demos' gate, in the operator's units.
3. **The precision is published, not hidden:** a `σ … n … вес α …` line under the needle, and the
   95 % interval drawn as a pale bar *behind* the needle, so the noise is visible instead of drawn
   with the authority of signal. The raw frame is still shown beside it, so nothing is taken away.
4. **The band itself stays fixed at 6 c and is never auto-widened.** It is the operator's target,
   not a thing to calibrate; auto-widening it would be the exclusion-allowlist failure — the tool
   would quietly learn to call a worsening player in-tune. Only the *verdict* is precision-aware.

What the operator actually reads now, driven through the page's own `poll()`:

```
clean, in tune (sd .07c)            | ✓ чисто
                                    | σ 0.07¢ · n 8 · вес α 1.00 · сырой кадр 0.0¢
clean, 20c flat                     | ♭ ниже — подтяни ВВЕРХ (-20.0¢)
                                    | σ 0.13¢ · n 8 · вес α 1.00 · сырой кадр -19.9¢
6dB-SNR noise, sitting on band edge | ⟂ не разобрать — разброс чтения ±4.4¢ шире самого решения
                                    | σ 4.44¢ · n 12 · вес α 0.96 · сырой кадр 7.3¢
6dB-SNR noise, truly in tune        | ✓ чисто
                                    | σ 3.95¢ · n 12 · вес α 0.97 · сырой кадр 1.3¢
only 2 frames in                    | набираю… (2/4 кадра)
                                    | σ — · n 2 · сырой кадр 0.0¢
```

Rows 3 and 4 are the point: **the same noise level, opposite verdicts.** Averaging beats the noise
where it can (row 4 decides, correctly, that a ±4 c-jitter reading centred near zero is in tune);
it abstains where it cannot (row 3, centred on the edge). On the old code row 3's last frame
(+7.3 c) printed a confident instruction to detune a note that may well have been fine.

### The re-read trap, which the change would otherwise have walked into

The page polls every 150 ms; `mesh-tuner` writes a few times a second. So the **same record is
served repeatedly**, and a window that counted a re-read as a fresh observation would drive σ → 0
and α → 1 — the page would become *maximally confident precisely because it looked at one sample
many times*, a purer version of the bug being fixed. The window dedupes on the producer's own `ts`
and `n` counts distinct producer samples, never polls. Arm 6 and mutant m2 exist for this alone.

## The evidence

`--test` no longer greps the page for its own vocabulary. It **slices the precision block out of the
served HTML between its markers and executes it under `node`**, with 8 fixture arms, plus a 9th arm
that runs the page's *entire* script under a minimal DOM shim and reads back the two lines the
operator sees — because testing the parts is not testing the wiring. **Ten mutants driven red from
scratch copies, control green:**

| mutant | arm that caught it |
|---|---|
| `undecided` collapsed into `in` | 4 undecidable · 5 shrinkage |
| no `ts` dedupe (re-reads counted) | 6 re-read: accepted 20 copies of one record |
| `alpha = 1` (no precision weighting) | 5 shrinkage: noisy shown 4 not smaller than clean 4 |
| `MIN_N = 1` (verdict from one frame) | 1 warmup: got in |
| `shown = m` (raw error displayed) | 5 shrinkage |
| window survives a note change | 7 note-change: window kept 9 samples |
| no age eviction | 8 age: stale −30 c sample still steering the verdict |
| `poll()` ignores `precision()`, reverts to `abs(cents)<=6` | 9 wiring |
| the σ/n/α line drops σ | 9 wiring: precision line missing sigma/alpha |
| warmup renders a verdict instead of `набираю…` | 9 wiring |

**One mutant passed GREEN on the first run and that is the finding, not a footnote.** The
note-change arm spaced its samples 1 s apart and put the new note 100 s later, so the **age**
eviction cleared the window on its own and the note-change reset was never the thing under test —
a green mutant means the experiment never ran. The fixture now keeps every sample inside `WIN_AGE`,
so only the reset can clear it, and m6 goes red.

Coverage travels with the verdict: with no `node` on `PATH` the executed arms are skipped and the
result line says `logic=UNEXECUTED (no node on PATH)` rather than a silent green; a red arm prints
`logic=executed (… RED)`, never `UNEXECUTED`.

## What is NOT claimed

- **The dispersion table is synthetic, not a room recording.** The mic lives on `default-string`,
  not here. What is measured is the *estimator's* dispersion versus SNR, register and window —
  the property that makes a constant band indefensible. A real room adds reverb, other sources and
  bow noise, so these are a **lower bound** on the σ the page will actually see, which strengthens
  the argument rather than weakening it. No σ from this table is compiled into the tool.
- **The page has not been opened in a browser by me.** There is no Chrome on this node (checked).
  What ran is the page's own script under a DOM shim, which exercises `poll()` → `precision()` →
  the two text lines, and nothing about layout, the SVG, or the metronome, which are untouched.
- **α is near 1 for most full windows, and I am not going to pretend otherwise.** The shrinkage acts
  on the *mean's* standard error, so with n = 12 even a σ of 4 c leaves α ≈ 0.96. It bites at small
  n and large σ (the arm-5 fixture, σ 18.8 c → α 0.55). In practice the visible work is done by the
  third word and the interval bar; α is the principled form of the same quantity and is published
  so the operator can see when the tool is discounting him.
- **The state file rounds `cents` to 0.1**, so the σ the page can ever *measure* has a quantization
  floor of 0.029 c. Still ~200× below the band, so the vacuous-at-the-clean-end argument survives;
  worth knowing before anyone reads a printed `σ 0.03¢` as physics.
- **Nothing was transferred about timing.** The sensorimotor-synchronization *bias* metric — the
  30–80 ms negative mean asynchrony between the operator's note onsets and the page's own metronome
  clicks — is the obvious next organ, and it does **not** apply here as the page stands: the
  browser's `AudioContext` clock and the tuner's onsets are on two machines with an unmeasured
  offset, and the onset resolution is `TUNER_FRAME=0.18 s`–`TUNER_WIN=0.40 s`, 2–13× coarser than
  the effect. Measuring it would need a browser-side onset detector on the metronome's own clock,
  and `getUserMedia` is blocked on the plain-HTTP LAN origin this page is served over. Recorded as
  refuted-for-now, with the reason, rather than half-built.

## The rule this earns

**A decision boundary on a noisy reading needs the reading's own dispersion, not a constant — and
where the dispersion is wider than the decision, the honest output is a THIRD word, not one of the
two confident ones.** Keep the target fixed (it is a goal, not a measurement), publish σ and n
beside every verdict, weight the correction you hand a human by the precision of the evidence behind
it, and count DISTINCT producer samples: a re-read of one record is not a second observation, and
counting it as one buys maximum confidence with zero evidence.

## Sources

- [Palmer & Demos (2022), *Are we in time? How predictive coding and dynamical systems explain musical synchrony*, Curr Dir Psychol Sci 31(2):147–153](https://pmc.ncbi.nlm.nih.gov/articles/PMC8988459/)
- [A Kalman Filter model for synchronization in musical ensembles, arXiv:2411.05971 (2024)](https://arxiv.org/html/2411.05971v1)
- [Lagarde, *The classical mean negative asynchrony in sensorimotor synchronization is not universal in humans. A cross-cultural study*, arXiv:2107.03971](https://arxiv.org/pdf/2107.03971)
- [Repp & Su, *Sensorimotor synchronization: A review of recent research (2006–2012)*, Psychon Bull Rev](https://link.springer.com/article/10.3758/s13423-012-0371-2)
- [Quantifying phase correction in sensorimotor synchronization: empirical comparison of three paradigms](https://pubmed.ncbi.nlm.nih.gov/22305349/?dopt=Abstract)
