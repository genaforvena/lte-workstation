# Live-literature review — autopoiesis: a constraint is only a constraint at a TIMESCALE

Date: 2026-08-04 · lane: genome (idea-queue LITERATURE task) · status: implemented + gated, uncommitted

## Area & angle

Autopoiesis & the biology of cognition (Maturana & Varela), entered as a **cross-domain transfer to
a distributed sensor mesh**. Searched the live literature (arXiv 2026, ALIFE 2026 tutorial track,
BioSystems' 50-years-of-autopoiesis special issue, AI&SOCIETY, Frontiers) and landed on the one axis
our existing closure instrument silently dropped.

## The concept (named, cited)

**Conservation of a constraint at the timescale of the process it constrains.**

Montévil & Mossio's *closure of constraints* (J. Theor. Biol. 372:179-191, 2015) — the operational
form of autopoiesis, and the paper `scripts/mesh-closure` already cites — defines a **constraint** as
an entity that (a) acts on a process **while (b) being CONSERVED at that process's timescale**. Our
implementation took (a) and dropped (b): an enablement edge was a *binary* fact — A is mentioned by
B, therefore A constrains B — with no clock on either end.

The live literature makes exactly that omission its subject:

> **López-Díaz & Gershenson, "A Matter of Time: Towards a General Theory of Agency", arXiv:2606.23122**
> (v1 2026-06-22, v2 2026-07-30) — https://arxiv.org/abs/2606.23122

Their thesis: *"the precarious physical realization of self-reference is necessarily diachronic"* —
constitutive constraints **act, decay and regenerate on different characteristic timescales**, and a
closure claim is only falsifiable once it is made **scale-explicit**. They name the process-enablement
graph as the *first* operational strategy for closure (the same object `mesh-closure` builds) and then
argue it is incomplete without its temporal parametrisation. That is precisely the delta.

Also read and **not** taken (recorded so the next review does not re-tread them):

- ALIFE 2026 tutorial *Autopoiesis & Structural Coupling* (https://autopoiesistutorial.netlify.app/) —
  argues the fundamental phenomenon is structural coupling, not autopoiesis. Already embodied:
  `docs/reviews/enactivism-4e-participatory-coupling-metric-2026-07-27.md`, the biosemiotics
  functional-cycle review, the reafference loop-closure review.
- Gahrn-Andersen, *Human languaging and large language models*, AI&SOCIETY 41(2) (2026),
  doi:10.1007/s00146-025-02599-x — LLMs cannot *language* because they are allopoietic. Its
  operative claim (our cognition is allopoietic) is already landed as `mesh-vitality`
  `allopoiesis_gap()` / `heteronomy_index()`.
- *Toward aitiopoietic cognition*, Front. Cognition 5:1618381 (2025) — a four-track research
  programme, no measurable.
- *Enactive Drift Regulation*, arXiv:2607.03834 (2026) — coherence/regime language, but the paper
  defines no coherence measure, no transition threshold. Nothing to implement.
- **Discarded after checking the artifact:** von Neumann's constructor/copier split (A + B + Φ) as
  surfaced by arXiv:2604.13934 (2026) predicts *sterile replicas* — nodes carrying the phenotype
  (`~/.local/bin/mesh-*`) without the tape (the repo), unable to found a third node. Checked both
  live peers: phaedra has `/root/lte-workstation/.git` + 622 tools + a `genome-mirror.git`; ilya has
  `/home/ilya/lte-workstation/.git` + 473 tools. **No sterile replica exists** — the concept does not
  apply here. (One line, as briefed.)

## Cross-domain transfer to the mesh

Every wired reflex declares its own characteristic time — its cron cadence. So each enablement edge
A→B already carries two: **τ_A** (how often A regenerates its product) and **τ_B** (how often B
consumes it). The conservation criterion is then readable directly off `~/.mesh/reflexes.cron`:

| class | criterion | reading |
|---|---|---|
| **CONSTRAINT** | τ_A ≥ τ_B | A's product is conserved across B's cycle. A genuinely constrains B. *Slower is not a fault — it is the definition; a constraint is supposed to be the slow term.* |
| **ALIASED** | τ_A < τ_B by ≥2× | A regenerates faster than B ever looks. At B's timescale A is not a constraint but another fluctuating **process**, and B discards most of what A pays a cron slot to produce. |
| **MARGINAL** | τ_A < τ_B, under 2× | noise; reported, not flagged. |
| **UNTIMED** | a cadence is unreadable at either end | honest n/a — counted as **neither**. |

And the loop criterion falls straight out: a mutual pair a↔b is a closed **constraint** loop only if
**both** legs are conserved (τ_a ≥ τ_b **and** τ_b ≥ τ_a), i.e. only when **τ_a == τ_b**. MATCHED
loops are timescale-valid closure; SKEWED loops are closure claimed at two different clocks. That is
the number the flat graph could not produce.

**Distinct from what we already embody.** `a-lease-must-exceed-its-producers-cadence` and the
liveness-touch convention are per-artifact **freshness** rules (one consumer, one TTL, is the value
stale?). This is an **edge property of the closure graph** and an aggregate over it. An ALIASED edge
is never stale — the consumer always reads a fresh value; the waste is on the **producer's** side, and
no freshness rule can see it. It is also the exact inverse of `PERIPHERAL`: not *"nobody consumes
you"* but *"your one consumer looks at 1 in N of what you make."*

## Concrete application (ONE file)

**`scripts/mesh-closure`** — new `--timescale` (and `--cadences`) modes, report-only, on-demand,
never prunes, never edits cron. A cron-period parser (mean inter-fire interval over a week,
`10080 / fires-per-week`) handles every spec shape the real `reflexes.cron` uses: `*/n`, `a-b/n`,
explicit lists, dom/dow/month restrictions, `@`-forms.

### Live run 2026-08-04 (223 wired reflexes, the real genome)

```
assessable edges=734   UNTIMED=100 (honest n/a)
CONSTRAINT=470   ALIASED=230   MARGINAL=34
LOOPS: MATCHED=16   SKEWED=58   UNTIMED=15
```

**The finding: of the 89 mutual-dependence loops that `mesh-closure` reports as the atoms of the
mesh's organizational closure, only 16 — 18% — survive the conservation criterion.** 58 are closure
claimed at two different clocks. And **31% of assessable enablement edges (230/734) are ALIASED**: a
producer burning a cron slot every 1–5 minutes for a consumer that reads it hourly or daily.

Worst offenders, and what they mean:

```
- mesh-chat-deliver (1m)  -> mesh-chat (526003.2m)     1 in 526003
- mesh-roz-channel  (1m)  -> mesh-chat (526003.2m)     1 in 526003
- mesh-sync-tools   (20m) -> mesh-pkg-watch (10080m)   1 in 504
- mesh-chat-sync    (3m)  -> mesh-log-attest (1440m)   1 in 480
- mesh-awaydigest   (5m)  -> mesh-home-digest (1440m)  1 in 288
```

**The `mesh-chat` rows are a real defect the tool found on its first live run, not an artifact of it.**
`mesh-chat`'s only cadence as a *scheduled* reflex comes from a **one-shot reminder cron left wired
past its own expiry** — `30 6 25 7 * mesh-chat "[task] … zai-glm-burn-revert …"`, i.e. 06:30 on 25
July, whose own trailing comment reads *"one-shot 2026-07-25 (remove after firing)"*. It fired 10 days
ago and is still in `~/.mesh/reflexes.cron` **and** in the live crontab (verified). The arithmetic is
correct — that line schedules `mesh-chat` **once a year** — which is exactly why it surfaced at the
top. Reported, not fixed: removing a live crontab line is cron-hygiene owned by whoever staked that
one-shot, not this review.

### Gate

`mesh-closure --test` (unchanged entry point, extended fixture). Two fixture graphs:

- a **cadence-parser** cron pinning every spec shape, including the documented bursty case
  (`*/5 * * * 1` → **35m weekly mean**, not 5m — the honesty bound is asserted, not just written);
- an **edge/loop** graph with a deliberate MATCHED loop *and* a deliberate SKEWED loop, so neither
  loop counter is green-by-vacuity.

**RED-first verified — 6 mutants, each seen fail then restored:**

| mutant | result |
|---|---|
| `tau[a] >= tau[b]` → `1` (everything conserved) | RED (6 asserts) |
| loop `tau[a]==tau[b]` → always MATCHED | RED |
| cron `a-b/n` step ignored | RED (5 asserts) |
| `MESH_CLOSURE_ALIAS_MIN` knob hardcoded | RED |
| dow leg ignored (bursty weekly-mean lost) | RED |
| `fires <= 0` guard removed | RED |

A **seventh** leg was *removed* rather than kept: a `$1 ~ /^@/ { next }` rule for `@reboot` lines
could not be made to fail — deleting it changed no output, because the arithmetic already drops those
lines via `fires <= 0`. A gate leg that cannot fail asserts nothing; the guard that actually does the
work now carries the assertion (`mesh-fp7`).

Two doctrine traps avoided in the render: no `head` in the aliasing pipeline (`set -o pipefail` +
early-exiting `head` SIGPIPEs `sort` and returns **141** while printing a correct report — verified,
then fixed), and the top-N truncation **announces its remainder** (`… and 218 more aliased edge(s)`)
rather than reading as "that's all of them".

## Not discarded — why it applies

It is operational (arithmetic over two files we already keep), it is a **different axis** from every
existing check — wired (`mesh-doctor`) / firing (`mesh-reflex-health`) / depended-upon
(`mesh-closure`) / **conserved at the consumer's timescale** (this) — it is genuinely un-embodied, the
mechanism is live (2015 JTB → 2024 arXiv → **2026 arXiv, revised six days ago**), and it produced a
precise, non-vacuous artifact plus one real cron defect on its first live run.

Landing point we have not been: **the mesh's claimed organizational closure read with a clock on it —
82% of its constraint loops turn out to be closure at two different timescales.**
