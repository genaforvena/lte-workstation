# Live-literature review — information theory of agency: ASSISTIVE EMPOWERMENT — maximize the OPERATOR's empowerment (his option-space), don't infer his reward

Date: 2026-07-28 · lane: genome (idea-queue LITERATURE task — information theory of agency / empowerment /
predictive information, from a RECENT 2023–2026 result) · status: fix in tree + deployed, uncommitted
(steward lands)

## Where we had already been (checked before landing, so this doesn't double-count)

Information theory of agency is a heavily-worked mesh seam. Every embodied piece treats empowerment as a
quantity a **MIND** maximizes or is allocated by — never the **operator's** empowerment as the objective:

- **classic single-agent option value** (reachable-future count) → `scripts/mesh-ideate`.
- **instrumental empowerment** — a mind's influence routed *through other minds* (Selmonaj et al., ECAI
  2025) → `scripts/mesh-mind-control:155`.
- **multi-agent empowerment as an interference channel** — egoistic per-mind maximization is collectively
  incoherent unless the mutual-coupling term is modelled (Shah, Nemenman, Polani & Tiomkin, Apr 2026) →
  `scripts/mesh-mind-control:1324`.
- **empowerment — action→future-sensor-state mutual information** (channel capacity of the sensor-actuator
  loop) → `scripts/mesh-algedonic` AGENCY_INFO sidecar.
- **Maximum Occupancy Principle** (occupy future action-path space; Ramírez-Ruiz & Moreno-Bote, Nat. Comm.
  2024) → `scripts/mesh-vitality` `action_occupancy()`.
- **predictive information / excess entropy** I(past;future) as a structure-vs-noise discriminator →
  review 2026-07-28, shipped into `mesh-sensorium`/`mesh-rhythm`.
- **overwrite control vs hidden-state identification** (Csaky 2026) → review 2026-07-24.
- **Expected Free Energy / active sensing** (Friston; the ACTION-half epistemic gate) →
  `scripts/mesh-interruptibility --probe`.

Every one of these asks *"how much control does a MIND have."* The unembodied branch flips the **subject**
of the empowerment functional from the mind to the **human**.

## The concept not yet embodied — ASSISTIVE EMPOWERMENT (maximize the human's empowerment)

**An assistant should maximize the *human's* empowerment — the mutual information between the human's
actions and future environment states, i.e. keep his reachable-future set as large as possible — INSTEAD
of inferring his reward and driving to it.** Classical assistance is inverse-RL: infer the human's
goal/reward, then act toward it. In high-dimensional, ambiguous settings that inference is brittle. The
empowerment framing sidesteps it: the assistant never needs to know *what* the human wants, only to keep
him maximally able to reach *whatever* he chooses.

**Primary source** (found via live web review 2026-07-28, full read):

- **V. Myers, E. Ellis, S. Levine, B. Eysenbach, A. Dragan, "Learning to Assist Humans without Inferring
  Rewards"**, *NeurIPS 2024* — arXiv:2411.02623 · <https://empowering-humans.github.io/>. Their objective
  **ESR (Empowerment via Successor Representations)** is a scalable, model-free contrastive estimator that
  maximizes the influence of the *human's* actions on future states; it scales past prior tabular
  empowerment-assistance work and beats reward-inference baselines on Overcooked.

**The recent caveat that makes it a live result, not a settled one:**

- **C. Yang, C. J. Zhang, M. Cakmak, M. Kleiman-Weiner, "When Assisting One Disempowers Another"**,
  arXiv:2511.04177 (**Nov 2025**, read in full) — in a multi-party scene, an assistant maximizing one
  party's empowerment can *narrow another party's action space / causal influence*. So operator-empowerment
  is **net-across-parties**, never a clean single number when a third party is co-affected.

**Why this is new ground for us.** The mesh is, structurally, an assistant to a human operator, and its
whole fusion stack is the *infer-the-reward* style the paper argues against: `mesh-operator-state`,
`mesh-home-state`, `mesh-situation`, EFE novelty/salience — all estimate *what the operator wants / is
doing* so a proactive organ can act toward it. **Nowhere does the mesh ask whether a proactive act ENLARGES
or FORECLOSES the operator's own option-space.** That is the assistive-empowerment axis, and it is
orthogonal to every gate we have.

