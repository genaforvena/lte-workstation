# Information theory of agency → PID: is `mesh-motion-fuse`'s "neither alone answers" a *measured* synergy?

**Date:** 2026-07-31 · **Lane:** genome literature live-review (feed auto-task) · **Organ named:** `scripts/mesh-motion-fuse`

## Area & what the mesh already embodies

Information theory of agency — empowerment and predictive information — is a near-saturated seam here
([[info-theory-agency-coverage]]). The measures we embody are all **scalar, single-channel** informations:

- **Empowerment** `MI(action; future-sensor)` — `mesh-algedonic` AGENCY_INFO (+ finite-sample null, 07-30).
- **Process / closed-loop empowerment** `I(action; Δpain | band0)` — algedonic CL companion.
- **Predictive information** `I(past; future)` — `mesh-precision --num pred_info`.
- **Transfer entropy** `TE(x→y)` — `mesh-cooscillate` (+ block-bootstrap surrogate null).

Every one of these answers *how much* one stream tells about another. **None of them answers the question
that arises the moment you have TWO source streams feeding ONE target:** when sensors X₁ and X₂ jointly
predict a fused verdict Y, is that joint information **redundant** (either axis alone suffices), **unique**
(only one axis carries it), or **synergistic** (the verdict is legible *only* from the two axes together)?
Plain `MI(X₁,X₂ ; Y)` collapses all three into one number and cannot tell them apart.

## The concept we do NOT embody — Partial Information Decomposition (PID)

**Partial Information Decomposition** (Williams & Beer, *Nonnegative decomposition of multivariate
information*, arXiv:1004.2515, 2010) splits the joint mutual information of two sources about a target into
four non-negative atoms:

> `I(X₁,X₂ ; Y) = Red(X₁,X₂ ; Y) + Unq(X₁ ; Y) + Unq(X₂ ; Y) + Syn(X₁,X₂ ; Y)`

- **Redundancy** — information *either* source alone already gives about Y.
- **Uniqueness** — information *only* X₁ (resp. X₂) gives.
- **Synergy** — information present *only when both sources are read together*, in neither alone.

It is a live, actively-published literature — not a settled list. Recent 2025–2026 work is specifically on
**estimators and their pathologies**: closed-form Gaussian PID estimators (arXiv:2605.09919, 2026), a unified
taxonomy via **integrated** information decomposition ΦID (PNAS, 2025), and documented **inconsistencies** in
multivariate PID (arXiv:2510.14864 / arXiv:2508.05530, 2025). On the agency side it is used to quantify a
reinforcement-learning agent's **autonomy** — how much its behaviour is synergistic internal integration vs
redundant echoing of the environment — and to quantify **multimodal fusion interactions** (Liang et al.,
*Quantifying & Modeling Multimodal Interactions*, arXiv:2306.04125, NeurIPS 2023): redundancy = both
modalities give the same prediction, uniqueness = one enables a prediction the other cannot, **synergy = both
together enable a prediction neither makes alone.**

That last sentence is, almost verbatim, the design charter of one of our organs.

## The concrete application — `scripts/mesh-motion-fuse`

`mesh-motion-fuse` fuses **two** axes — a **body-motion** sensor (phone accel: walked / carried / handled vs
STILL) and an **RF/ambient-motion** sensor (wifi-CSI: MOTION / STILL) — into an occupancy-attribution verdict:

- `BODY-MOVING` — the tracked body itself moves,
- `AMBIENT-ONLY` — RF moves while the body is STILL → *someone else* moving in the space,
- `QUIET` — both still.

Its header states the reason it exists (`scripts/mesh-motion-fuse:12`):

> *"Neither alone answers 'is the activity the node/phone being handled, or PEOPLE moving around a put-down
> phone?' … This tool exposes it."*

**That is a synergy claim in prose.** "Neither alone answers" = `Syn(body, rf ; verdict) > 0`, and moreover
that the AMBIENT-ONLY⁄BODY-MOVING split lives *in the synergy atom* — it is exactly legible only from the two
axes jointly. PID is the metric that would **verify that claim against the artifact**, and right now the
claim is **unfalsifiable**: `mesh-motion-fuse` is a stateless on-demand classifier that **logs nothing**
(no `~/.mesh/motion-fuse.log`; it `printf`s the verdict to stdout at line 260 and exits). There is no history
on which synergy could ever be measured. A load-bearing information-theoretic claim with no artifact behind it
is the mesh's own recurring shape — *a claim in prose is not the artifact*
([[a-comment-is-not-a-channel-to-the-reader]], [[non-empty-is-not-correct]]).

