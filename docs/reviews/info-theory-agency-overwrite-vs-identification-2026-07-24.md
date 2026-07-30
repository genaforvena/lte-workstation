# LITERATURE (live review) — information theory of agency → a distributed sensor mesh

**Area:** information theory of agency — empowerment, predictive information
**Angle:** cross-domain transfer (agency theory → mesh liveness instrumentation)
**Reviewer:** genome mind · 2026-07-24 · live web search + full read of the source
**Verdict:** LAND — one un-embodied concept, one shipped (report-only) application
**Status:** uncommitted in the tree; steward lands

---

## The concept we did not have

**Overwrite control vs hidden-state identification — the prediction/empowerment separation.**

R. Csaky, *"Prediction and Empowerment: A Theory of Agency through Bridge Interfaces"*,
arXiv:2605.06346, submitted **7 May 2026** — <https://arxiv.org/abs/2605.06346>
(read: abstract + HTML full text, <https://arxiv.org/html/2605.06346>).

The paper models sensing and actuation as **bridge interfaces**, each split into an
**agent-owned parameter** and an **environment-owned channel state**, inducing a deterministic
POMDP over latent microstates with many-to-one observation coarsening. Its result is a
*separation*, not a new objective:

- **Identification** (Def. 1): the transcript is lossless for the target, `H(Q | 𝒯_T) = 0`.
- **Overwrite control** (Thm 3, §4): the agent maps many latent values to the same terminal
  target, making the future **action-determined**. Prediction succeeds by *collapse*, not by
  learning anything.
- **Proposition 1** exhibits arbitrary separations, including **perfect prediction via overwrite
  despite `I(Z; M_T) = 0`** — a prediction objective *maximally satisfied while carrying zero
  bits about the world* — and its sibling, **distractor control**: high empowerment over a
  settable light while the task-relevant latent stays unresolved.
- **Interface refinement** (Thm 5): a Blackwell-finer interface can only raise `I(Z; O)`.

**Why this is new ground for us.** The mesh has reviewed empowerment repeatedly — classic
single-agent option value (`review-empowerment-metric-2026-06-20`), instrumental/multi-agent
(`…-mesh-mind-control-2026-06-21`, ECAI 2025), process/closed-loop (`…-2026-07-05`, J. Phys.
Complexity 2025), egoistic interference (`…-2026-07-07`), and the forward-allocation axis
(`lit-empowerment-forward-axis-…-2026-07-10`). Every one of them treats empowerment as a
*quantity to maximise or allocate by*. None of them carries the **separation**: that a
prediction/liveness objective can be satisfied by the agent's **own action** instead of by the
world. `grep -rn 'overwrite control|hidden-state identification|bridge interface|Blackwell'`
over `scripts/`, `docs/`, `~/.mesh/knowledge/` returns nothing. The 2026-06-24 AREA-MINED note
discarded this area for want of a trained encoder / reward channel — this transfer needs
neither: it is a statement about **which component of an interface a verdict rests on**.

## Where it bites — `scripts/mesh-reflex-health`

Our liveness predicate is **mtime**. The mesh's own liveness-touch convention
(`mesh-state-touch`: touch on *every* successful eval, so a long-stable value cannot decay into
a false STALE) makes mtime an **agent-owned parameter by construction**. In the paper's terms
our freshness verdict is **overwrite-satisfied**: it is action-determined, and therefore cannot
— at *any* threshold — separate

> "the reflex read the world" from "the reflex ran and its probe handed back last week's value".

That is not a hypothetical. It is `mesh-psi` (cron beat every 10m, lease-fresh, `.psi.state`
frozen four days) and the `mesh-mag`/`mesh-gyro` empty-read class (cron green, state artifact
five days stale). The file already names the gap — the D&G refrain block at `:~386`, "a fresh
BEAT is not an OPEN refrain" — and **HELD** the fix, on the grounds that telling "the world is
genuinely constant" from "the read is frozen" needs a per-reflex expected-variation model.

**The bridge-interface split dissolves that blocker for the reporting half.** No variation model
is needed to state *which component carried the verdict*: mtime (agent-owned) or content
(environment-owned). The refrain gave the grammar; this gives the discriminator.

## Shipped (uncommitted) — report-only attribution

`scripts/mesh-reflex-health`:

- `overwrite_probe()` — digests an artifact's **content only** (capped tail read; **mtime
  deliberately excluded** — it is the very agent-owned parameter under corroboration) and
  reports how long an mtime-**fresh** artifact's bytes have not moved.
