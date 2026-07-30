# Live-literature review — information theory of agency: PROCESS (closed-loop) EMPOWERMENT — the open-loop empowerment estimator SEVERELY UNDERESTIMATES agency in stochastic environments

Date: 2026-07-28 · lane: genome (idea-queue LITERATURE task — information theory of agency / empowerment /
predictive information, from the angle of a known **CRITIQUE / failure mode** of the area) · status: fix in
tree + deployed, uncommitted (steward lands)

## Where we had already been (checked before landing, so this doesn't double-count)

Information theory of agency is a heavily-worked mesh seam. Every embodied piece measures empowerment as an
**OPEN-LOOP** quantity — the mutual information between an action (a one-shot push) and a later state —
never the closed-loop, feedback-conditioned version:

- **empowerment — action→future-sensor-state MI** (channel capacity of the sensor-actuator loop) →
  `scripts/mesh-algedonic` AGENCY_INFO sidecar (marginal MI between board ACTION presence and the next
  algedonic pain-change bucket). **Open-loop by construction.**
- **causal action empowerment** (extract controllable action/state/reward relations; Cao/Chu et al., Sci.
  China Inf. Sci. 2025) → already *cited* in `mesh-algedonic`'s header.
- **instrumental / multi-agent empowerment** (through other minds; interference channel) →
  `scripts/mesh-mind-control:155`, `:1324`.
- **Maximum Occupancy Principle** (occupy future action-path space; Ramírez-Ruiz & Moreno-Bote 2024) →
  `scripts/mesh-vitality`.
