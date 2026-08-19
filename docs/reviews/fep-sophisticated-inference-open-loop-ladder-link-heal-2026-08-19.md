# FEP / active inference — LIVE literature review, 2026-08-19

## Sophisticated inference: the plan must stay CONTINGENT on the state. `mesh-link-heal`'s ladder is a line over ticks, not a tree over shapes.

**Area:** free energy principle & active inference (Friston) · **Angle:** an OPERATIONAL mechanism
(not philosophy) we could implement · **Organ:** `scripts/mesh-link-heal` · **Status:** review only —
the finding is structural and verified; the lens it proposes was NOT built in this session (a second
idea-queue task pre-empted the build; see "What is not done" below).

## The source (live, read today off the arXiv feed)

- **Nuijten, W. W. L. & de Vries, B. — "Sophisticated Policies from Epistemic Priors."**
  arXiv:2607.19518, submitted 2026-07-21. https://arxiv.org/abs/2607.19518
  Read: the paper represents Sophisticated Inference inside an epistemic-prior variational
  framework. Its operational core, in its own terms: maintain **a joint posterior over future
  states and actions**, keeping "future actions dependent on future states" inside the variational
  posterior, which yields *state-contingent control* over the planning horizon. Its stated contrast
  with standard EFE planning: standard EFE planning **factorizes actions from future states**, so
  lookahead actions cannot adapt to what will have been observed — an open-loop action sequence.
  Its empirical claim: **neither ingredient suffices alone** — epistemic drive without closed-loop
  structure seeks information without reaching the goal; closed-loop structure without epistemic
  incentive fails to explore.
