# Predictive processing / Bayesian brain — LIVE literature review, 2026-08-22

## Perception has TWO clocks — processing time and stimulus time — and conflating them is a named methodological error. Our iMac eye has exactly one clock, and it keeps the frame at stimulus-time ≈ 0: the camera's prior, not the room.

**Lane:** predictive processing & the Bayesian brain, angle = **a recent result (2023–2026)**
**Arm:** treated (assigned) · target organ drawn by coin at p=0.20 from the 571 never-reviewed
tools, not chosen by me or by the lane · **Window:** genome
**Landed:** `scripts/mesh-imac-cam.m` (+ the contract change it forces in `scripts/mesh-imac-cam`),
**uncommitted in the tree, not deployed.**

---

## 1. How the live surface was swept

Live, this session, not from a fixed list:

1. **arXiv API, newest-first, 25 each** over `all:"predictive processing"`, `all:"predictive
   coding"`, `all:"Bayesian brain"`, `all:"prediction error" AND all:"precision"` (fetched
   2026-08-22 over `https://export.arxiv.org/api/query`; note `http://` returns a 0-byte body from
   this vantage, `https://` works).
2. **Web search** on the within-trial prior/likelihood dynamics branch and on precision/gain
   convergence.

Read and **DISCARDED**, with reasons:

- **Corva, arXiv:2607.20306** (state-dependent observation noise restoring epistemic value) — the
  first thing the search surfaced and the obvious fit for a *sensor*. **Already ours**: cited in
  three corpus reviews and landed on 2026-08-14 as `mesh-precision --reachable`
  (`fep-h3-reachable-non-constancy-epistemic-affordance-precision-2026-08-14.md`). Checked against
  the corpus, not from memory — this is exactly the re-landing the lane exists to avoid.
- **Leutenegger, arXiv:2608.12408** (evaluation resolution confounds learning-rule comparisons in
  model–brain RSA) — a real and sharp confound result, but it is about *comparing models to brains*,
  and we run no RSA.
- **Smith et al., arXiv:2608.05481** (recurrent Forward-Forward yields predictive representations
  from local contrastive learning) and **Shaw et al., arXiv:2608.02816** (persistent homology of
  predictive coding networks) — both are about the *implementation* of predictive coding in
  networks we do not train.

## 2. The source (read)

**Laurent Caplette & Frédéric Gosselin, "Time²: A framework for the neural dynamics of visual
perception", arXiv:2608.04218, submitted 4 Aug 2026.** Found via the `all:"predictive processing"`
newest-first sweep above; abstract read via the arXiv API.

Their claim, in their words:

> "it takes hundreds of milliseconds for the brain to process visual information reaching the
> retina. Second, we have to look at an object for a certain amount of time to perceive it … These
> two temporal facets of perception, which we term **processing time** and **stimulus time**, are
> often **conflated in the literature**. Moreover, processing time and stimulus time are usually not
> considered together in experiments."

Their contribution is a 2-D reverse-correlation method (Time²) that measures both axes
**simultaneously**, which they show is what makes rhythmic perception, predictive processing and
coarse-to-fine sampling separable at all.

**The concept we did not embody:** *processing time and stimulus time are different quantities, and
a measurement that reports only one of them cannot distinguish "our pipeline was slow" from "the
sensor had not yet resolved the scene."* The corpus holds two-timescale predictive processing
(`predictive-processing-local-global-two-timescale-2026-07-27`) and time-locked omission
(`…-when-expectation-time-locked-omission-novelty-2026-08-15`) — both are about *hierarchical* or
*expectation* timescales. Neither is this axis: this is about a single sense's own **sampling
transient**, and about publishing the two clocks separately instead of collapsing them.

## 3. Where it bites, in our own genome

`scripts/mesh-imac-cam.m` had exactly one clock:

```objc
NSDate *deadline = [NSDate dateWithTimeIntervalSinceNow:8.0];   // from startRunning
...
- (void)captureOutput:… { if (self.done) return; /* keep this buffer */ … self.done = YES; }
```

