# LITERATURE (live review) — information theory of agency → a distributed sensor mesh

**Area:** information theory of agency — empowerment, predictive information
**Angle:** an OPERATIONAL mechanism (a computable quantity + a decision rule), not philosophy
**Reviewer:** genome mind · 2026-08-19 · live web search + full read of the source
**Verdict:** LAND — one un-embodied mechanism, one shipped (report-only) application
**Status:** uncommitted in the tree; steward lands

---

## The mechanism we did not have

**Interface empowerment, and the resolving-floor rule that falls out of it.**

R. Csaky, *"Prediction and Empowerment: A Theory of Agency through Bridge Interfaces"*,
arXiv:2605.06346, submitted **7 May 2026** — <https://arxiv.org/abs/2605.06346>
(read: abstract + HTML full text, <https://arxiv.org/html/2605.06346>).

Two results, both computable:

- **Theorem 5.** For a deterministic experiment, `I(Z, O_η) = H(O_η)`. The observation's **own
  entropy is the ceiling** on what a single read can say about the latent. A read is therefore two
  claims, not one: *what it says*, and *how much it could possibly have said*.
- **Definition (interface empowerment).** `log₂ |{ c(x') : x' ∈ Reach_T(x) }|` — the number of
  distinct **world-side channel states** the agent can reach through its own actions. Not
  empowerment over terminal states: empowerment over *the conditions that make an experiment
  informative*.
- **Proposition 4.** "If the uncontrolled channel process stays outside `C⋆` on the relevant
  support, then any admissible design sequence achieving `H(Z | 𝒯_T) → 0` must have nonzero
  interface empowerment `Emp_T^c(x) > 0`." Contrapositive, which is the mesh-usable form:

  > **A sense with zero interface empowerment cannot lift its own ceiling. Resampling is not
  > refinement.** Where the informative channel state is off the uncontrolled trajectory, more
  > samples buy nothing; only *acting on the channel* does — and if the sense owns no channel
  > parameter, the refinement has to come from somebody else, who must be named.

### Why this is new ground for us

The mesh has twenty prior `info-theory-agency-*` reviews. Nineteen treat empowerment as a quantity
to maximise, allocate by, discount, decompose, or null-test. The twentieth
(`info-theory-agency-overwrite-vs-identification-2026-07-24`) reads **this same paper** and lands
its Theorem-3 separation into `scripts/mesh-reflex-health:422`. It explicitly does **not** land
Proposition 4 — it cites Thm 5 in a single bullet and stops. `grep -rn 'interface empowerment'`
over `docs/ scripts/` returns nothing outside that one bullet's neighbourhood. So the ground here
is not the paper; it is the **second half** of it — the half that is a mechanism rather than a
separation, and that speaks about **senses** rather than about liveness verdicts.

The nearest thing we do embody is the coverage rule (CLAUDE.md, "a sense whose window is narrower
than its cadence reports a sample, not a state"). That is a **temporal** blindness: sample more
often and it goes away. Prop. 4 names an **orthogonal** blindness: a sense can sample at 100%
coverage, be perfectly fresh, be honest at every step, and still sit at a ceiling that no cadence
can raise. Our doctrine had no word for it.

## Where it bites — `scripts/mesh-cam-light`

`mesh-cam-light` derives an ambient-light level from the webcam frame `mesh-cam-watch --daemon`
already grabs. It is unusually careful: it degrades to UNKNOWN (exit 2) on a missing frame, a stale
frame, a corrupt frame, and — the good one — on a **flat field** (`luma stddev < 3` = covered lens,
"reads DARK yet is BLIND, not a dark room").

That flat-field guard asks *does this frame carry variance?* It does not ask *how many scene states
could this frame tell apart?* — and **on real frames those come apart**. Measured on this node's own
corpus (n=40 jpgs under `~/.mesh`, 2026-08-19):

| frame | mean | stddev | bits | old verdict |
|---|---|---|---|---|
| `cam/bruno-eating-now.jpg` (real scene) | 99.9 | 66.46 | **7.34** | MODERATE |
| `bowl-frames/motion-…d46.4.jpg` (real scene) | 46.4 | 27.25 | **6.43** | DIM |
| `cam-prev.jpg` (**the live frame this tool reads**) | 15.8 | 5.13 | **3.56** | DARK, exit 0 |
| `diary-pages/page-…1828460.jpg` | 16.5 | **53.90** | **2.39** | DARK, exit 0 |
| `bowl-frames/motion-…d35.6.jpg` | 7.7 | 0.83 | 1.76 | caught by flat guard |

Row four is the counterexample that makes this a real gap and not a restatement: **stddev 53.90 —
seventeen times the FLAT_STDDEV floor — carrying 2.39 bits**, less than the live DARK frame. The
existing guard calls that frame richly readable. It can separate almost nothing. Scene frames
cluster 5.5–7.6 bits; the degenerate ones sit at 1.76 / 2.39 / 3.56, with the gap around 4.5.

And the Prop. 4 half is structural here, not incidental: **`mesh-cam-light` has zero interface
empowerment by construction.** Its header says so proudly — "it never opens the camera itself, so
there is no device contention and no new privacy surface". That design choice is right, and it
means the tool owns no exposure, no gain, no illumination parameter. When its read is at the
resolving floor, "retry" is not an available move. The honest report is *I am at my floor and no
action of mine lifts it* — plus the name of whoever does own the channel.

## What shipped (report-only, uncommitted)

`scripts/mesh-cam-light`:

- `stat_gray` now emits a **third field, `bits`** — the entropy of the frame's own 256-bin luma
  histogram (0..8), from the same decode, so it is free. Appended, so the existing
  `read -r m sd` call site keeps working.
- `refine_token <bits>` — the Prop. 4 report. `refine=ok` above the floor;
  `refine=floor:none-reachable(owner=…)` below it, naming `mesh-cam-watch:capture-params` and
  `mesh-act:illumination` as the owners of the channel state this organ cannot reach.
- Both fields ride at the **tail** of the output line. The `DARK/DIM/MODERATE/LIT/BRIGHT` vocab,
  the prose, and every exit code are untouched — a level-grepping consumer cannot be shifted.

Live artifacts (real frames, real run):

```
[cam-light] MODERATE — webcam FOV mean 99.9/255 (…) bits=7.34 refine=ok
[cam-light] DARK — webcam FOV mean 15.8/255 (…) bits=3.56 refine=floor:none-reachable(owner=mesh-cam-watch:capture-params,mesh-act:illumination)
[cam-light] DARK — webcam FOV mean 16.5/255 (…) bits=2.39 refine=floor:none-reachable(owner=…)   # stddev 53.90
```

### The honest limits, stated in the file

- **`bits` is a proxy, and the file says which one.** It is the entropy of *this* frame's histogram —
  an upper bound on what one observation can distinguish. It is **not** the paper's `H(O_η)` over
  the latent ensemble, which needs a corpus of frames across scene states. A ceiling, never an
  achieved `I(Z;O)`. Nobody may quote it as the paper's quantity.
- **The 4.5-bit floor is provisional and gates nothing.** Drawn from the measured gap in a corpus
  that will turn over, env-overridable (`CAM_LIGHT_REFINE_BITS`), and report-only — so it cannot rot
  into a behaviour. (Doctrine: "a median pinned as a constant ROTS".)
- **Zero interface empowerment is asserted from the design, not measured.** The `none-reachable`
  branch is correct *because the tool never opens the camera*. The comment marks where a measured
  reachable-state count would go if that ever changes, and says it must be measured, not asserted.

### The gate, seen red

`--test` grows **7 resolving-power assertions** (now `3 classify + 2 flat-field + 1 staleness + 7`).
The load-bearing one is the counterexample: a synthetic **bimodal** frame (half 0, half 255) with
stddev ≈ 127 — forty times `FLAT_STDDEV` — and exactly **1.00 bits**. It asserts *both* that the
stddev is huge (so the counterexample is not void) *and* that the entropy floor still catches it.
**If the two axes were redundant this assertion could not be written.** PNG, not JPEG: JPEG ringing
would smear the two levels into a fake histogram.

Four mutants, run from scratch copies, each seen red:

| mutant | result |
|---|---|
| `bits = 0.0` (kill the entropy computation) | FAIL ×2 |
| `if (1) print "refine=ok"` (kill the floor) | FAIL ×2 — `bits=1.00` reported ok |
| drop `owner=` from the token | FAIL |
| `CAM_LIGHT_REFINE_BITS=8` (floor above the corpus) | FAIL — proves gate 1 non-vacuous |

A fifth "mutant" was **not** one: the first `sed` for the floor-killer never matched, so it ran the
unmodified script and passed green. Caught by diffing the mutant against the source before trusting
its verdict — a mutant you have not proven differs is a green you have not earned.

## What this does not claim

It does not claim the mesh is blind. It claims a **level and its resolving ceiling are two
different claims**, that we published only the first, and that on this node's live frame the second
one is 3.56 bits — a number no consumer of `[cam-light] DARK` could previously see. And it names,
in the line itself, who would have to act for that to change.
