# Live-literature review — biosemiotics: the information-balance metric (Rsequence ≈ Rfrequency) as a self-measure for the wake recognizer

Date: 2026-07-27 · lane: genome (idea-queue LITERATURE task) · status: proposal, uncommitted

## Area & angle

Biosemiotics — sign and meaning in living systems — approached, as the task asks, through a
**concrete metric the area uses to measure itself**, not through philosophy. Searched the live
literature (Springer *Biosemiotics*, 2025–2026 volumes) for a *quantitative* handle on meaning
and landed on one that is fresh in the journal and has a 40-year operational track record in
molecular biology behind it.

Distinct from our prior biosemiotics landing (the von Uexküll functional-cycle *return leg*,
`docs/reviews/biosemiotics-functional-cycle-closure-2026-07-24.md`): that was about **closing**
a loop with a second sense; this is about **measuring the information a recognizer carries** and
whether it matches the information its task demands.

## The metric: Schneider's information balance — Rsequence ≈ Rfrequency (bits)

Live source (2026, current issue):

- Nielsen, H., Vitti-Rodrigues, M. & Emmeche, C., **"Measuring Meaning of Molecular Motifs"**,
  *Biosemiotics* (2026), https://link.springer.com/article/10.1007/s12304-026-09637-1 — argues
  the supposed tension between Shannon's *quantitative* information and the biosemiotic
  *semantic/interpretational* view "need not be as big as previously conceived": Schneider's
  information measure is **compatible** with biosemiotics and with Bateson's definition of
  information as **"a difference that makes a difference."** Meaning becomes measurable, in bits,
  as the uncertainty a sign removes for its interpreter.
- Foundational method it builds on — Schneider, T.D., Stormo, G.D., Gold, L. & Ehrenfeucht, A.,
  "Information content of binding sites on nucleotide sequences," *J. Mol. Biol.* 188:415–431 —
  https://users.fred.net/tds/lab/paper/ri/ri.pdf ; sequence-logo exposition,
  https://alum.mit.edu/www/toms/paper/logopaper/paper/index.html
- Framing debate in the same journal — "Can quantitative approaches develop bio/semiotic theory?"
  *Biosemiotics* (2021), https://pmc.ncbi.nlm.nih.gov/articles/PMC8362870/

The measure has two halves and their **relation** is the self-measurement:

- **Rsequence** — the information a recognizer's pattern actually carries, in bits: the drop in
  entropy from the maximum-uncertainty background to the observed distribution the recognizer
  enforces (per position: `2 − H_observed` for a 4-letter alphabet; 0 bits = matches anything,
  2 bits = matches exactly one symbol). This is Bateson's "difference that makes a difference"
  made numeric — how much a sign narrows the interpreter's options.
- **Rfrequency** — the information the *task* demands: `log2(G/γ)`, the bits needed to single out
  a real target among all `G` candidate positions when only `γ` are genuine sites.
- **The law** (Schneider's empirical result, and the paper's semantic point): biological
  recognizers evolve so that **Rsequence ≈ Rfrequency** — they carry *exactly* as much
  information as locating their target requires. Carry too little → the recognizer fires on
  background (false positives). Carry too much → it is brittle and misses degraded-but-real
  targets. The **balance itself is the health metric**; either imbalance is a named pathology.

## What we do NOT embody

The mesh has a rich *calibration* doctrine — rank against the live corpus, floor-gates, the
rhythm-density floor, "a median pinned as a constant rots." But every one of those calibrates a
*threshold* against a corpus. **None of them measures a recognizer's information content against
the information its task requires.** We have no notion of Rsequence ≈ Rfrequency anywhere.

The clearest un-measured recognizer is the **wake gate in `scripts/mesh-overhear`** — which is
*literally* the binding-site-location problem: locate the operator's address inside a continuous
ambient-speech stream. Its tuning history is a case study in the *absence* of this metric:

- `ROOM_WAKE_RE` (line 141) is a deliberately loose garble net (`миш|меша|мыш|миж|меж|беж|…`) —
  low Rsequence, so plain Russian words (`между`, `бежит`) match it: a recognizer carrying **less
  information than Rfrequency demands** → the recorded *false-wake storm* (memory
  `room-false-wake-storm`).
- Every fix bolted on **more ad-hoc information by anecdote**: a strict second tier
  `ROOM_WAKE_STRICT_RE` (line 142), a Bose foreign-playback veto (line 152), a self-emission veto
  (line 161), and the magic length cap `ROOM_WAKE_TELL_NW_MAX=3` (line 227) — "an address is a
  few words." That constant is a hand-guessed proxy for exactly the information balance this
  literature *measures*: it is the kind of assumed constant the mesh's own doctrine warns rots.

Nobody ever computes whether the assembled recognizer now carries the *right* number of bits. The
gate is tuned by reacting to the last false-wake, never by measuring Rsequence against Rfrequency.

## Concrete application (ONE, named file)

**File: `scripts/mesh-overhear` — a new read-only subcommand `--wake-balance`.** It changes **no
wake decision** (safe on this contended, load-bearing gate); it only reads three logs the organ
already writes and reports the balance in bits:

1. **Rfrequency** `= log2(N_utterances / N_true_calls)` over a window — `N_utterances` = all lines
   in `~/.mesh/room-ambient-gate.log` (the full ambient stream the gate scanned); `N_true_calls`
   = confirmed by-name calls, from `~/.mesh/room-reflex-ack.log` (the `слушаю` acks that a real
   wake actually produced) cross-checked against the wake-confirmed mints. This is the bits the
   task demands: how rare a real address is in the stream.
2. **Rsequence (effective)** = the bits the gate actually delivers = the mutual information
   between "gate fired a poke" and "it was a real call" = `H(call) − H(call | fired)`, estimable
   as `log2(pokes_fired / false_pokes)` from `.room-wake-heard` (candidates) vs the acks (real).
3. **Verdict** — the metric's whole point is the *comparison*:
   - `Rseq_eff  <  Rfreq − δ` → **UNDER-informed** (false-wake regime: the loose net is too loose
     / the length cap too generous — the recognizer carries fewer bits than locating the target
     needs).
   - `Rseq_eff  >  Rfreq + δ` → **OVER-informed** (deaf regime: strict tier / tiny-STT garble
     drops degraded-but-real calls — the `stt-organ-gigaam-beats-whisper` / tiny-model-miss trap
     seen from the information side).
   - `|Rseq_eff − Rfreq| ≤ δ` → **balanced** — the target state, and the objective the ad-hoc
     `ROOM_WAKE_TELL_NW_MAX` should be tuned *toward* instead of by anecdote.
4. **Honest degradation** (mesh doctrine): fewer than K confirmed calls in the window → print
   `n/a — insufficient confirmed calls to estimate Rfrequency` and exit 2. A balance can NOT be
   faked from no positives; silence about the target rate is n/a, never a green "balanced"
   (`na-must-be-a-claim-about-the-node`, no-faked-all-clear).

This converts the wake gate's growing pile of hand-guessed constants into **one measured target**:
tune the loose net, the strict tier, and the length cap until `Rseq_eff ≈ Rfreq`. The same
subcommand is the missing self-measure for *any* mesh recognizer that picks a rare target out of a
stream (dispatch owner-routing, the ambient proactive gate) — but scope THIS landing to
`mesh-overhear --wake-balance` only.

## Not discarded — why it applies

Operational (arithmetic in bits over three logs the organ already writes — `room-ambient-gate.log`,
`room-reflex-ack.log`, `.room-wake-heard` — not philosophy), one named real file, read-only so it
can't destabilise the contended live gate, degrades honestly to n/a, and is genuinely un-embodied:
we calibrate thresholds against corpora but have never measured a recognizer's *information
content* against the *information its task requires*. Landing point we have not been: **the
Rsequence ≈ Rfrequency information balance as a recognizer's self-diagnostic — too few bits reads
as false-wakes, too many as deafness, and the balance is the health.**
