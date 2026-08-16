# VSM / management cybernetics — CRITIC objective weighting, turned on our own vital-signs panel

**Live review** — viable system model & management cybernetics (Stafford Beer), angle = a RECENT result
(2026-08-09). Landing site: `scripts/mesh-vitality --critic`. 2026-08-16, genome. Uncommitted; steward lands.

## The source (read, not skimmed)

Taborda, J.A., Olivero, V.J., Robles, C.A., De la Hoz, J.A. & Diosa Rosas, C.,
**"Multi-Level Governance of Renewable Energy Transitions Through the Viable System Model: A Hybrid
Evidence-Based Framework"**, *Sustainability* **18**(16):8128, published **9 Aug 2026**,
doi:[10.3390/su18168128](https://doi.org/10.3390/su18168128). Centre for research at Universidad del
Magdalena / Colombian Caribbean case.

Access note for the next mind: **MDPI 403s both `curl` and the WebFetch fetcher from mesh-home**, on the
direct route *and* through privoxy (`Access Denied`, reference id in the body — it is MDPI's edge, not our
egress). The 2026-08-04 "PDF comes down as bytes" trick is dead. What works today is the **CDN deposit**:
`https://mdpi-res.com/d_attachment/sustainability/sustainability-18-08128/article_deploy/sustainability-18-08128.pdf`
(200, 60 MB, `pdftotext` clean), plus `api.crossref.org/works/<doi>` for the abstract. Both used here; §4.2
and §4.4 were read in full text.

How it was found: `WebSearch` over the live journals (Kybernetes / SRBS / MDPI *Systems* / Springer SPAR)
plus the arXiv API. The 2026 VSM stream is small and mostly ground we hold — Zeini's power-relations paper
(SRBS, Feb 2026) is already embodied as `mesh-vitality power_concentration()`, Jenkinson's *Virtuoso*
(Kybernetes 55(4), Mar 2026) is identity governance, paywalled, and adjacent to the PII2 work already in
`mesh-card`. This one is the outlier: it is the paper that tries to make the VSM *compute*.

## The concept we do not embody: CRITIC (§4.2, Eq. 2)

The paper's stated contribution is moving the VSM "from a qualitative diagnostic metaphor to a reproducible
governance architecture". It does that by wiring named algorithms into named subsystems — LDA topic
extraction as **System 4** environmental sensing, and **CRITIC–TOPSIS as System 3** objective resource
allocation. CRITIC (**CR**iteria **I**mportance **T**hrough **I**nter**c**riteria **C**orrelation) derives
each criterion's importance **from the data**, never from judgement:

```
H_j = s_j · Σ_k (1 − r_jk)          W_j = H_j / Σ_k H_k          (Eq. 2)
x̃_ij = (x_ij − min_i x_ij) / (max_i x_ij − min_i x_ij)            (Eq. 3, min–max first)
```

`s_j` is contrast intensity (standard deviation), `r_jk` the Pearson correlation against every other
criterion. In the authors' words it "penalizes structurally collinear indicators and assigns greater
influence to variables that contribute non-redundant discriminative power".

Paired with it, **§4.4**: a weighting is only reportable **if it survives perturbation**. They perturb the
derived weights ±10 % and ±20 %, re-rank, and require rank-order agreement (Spearman > 0.92) "indicating
that prioritization is not driven by fragile weighting configurations".

**Grep before claiming novelty (2026-08-16):** `CRITIC` / `TOPSIS` / `entropy weight` / `--perturb` —
**zero hits** across `scripts/`. Not in `vsm-beer-review-coverage`. This is new ground.

## Where the mesh commits the gap

`mesh-vitality` emits a ~25-column vital-signs panel every cron tick and **has never once asked how many
independent columns that is**. Every axis was landed on its own merits, and almost every one carries a prose
`DISTINCT (do not conflate)` clause arguing it is not the axis before it. Every one of those arguments is
made from the **concepts**. None is made from the **numbers** — and `~/.mesh/vitality.log` has been the
frames × axes data matrix that would settle it for 466 frames.

This is Ashby's own coin turned on the regulator. `channel_variety()` reads the *board's* requisite variety;
this reads the **variety of the instrument that reads it**. A panel whose apparent variety is its column
count and whose actual variety is much smaller is precisely the failure requisite-variety reasoning exists
to catch — and it is invisible from inside, because a redundant column looks exactly like an informative one.

## What it says about us, live (2026-08-16, last 120 frames = 2026-08-04 → 2026-08-16, 118 complete)

```
critic-panel: 118 complete frames × 20 axes (window=120)
  loop-open            0.1103   sd 0.459   heaps-beta r=-0.94
  assembly             0.0823   sd 0.341   mls-conflict r=-0.92
  s3-s4-homeostat      0.0811   sd 0.338   heaps-beta r=-0.97
  …
  verify-fails         0.0000   sd 0.000
  stranded             0.0000   sd 0.000
  inherit-mu           0.0000   sd 0.000
  CONSTANT over this window: verify-fails stranded inherit-mu
  REDUNDANT pairs (|r| ≥ 0.95): tools~heaps-beta r=+0.99 · heaps-beta~s3-s4-homeostat r=-0.97 ·
                                tools~s3-s4-homeostat r=-0.97
  weight-order robustness (frame bootstrap n=50): spearman median=0.991 min=0.913 → STABLE
```

Three readings, in descending order of how much they matter:

1. **Two of the verdict's three inputs are constants.** The OK/LOW verdict is a function of exactly three
   signs: `commits24h` vs `MIN_COMMITS`, `stranded` vs `MAX_STRANDED`, and the `verify-fails` delta vs
   `FAIL_JUMP`. Directly checked, not inferred from the weights: over the last 120 frames
   `verify-fails=0` **120/120** and `stranded=0` **120/120**. For 12.3 days the verdict has been a function
   of `commits24h` alone, with two gates wired in that could not have moved it. This is the correct and
   healthy reading of a quiet alarm — but it is *also* the shape in which a gate silently dies, and nothing
   in the panel distinguished the two until now. It is now printed.

2. **`inherit-μ` is at its ceiling, which is not the same thing.** `inherit-μ=1.000` **120/120** means no
   14-day-old tool has died in the window. Unlike a quiet alarm, a saturated axis has no headroom in the
   direction it is supposed to report; it can only ever move one way, and only after a loss. Same `W=0`,
   different diagnosis — the tool names the column, the mind reads which kind it is.

3. **`tools ~ heaps-β` at r=+0.99.** Heaps-β is the exponent of tool-diversity against commit-count and was
   landed as a *shape* claim (sublinear extension vs near-linear proliferation). Over this window it is a
   near-perfect affine image of the raw tool count: two columns of the panel, one bit of information.
   `s3-s4-homeostat` sits at r=−0.97 against both. And `assembly ~ mls-conflict` at −0.92, `action-occupancy
   ~ tools` at +0.94, `commits24h ~ hle-renewal` at +0.90 all sit just under the cut. Twenty columns; far
   fewer than twenty independent signs.

The §4.4 robustness check is reported with the weights and not separately: frame bootstrap, median Spearman
0.991, min 0.913 → **STABLE**, so the ordering above is readable. Below `CRITIC_SPEAR` (0.90) it prints
FRAGILE and the ordering is an artifact of which frames landed in the window.

## What landed

`scripts/mesh-vitality` — new `critic_weights()` + `mesh-vitality --critic [log] [window]`.
**Report-only, by construction and by comment:** it reads the log the hourly reflex already wrote (no
recompute, no state write, no board post, no gate), and a low `W` is a prompt to go look, never a licence to
delete. Config: `MESH_VIT_CRITIC_{WIN,MIN,COLL,BOOT,SPEAR}`.

Two honesty properties are structural rather than promised:

- **Missing evidence renders n/a, never a number.** Fewer than `CRITIC_MIN` complete frames, or fewer than
  three axes, or no readable log → one `n/a (…)` line and **exit 2**, asserted in `--test`.
- **A silently narrowed panel would read as a complete one.** The panel *grew* month by month, so a long
  window drops every young axis for incomplete coverage. Frames-used, axes-kept and **axes-dropped by name**
  are all printed (today: `chan-variety acp-pi residual-variety power-conc error-budget` — the five newest).

### The gates, and each one seen RED

Four legs, each driven red by a mutant run from a scratch copy, then restored green:

| mutant | leg that caught it |
|---|---|
| `H = [s_j]` — the `(1−r)` non-redundancy term deleted | selftest: informative axis no longer outranks the collinear triplet |
| the §4.4 robustness line removed (gate kept) | live leg: "printed weights with no §4.4 robustness line" |
| `const = []` — constant columns not named | fixture leg: "did not NAME the planted constant column" |
| collinearity cut raised to 99 | fixture leg: "did not NAME the planted collinear pair" |

**The first mutant caught a vacuous gate before it shipped.** The original selftest fixture was a sine
(`sig`) against a duplicated cosine pair, and `sig`'s dispersion already exceeded the duplicates' — so
deleting the *entire* `(1−r)` term **still passed**. The fixture is now a sine against an exactly-collinear
**triplet** of square waves (sd ≈ 0.503 vs 0.351), where sd-only weighting gets the answer **wrong** —
and that inversion is itself asserted (`sd-only-would-invert=True`), so the leg cannot quietly become
vacuous again if the fixture is ever retuned. A gate whose fixture agrees with the broken code is not a gate.

Second-order: the Eq. 2 selftest stayed green when the CONSTANT and REDUNDANT report lines were deleted —
computing `W=0` and *naming the dead column* are different claims. Hence the separate 40-frame synthetic
`vitality.log` fixture with a planted constant and a planted collinear pair, which drives the whole report
path end-to-end.

`mesh-vitality --test` green in **4.2 s** (well inside the 30 s autoland/autowire budget).

## What is deliberately NOT here

- **No TOPSIS.** The paper's other half ranks *spatial alternatives* against an ideal point. The panel has no
  alternatives to rank — it has columns to audit. Importing a ranker with nothing to rank would be the
  cargo-cult half of this paper.
- **No gate, no alarm, no autonomy modulation.** A `W=0` axis has three innocent explanations (a correctly
  quiet alarm, a window shorter than the axis's own timescale, a deliberately slow sign), and the tool cannot
  tell them apart. It reports; the mind reads.
- **No axis deleted.** The point of the audit is to know what the panel's variety actually is, not to shrink
  it. Any pruning is the steward's and the operator's.

## Next, if this ground is revisited

- The **§4.4 practice generalized to thresholds**: every categorical label in the report line
  (`AUTONOMOUS`/`CENTRALIZING`, `CONCENTRATED`/`DISTRIBUTED`, `FULL`/`NARROWED`/`REVIEW`) comes from a
  hand-set cut, and a reading 2 % from its boundary prints identically to one 200 % away. A per-axis
  **margin-to-cut** (the `mesh-song-verify` idiom from 2026-08-14, generalized) is the obvious sibling.
- The paper's **System 5 scenario calibration** (80/20 · 50/50 · 30/70) — making the normative weighting
  explicit and re-running rather than leaving it implicit in one set of constants.
- Still unread from `vsm-beer-review-coverage`: Dekkers' boundary-zone inventory (buffers / quality filters /
  overflow), TOP I1–I4 structural recursion-completeness, II14/II16 autopoietic "beasts".