- **predictive information / excess entropy** as a structure-vs-noise discriminator → `mesh-sensorium`/`mesh-rhythm`.
- **overwrite control vs hidden-state identification** (Csaky 2026) → review 2026-07-24.
- **assistive empowerment** (maximize the OPERATOR's option-space; Myers et al. NeurIPS 2024) →
  `scripts/mesh-interruptibility --foreclosure` (review 2026-07-28).
- **EFE / active sensing** (Friston) → `scripts/mesh-interruptibility --probe`.

The unembodied branch is the **critique of the open-loop assumption itself** — the axis on which every one
of the above is silently exposed.

## The concept not yet embodied — PROCESS (closed-loop) EMPOWERMENT, and the failure mode it names

**Standard (open-loop) empowerment SEVERELY UNDERESTIMATES an agent's control in STOCHASTIC environments,
because it treats an action as a one-shot committed push and never models that a real agent OBSERVES
intervening feedback and adapts.** In a noisy world the raw MI(action; later-state) gets diluted — the same
"action present" bucket mixes runs where intervening noise, not the action, drove the outcome — so a channel
that is genuinely controllable *with feedback* reads as near-zero agency. The fix, **process empowerment**,
lets the probing consider feedback while choosing actions (closed-loop options) and recovers the control the
open-loop measure buried.

**Primary source** (found via live web review 2026-07-28, cross-confirmed across three independent search
returns; the publisher PDF sits behind a Radware bot-wall so it is cited, not fetched in full):

- **L. Tiomkin, C. Salge, D. Polani, "Process empowerment for robust intrinsic motivation"**, *Journal of
  Physics: Complexity* **6**(3), 2025 — doi:10.1088/2632-072X/adf2ec. Key finding, verbatim from the
  indexed abstract: *"Using open-loop options can lead to severe **underestimation** of empowerment in
  stochastic environments, resulting in agents that aim to reach low-empowerment states. In contrast, when
  using closed-loop options the empowerment will grow quadratically with the option length…"* — i.e. the
  open-loop estimator is not merely noisier, it is **biased toward reading real agency as powerlessness**.

**Why this is new ground for us.** `mesh-algedonic`'s AGENCY_INFO is *exactly* the open-loop shape the paper
critiques: marginal `MI(action; Δpain-bucket)`, blind to the fact that minds act **conditioned on the pain
band they observe**. On a noisy mesh tape (many events between an action window and a pain-change) this will
label a feedback-controllable-but-noisy pain channel `AGENCY_LOW` — and a naive consumer reads that as *"the
mesh cannot steer its own pain,"* the precise underestimation failure mode, an open-loop artefact reported as
a fact. None of the eight embodied items above carries a feedback-conditioned companion.

## The one concrete application (shipped, report-only) — `scripts/mesh-algedonic` AGENCY_INFO

Added a **closed-loop companion** to `agency_info()`: alongside the open-loop marginal MI, compute the
**band-conditioned** mutual information `I(action; Δpain | band0)`, where `band0` (lo/mid/hi pain at the
interval's START) is the feedback a mind actually observes before acting. Two extra output fields
(`closedloop=<label> clmi=<mi_closed>`) on the same status line; positions 1–4 unchanged (backward-compatible
with the existing test and log readers).

The **load-bearing flag** is the failure-mode guard:

```
mi_closed − mi_open ≥ AI_CL_MARGIN (0.05)  →  CL_UNDERCOUNT   (open-loop diluted real, feedback-conditioned
                                                                agency — do NOT trust the LOW label)
mi_open − mi_closed ≥ AI_CL_MARGIN         →  CL_INFLATED     (open-loop over-read: a band confound faked control)
otherwise                                  →  CL_CONCORD
every band too thin (< AI_CL_MIN_N pairs)  →  CL_NA           (honest n/a, never a fabricated concordance)
```

So a `AGENCY_LOW` reading can **never again pass silently** as low agency: if conditioning on observed
feedback recovers the control the marginal buried, the line says `closedloop=CL_UNDERCOUNT` next to it. This
is the honest-degraded twin of the open-loop number — a **companion, not a replacement**, and still
**report-only** (no escalation, no policy control), consistent with the sidecar's read-only charter.

### Verification (artifact, not assertion)

- **Live on the real tape** (2026-07-28T22:03Z): `agency=AGENCY_LOW mi=0.000 … closedloop=CL_CONCORD
  clmi=0.002` — on current real data the open-loop LOW is honestly concordant (no hidden agency to recover);
  it does **not** false-positive.
- **Suppressor fixture** (action carries ~0 marginal info but perfect info once conditioned on band —
  lo-band act→improve, hi-band act→worse): `AGENCY_LOW 0.007 … CL_UNDERCOUNT 0.984` — open-loop reads
  powerlessness, closed-loop recovers near-perfect agency. The exact failure mode, caught.
- `mesh-algedonic --test` → `smoke-test: ok`, rc 0 (test 7b added).
- **Gate seen RED:** breaking the band conditioning (`band0` → constant, so conditional == marginal) flips
  the fixture to `CL_CONCORD` and the suite fails: `FAIL: closed-loop UNDERCOUNT flag → expected
  'CL_UNDERCOUNT' got 'CL_CONCORD'` / `smoke-test: FAIL`. The gate asserts the real recovery, not its own text.
- **Honest n/a proven:** `AI_CL_MIN_N=99` (every band too thin) → `CL_NA`, not a faked concordance.
- Source edited in `scripts/mesh-algedonic`; deployed to `~/.local/bin/mesh-algedonic` (source→bin, correct
  direction — no drift). Uncommitted; steward lands.

## Verdict

**LAND.** One un-embodied concept from a genuine 2025 **critique** of the area (process / closed-loop
empowerment — open-loop MI underestimates agency in stochastic environments), one recent primary source
(Tiomkin, Salge & Polani, J. Phys. Complexity 2025), one shipped report-only application on a named organ
(`mesh-algedonic` AGENCY_INFO closed-loop companion + `CL_UNDERCOUNT` guard), gated by a test seen to fail
when the conditioning is defeated.

---

Sources:
- [Process empowerment for robust intrinsic motivation — IOPscience (J. Phys. Complexity 6(3), 2025)](https://iopscience.iop.org/article/10.1088/2632-072X/adf2ec)
- [Empowerment and intrinsic motivation — D. MacKinlay (survey of critiques/failure modes)](https://danmackinlay.name/notebook/empowerment.html)
- [Causal action empowerment for efficient RL in embodied agents — Cao et al., Sci. China Inf. Sci. 2025](https://link.springer.com/article/10.1007/s11432-024-4396-3)
