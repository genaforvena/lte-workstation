# FEP / active inference — LIVE literature review, 2026-08-22 (second pass)

## The SELF-PRIOR: a learned density over FAMILIAR MULTISENSORY experience is enough to find a mark on your own face with no reward and no extra sense. Every self-check this mesh owns is per-axis, so the mesh is structurally blind to the mark: a configuration where every axis is normal and the COMBINATION has never happened.

**Lane:** free energy principle & active inference (Friston), angle = **a recent result (2023–2026)**
**Window:** genome · **Landed:** `scripts/mesh-sensorium --self-prior` (+ a `# reflex-cadence:`
header scoping the schedule to that mode), **uncommitted in the tree, not deployed.**

---

## 1. How the live surface was swept

Live, this session:

1. **arXiv API newest-first, 30 each** over `all:"free energy principle"`, `all:"active inference"`,
   `all:"expected free energy"` (fetched 2026-08-22; `https://export.arxiv.org/api/query` — the
   `http://` form returns a 0-byte body from this vantage).
2. **Each candidate checked against the corpus by arXiv ID**, not from memory — this lane's real
   failure mode is re-landing something already held. That check is what killed the first four
   picks:

| id | why discarded |
|---|---|
| `2607.20306` state-dependent observation noise | **already ours** — landed 2026-08-14 as `mesh-precision --reachable` (`fep-h3-reachable-…-2026-08-14`), cited in 3 reviews |
| `2606.23325` the adaptive nature of confirmation bias | already read and discarded 08-18: no binary-hypothesis evidence-*selection* site in the mesh |
| `2607.16858` model-free epistemic free-energy estimators | 3 corpus citations |
| `2606.23122` a general theory of agency | 5 corpus citations |
| `2607.20708` perspective latents / causal emergence | uncovered, and a sharp claim (scalar Φ_r is largely *architectural* and *decreases* with training). Discarded because its transferable form — read per-atom sign-invariance across regimes, not the aggregate — is what `fep-stable-blanket-invariance-across-environments-correlate-2026-08-22` landed on `mesh-correlate --stable` **this same day**. Worth a later pass on `mesh-leadlag`; not a second landing of the same mechanism today. |

## 2. The source

**Dongmin Kim, Hoshinori Kanazawa & Yasuo Kuniyoshi, "Active Inference with a Self-Prior in the
Mirror-Mark Task", arXiv:2604.09673, submitted 2 Apr 2026** (code:
`github.com/kim135797531/self-prior-mirror`). Not in the corpus at any ID.

Their claim, in their words:

> "this behavior emerges spontaneously through a single mechanism, **the self-prior**, without any
> external reward. The self-prior … **learns the density of familiar multisensory experiences**; when
> a novel mark appears, **the discrepancy from this learned distribution** drives mark-directed
> behavior through active inference."

> "A simulated infant, **relying solely on vision and proprioception without tactile input**,
> discovered a sticker placed on its own face in the mirror and removed it in approximately 70% of
> cases without any explicit instruction. Expected free energy decreased significantly after sticker
> removal, confirming that the self-prior operates as **an internal criterion for distinguishing self
> from non-self** … functioning as a **probabilistic body schema**."

**The mechanism we did not embody.** Not "novelty" — the corpus is full of that
(`predictive-processing-bayesian-surprise-vs-shannon`, `mesh-novelty --bayesian`, `--conditional`,
`--levels`). It is that the criterion is a **joint density over modalities**, so the signal exists
*only* in the combination. No modality is out of range in the mirror-mark task: the face is a normal
face, the proprioception is normal proprioception. The sticker is visible **only as a discrepancy
from the joint**, and the agent has no tactile channel that could report it directly.

## 3. Where it bites, in our own genome

Every self-check the mesh owns is **per-axis against that axis's own declared contract**:

- `mesh-health` / `mesh-hw-health` / `mesh-reflex-health` / `mesh-doctor` — each asks "is this organ
  inside ITS range / did it produce ITS artifact".
- `mesh-card --refresh` `invariant-check` — per-invariant.
- `mesh-novelty` — **marginal** surprisal, and over **one** modality (board event types).
- `mesh-sensorium --amplification` / `--damage-response` — pairwise, but over the substrate *coupling
  graph*, i.e. topology; they never look at the joint distribution of the **readings**.

So the mesh holds no density over what its own body normally *feels like across senses together*, and
a configuration in which every axis is individually familiar while the combination has never occurred
is invisible to all of it — by construction, not by oversight. That is the mark.

## 4. What landed

**`scripts/mesh-sensorium --self-prior`** — the smallest honest form of a self-prior over the state
this node already publishes about itself. `mesh-sensorium --cached` is the mirror: 17–19 discrete
words per snapshot (`room=PRESENT`, `tempo=RESTING`, `operator-home=HOME`, `media=TV-LIKELY`,
`perimeter=CALM`, …). The mode reads that roll, keeps a ledger of joint configurations at
`~/.mesh/self-prior.log`, and names the pair that is **familiar in each member and never seen
together**.

Live on this node, first invocation:

```
coverage: 0 ledger row(s) over 0 distinct hour(s) / 0h span · 17 axis/axes read · 2 dropped
          (motion[sentinel:body-covered] hw[aging])
observation: ambient=QUIET audio-path=IDLE context=ENGAGED-QUIET home-state=ACTIVE
             interruptibility=AVAILABLE light=LIT media=TV-LIKELY mode=ACTIVE operator-home=HOME
             perimeter=CALM power=OK prox=NEAR room=PRESENT situation=WATCH tempo=RESTING
             watchtower=REACH-OK wifi-motion=STILL
verdict: INSUFFICIENT — 0 distinct hour(s) of body history, floor is 30. No mark is named.
```

**Four places this could have lied, and what stops each:**

1. **Support is counted in DISTINCT HOURS, not rows.** The roll is sampled far faster than the state
   changes, so consecutive rows are near-copies. Counting rows would let pure **dwell** manufacture
   "familiar" and would mint a fresh "never co-occurred" pair at every transition. Hour buckets
   deflate that autocorrelation: a token is familiar if seen in ≥6 distinct hours; a pair has
   co-occurred if seen together in ≥1 distinct hour.
2. **Only `(fresh)`/`(recent)` axes are evidence.** An `(aging)`/`(STALE)` field — or a value carrying
   a *fallback provenance* where a freshness word should be — is dropped and **named** in coverage. A
   self-prior that eats stale axes learns a body it no longer has.
3. **A bracketed value is a blindness SENTINEL, not a body state.** Live here: `motion=[body-covered]`.
   Learning it as a configuration is `[[a-blindness-sentinel-fused-as-a-reading]]`. Dropped, named.
   Same for the null alphabet (`UNKNOWN`/`OFFLINE`/`?`/…) already used by `--viability`.
4. **Below the floor it refuses.** Under 30 distinct hours of history it prints `INSUFFICIENT` and
   names **no** mark — because below the floor every unseen combination is unseen for the boring
   reason. Coverage (rows / distinct hours / span / axes kept / axes dropped) prints with **every**
   verdict, including the refusals.

**A capability nobody samples does not exist**, so the mode carries `# reflex-cadence: 8,28,48 * * * *`
with `# reflex-args: --self-prior` — **only** that mode is scheduled, and it reads the cached roll, so
it raises no live probe and no phone SSH. 3/h across the clock reaches the 30-hour floor in ~1.5 days.
Offsets 8/28/48 are clear of this node's heavily-squatted `*/5`, `*/10` and `:17/:23/:41` phases.

## 5. The gate (driven RED three ways, then green)

Five cases in `mesh-sensorium --test`, none passable alone:

| case | asserts |
|---|---|
| planted mark | `room=PRESENT × tempo=SPRINTING`, each in 20h, together in 0h → named, exit 3 |
| **control** | same fixture, pair co-occurring in 4h → **no mark**. A tool reporting "unseen" for anything it did not just see passes case 1 and fails here |
| young ledger | 5 hours → `INSUFFICIENT`, and no mark named |
| rare members | both tokens present but each in only 2h → **not** a mark; else every transient is one |
| sentinel/aging | `motion=[body-covered]` + `situation=WATCH (aging)` → both dropped and named in coverage, neither in the observation |

Mutants, each run against the real `--test`:

```
MUTANT A (support floor deleted)  → FAIL: marked a pair whose members are individually RARE
MUTANT B (young-ledger refusal deleted) → FAIL: named a mark on a 5-hour ledger
MUTANT C (sentinel drop deleted) → FAIL: read a blindness sentinel as a body state
RESTORED → ok: --self-prior names the planted mark, stays silent on a co-occurring pair,
                refuses a young ledger, holds the rare-member floor, drops sentinel/aging axes
smoke-test: ok
```

## 6. What is NOT verified, plainly

- **No mark has been found on this node, because there is no history yet.** The ledger was created by
  the first live run and holds one row. Every claim above about *behaviour on real data* is
  unmeasured; what is measured is the fixture behaviour and the live parse (17 axes read, 2 correctly
  dropped). Read the first real verdicts after ~1.5 days of cadence before believing anything about
  the mark **rate** — including whether the hour-bucket floor is aggressive enough. If the node
  emits marks constantly, the floors are the knobs (`MESH_SELF_PRIOR_FLOOR`, `MESH_SELF_PRIOR_NMIN`),
  and a constant mark rate means the pairing is measuring the mesh's regime churn, not its body.
- **The cadence is not live.** `mesh-autowire` scans `$HOME/.local/bin`, not the genome, so the header
  wires only after the steward lands this and `mesh-sync-tools` deploys it. `mesh-autowire --check`
  prints nothing for `mesh-sensorium` right now, correctly.
- **Pairs only, not higher-order joints.** The paper's self-prior is a full density (a Transformer
  over the multisensory stream). This is the second-order slice of it. A mark that lives only in a
  triple is not found. Named as a limit, not sold as the whole mechanism.
- **This is not an alarm channel.** The mode prints and exits; nothing posts to the board. That is
  deliberate until the mark rate on real data is known — an unmeasured detector wired to the board is
  how a lane manufactures noise.

## 7. Files

- `scripts/mesh-sensorium` — `--self-prior` mode, 5 `--test` cases, `# reflex-cadence:`/`# reflex-args:`
  header, usage line (modified)
- ledger (runtime): `~/.mesh/self-prior.log`
