# The constraint's own timescale — a sense that cannot witness its ceiling moving

**Live literature review, 2026-08-25, genome mind.**
Area: autopoiesis & the biology of cognition (Maturana & Varela), entered from the angle of a
concrete METRIC the area uses to measure itself.
**Arm:** treated (assigned)
**Target organ (assigned by coin, p=0.20, drawn uniformly from the 568 never-reviewed tools):**
`scripts/mesh-gpu-activity`. Not chosen by me and not chosen by the lane.

## The area does apply — and the assigned organ turned out to be a clean instance

The honest risk of an assigned target is that the area is a poor fit and the review becomes a
stretch. It did not happen here, and the reason is structural rather than lucky: this literature's
central operational move is the **constraint/process distinction**, and `mesh-gpu-activity` is
exactly a tool that measures a process and reads a constraint. It read the constraint and threw it
away.

## What was already ours (the negative half)

This lane has been in this area repeatedly and I checked before claiming novelty:

- `docs/reviews/autopoiesis-closure-of-constraints-organizational-2026-07-28.md` → landed
  `scripts/mesh-closure`, which computes organizational closure over the wired-reflex set. Its own
  header says it "measures a **STATIC** graph".
- `docs/reviews/autopoiesis-semantic-closure-interpreter-provenance-closure-semantic-2026-08-16.md`
  → Signature 1 of the paper below is already ours.
- `docs/reviews/autopoiesis-measurement-control-complementarity-link-heal-2026-08-18.md`
  → Signature 2 is already ours.
- CLAUDE.md already carries `a-senses-coverage-is-window-over-cadence` — a sense must publish the
  coverage of **its own sample window**. `docs/window-cadence-coverage-2026-08-15.md` even lists
  this exact tool (300s cadence, 2.0s window, 0.67% coverage).

So the mesh embodies closure as **topology**, and it embodies the timescale of the **process**. The
gap is the third thing.

## The find

**López-Díaz, A. J. & Gershenson, C., "A Matter of Time: Towards a General Theory of Agency",
arXiv:2606.23122v2** — submitted 22 Jun 2026, revised 30 Jul 2026. One month old; this is live
literature, not a fixed list.

Two load-bearing pieces, quoted:

- Abstract: *"the precarious physical realization of self-reference is necessarily diachronic;
  constitutive constraints **act, decay, and are regenerated over distinct characteristic
  timescales**."*
- §8 "Operational Signatures of Biological Agency", **Signature 7 — Organizational Closure and
  Falsifiability**: tests whether constitutive constraints act, decay and are regenerated over
  distinct characteristic timescales; *"operationally falsifiable by demonstrating constraint decay
  without regeneration causes system disintegration."*
- §4 "Temporally Parametrized (F,A)-systems": *"Each process-type g is assigned a characteristic lag
  τ_g. This indexing specifies when an output can become available relative to the inputs and
  constraints that enable it; it is not a global synchronous update rule."*

Grounded in the classic it operationalizes — **Montévil, M. & Mossio, M., "Biological organisation
as closure of constraints", J. Theor. Biol. 372:179–191 (2015)**, where a constraint is defined **at
a given time scale**: it breaks the symmetry between a process A→B and that same process under the
influence of C (AC→BC) *at a specific time scale*. The constraint/process cut is not structural, it
is **temporal** — a constraint is whatever is conserved over the timescale of the process it acts on.

**The concept we do not embody: a sense must publish the characteristic timescale of the CONSTRAINT
it is normalized against, and be able to witness that constraint moving.** Our doctrine covers the
process window (coverage = window ÷ cadence) and the reading's freshness. Nothing anywhere covers
the denominator's own lifetime. A normalizing constant is treated as timeless everywhere in the
mesh — and that is precisely what Signature 7 says is false of every constitutive constraint.

## The instance in the assigned organ

`scripts/mesh-gpu-activity` computes `busy% = (1 − Δrc6/Δwall)·100` — a **process** reading: what
fraction of wall time the GPU was out of RC6 deep sleep. The GPU's frequency ceiling
(`gt_max_freq_mhz`) is the **constraint** that makes two such readings comparable.

The tool read that constraint into `$maxf`, printed it on the terminal line and in `--json`, and
then **dropped it from both durable artifacts**:

- state row was `LEVEL busy% actMHz` — no ceiling. This is the artifact `mesh-stress`
  (`read_gpu_state`) and `mesh-operator-focus` actually consume.
- log row was `ts busy level cur act` — no ceiling. So the corpus that any recalibration would read
  **could not answer whether the ceiling moved under a sample**, which is the only question that
  separates a workload change from a constraint change.

