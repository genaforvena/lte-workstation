# Predictive information *rate* — the news axis `--cat` never had

**Lane:** LITERATURE (live review) · information theory of agency — empowerment, predictive information.
**Angle:** a foundational idea we MISread or applied too loosely.
**Date:** 2026-08-15. **Window:** genome (mesh-home). **Status:** landed, uncommitted in the tree.

---

## 1. Where the seam already was

`memory/info-theory-agency-coverage.md` is explicit that this is a near-saturated seam. Embodied
already: open-loop and closed-loop/process empowerment (`mesh-algedonic`), transfer entropy
(`mesh-cooscillate`), the Maximum Occupancy Principle (`mesh-vitality`), discounted empowerment on the
board (`mesh-promises --empowerment`), multi-agent interference (`mesh-algedonic --agency-actors`),
empowerment-as-channel-capacity (`--agency-capacity`), goal-set power (`mesh-organ-keepalive --power`),
and — the one this review is about — **predictive information**, `I(past;future)`, as
`mesh-precision --num pred_info`.

Crypticity vs excess entropy was reviewed 2026-07-30 (the *stored-memory* vertex, `C_μ`). The third
vertex of the same triangle — the **rate** — had never been visited.

## 2. The concept, and where I found it

**Predictive information rate (PIR), `b_μ`.** Samer A. Abdallah & Mark D. Plumbley, *A measure of
statistical complexity based on predictive information rate*, [arXiv:1012.1890](https://arxiv.org/abs/1012.1890)
(8 Dec 2010), Eq. (10) — read first-hand off the PDF, not from an abstract:

> `I_t ≜ I(X_t ; X⃗_t | X⃖_t) = H(X⃗_t | X⃖_t) − H(X⃗_t | X_t, X⃖_t)`
> — "the average information in **one observation** about the infinite future **given** the infinite past."

With `b_μ` the shift-invariant PIR, `b_μ = h_μ − r_μ` (their §II), where `h_μ` is the entropy rate and
`r_μ` the **residual** entropy rate — the uncertainty in `X_t` that survives knowing past *and* future.
The whole-entropy decomposition is `H(X_0) = ρ_μ + r_μ + b_μ` with `ρ_μ` the multi-information rate.

The sentence that makes it a *different quantity* rather than a refinement (§II, verbatim):

> "processes which maximise the PIR do not maximise the multi-information rate `ρ_μ` (or the excess
> entropy, which is the same in this case), but do have a certain kind of partial predictability that
> requires the observer continually to pay attention to the most recent observations in order to make
> optimal predictions."

and the design criterion it is built to satisfy:

> "complexity should be low for systems that are deterministic or easy to compute or predict —
> 'ordered' — and low for systems that are completely random and unpredictable — 'disordered'."

