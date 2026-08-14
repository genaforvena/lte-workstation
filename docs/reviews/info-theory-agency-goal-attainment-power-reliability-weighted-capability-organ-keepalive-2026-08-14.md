# Information theory of agency — breadth counted is not power

**Live review, 2026-08-14 · genome@mesh-home · landed report-only in `scripts/mesh-organ-keepalive`**
**Status: uncommitted in the tree (steward lands).**

## The source (live literature, found this session)

**Jobst Heitzig & Ram Potham, "A Fair Objective for Human-Empowerment-Preserving AI: Desiderata,
Design, and Likely Behavioral Consequences", arXiv:2608.08240 — submitted 8 Aug 2026** (six days ago;
later than every prior landing on this seam). Found by web search for current empowerment work, read at
<https://arxiv.org/html/2608.08240>.

Verbatim from the abstract: the paper designs *"a parametrizable and decomposable objective function for
AI systems that represents an inequality- and risk-averse long-term aggregate of human power"*, and
*"prove[s] how certain desiderata enforce particular functional forms and restrict parameter ranges"*.

Two of those forced forms matter here. Both are **axiomatically derived**, not chosen:

- **Individual power (desiderata I1–I7)**, where `C_h^g ∈ [0,1]` is the discounted probability that
  party `h` **attains** goal `g`:

  ```
  I_h(s) = log2  Σ_g  C_h^g(s)^ζ ,       ζ > 1
  ```

  The axiom that forces `ζ > 1` is **I5, "Reliability Preference"** — a **dual** Pigou–Dalton condition:
  *transferring capability from a less attainable goal to a more attainable one INCREASES power.* Note
  the direction. At the population level the paper's **P6** is the ordinary Pigou–Dalton (transfer from
  the more to the less powerful increases the aggregate). **The two levels of the same objective carry
  opposite curvature** — convex within a party, concave across parties — and each is forced by its own
  axiom.

- **Population power (P0–P8)**, forced to an inequality-averse soft-minimum:

  ```
  P(s) = -log2  Σ_h  2^{-ξ I_h(s)} ,     ξ > 0
  ```

  with **P4 "Disempowerment Focus"**: adding an already-omnipotent party must not change the aggregate.

## Where we had already been on this seam (checked, not assumed)

`memory/info-theory-agency-coverage.md` + `docs/reviews/info-theory-agency-*` (14 files): open-loop and
process empowerment, finite-sample MI bias + shuffled null, multi-agent interference channel, discounted
empowerment (EELMA) on the board, plasticity as the observation→action dual, PID synergy, and the
foundational correction that **empowerment is a channel capacity, not the achieved flow**.

Every one of those scores an information **flow or capacity of a single scalar channel**. **None scores a
party's power over a GOAL SET**, and nothing anywhere in the mesh weights a declared capability by
whether it is actually attained. That is the gap.

## The gap, concretely — `scripts/mesh-organ-keepalive`

Set `ζ = 1` and `C ≡ 1` in `I_h = log2 Σ_g C^ζ` and it degenerates to `log2(number of goals)` — **a pure
breadth count**. That is exactly how this mesh reports capability today:

```
$ mesh-organs --json
{"node":"mesh-home", … ,"live":11,"total":11}
{"node":"phaedra",   … ,"live":7,"total":7}
```

`mesh-organ --list`, the card's `senses:`/`actuators:` lines and the `health` dash's
`organs 11LIVE/0DARK` are all the same count. The axiom says a count is not power: half-attaining ten
goals is **weaker** than reliably attaining five, and no count can see the difference.

`mesh-organ-keepalive` is the only place `C_h^g` is estimable — its `probe()` is literally a Bernoulli
trial on *"can this node attain capability g right now?"*, run every 600s by `mesh-liveness-loop`. **It
was never recorded.** The reflex logged only EDGES (`DARK` / `REMEDIED` / `UP-edge`), so the attainment
**rate** that `C` is has never existed on any node.

### What the measurement immediately exposed (live, this node)

`probe()`'s catch-all is `*) return 0` — "unknown organ class: don't false-alarm". It is honest as an
alarm policy and fatal as evidence: **6 of mesh-home's 11 declared organs have no probe at all** and
their `LIVE` is a constant. First run of the new ledger, verbatim:

```
2026-08-14T23:40:29Z mesh-home irq            ok catchall reflex
2026-08-14T23:40:29Z mesh-home docker-compute ok catchall reflex
2026-08-14T23:40:29Z mesh-home volume         ok catchall reflex
2026-08-14T23:40:29Z mesh-home tv             ok catchall reflex
2026-08-14T23:40:29Z mesh-home dlna-tv        ok catchall reflex
2026-08-14T23:40:29Z mesh-home shadowsocks    ok catchall reflex
```

Their `C` is **not 1.0 — it is unknown**, so `--power` excludes them rather than reading a fabricated
pass as full attainment (missing evidence renders `na`, never 0 **and never 1**). Same shape as the
silent-fallback doctrine (`|| echo 500`), one level up: here the fallback is a *return code*.

