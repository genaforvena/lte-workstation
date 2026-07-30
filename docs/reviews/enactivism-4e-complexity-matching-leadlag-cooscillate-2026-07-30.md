# Enactivism & 4E cognition (live review): complexity matching and the lag-0-vs-±1 discriminator — telling *anticipatory* coupling from *reactive* follow-the-leader

**Date:** 2026-07-30
**Area:** enactivism / 4E cognition (embodied · embedded · enacted · extended), from the angle of a concrete *metric* the field uses to measure a system's own coupled/embodied character.
**Landing:** a mechanism we do NOT embody — the **lead/lag cross-correlation signature** (peak at lag 0 vs peaks at ±1) that 4E coordination-dynamics research uses to separate *genuine mutual/anticipatory coupling* from *reactive asynchrony-correction*. Proposed as a **report-only** diagnostic axis on `scripts/mesh-cooscillate`. The heavier half of the same literature — **DFA/MFDFA complexity matching** — is DISCARDED here as a hollow sense on our short windows (finite-length bias, the crypticity precedent).

---

## What this area already gave us (so this doesn't re-tread)

4E/enactivism overlaps heavily with concepts already landed, and I checked each before proposing:

- **Autopoiesis / operational closure / adaptivity / precariousness** (Maturana–Varela; Di Paolo) — embodied in `mesh-vitality` (closure-of-constraints, allopoiesis gap) and the autopoiesis review series.
- **Relevance realization / efficiency↔resiliency** (Vervaeke) — embodied (`mesh-sensorium --balance`).
- **Structural coupling as a reciprocal relation** (Maturana–Varela, *Tree of Knowledge* 1987) — already embodied *inside `mesh-cooscillate` itself* (the APPLIANCE×APPLIANCE reciprocity branch, `:505–515`: two fixed units cannot co-move, so their shared signal is scanner-side common-mode, not a presence cluster).
- **Coupling significance / surrogate falsification** (Theiler; Riedl 2025) — queued on `mesh-cooscillate` (the `info-theory-agency-surrogate-null-cooscillation-2026-07-30` review; block-bootstrap null, report-only `--surrogate` first).
- **Critical slowing down** (variance + lag-1 autocorrelation) and **criticality** (MPR `C_JS`, Rosas-Ψ) — embodied.
- **Crypticity / statistical complexity `C_μ`** — built then discarded, hollow on short logs (`…-crypticity-stored-memory`).

So *coupling detection* between two mesh signals is well covered. What is **not** covered is the **kind** of coupling: whether two co-oscillating streams are mutually/anticipatorily coupled (the enactive, participatory-sense-making signature) or one is merely *reacting* to the other a step late.

## The concept, and where I found it (live + seminal literature)

**Interaction-dominant dynamics** (Van Orden, Holden & Turvey 2003, *Self-organization of cognitive performance*, JEP:General) and **complexity matching** (Marmelat & Delignières 2012, *Strong anticipation: complexity matching in interpersonal coordination*, Exp Brain Res 222:137–148, doi:10.1007/s00221-012-3202-9; multifractal operationalization Delignières et al. 2016, doi:10.1007/s00221-016-4679-4) are the 4E field's answer to *"are two agents genuinely coupled as one embodied interaction, or two independent processes producing similar output?"*

The full metric matches two agents' **1/f (multifractal) complexity signatures** — the correlation of their DFA/MFDFA exponents across windows. But the load-bearing *discriminator*, and the part that is both new to us **and** computable on the data we actually have, is smaller and sharper:

> **Windowed detrended cross-correlation, lag −1 / 0 / +1.**
> - **Genuine anticipatory / complexity-matched coupling → a single positive peak at lag 0.** The two systems' *movements* align with no lead — the signature of mutual, strongly-anticipatory coupling.
> - **Reactive follow-the-leader (discrete asynchrony-correction) → peaks at lag ±1 with a weaker/negative peak at lag 0.** One stream corrects toward the other a step late.

This is the exact test Marmelat & Delignières use to prove observed inter-agent synchrony is *complexity matching* and not trivial reactive tracking.

## The gap in the genome (`scripts/mesh-cooscillate`)

`mesh-cooscillate` pairs every two numeric mesh signals (RSSI, lux, baro, battery…), first-differences them, and tests **lag-0 Pearson r on the deltas**:

- `:455–461` builds `da`, `db` (the two delta series over the common window) and appends `(A, B, pearson(da,db), nd)` — **only lag 0**.
- `:496` reads phase purely from the *sign* of that lag-0 r ("in sync" / "in anti-phase").