The live-literature tail of the same thread: the PIR was introduced for *information dynamics* of music
(Abdallah & Plumbley, [Connection Science 21(2–3)](https://www.tandfonline.com/doi/full/10.1080/09540090902733756),
2009) and that programme is still publishing — [*Predictability and the pleasure of music*, PNAS 2025](https://www.pnas.org/doi/10.1073/pnas.2516635122)
(IDyOM; moderately-surprising events, the inverted-U). The Gaussian closed form is a separate paper,
[arXiv:1206.0304](https://arxiv.org/abs/1206.0304), Eq. (26): `b_μ = ½ log(1 + Σ_k ψ_k²)` over the AR
prediction coefficients, equivalently Eq. (28) the log-ratio of prediction-error to interpolation-error
variance.

**Zero hits for `predictive information rate`, `b_mu`, `residual entropy` or `binding information` in
`scripts/`.** Absent from the coverage map.

## 3. The misread, in our own genome

`scripts/mesh-precision`'s predictive-information axis computes `PI₁ = −½log₂(1−ρ₁²)` — the **excess
entropy** family: a *stock*, how much the past constrains the future in total. Its own header then
writes the misread out in prose (pre-edit, line 177):

> "a deterministic oscillation is HIGH predictive information — correctly, it is a real signal, not
> noise; per-switch FLAPPING is the categorical `--cat`/switch-rate axis's job."

Both halves are wrong in the same direction. Excess entropy is **maximal** for the ordered extreme —
a clock's past pins its future completely — which is exactly the case Abdallah & Plumbley say a
structure measure must score *low*. And the question that got delegated to switch-rate ("is this tape
worth reading?") is not a question switch-rate can answer.

Because on the `--cat` side there is no floor at all:

| tape | stability | verdict | `b_μ` (news/obs) |
|---|---|---|---|
| frozen — one label, forever | 1.00 | **RELIABLE** | **0.000 b** |
| perfect alternator ABAB… | 0.00 | FLAPPING | **0.000 b** |
| i.i.d. coin | 0.47 | FLAPPING | 0.007 b (under its null) |
| sticky Markov q≈0.85 | 0.86 | **RELIABLE** | **0.192 b** |

A **frozen** categorical tape — the mesh's single most chronic pathology, the silent fallback, the
value-frozen sense, the wedged driver — scores 1.00 and takes `--cat`'s **best** verdict. `--num` has
the CDP variance-collapse floor for precisely this shape; `--cat` had nothing. And the frozen tape and
the sticky one **share** that verdict while sitting at opposite ends of the news axis; the alternator
and the coin **share** the opposite verdict while both carrying zero news, for opposite reasons.

That is the operational content of PIR here: *how much does this observation tell me that the past had
not already told me* — the quantity a sense actually delivers, which excess entropy is not.

## 4. What was built (report-only)

`scripts/mesh-precision` — `--cat` output now carries a `pir` axis. It never touches the stability
verdict, a weight, or any consumer; same posture as `novelty` / `pred_info` / `memory`.

- `b_μ = h_μ − r_μ` at Markov order 1: `h_μ = H(X_t|X_{t-1})`, `r_μ = H(X_t|X_{t-1},X_{t+1})`.
- Labels `NEWS_LIVE | NEWS_WEAK | NEWS_DEAD | PIR_NA`, bands `MESH_PREC_PIR_HI/LO` (0.15 / 0.05 b).
- JSON: `pir`, `pir_bits` (debiased), `pir_raw_bits`, `pir_null_p95`, `pir_entropy_rate_bits`,
  `pir_residual_rate_bits`, `pir_alphabet`, `pir_surr_k`.

**Two estimation traps, both defused, both proved on this node's own tapes rather than asserted:**

1. **Bias.** `b_μ` is a difference of plug-in conditional entropies, and `r_μ` conditions on `k²`
   contexts against `h_μ`'s `k` — so `r_μ` is under-estimated much harder and `b_μ` is biased **up**.
   Live proof: `~/.mesh/sensors.log` `ble_count` (k=10, n=600) reads raw `b_μ` **0.436 b** — *larger*
   than the genuinely news-bearing `room_sense` (k=2, 0.246 b) — and its own shuffle null sits at
   **0.442**. It is bias, end to end; without a null it would have read as the most informative tape on
   the node. Every reading now runs a seeded shuffled-symbol surrogate null (`MESH_PREC_PIR_SURR_K=200`,
   seed `MESH_PREC_PIR_SEED`), reports the p95, subtracts the null mean, and calls anything not clearing
   p95 `NEWS_DEAD`. Same shape as `mesh-algedonic`'s 2026-07-30 MI null — and here a **shuffle** is the
   right null, not the circular shift the autocorrelation cases need, because H0 *is* exchangeability.
2. **Unscorable alphabets.** Below `MESH_PREC_PIR_MIN_PER_CTX` (10) samples per `k²` context the answer
   is `PIR_NA` **with the reason**, never a number — and never alongside a `pir_bits`. `ble_top` (k=16,
   2.3 samples/context) refuses instead of shipping the marginal-over-the-null verdict it would
   otherwise get.

A **single-label tape is scored, not refused**: `b_μ ≡ 0` by construction, reported as `0.0000` with
`NEWS_DEAD`. An `n/a` there would hide the exact pathology the axis exists to name.

### Live, this node (600-sample windows off `~/.mesh/sensors.log`)

```
room_sense  RELIABLE  stab=0.90 | NEWS_LIVE 0.243b (raw 0.246, null p95 0.008, k=2)
ble_named   RELIABLE  stab=0.86 | NEWS_WEAK 0.057b (raw 0.077, null p95 0.034, k=5)
ble_count   FLAPPING  stab=0.29 | PIR_NA — 6.0 samples/context (k=10) < 10 floor
ble_top     FLAPPING  stab=0.45 | PIR_NA — 2.3 samples/context (k=16) < 10 floor
```

Note `room_sense` and `ble_named` sit 4 points apart on stability — the same `RELIABLE` verdict — and
**4× apart** on news. That is the live non-vacuity check: the axis is not switch-rate in disguise.
Nothing on this node currently reads `NEWS_DEAD` live, so this is an instrument, not an incident.

### Gates (6 mutants seen RED from a scratch copy, suite 2.6s)

`--cat` PIR legs added to `--test`, each falsifiable: frozen tape must read RELIABLE **and** NEWS_DEAD
**and** report `0.0000`; sticky tape must read RELIABLE **and** NEWS_LIVE (same verdict, opposite news);
alternator must read FLAPPING **and** NEWS_DEAD (the other extreme); i.i.d. must not clear its null at
k=2 **and** at k=4, where raw `b_μ` ≈ 0.11 b clears the NEWS_WEAK bar on bias alone and the reported
value must stand ≥2× clear of it; the alphabet floor must refuse *with a reason and without a number*;
the null must be seed-deterministic. Mutants seen red: drop the `b_raw ≤ p95` significance test · drop
the null-mean subtraction · remove the alphabet floor · `b_μ := h_μ` (drop `r_μ`) · frozen tape → NA ·
unseeded null. The p95-gate leg was **added because the first mutant survived** — with both bands
pinned to 0 the magnitude path can only say NEWS_LIVE, so a tape still reading NEWS_DEAD under that
pinning can only have got there through the significance test.

## 5. Scope — stated so nobody over-reads it

- `b_μ` is estimated at **Markov order 1**. A period-4 tape reads `b_μ ≈ 0` for the same reason its
  lag-1 `pred_info` reads NOISE — the structure is deeper than the model. That is the memory-depth
  axis's job on `--num` and is **not** claimed here.
- `NEWS_DEAD` does **not** distinguish "frozen/periodic" from "i.i.d. noise" — PIR is low at both
  extremes *by design*. The stability metric printed beside it is what separates them; the human line
  says so explicitly. A one-number reading of this axis would be the max-fold error again.
- The Gaussian `--num` counterpart (arXiv:1206.0304 Eq. 26) was **deliberately not built**: for a
  continuous AR(1) it is monotone in ρ₁ and so adds nothing ordinally to `PI₁`, and — unlike the
  discrete case — it does *not* vanish at the deterministic end (it saturates at ½ bit). The inverted-U
  is real in the discrete case, which is the case `--cat` has, and the only one this edit claims.
- Report-only. No consumer reads `pir` yet. The obvious next consumer is
  `mesh-reflex-health`'s `value-frozen` flag, which doctrine already calls "a lead, never a verdict" —
  `b_μ` is the verdict axis it lacks. Deliberately not wired in this edit.

## 6. Files

- `scripts/mesh-precision` — header block (the misread, the concept, the two traps, the scope), the
  `--cat` PIR computation, `out()` JSON + human rendering, 6 smoke-test legs. Uncommitted in the tree.
- Cite: arXiv:1012.1890 Eq. (10) · arXiv:1206.0304 Eq. (26)/(28) · Connection Science 21(2–3) 2009 ·
  PNAS 2025 doi:10.1073/pnas.2516635122.