## What landed (report-only, `scripts/mesh-organ-keepalive`)

1. **The producer.** A per-probe attainment ledger `~/.mesh/organ-attain.log`, one Bernoulli trial per
   organ per reflex run: `<ts> <node> <organ> <ok|dark> <real|catchall> <mode>`. Separate file from
   `$LOG` on purpose — `$LOG` is the edge/liveness log a watchdog reads, and a `--test` must never write
   the artifact it checks (09f7914). `MESH_ORGAN_ATTAIN_LOG` redirects it for the test.
   `PROBE_KIND` is set **once** at the top of `probe()` and flipped **only** in the catch-all — not a
   second case list, which would drift from the first
   (`two-renderings-of-a-value-must-be-canonicalized`).
   Recorded on the **reflex** path only: `--status` is called ad hoc by `mesh-organs` from any node, and
   an irregularly-sampled rate is not the cron-cadence rate `--power` claims to estimate.

2. **The reader.** `mesh-organ-keepalive --power` (read-only; writes nothing, not even its own input):

```
  declared (breadth the fleet map counts) : 11  → I_count = log2(11) = 3.459 bits
  measured (real probe, n>=5)             : 5
  I_power = log2(Σ C^2 over measured)      = 2.322 bits
  gap = 1.138 bits = 1.138 (unprobed/thin: 6 organ(s)) + 0.000 (flaky: measured C<1)
  verdict: RELIABILITY_INFLATED — the capability count overstates attainment power by
  1.138 bits; dominant cause: UNPROBED breadth.
POWER node=mesh-home declared=11 measured=5 I_count=3.459 I_power=2.322 gap=1.138 verdict=RELIABILITY_INFLATED
```

   The gap is decomposed exactly — `log2(declared) − log2(measured)` (breadth never probed) plus
   `log2(measured) − log2(Σ Ĉ^ζ)` (measured flakiness) — so the verdict **names which cause it came
   from** rather than max-folding two different failures into one word
   (`a-sub-axis-is-not-the-verdict`, `max-fold-effaces-the-disjunction`).
   Verdicts: `POWER_NA` (no evidence — the breadth read stands *unbacked*, which is not a power of 0) ·
   `RELIABILITY_INFLATED` · `POWER_OK`. Knobs: `MESH_ORGAN_POWER_{ZETA,DAYS,MIN_N,GAP_BITS}`.

3. **What Ĉ is and is not.** The probe is instantaneous, the cadence is 600s, so Ĉ is the probability the
   organ is attainable **at a probe instant** — the quantity a router actually needs ("can I reach it if
   I ask now?"), and **not** a duty cycle. An outage shorter than the cadence is invisible to it. Stated
   in the file so no consumer mistakes the narrow claim for the wide one
   (`a-senses-coverage-is-window-over-cadence`).

### Gates (6 mutants, all verified RED from a scratch copy)

| mutant | result |
|---|---|
| M1 catch-all no longer marks itself (`PROBE_KIND` unset) | RED |
| M2 `--power` counts catch-all rows as attainment | RED (`measured=3`, `I_power=1.170`) |
| M3 `--power` appends to the ledger it reads | RED |
| M4 empty ledger renders a power of `0` instead of `na` | RED |
| M5 `MESH_ORGAN_ATTAIN_LOG` override ignored (test would forge the real ledger) | RED |
| M6 `ζ` dropped to 1 (linear, breadth-like) | RED (`I_power=0.585`) |

Honesty note on M5: it goes red via the *override* symptom (the child reads the real ledger → `measured=0`)
rather than via the "real ledger grew" assert, because the test's own `attain_record` write still lands in
the scratch file. Same defect, different message — flagged rather than claimed clean
(`a-mutant-can-go-red-for-the-wrong-reason`).

The load-bearing gate is M2: a fixture where `gamma` has **six `ok` rows but no real probe** must read
`measured=2`, never 3 — a fabricated pass may not raise power.

## Deferred, with the reason

The **population-level** aggregate `P(s) = -log2 Σ_h 2^{-ξ I_h}` (P4 + P6 — a fleet number a strong node
cannot flatter) is **not** built. It needs per-node `I_h` fanned in across peers, which belongs in
`mesh-organs`' existing SSH loop, not in a node-local reflex; and it only bites with ≥2 parties carrying
ledgers (today: 2 nodes online, 0 ledgers until this deploys). `--power` emits a machine-readable
`POWER …` line precisely so that fold is a one-liner later. Naming the axiom without measuring it would
be the `declaring-an-organ-before-arming-it` shape.

Not claimed: that mesh-home's capability concentration is *itself* measured here (it is not — that is the
deferred P). Not claimed: any number from this ledger yet — `n=5` per organ from five hand-runs is a
demonstration of the path, not a rate.

## One live consequence, stated plainly

Until this deploys to `~/.local/bin/`, the ledger does not accumulate — the cron/liveness-loop copy is the
old one. The finding that needs no code at all, and holds right now: **`organs 11LIVE/0DARK` on the health
dash is 5 measurements and 6 constants**, and nothing before today could tell them apart.
