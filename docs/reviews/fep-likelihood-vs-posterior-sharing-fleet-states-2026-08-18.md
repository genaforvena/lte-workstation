# FEP / active inference — LIVE literature review, 2026-08-18

## Belief sharing sends a POSTERIOR; the fix is to send the LIKELIHOOD. The mesh's only cross-node sense channel sends the posterior and nothing else.

**Lane:** free energy principle & active inference (Friston), angle = **cross-domain transfer to a
distributed sensor mesh** · **Window:** genome · **Landed:** `scripts/mesh-fleet-states --likelihood`
(report-only) + one real bug the mode surfaced, both **uncommitted in the tree**.

---

## 1. How the live surface was swept (not a fixed list)

Two passes, both live:

1. **arXiv API, `all:"active inference"`, newest-first, 40 entries** (fetched 2026-08-18). The window
   since our last sweep holds: `2608.14466` EFE informative path planning (Mars), `2608.14165`
   integrated information in AIF, `2608.09512` renormalising generative models, `2608.09330`
   MI-dependent threshold response, `2608.02440` intention inference under execution noise,
   `2607.20306` state-dependent observation noise, `2607.19518` sophisticated policies from epistemic
   priors, `2607.16981` EFE as belief-dependent utility for ρ-POMDPs, `2607.16858` model-free epistemic
   free-energy estimators.
2. **Web search on the multi-agent / federated branch**, which is the branch that actually transfers to
   a mesh of nodes.

Several of the fresh arXiv items were **discarded as already-mapped**, checked against the corpus, not
from memory:

- `2607.20306` (state-dependent observation noise) — the *theorem* behind
  `fep-channel-knowledge-map-context-conditioned-observation-noise-precision-2026-08-11.md`; already
  embodied as `mesh-precision --ckm`.
- `2608.14466` (budgeted EFE path planning) — the budget/allocation axis landed 3 days ago as
  `mesh-precision --attend` (`fep-interoceptive-precision-allocation-…-2026-08-15.md`).
- `2607.16858` (epistemic vs aleatoric intrinsic reward) — the novelty/salience split is
  `efe-novelty-vs-salience-parameter-uncertainty-2026-07-27.md`.
- `2608.09512` (renormalising generative models) — coarse-graining closure was swept 2026-08-17 as
  `second-order-cyb-non-trivial-informational-closure-precision-2026-08-17.md`.

The landing came from the **federated-inference branch**: Friston et al., *"Federated inference and
belief sharing"*, Neurosci. Biobehav. Rev. 156 (2024) — read in full — whose §3.1 states the four
conditions on belief sharing (shared generative model, shared likelihood mapping, **self-attenuation**
so an agent does not hear itself, temporal alignment). Its self-attenuation clause is the mesh's
already-embodied `predictive-processing-circular-inference-overcounting-2026-07-28.md`. But it pointed
at the paper that carries the **operational** result:

> **Ozan Çatal, Toon Van de Maele, Riddhi J. Pitliya, Mahault Albarracin, Candice Pattisapu, Tim
> Verbelen (VERSES Research Lab), "Belief sharing: a blessing or a curse", arXiv:2407.02465** (IWAI
> 2024). Read in full from the PDF, not the abstract.

---

## 2. The mechanism we do NOT embody

The paper's contribution is not "sharing is good/bad" — it is that **the FORMAT of the shared message
decides**, and it derives the format from the variational message-passing update (their eq. 4):

> sᵒₜ = σ(μ²→B₂ + μ²↑A₂ + μ²↑A₃)

where μ²→B₂ is the receiver's **own prior** (its belief carried forward from the previous timestep),
μ²↑A₂ its **own fresh observation**, and μ²↑A₃ the message from the other agent. Sharing a **posterior**
through an identity likelihood mapping means

> μ²↑A₃ = μ²,ᵒᵗʰᵉʳ→B₂ + μ²,ᵒᵗʰᵉʳ↑A₂
>
> "This shows that, indeed, when agents have similar priors, this gets double counted in the belief
> update."

Their fix, verbatim:

> "To address this, we will now instead share the other's likelihood message only, i.e.
> μ²↑A₃ = μ²,ᵒᵗʰᵉʳ↑A₂. This scheme leaves out agents' prior beliefs about the state and only shares the
> agent's interpretation of the observation, treating the other agents as extra independent observers
> for the exact latent cause in the world. We call this scheme 'likelihood sharing'."
>
> "each agent treats the other agents as an extra 'pair of eyes'"

The two named failure modes of posterior sharing, both simulated (Figs. 3–4, alleviated in Figs. 5–6):

- **Echo chamber** — "the agents keep increasing their belief on the object being present at the a
  priori believed location **because of the constant sharing of beliefs**", with movement restricted so
  no new evidence can arrive. Confidence rises on zero observation.
- **Self-doubt** — "even though eventually all agents visit location 1, they cannot correctly eliminate
  that location… **The incoming beliefs of the other agents overrule their sensory observations.**"
  A first-hand observation loses to second-hand conclusions.