That 8 s bound is **processing time** — how long *our* pipeline waits for the device to open,
negotiate a format and deliver anything. The frame kept is buffer **#1**, i.e. **stimulus time ≈ 0**:
formed before the camera's own auto-exposure / auto-white-balance / gain loop has seen the room. In
Bayesian terms the kept frame is the sensor's **prior** (its power-on gain guess), not a posterior
over the scene. It is systematically dark and low-contrast.

That lands on live consumers:

- `scripts/mesh-imac-cam-watch` classifies each frame with
  `mean<30 and sd<1.5 → COVERED` · `span<12 and mean<30 → DARK` · `span<12 → FLAT`, and posts
  `[cam-covered] iMac (ilya) camera lens BLIND` off it. An unconverged frame is low-mean and
  low-span **by construction** — the organ can accuse the operator's lens of being blind on evidence
  it manufactured by sampling too early.
- The same watcher fires a **Groq vision call** whenever `diff_metric ≥ 14` against the previous
  frame. Every capture opens a **fresh** `AVCaptureSession` (the helper exits per frame), so the
  transient is **re-drawn independently each cycle** and its variance lands in the frame diff as
  "the scene changed". That call is expensive enough that the cooldown already had to go 45 s → 450 s
  to stop it exhausting the daily token budget in ~2.4 h.

This is the mesh's own **plausible-constant** failure with a new mechanism: a dim frame is
indistinguishable from a dim room, and nothing in the output said which clock produced it.

## 4. What landed

**`scripts/mesh-imac-cam.m` — two clocks, measured and published separately.**

- A **stimulus-time settle loop**: frames are dropped until the sensor's own loop converges —
  mean luma stable within `tol` (3 %) for `stable_needed` (2) consecutive frames, never before
  `min_frames` (3) and `min_ms` (250 ms) of *stimulus* time. Luma is read from a sparse grid of a
  32BGRA buffer (requested only if the device offers it).
- **Stimulus time is measured from the FIRST delivered buffer, not from `startRunning`** — that is
  the whole distinction. Measuring it from session start would let a slow device open *buy*
  convergence the sensor never did.
- **Both clocks are published with the reading**, one machine-readable line:
  `imac-cam: frames=N open_ms=X settle_ms=Y settled=yes|no|degenerate luma=L|na dluma=D|na`.
  `open_ms` is processing time, `settle_ms` is stimulus time.
- **`degenerate`**: a perfectly stable pure-black field is *stable from frame 1* — a real frame, and
  a covered lens is a genuine observation the watcher is entitled to classify COVERED — but it is
  **not evidence that exposure converged**, so it does not get to wear `settled=yes`.
- **Missing evidence renders `na`, never 0**: if the device refuses BGRA there is no luma axis, the
  core falls back to frames+time, and `dluma` stays `na` rather than a fabricated `0` that would
  read as "perfectly still".

**`scripts/mesh-imac-cam` — the narrowing every reader already supports.** An unsettled frame
(helper rc=5) is a sample of the transient, not of the room, so it is **not written to the canonical
path**: it is quarantined at `~/.mesh/cam/imac-unsettled.jpg`, `imac-last.jpg` is left untouched and
the wrapper exits 3. This follows `[[a-sidecar-cannot-narrow-a-bit-its-readers-never-open]]` —
~5 consumers read only the JPEG; none of them would open a `settled=no` sidecar, but all of them
already handle "no fresh frame" (`mesh-imac-cam-watch` has a `CAPTURE-FAIL` state). The ledger
`~/.mesh/cam/imac-cam-settle.log` is the ONE reader kept watching the narrowed-away case, and it is
written on **every** outcome so the rate has a denominator. Its `settle_ms` distribution is itself a
new sense: a rising settle time is the camera or the room degrading.

## 5. The gate (seen RED, twice, then green)