## The one concrete application (shipped, report-only) — `scripts/mesh-interruptibility`

`mesh-interruptibility` already answers *"may I interrupt NOW?"* — a **timing** question over the operator's
attention (bands DO-NOT-DISTURB / FOCUSED / RESTING / AVAILABLE / AWAY / UNKNOWN). It does **not** answer the
orthogonal question ESR poses: *given that it's an OK time, which FORM of the act least forecloses the
operator's option-space?* Two acts carrying the **same intent** are not equal at the same band — a
dismissible TG line preserves his control; seizing the one shared speaker, or acting toward a third party
on his behalf, forecloses it.

Added a pure, offline-testable **`--foreclosure`** verb (globals `_foreclosure`, gated in `--test`):

```
foreclosure = reversibility + exclusivity + attention-capture      (each 0..3; total 0..8)
  reversibility  — can he undo/ignore it at ~zero cost?            (0 ignore … 3 irreversible)
  exclusivity    — does it seize a shared/scarce resource he loses? (0 private … 3 scarce-external)
  attention      — does it commandeer his attention (forced switch)?(0 pull … 3 hard capture)
```

| form (same-intent alternatives) | rev | exc | att | foreclosure | band |
|---|---|---|---|---|---|
| `tg-line` / `board-post` | 0 | 0 | 0 | **0** | LOW |
| `ambient-mix` (quiet mix, shared speaker) | 1 | 2 | 1 | 4 | MED |
| `speaker-say` | 1 | 2 | 2 | 5 | MED |
| `speaker-autoplay` | 2 | 2 | 2 | 6 | HIGH |
| `ring-call` | 2 | 1 | 2 | 5 | MED |
| `tv-seize` | 2 | 3 | 2 | 7 | HIGH |
| `act-third-party` (SMS/msg on his behalf) | 3 | 3 | 1 | 7 | HIGH |

**The consumer rule (ESR as a tie-break over forms):** among the action forms that carry your intent, pick
the **minimum foreclosure**. E.g. "surface a new music mix" → prefer `tg-line` (0, he plays it if he wants)
over `ambient-mix` (4) or `speaker-autoplay` (6). This maximizes the operator's empowerment without ever
inferring *whether he wants the mix* — exactly the ESR move.

**The disempowerment caveat is honored, not collapsed.** A `+party` flag (Yang et al., Nov 2025) tags the
score `caveat=multi-party-disempowerment` rather than pretending a single number is complete — the
honest-degraded spirit of the rest of the tool: an act that empowers the operator may disempower a
co-present party, so the score is explicitly *not* the whole objective there.

**Report-only** — it nominates the least-foreclosing form; it never actuates (conservative-actuator
doctrine, same as `--probe`). **Anti-silent-fallback:** an unknown/out-of-range form is *refused* (exit 2),
never scored 0 — a 0 would read as "maximally empowerment-preserving," the exact all-clear-from-a-failure
trap CLAUDE.md warns against.

### Verification (artifact, not assertion)

- `mesh-interruptibility --test` → `smoke-test: ok (… + 10 foreclosure/ESR)`, rc 0.
- **Gate seen RED:** inverting the `tg-line` row (0,0,0 → 3,3,2) makes the ESR-ordering assertion fail
  (`reversible-private (tg-line=8) must foreclose LESS than exclusive-irreversible (speaker-autoplay=6)`,
  rc 1) — the gate asserts the real ordering, not its own text.
- Live: `--foreclosure act-third-party +party` → `foreclosure=7/8 band=HIGH … caveat=multi-party-…`.
- Deployed to `~/.local/bin/mesh-interruptibility`; source edited in `scripts/` (steward lands).

## Verdict

**LAND.** One un-embodied concept (assistive empowerment — maximize the *operator's* option-space, don't
infer his reward), one recent primary result (Myers et al., NeurIPS 2024) + its live caveat (Yang et al.,
Nov 2025), one shipped report-only application on a named organ (`mesh-interruptibility --foreclosure`),
gated by a test seen to fail when the core ordering is broken.