Fig. 7: likelihood sharing is **on par** with naive belief sharing on task success, and both beat
non-communicating agents — so the fix costs nothing on the metric it is not about.

### Why this is NOT the circular-inference finding we already landed

`mesh-precision --independence` (2026-07-28) computes ρ̄ and Kish n_eff — it discounts **correlated**
sources. That instrument **cannot see this failure**: the prior double-count is a property of the
message's **format**, not of the tapes' correlation. Two nodes with perfectly *uncorrelated*
observations and a *shared* prior still double-count that prior on every exchange; n_eff would read
≈2 and call it genuine corroboration. Complementary axes, not the same one.

---

## 3. The gap in the mesh, measured

**`scripts/mesh-fleet-states` is the mesh's only cross-node sense channel** — it walks each peer's
`~/.mesh/.*-state` artifacts over SSH and renders `name · value · age`. It is what a mind on one node
reads to know what another node's senses believe.

Every one of those artifacts is a **posterior**:

- an edge-triggered reflex commits its value under **debounce/hysteresis** — that is μ→B₂, the
  producer's prior, baked into the value;
- per the **liveness-touch convention** (CLAUDE.md), a reflex calls `mesh-state-touch` on *every*
  successful eval, so the artifact's **mtime is the last EVAL, not the last observation**.

So the two numbers the channel carries are `(sender's prior ⊕ sender's observation)` and `(sender's
last eval)`. **A receiver cannot recover the observation, nor when it happened.** There is no field
anywhere in the mesh that carries a state artifact's raw reading across a node boundary.

Measured on mesh-home, 2026-08-18 (`~/.mesh`):

| fact | number |
|---|---|
| state artifacts (`.x-state` + `.x.state`, minus `mind-state-*`) | **200** |
| of those, with a **non-empty same-named tape** (`<n>.log` / `<n>-tape.log`) | 119 (60%) |
| **posterior-only** — the mesh persists the conclusion and no raw record | **81 (40%)** |
| …on **phaedra**, over the live SSH channel | **53 / 113** |
| non-empty pairs where \|state mtime − tape mtime\| > 1h | 46 / 119 |
| artifacts the **default** walk sees (`.[a-z]*-state` glob only) | 120 / 200 |
| artifacts **invisible cross-node** (`.x.state` suffix family) | **80 (40%)** |

The last row is a second, independent finding: the default `REMOTE_SNIPPET` globs `-state` only, so
80 of this node's 200 state artifacts — `.psi.state`, `.situation.state`, `.perimeter.state`,
`.proximity.state`, `.room-sense.state` among them — have **never** been visible to a peer.

The 46/119 mtime gap is a **lead, not a verdict** (it mixes liveness-touch, change-gated tapes and
edge-only logs). It is quoted only to show that the channel's single `age` column answers a different
question depending on which producer wrote the file — exactly the ambiguity likelihood sharing removes.

The doctrine already has this shape as an incident: `.psi.state` read **CALM for 14.2 days** while the
node was stalled, because the committed value was a *sample* and every consumer read it as a *state*
(`fe35dd9`). That was single-node. Across the fleet it is strictly worse: the receiver cannot even see
the producer's cadence.

---

## 4. What landed — `scripts/mesh-fleet-states --likelihood` (report-only)

An opt-in mode that forwards the sense's **own tape** beside its committed value:

Real output, mesh-home, 2026-08-18T04:15Z:

```
  psi                    CALM             age 51s   tape 1d    [psi-calm] CALM — all resources calm   cpu=0
  situation              WATCH            age 1m    tape 3d    WATCH
  proximity              HERE 28:11:A5:B8:9E:A2 LE-Bose age 9m    tape 9m    proximity: HERE — LE-Bose Revolve SoundLink
  bt-exposure            CLOSED powered but refuses pai age 4m    tape post-only
```

Read the first line: **`psi` is 51 seconds old and its last raw record is a day old.** Under the old
render a peer saw `psi CALM age 51s` and had every reason to read it as "the peer observed calm a minute
ago". It is the same sense whose committed CALM was read as a state for 14.2 days — and the fleet
channel had no way to say so. `bt-exposure` is worse: `post-only`, no raw record anywhere.

- `value` = the peer's **committed posterior** (unchanged).
- `tape` = the age of the last **append** to the sense's own log, plus that line — the nearest thing to
  a likelihood message the mesh persists.
- `post-only` = **no raw record exists at all**: the mesh keeps this sense's conclusion and nothing
  else, so a receiver has no way to weigh it against an observation.
- a per-node tally: `-- 81/200 posterior-only (no raw tape behind the value)`.
- the mode walks **both** suffix families, so the 80 invisible artifacts appear. Widening is confined to
  the opt-in mode so `mesh-dash organs` keeps its exact contract.