**Proposed edit (report-only, two honest steps):**

1. **Give the fusion a history.** Append one line per invocation to `~/.mesh/motion-fuse.log`:
   `<ts> verdict=<V> wifi=<MOTION|STILL|UNREACH> body=<MOVING|STILL|UNREACH> corr=<yes|no> degraded=<..>`.
   The two source axes are already in hand at line 260 (`wifi=%s body=%s`) — this is a one-line append, gated
   by its own `--test` asserting the line is written and re-readable (never written *by* `--test` itself —
   [[a-tests-forged-artifact-mimics-a-flapping-sense]]).

2. **`mesh-motion-fuse --pid`** (once N accrues) — a report-only diagnostic that reads the log, discretises
   the two source columns and the verdict, and computes the Williams–Beer PID
   (`Red = Σ_y p(y) min_i I(X_i ; Y=y)`, the `I_min` redundancy; the other atoms follow by Möbius). It reports:
   - `SYN_CONFIRMED` — `Syn / I(X₁,X₂;Y)` is a real fraction above a shuffled-source surrogate null (reuse the
     algedonic/cooscillate null idiom — PID's small-sample bias is the same trap, [[surrogate-null-cooscillation]]).
     The two-axis fusion earns its cost; the AMBIENT-ONLY split is genuinely legible only from both.
   - `SYN_HOLLOW` — the verdict is dominated by **redundancy** (one axis reconstructs it): the fusion's central
     distinction is illusory in the lived data, and the tool is an expensive `OR` of two axes that mostly agree.
   - `AXIS_DEAD` — one axis's `Unq` ≈ 0 **and** it is UNREACH most cycles: that axis contributes nothing; its
     failure is being silently tolerated.

**Why this is actionable, not decorative.** The three atoms map straight onto the **honest-fusion rule**
(an unreachable input must render UNKNOWN, never a faked all-clear):
a **redundant** axis pair means one axis's loss is *tolerable* — fusion may stay confident on the survivor; a
**synergistic** pair means losing *either* axis MUST collapse the verdict to UNKNOWN, because the distinction
lives only in the pair and cannot be recovered from one. Today `mesh-motion-fuse` hard-codes that policy by
hand (the `body-unreach` / `rf-unreach` degraded branches at lines 78–81, 215) **without ever measuring which
losses are actually fatal.** PID is the measurement that tells you whether those degraded branches match the
real information geometry — or whether the tool degrades gracefully on a loss that in fact guts its only
reason to exist. Same lesson, RF-fusion flavour, as [[writer-redundancy-blinds-mtime-liveness]].

## Discarded alternative (one line)

**Dynamical independence** (Barnett & Seth, *Phys. Rev. E* 108:014304, 2023 — emergence as minimised
micro→macro transfer entropy): **discarded** — it needs a high-dimensional *microscopic state vector* to
coarse-grain, which no mesh organ exposes; our streams are already macroscopic scalars, so there is no
micro-level for it to be independent *of*.

## Status

This review is the artifact (proposal + grounded target + discard). **No tool edited this turn** — the honest
first step (axis+verdict logging) has no data behind it yet, and forcing a `--pid` implementation onto an
empty log would be exactly the hollow `--test`-asserts-a-real-read anti-pattern this lane exists to catch.
The proposal names the file, the lines, the estimator, and the null so the logging step + `--pid` land
directly when picked up. Uncommitted in tree (this doc). Steward lands.

## Cite

- Williams & Beer, *Nonnegative Decomposition of Multivariate Information*, arXiv:1004.2515 (2010) — origin of PID.
- Liang et al., *Quantifying & Modeling Multimodal Interactions*, arXiv:2306.04125 (NeurIPS 2023) —
  redundancy/uniqueness/synergy for multimodal (multi-sensor) fusion.
- *Closed-Form Gaussian Estimators for Multi-Source Partial Information Decomposition*, arXiv:2605.09919 (2026).
- *Subsystem Inconsistency in Partial Information Decomposition*, arXiv:2510.14864 (2025);
  *Multivariate PID: Constructions, Inconsistencies, Alternative Measures*, arXiv:2508.05530 (2025).
- Barnett & Seth, *Dynamical independence*, Phys. Rev. E 108:014304 (2023) — the discarded alternative.