- Antecedent (the mechanism's origin, for the definition):
  **Friston, Da Costa, Hafner, Hesp, Parr — "Sophisticated Inference."** *Neural Computation*
  33(3):713–763 (2021); arXiv:2006.04120. https://arxiv.org/abs/2006.04120
  Sophistication = the degree to which an agent has *beliefs about beliefs*; the recursive free-energy
  functional implements a deep tree search **over sequences of belief states**, not over states, so
  future actions are evaluated *conditionally at each branch*.

## Where we had already been (so this does not double-count)

`docs/reviews/` carries 13 `fep-*` and 13 `predictive-processing-*` reviews. Checked against all of
them: we have EFE's **epistemic value** (`fep-active-inference-epistemic-value-…`), its **ambiguity**
term (`fep-expected-free-energy-ambiguity-price-…`), **prior preferences / dark room**, **Bayesian
model reduction and expansion**, **precision allocation** (interoceptive, channel-conditioned,
reachable non-constancy), **solenoidal flow**, **likelihood-vs-posterior sharing**. Every one of them
is about the *objective* or the *precision* — none is about the **factorization of the posterior over
policies**, which is what sophisticated inference changes. `grep -ril "sophisticated inference|
state-contingent|closed-loop plan"` over `docs/reviews/` returns no file that uses the term in this
sense. New ground.

## The gap, verified in the source (not asserted)

`scripts/mesh-link-heal` is the mesh's most-escalating healer — it tends this node's **sole uplink**.
Its planner is one function:

```
choose_rung() {
  local n="$1" last="$2" secs="${3:-0}" settle_left="${4:-0}"
  ...
  if   [ "$n" -ge "$SHOUT_AFTER" ];   then printf shout
  elif [ "$n" -ge "$REPLUG_AFTER" ] ...; then printf replug
  elif [ "$n" -ge "$RELOAD_AFTER" ] ...; then printf reload
  elif [ "$n" -ge "$BOUNCE_AFTER" ] ...; then printf bounce
  elif [ "$n" -ge "$REASSOC_AFTER" ] ...; then printf reassociate
  else printf none
}
```

**The outage SHAPE is not an argument.** The rung is a function of elapsed ticks/seconds and the
previous rung — a plan indexed by *time*. That is precisely the factorization the paper names: the
action sequence is chosen independently of the state the agent will be in.

And the tool **already has the state**. It measures the shape on every check and names three of them
in its own header:

```
#   DEAUTHED   not associated to the AP
#   WEDGED     associated, has a default route, and the gateway answers nothing
#   ROUTELESS  associated, and the node has no default route at all (L2 up, L3 gone)
```

It carries `EPISODE_SHAPE` across checks in `~/.mesh/.link-heal.state` (field 8), collapses a
changing shape to `mixed`, prints `shape=` on every `RECOVERED` line, prints `state=` on every
`ACTION` line, and `--cost-drift` even reports a **SHAPE stratum** row count. The belief state is
computed, persisted, logged, and published — and then thrown away at the one moment it would change
what the healer does.

The tool's own header already argues the case against itself:

> "A modprobe cycle rebinds the driver but never re-enumerates the device, so **if the wedge lives in
> the USB endpoint rather than in the driver state, reloading is theatre.**"

The header knows the cure is shape-dependent. The planner does not read the shape. On a `WEDGED`
episode the open-loop ladder spends `REPLUG_AFTER - 1` ticks (default 9, ≈9 minutes of a dark sole
uplink) on `reassociate`/`bounce`/`reload` — three rungs that act on the supplicant and the driver —
before it reaches the one rung that addresses a USB endpoint. In active-inference terms that is the
**ambiguity price of factorizing q(s,π) into q(s)q(π)**, paid in minutes of outage.

## What the tape can and cannot say today (measured, 2026-08-19)

`~/.mesh/link-heal.log`, 100 lines, 82 `RECOVERED` + 18 `ACTION`. Shape × curing-rung, by `awk`:

```
57  (no shape field)  none          <- pre-shape format
12  (no shape field)  reassociate
 9  DEAUTHED          none
 1  DEAUTHED          reload
 1  WEDGED            none
 1  ROUTELESS         none
 1  (no shape field)  reload
```

Only **12 rows carry `shape=` at all** (the field lands forward from the commit that added it), and
the two shapes that would *decide* the question have **n=1 each**. So the honest reading today is
`na` — and `na` here is a claim about the node, not a shrug: *the contingency table exists, has the
right columns, and has no evidence in it yet.* Any ladder re-ordering proposed on this data would be
a story about two episodes. The structural finding stands on the source (`choose_rung`'s signature),
not on the tape; the tape is what would license *changing behaviour*, and it does not yet.

## The concrete proposal — ONE mode, on ONE named file

**`scripts/mesh-link-heal`, new read-only mode `--contingent [--json]`.** Report-only: it never
touches the ladder. It replays the tape into the shape-conditioned cure table that a closed-loop
policy needs and reports whether the open-loop factorization is costing anything:

1. **Per shape**: episodes, which rung preceded each recovery, and which rungs fired *without*
   curing that shape (from the `ACTION … state=<shape>` lines).
2. **The open-loop price**: per shape, the ticks and seconds spent on rungs that have never cured
   that shape — the ambiguity term made into seconds of dark uplink.
3. **A verdict with a null**: permutation test on the shape label (shuffle shapes, statistic =
   Σ_s n_s·TV(p_s, p_pooled)) → `CONTINGENT-WARRANTED` / `CONTINGENT-NOT-WARRANTED` / `na`, reusing
   the seed/permutation/α machinery `--cost-drift` already carries.
4. **Coverage in the reading**: `shape_rows/total`, per-shape n, and the minimum-n gate, so a
   consumer can never mistake a two-episode table for a policy.

Only once (3) reads `CONTINGENT-WARRANTED` on real episodes does a second commit earn the right to
pass the shape into `choose_rung()` — a branch, not a line. That ordering is the point: the paper's
mechanism arrives as a **measurement first**, because a healer on the sole uplink is not a place to
land an unmeasured re-ordering.

## What is not done

The mode is **not implemented** — this document is the review, and the build was pre-empted by the
next idea-queue task. Everything above that is stated as fact was read out of the source or measured
off the live tape in this session; nothing here claims an artifact that does not exist.

## Sources

- [Sophisticated Policies from Epistemic Priors — Nuijten & de Vries, arXiv:2607.19518 (2026-07-21)](https://arxiv.org/abs/2607.19518)
- [Sophisticated Inference — Friston et al., Neural Computation 33(3) / arXiv:2006.04120](https://arxiv.org/abs/2006.04120)
- [Active Inference: A Process Theory (background on EFE policy selection)](https://activeinference.github.io/papers/process_theory.pdf)