And the constraint genuinely moves: `gt_max_freq_mhz` is an **RW** sysfs attribute — a power daemon,
a tuning script or a hand can write it — unlike `gt_RP0_freq_mhz`, the silicon's fixed ceiling. So
100% busy under a 1150 MHz ceiling and 100% busy after the ceiling drops to 350 MHz are **3.3×
different work rendering as the same reading**, with the BUSY/LIGHT/IDLE label unmoved. A
constitutive constraint that decays with no sense able to witness the decay: Signature 7's failure
case, in one file.

## What was landed (uncommitted, steward lands)

`scripts/mesh-gpu-activity` — a **constraint tier** beside the process reading:

- `~/.mesh/.gpu-activity-ceiling` journals `<max_mhz>\t<epoch first seen at this value>`, rewritten
  **only on change**, so the epoch is genuinely "first seen at this value", not "last time we
  looked". That epoch difference **is τ**, the ceiling's characteristic timescale.
- Every run publishes `ceil=`, `held=` (τ) and `moved=` into the **state row** and the **log**, plus
  `rp0_mhz` and `headroom = max/RP0` (the decay axis — a software ceiling well under the hardware one
  is a constraint already partly decayed) in `--json`. New `--ceiling` subcommand exposes the tier
  alone.
- **A reading whose ceiling moved says so** and is marked not comparable to its predecessor, instead
  of looking like a workload change.
- **Three honest-n/a shapes kept apart.** No history yet → `held=0 moved=no`; unchanged → `held=τ
  moved=no`; unreadable ceiling → `ceil=na headroom=null` and **never** a guessed denominator. The
  first is the one that matters: rendering "we have no history" as "it just moved" would fabricate an
  event, and rendering it as "it has held forever" is the opposite lie.
- Fields are **appended**, field 1 untouched — both live consumers key on the leading token only, so
  the tier reaches them with no format sweep. `mesh-stress --test` and `mesh-operator-focus --test`
  re-run green.

**Gate, seen red.** Six fixture arms, all **node-free** (freq dir and ceiling journal are
env-overridable) so they run on a node with no i915 — which is the node that authored them. Driven
red by four independent mutations:

| mutation | goes red on |
|---|---|
| state row drops the ceiling again (the original defect) | state-row + na arms |
| first sighting reported as a move | fabricated-event arm |
| unreadable ceiling gets a guessed denominator | honest-n/a arm + `--ceiling` rc |
| classification made to follow the ceiling | process-invariance arm |

The fixture pins the process reading at exactly **100.0%** (rc6 delta of zero → 100.0 for any dt, no
timing assumption), so the invariance arm has teeth and lands on the header's motivating example: the
ceiling moves 1150→350 while the process reading is byte-identical.

**One thing this review fixed that it did not set out to fix.** The arms sit *before* the real-read
gate, and that gate exits 2 "n/a — no i915" unconditionally. On this node the entire constraint tier
could have been red and `--test` would still have reported node-absence — rc=2 laundering a logic
failure into "no hardware", on every node without an iGPU. The gate now refuses to claim n/a while
`fail` is set: **rc=2 is a claim about the NODE and is only honest when nothing else has already
failed** (`a-red-gate-hides-every-gate-after-it`, `na-must-be-a-claim-about-the-node`).

## Not discarded — and the limit of the receipt

The organ is `UNREACHABLE` on mesh-home (NVIDIA only; `rc6_residency_ms` absent), so **no live
hardware reading exercised this tier** — the receipt is fixture-driven end-to-end through the real
main path, plus mutation. The one claim resting on documentation rather than on a measurement here is
that `gt_max_freq_mhz` moves at runtime on a live i915; it is stated as the RW/RO distinction against
`gt_RP0_freq_mhz` and should be confirmed on the IdeaPad before anything downstream *acts* on
`moved=yes`. Nothing does yet — the tier publishes, it does not actuate.

## Sources

- [López-Díaz & Gershenson, *A Matter of Time: Towards a General Theory of Agency*, arXiv:2606.23122](https://arxiv.org/abs/2606.23122)
- [Montévil & Mossio, *Biological organisation as closure of constraints*, J. Theor. Biol. 372:179–191 (2015)](https://www.sciencedirect.com/science/article/abs/pii/S0022519315001009)
- [Brown & Vittadello, *Studying self-organisation across the biosphere with process-enablement graphs*, arXiv:2411.17012](https://arxiv.org/abs/2411.17012) — read as a candidate; its cycles-in-graphs formalism is the *topological* reading we already hold in `mesh-closure`, so it is the negative half of this review, not the find.
- [Closure of Constraints as a Theoretical Model, *Philosophy of Science* (Cambridge Core)](https://www.cambridge.org/core/product/66F5B26F146D1DF12CB1B3019B50734A/core-reader)