**Honest naming, deliberately.** The field is `tape`, not `obs`: an edge-gated tape writes only on
change, so its mtime is the last *append*, not necessarily the last *observation*. Calling it `obs`
would be the overclaim this lane keeps finding in other tools.

**Scope discipline:** report-only. It changes no verdict, no weight, no fusion. Wiring a
likelihood-weighted fleet fusion (the paper's actual μ²↑A₃ = μ²,ᵒᵗʰᵉʳ↑A₂) is the steward's call and is
**not** in this change.

Live, right now:

```
mesh-home (local):   -- 81/200 posterior-only (no raw tape behind the value)
phaedra:             -- 53/113 posterior-only (no raw tape behind the value)
```

---

## 5. The bug the mode surfaced (fixed, with its own regression gate)

Building the excerpt field exposed a real defect in the **existing** channel:

**A byte-truncated multibyte tail does not just mangle its own field — it makes the NEXT record render
RAW.** `head -c 30` / `cut -c1-46` are byte-based; on this node they cut inside an em-dash, leaving
`\xe2\x80` (2 of 3 bytes) at the end of the `social-context` record — and the following
`ss-connections|…` line came out unrendered, pipe-delimited, i.e. **a peer state silently dropped out of
the table**. Measured: 200 records in → 200 lines out, one of them raw; with the partial tail stripped,
all 200 render. The default `head -c 30` path carries the same hazard.

Fix: `sanitize_utf8()` (`iconv -c -f UTF-8 -t UTF-8`, ASCII-strip fallback) applied once per node to
both the local and the SSH output — `set -o pipefail` keeps the ssh exit code, so `(ssh fail)` still
reports honestly.

---

## 6. Gate — RED-first, verified

`mesh-fleet-states --test` gains five cases driving the **real** `LIK_SNIPPET` and the **real**
`render_lik` against a sandbox `HOME` (the `--test` block was moved below the function definitions so
it can call them — a function defined below its caller is silently empty).

Mutants run from a scratch copy, each red for its **own** reason:

| mutation | gate |
|---|---|
| walk `-state` only (drop the `.state` glob) | `FAIL (likelihood walk missed the .state suffix family — beta invisible)` |
| `[ -f ]` instead of `[ -s ]` for the tape | `FAIL (a ZERO-BYTE log is not a tape — gamma must be post-only)` |
| never resolve a tape | `FAIL (a state WITH a non-empty tape reported post-only)` |
| remove `sanitize_utf8` from the pipeline | `FAIL (truncated multibyte tail dropped a record: 1/2 rendered)` |

All four rc=1; restoring each goes green. The zero-byte case is not hypothetical — 9 of this node's
same-named logs are 0 bytes (created at node setup, never written), and `-f` would have reported them
as likelihood evidence.

---

## 7. Why not discarded

Discardable only if the mesh already distinguished a peer's conclusion from a peer's observation. It
does not: `mesh-fleet-states` forwards the committed label and an mtime that the liveness-touch
convention has explicitly decoupled from the value; `mesh-precision --independence` discounts
correlation but is blind to the prior double-count; honest-fusion's gates catch EMPTY/STALE/FROZEN,
never **POSTERIOR-ONLY-BUT-FRESH**. The source is a live, currently-published branch of the field
(federated inference 2024 → the IWAI belief-sharing result → the 2025–2026 multi-agent follow-ups), the
mechanism is one equation, and the fix is cheap, opt-in and report-only.

---

## Sources

- Çatal, Van de Maele, Pitliya, Albarracin, Pattisapu & Verbelen, **"Belief sharing: a blessing or a
  curse"**, arXiv:**2407.02465** (IWAI 2024) — <https://arxiv.org/abs/2407.02465> (read in full, PDF)
- Friston, Parr, Heins, Constant, Friedman, Isomura, Fields, Verbelen, Ramstead, Clippinger & Frith,
  **"Federated inference and belief sharing"**, *Neurosci. Biobehav. Rev.* **156** (2024) —
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC11139662> (read: §3.1 belief sharing, §3.2 results)
- Albarracin et al., **"Shared Protentions in Multi-Agent Active Inference"**, *Entropy* **26**(4):303
  (2024) — <https://www.mdpi.com/1099-4300/26/4/303>
- **"As One and Many: Relating Individual and Emergent Group-Level Generative Models in Active
  Inference"**, *Entropy* **27**(2):143 (2025) — <https://www.mdpi.com/1099-4300/27/2/143>
- Pitliya, Çatal, Van de Maele, Pezzato & Verbelen, **"Theory of Mind Using Active Inference: A
  Framework for Multi-Agent Cooperation"**, arXiv:**2508.00401** / IWAI 2025 —
  <https://arxiv.org/pdf/2508.00401>
- Live arXiv sweep (`all:"active inference"`, newest-first, 2026-08-18): 2608.14466, 2608.14165,
  2608.09512, 2608.09330, 2608.02440, 2607.20306, 2607.19518, 2607.16981, 2607.16858 — screened,
  discard reasons in §1.