- The floor is **derived, never a literal**: `MESH_REFRAIN_MULT` (default 4) × that reflex's own
  `eff_maxage`, i.e. the same live-cron authority the staleness threshold already uses. A
  run-count floor would be silently vacuous for any watched reflex slower than the health
  cadence — the same class as a `max_age` literal that stops matching its cron.
- Past the floor, `--check` and the trace annotate `overwrite-only: <name>(value-frozen Ns ≥ Ms)`.
  It **never** enters `stale`, never debounces, never fires `[reflex-stale]`, never changes the
  exit code, and never uses the stale vocabulary `mesh-needs` scrapes. A genuinely-constant
  artifact is a legitimate reading; calling it dead is exactly the false-STALE the touch
  convention exists to kill. Honest fusion in both directions: disclose the provenance, don't
  guess the world.
- Trace emission is edge-triggered against the last reported set.

**Verification (artifacts, not claims):**

| claim | artifact |
|---|---|
| the gate is real | mtime put back into the digest → **5 assertions went RED**, restored → green |
| the gate was vacuous first | a bare `touch` inside the same second left `%Y` unchanged, so the mtime-exclusion assert passed against a *broken* digest; fixture now moves mtime by an explicit offset |
| test isolation | `MESH_REFRAIN_DIR` is read at **call** time — as a load-time global the `--test` silently wrote the LIVE store (seen: `~/.mesh/.refrain/k1`), the test-forges-its-own-artifact fault |
| first sight is silent | `read … < "$f" 2>/dev/null` leaked one stderr line per reflex (redirect order); guarded, asserted |
| report path fires | `MESH_REFRAIN_MULT=0 mesh-reflex-health --check` → all 7 fresh reflexes attributed |
| trace fires once | 3 forced runs → **exactly 1** `[reflex-overwrite]` line in `~/.mesh/traces.log` (edge-trigger holds) |
| nothing else moved | `--test` green, `--check` `ok (7 per-run reflex(es) fresh)`, rc=0 |

Note: the one `[reflex-overwrite]` line at 21:41:40Z in the live trace is that forced-floor
(`0×`) drive, not a real finding.

## What is still HELD

The **openness gate** — deciding whether a frozen value means a wedged probe — remains held, and
the paper says why in its own terms: that judgement needs the interface's environment-owned
channel to be *modelled*, not merely *named*. Attribution is shippable; adjudication is not.

## Sources

- [Prediction and Empowerment: A Theory of Agency through Bridge Interfaces — arXiv:2605.06346 (7 May 2026)](https://arxiv.org/abs/2605.06346) · [full text](https://arxiv.org/html/2605.06346)
- [Towards reasoning-empowered task-oriented communication for agent networks — npj Wireless Technology (2026)](https://www.nature.com/articles/s44459-026-00028-z) — surfaced in the same sweep; **discarded**: task-oriented comms presupposes a jointly-trained transmission policy, the same missing-architecture reason the 2026-06-24 AREA-MINED note gave.
- Prior mesh reviews of this area (for non-duplication): `~/.mesh/knowledge/review-empowerment-metric-2026-06-20.md`, `review-instrumental-empowerment-cooperation-values-mesh-mind-control-2026-06-21.md`, `review-process-empowerment-closed-loop-2026-07-05.md`, `review-multiagent-empowerment-interference-egoistic-fitness-2026-07-07.md`, `lit-empowerment-forward-axis-vs-neglect-gradient-2026-07-10.md`, `review-info-theory-agency-AREA-MINED-frontier-2026-06-24.md`.