So the tool can say *that* two streams co-move and *in which phase* — but it is structurally **blind to lead/lag**. A phone RSSI that consistently *reacts* to an appliance's RF one scan later, and a phone that is *anticipatorily* coupled to it, produce the **same** lag-0 finding today. That is precisely the anticipatory-vs-reactive distinction the 4E literature makes computable, and our current toolkit cannot express it.

## Honest split: what is embodiable vs what is hollow here

**DISCARDED — the DFA/MFDFA complexity-matching exponent correlation is a hollow sense on our windows.** `mesh-cooscillate` runs on `MIN_OVERLAP=8` Δ-steps (`:137`), and real pairs surface at nd≈8–20. A stable DFA α needs hundreds of points; a multifractal spectrum width needs more. Computing an exponent on 8–20 deltas would **hallucinate** one under finite-length bias — the identical trap the crypticity review hit (its χ estimator fired CRYPTIC 1.53b on a clean period-10 stream from finite-L bias alone, and was reverted as a hollow sense). Do **not** put a DFA exponent on these logs.

**EMBODIABLE — the lag-±1 cross-correlation discriminator is data-frugal and genuinely new.** On nd≥8 deltas you can compute `pearson` at lags −1/0/+1 with nd−1 pairs — no exponent, no fitting, just three correlations the tool almost already computes. It qualifies each co-oscillation as:

- **SYMMETRIC/anticipatory** — |r₀| is the max and clearly exceeds |r±1|.
- **LEAD/LAG (reactive)** — |r₊₁| or |r₋₁| exceeds |r₀|; name which stream leads.

## Proposed application (deferred, sequenced — not landed as code here)

Add to `scripts/mesh-cooscillate` a **report-only** lead/lag axis:

1. A `xcorr_lag(da, db)` helper returning `(r_m1, r0, r_p1)`.
2. A `--leadlag` (or fold into `--dry`) diagnostic that, for each **already-emitted** pair, prints the lag signature and the SYMMETRIC/LEAD/LAG classification. **Do not touch the emit gate** (still lag-0 r ≥ MIN_R, Bonferroni fisher_p ≤ ALPHA) and **do not touch the finding text** — the `CO-OSCILLATION (auto, real data): …` prefix has a byte-exact downstream contract with `mesh-queue-tend`'s resolver (`:499–504`); the lag signature goes to a diagnostic line/log, never into the resolved finding.
3. RED-first test: plant one synthetic **reactive** pair (`db[t] = da[t−1] + noise` → peak at lag +1) and one **anticipatory** pair (`db[t] = da[t]` → peak at lag 0); assert the classifier labels each correctly; break it, watch it go RED, restore.
4. Report-only against **live** `presence.log` co-oscillation pairs first (mirrors the surrogate-null review's `--surrogate` discipline) — the signature is only meaningful on real coupled pairs, of which there may be none in a given window, so it must prove itself on real data before any consumer reads it.

**Why deferred, not landed now:** this is a second additive change to the *same* live reflex on which the block-bootstrap surrogate null (`info-theory-agency-surrogate-null`) is already queued. Both are report-only diagnostics on `mesh-cooscillate`'s core; they should be **sequenced deliberately** (surrogate null first — it changes the emit *significance*; then this lead/lag axis on top) rather than piled up as two uncommitted refactors racing on one file. The concrete, file-named, RED-testable plan above is the artifact; the code lands in its turn.

## Citations (verifiable)

- Van Orden, Holden & Turvey (2003), *Self-organization of cognitive performance*, J. Exp. Psychol. General.
- Ihlen & Vereijken (2010), *Interaction-dominant dynamics in human cognition: beyond 1/fα fluctuation*, JEP:General 139(3):436–463, doi:10.1037/a0019098.
- Marmelat & Delignières (2012), *Strong anticipation: complexity matching in interpersonal coordination*, Exp Brain Res 222:137–148, doi:10.1007/s00221-012-3202-9.
- Delignières et al. (2016), *Multifractal signatures of complexity matching*, Exp Brain Res, doi:10.1007/s00221-016-4679-4.
- Coco & Dale (2014), *CRQA of categorical and continuous time series* (R package), arXiv:1310.0201 — the CRQA runner-up (structural coordination metrics; moderate overlap with our coupling-null work, so not the pick).
- Goldstein et al. (2026), *Cross-recurrence quantification analysis captures inter-brain coupling during naturalistic negotiation*, Front. Neurosci. 19:1713357, doi:10.3389/fnins.2025.1713357 — live CRQA application.

## Related memory

Ties to `[[cooscillate-parametric-p-ignores-autocorrelation]]` (same tool, the queued surrogate-null work this sequences behind) and `[[crypticity-vs-excess-entropy-hollow-on-short-logs]]` (the finite-L hollow-sense precedent that rules out the DFA half here).