The settle core is **pure C on purpose** — `cc -x c -DIMAC_CAM_SELFTEST scripts/mesh-imac-cam.m`
builds it standalone on any node, **no Mac, no camera, no frameworks** — and `mesh-imac-cam --test`
runs it as its first leg. Eight cases: AE ramp · polarity drill · still lit scene · covered lens ·
dim-but-real room · flicker (never settles → timeout) · no-luma fallback · env overrides.

Driven red on this Linux node before being trusted:

```
### RED ARM A: tol default 0.03 -> 0.90
    FAIL: AE ramp kept luma 57.0 — that is the sensor's transient, not the room (117)
### RED ARM B: the ORIGINAL organ behaviour restored (accept buffer #1)
    FAIL: AE ramp accepted at 0ms stimulus time, under min_ms
    FAIL: AE ramp kept luma 6.0 — that is the sensor's transient, not the room (117)
    FAIL: AE ramp accepted the FIRST buffer — this is the bug the change exists to fix
    FAIL: flicker times out -> yes (want no)                       … settle-core: FAIL (7)
### RESTORED
  settle-core: ok (8 cases: …)
```

Arm B is the point: re-introducing the exact pre-change behaviour makes the gate name the bug in its
own words. The load-bearing assertion is on the **kept luma** (must be the room, ≈117, not the ramp),
not on the frame index — an index assertion was masked by `min_ms` and passed under arm A.

## 6. What is NOT verified, plainly

- **The ObjC half has not been compiled.** The iMac (`ilya@192.168.8.214`) is asleep — the LAN is
  healthy (gateway 0 % loss, `ip route get` via `wlxbcec43434a22`, `mesh-card --exit-node-lan` =
  `ok`) but the Mac itself gives `No route to host`. `mesh-imac-cam --test` correctly returns
  **n/a (exit 2)**, not a green. Only `cc -x c -DIMAC_CAM_SELFTEST` ran here. The wrapper's
  `ensure_binary` md5-compares and recompiles, so the first reachable call is the compile — and if
  it fails, that call reports `deploy/compile failed`, it does not fall back to the old binary.
- **The magnitude of the transient on THIS camera is unmeasured.** The mechanism is in the code and
  the consequence is in the classifier's thresholds, but "how dark is buffer #1 on this FaceTime
  camera" is a number nobody here has. The change is also the instrument that answers it: the first
  cycles after the iMac wakes will write `settle_ms` and `luma` to the ledger. Read that before
  believing any size claim, including this review's.
- **The risk to watch**: if this camera genuinely never converges inside 5 s of stimulus time, the
  organ moves from "working with dubious frames" to reporting `CAPTURE-FAIL`. That is the honest
  reading of a sensor that cannot resolve the room — and it is loud rather than silent — but the
  ledger's `rc=5` rate is the number that says whether the deadline needs raising. `IMAC_CAM_SETTLE_MS`
  is the knob.

## 6b. A skew the change itself created (found by running it)

`mesh-land` landed and deployed the **wrapper** while the `.m` was still settling, so for one window
the node held a new wrapper beside an old helper — and the new `--test` reported
`settle-core did not compile` (the `.m`'s `#import` lines hitting the C front end). That wording sends
the reader to the wrong file. Worse, the skewed pair fails silently in production: an old helper has
no settle core, never returns rc=5, so **every transient frame passes the wrapper wearing "settled"** —
a false green in exactly the direction this change exists to close. The gate now checks for the
`IMAC_CAM_SELFTEST` marker first and names the state as **version skew**, with what it implies.
Drilled against the actually-deployed old `.m`; the genome pair stays green.

## 7. Files

- `scripts/mesh-imac-cam.m` — two clocks, settle core, marker line, offline self-test (rewritten)
- `scripts/mesh-imac-cam` — marker capture, ledger, quarantine + exit 3, settle-core + version-skew gates in `--test` (the wrapper half was landed+deployed by `mesh-land` as `fab44a2` mid-session; the skew gate is a later edit, still uncommitted)
- ledger (runtime): `~/.mesh/cam/imac-cam-settle.log` · quarantine: `~/.mesh/cam/imac-unsettled.jpg`
