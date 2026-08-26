# Predictive processing / the Bayesian brain — memory-of-one is the REWARD for choosing your evidence, and we took the reward without doing the work

**Date:** 2026-08-26 · **Channel:** genome
**Area:** predictive processing & the Bayesian brain
**Angle:** a concrete METRIC the area measures itself with
**Arm:** treated (assigned) · target organ `scripts/mesh-note3-tool-install` drawn uniformly by coin
at p=0.20 from the 560 never-reviewed tools in the lane's own denominator — not chosen by me, not
chosen by the lane.
**Verdict:** APPLIES. Landed on the assigned organ.
**Landed:** `scripts/mesh-note3-tool-install` — **uncommitted in the tree, not deployed** (steward lands).

---

## What was already ours, checked before searching so this could not re-land

The PP/FEP shelf here is 39 files deep. Already embodied: Bayesian surprise vs Shannon
(`…bayesian-surprise-vs-shannon-2026-07-28`), the genuine MMN and its matched control
(`…genuine-mmn-matched-control-novelty`), omission responses and their learned WHEN
(`…when-expectation-time-locked-omission-novelty`), Bayesian model reduction
(`…bayesian-model-reduction-occam`), model recovery / identifiability, conformal coverage,
volatility vs stochasticity, metacognitive (type-2) sensitivity, active data selection
(`fep-active-data-selection-…`), observation aliasing, reafference vs gating, forced fusion.

None of them is about **which observable you point at**, and none of them prices **memory
footprint** as evidence of anything. That is the gap this lands in.

## The source (live, read this session)

**Dorje C. Brody, Karl J. Friston, Bernhard K. Meister, Emmanuel M. Pothos — "The adaptive nature of
confirmation bias", arXiv:2606.23325v1, submitted 22 June 2026 (q-bio.NC / quant-ph).**
<https://arxiv.org/abs/2606.23325> · PDF read in full: <https://arxiv.org/pdf/2606.23325>

The set-up is binary hypothesis testing where the agent gets to **choose the observable** (evidence
is a matrix ξ̂(θ) on square-root-probability space, θ indexing which question you ask; θ₁ and θ₂ are
the directions aligned with the two hypotheses). The optimal choice θ\*(p) is the one that minimises
expected error probability for the current prior p — and it turns out to be **biased toward the
hypothesis you already favour**: "the information source is biased towards where the prior view is
stronger." Confirmation bias falls out of optimality rather than out of irrationality. The paper
then shows the active-inference route (choose the evidence with maximum information gain) picks the
**same** observable.

### The two metrics it measures itself with

1. **Neutrality N(p) ∈ [0,1]** — the separation |θ\*(p) − θ₂| (for p > ½; |θ\*(p) − θ₁| for p ≤ ½),
   normalised by its maximum over priors. "N(p) = 1 represents unbiased query, whereas N(p) = 0
   represents a 100% biased search." N(½) = 1; N → 0 as p → 0 or 1, monotonically.

2. **Error probability after n optimally-chosen samples** —

   > P⁽ⁿ⁾_θ\*(p) = ½ ( 1 − √( 1 − 4p(1−p) cos²ⁿ(½δ) ) )  ~  p(1−p) · exp( ln cos²(½δ) · n ),  δ = θ₂ − θ₁

   i.e. **exponential** decay in sample size. The comparison arm is the case "where the observable
   ξ̂(θ) is fixed and there is no flexibility of choosing evidence to sample, thus confirmation bias
   is prohibited" — there, the paper's Fig. 3 shows, "the error probability decreases very slowly."

3. **And the memory result, which is the one that bites us.** With a **fixed** observable, the
   posterior after n trials depends only on the count of positive outcomes, so memory grows
   2ⁿ → n (exponential → linear). With the **adaptively chosen** observable, identity (5) makes
   π(1−π) independent of the outcome, and memory collapses **2ⁿ → 2**: "we only need to know the
   outcome of the final trial… a Bayes-optimal inference can be made purely on the basis of the
   current observation, **because that observation is informed by our past experience**."

## The concept we did not embody

**Minimal memory is a two-flavoured signature, and the flavours are indistinguishable from the
footprint alone.**

A memory-of-one agent is either

- **earned** — it keeps no history because the history has been folded into *which question it asks*
  (θ\* tracks the posterior); error probability then falls exponentially in n; or
- **unearned** — it keeps no history because there is no history and no choice: one fixed observable,
  asked forever. Same footprint, and the error probability does **not** fall.

And the term that separates them is **δ, the angular separation of the two hypotheses' evidence
directions** — the diagnosticity of the question. When δ → 0, cos²(½δ) → 1 and the exponent in (7)
goes to zero: P⁽ⁿ⁾ = P⁽⁰⁾ for every n. **A test whose δ is zero for the failure mode that matters is
not a weak test; it is not a test at all, and no amount of repetition converts it into one.**

This is a genuinely different axis from anything on our shelf. We have a lot of cheap, stateless,
memory-of-one reflexes and we have been reading their cheapness as elegance.

## The organ, in those terms

`scripts/mesh-note3-tool-install` is the shared installer that seven Note3 sensor organs
(`mesh-baro`, `mesh-mag`, `mesh-note3-{ambient,ear,orient,light-raw,mag}`) call before every read.
It is a binary hypothesis test: **H+** "the current build of `<bin>` is on the phone" vs **H−** "it
is not". Its evidence choice was one line:

```bash
if timeout 8 $ADB shell "[ -x /data/local/tmp/$b ] && echo y" 2>/dev/null | grep -q y; then return 0; fi
```

- **Memory: 1.** It remembers nothing across calls. Textbook memory-of-one — and **unearned**: the
  observable is nailed to `[ -x ]` and can never move, whatever the belief does.
- **δ = 0 for the failure mode that matters.** Against a *stale* binary — the phone carrying the
  previous build, mode 755 — H+ and H− produce the identical reading. `~/.mesh/note3/BUILD.md`'s
  deploy recipe is an unconditional hand `adb push`; the installer is what the *organs* call. So the
  concrete, live consequence is: **after any rebuild of `sensorcat`/`slrec`, the new binary reaches
  the phone only if a human remembers to push it by hand. The installer will report `ok` forever.**
  Seven organs then read the old HAL client and every one of them is green.
- **P⁽ⁿ⁾ is flat.** Calling it a thousand times buys exactly the confidence of calling it once.
- **The action was open-loop.** `adb push … || return 1` then `chmod … >/dev/null 2>&1` with the
  result discarded, and no look afterwards: a push that half-landed returns success.

Note the shape is *not* the mesh's existing `a-mode-bit-is-not-the-write` rule (that one is about a
mode bit lying about writability). Here the mode bit is telling the exact truth about the thing it
describes; the defect is that we asked it a question it structurally cannot answer, and then asked
it again forever.

## What landed

An **evidence ladder** on the organ, with the rung that answered published in every verdict:

| rung | observable | separates | cost |
|---|---|---|---|
| `mode` | `[ -x ]` | absent / present | — |
| `size` | the size column of `ls -l` | a *different build* by length | free (same round trip) |
| `md5` | `md5` \| `md5sum` \| `toybox md5sum` | same-length builds | one extra round trip |

- **The hot path pays nothing.** `[ -x … ] && echo XOK; ls -l …` is one adb invocation, so the
  seven callers still cost two round trips per read (reachability + probe), exactly as before —
  δ went from 0 to non-zero for free.
- **The observable follows the belief.** A bin caught stale once is recorded in
  `~/.mesh/.note3-tool-install.escalate` and is md5-verified from then on. That is θ\* tracking the
  posterior, which is the whole mechanism the paper is about; `--all`/`--verify` run at `md5` too.
- **`unverifiable` is a word, and it is not `ok`.** The Note3 toolbox has no `stat`, no `wc`, no
  `busybox` and rejects `ls -1` — `ls -l` is the only size oracle on this device, and its exact
  column layout has **not** been confirmed against the live phone (it is dark). So the size is
  parsed by **anchoring on the grammar** (the column immediately before the `YYYY-MM-DD` stamp),
  never by field offset; when no stamp is found the verdict is `unverifiable evidence=mode`,
  rc 0 (present, old behaviour preserved) and **never the word `ok`**.
- **The push looks again.** After pushing, the organ re-probes and fails loudly if the artifact is
  not there; a failed push can no longer read as a fix.
- **A row per CALL, not per push** (`~/.mesh/note3-tool-install.log`), so the pushes are a numerator
  with a real denominator beside them. `--check` reports the verdict counts, the **stale rate** —
  which is the rate at which a rebuild silently failed to reach the phone — and which rung of the
  ladder actually answered.

## The gate

`--test` runs **17 fixture arms** against a stub `adb` on `PATH` under `env -i HOME=<fake>`, and
asserts the stub actually won the race (a stub is only ahead of the real tool until the subject
exports its own `PATH`, and this script does). **Six mutants driven red, control green:**

| mutant | arm that caught it |
|---|---|
| presence-only test (the original defect) | `stale size -> stale`, `stale pushes`, `escalation armed` |
| `unverifiable` rendered as `ok` | `unparsed -> unverif`, `unverifiable is not ok` |
| observable never follows the belief (no escalation) | `escalated -> md5 sees` |
| ledger written only on push (numerator only) | `ledger row per call`, `ok calls are on the tape too` |
| size by fixed field offset instead of the grammar anchor | `fresh -> ok/size`, `stale size -> stale` |
| open-loop push (no re-verify) | `failed push -> FAIL`, `failed push -> rc!=0` |

The first tightening was itself caught by a mutant: the ledger arm was `rows >= 5` against 6 calls,
so dropping the `ok` rows still passed. It is `-eq 6` plus a positive assertion now.

## What is NOT claimed

- **The live path is unexercised.** `adb devices` is empty — the Note3 is dark (the known
  `note3-adb-dark-while-physically-on-usb` state). `--test` says so in its own output:
  `coverage: fixture-only, live adb path unexercised`, and still exits 2 per the organ's contract.
  The `ls -l` grammar and the presence of a digest tool on Android 5.0's toolbox are **assumptions
  that fail toward `unverifiable`**, never toward a false `ok`.
- **No stale binary has been observed on the phone.** The claim is that the old evidence *could not
  see one*, which is a property of the test and is proved by the mutant, not a claim about a
  measured incident.
- The paper's quantum-probability formalism is not transferred. What transfers is the scoring:
  evidence choice is priced by the error exponent it buys, and memory footprint alone does not
  distinguish a good one from a vacuous one.

## The rule this earns

**A memory-of-one reflex is only cheap-because-smart if its OBSERVABLE moves with its belief; if the
observable is nailed down, the same footprint means the past has been discarded, not folded in — and
where the fixed observable cannot separate the hypotheses, repetition adds exactly zero.** Publish
which observable answered, and give the case it cannot see its own word.
