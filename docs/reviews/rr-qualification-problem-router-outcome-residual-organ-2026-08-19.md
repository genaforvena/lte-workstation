# Relevance realization & the frame problem — LIVE literature review, 2026-08-19

## The QUALIFICATION problem: the other half of the frame problem. `mesh-organ` declares three constraints, calls the set complete, and cannot learn a fourth because it hands off and forgets.

**Area:** relevance realization & the frame problem (Vervaeke) · **Angle:** CROSS-DOMAIN transfer —
apply it concretely to a distributed sensor mesh · **Organ:** `scripts/mesh-organ` (the capability
router) · **Status:** built, uncommitted in the tree; steward lands.

## Where we had already been (so this does not double-count)

`docs/reviews/` carries 11 `rr-*` reviews. We have **opponent processing**
(`rr-opponent-processing-…`), **efficiency↔resiliency** (`rr-efficiency-resiliency-sensorium`),
**cognitive scope general↔special** (`rr-cognitive-scope-signature-normalizer-…`), **cognitive
tempering** (`rr-cognitive-tempering-arousal-coupled-novelty`), **the diametric autism/psychosis
model** (`rr-diametric-…`), **insight/reframe at impasse**, **ecological rationality**, **the prior
dilemma**, **declared-vs-enacted worlds**, and — decisively — the **RAMIFICATION** half of the frame
problem (`rr-frame-problem-ramification-change-anchored-supersession-doctor-2026-08-17.md`).

`grep -ric "qualification problem" docs/` returns **zero** across all 234 reviews. The frame problem
has two halves and we had landed exactly one of them.

## The concept, and where I read it

**McCarthy's QUALIFICATION problem** (McCarthy 1977; formalized by Ginsberg & Smith 1988): you
cannot axiomatize all the preconditions of an action. Ramification says you cannot enumerate an
action's *effects*; qualification says you cannot enumerate what must be true for it to *work*.

The RR reading of why this is not a bug to be engineered away —

- **Jaeger, J., Riedl, A., Djedovic, A., Vervaeke, J. & Walsh, D. — "Naturalizing relevance
  realization: why agency and cognition are fundamentally not computational."** *Frontiers in
  Psychology* 15:1362658, published 2024-06-25.
  https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2024.1362658/full
  Read: an algorithm "exists in a **small world** by definition, since it is embedded within a
  predefined formalized ontology"; **large-world** features are an indefinite collection that
  "cannot be prestated explicitly in the form of a mathematical set". Relevance realization is what
  "turns ill-defined problems into well-defined ones" — it *makes* the small world; it is not
  performed inside one. The paper offers **no implementable diagnostic** and says so; that is not a
  defect of my reading, it is its explicit position, and it is why the mechanism below is taken
  from the robotics literature rather than from this paper.

The operational answer — *don't enumerate harder, learn the precondition from outcomes* —

- **Sliwowski, D. & Lee, D. — "ConditionNET: Learning Preconditions and Effects for Execution
  Monitoring."** arXiv:2502.01167 (2025). https://arxiv.org/abs/2502.01167
  Learns a model of preconditions **and** effects and uses it as an execution monitor, instead of
  handcrafting the precondition list.
- **"Language-Augmented Symbolic Planner for Open-World Task Planning" (LASP).** arXiv:2407.09792,
  RSS 2024. https://arxiv.org/abs/2407.09792
  Its framing of the gap is the one that transfers: a planner operating with "only incomplete
  knowledge of action preconditions"; on execution failure it **diagnoses the cause from
  observation and incrementally builds up its knowledge**. Its worked example is a `pour` action
  missing a precondition about the target — the milk ends up on the table, and the *failure* is
  what reveals the precondition nobody wrote down.

## The cross-domain transfer, verified in the source

`scripts/mesh-organ` is the mesh's capability router: `mesh-organ camera` finds a node that has a
camera, runs it there, returns the artifact. **It is a small world by construction.** It declares
exactly three constraint types and its `--why` mode reconstructs all three:

```
constraint types declared by this router: where(cap-scope) who(cap-allow) reach(~/.mesh/nodes address)
```

That closed set is the qualification problem in one line. The router cannot represent the wedged
USB dongle, the missing `video` group, the driver returning empty, the daemon that died after boot
— every one of which is a live, named failure on this fleet. And its own tie-break tells you the
cost, in a comment it already prints to stderr:

```
NOTE: first-offered is the whole tie-break. The router does NOT retry the runners-up if the
      winner's ssh fails — the header's word 'failover' overstates it.
```

Among fungible offerers, **first-offered wins, forever, no matter how many times that offerer has
failed at exec.**

And here is the part that makes it structural rather than merely unimplemented: **it could not
learn otherwise even in principle, because it handed off and forgot.** Both terminal paths were

```
exec "$CAP_DIR/$name" "$@"          # local
exec "$HOME/.local/bin/$tool" "$@"  # local, legacy organ
ssh "${opts[@]}" "$user@$ip" ...    # remote, as the script's last command
```

`exec` **replaces the process**. No line of `mesh-organ` ran after the capability did. There was no
outcome tape, no rc, no duration — nothing. A router with no outcome memory has no discovered-
precondition lane available to it at any price.

## What was built — `scripts/mesh-organ`

**1. An outcome tape.** Every routed execution appends one line to `~/.mesh/organ-routes.log`:

```
<ts>  ROUTE cap=<name> node=<short> caller=<role> route=<local|remote> offerers=<n> \
      decisive=<constraint> rc=<int> secs=<int>
```

`decisive` is the same axis `--why` prints — which is what makes the residual a claim about the
*declared framework* ("every constraint said go, and it still failed") rather than a bare failure
rate. Writes are append-only and best-effort (`|| true`, `2>/dev/null`); a tape that cannot be
written is a silent no-op and **can never change a routing decision**.

**2. `mesh-organ --qualify [<cap>] [--json]`** — read-only, never executes a cap. Per capability:

- `n` routes, `failed`, and the **residual** — the share of framework-approved routes the world
  refused anyway. That number *is* the qualification problem's bite in this router.
- Where ≥2 offerers have run the cap: a **permutation test on the node label**, statistic
  `Σᵢ nᵢ·|pᵢ − p_pooled|`, null = the same failure multiset reshuffled across the same offerers.
  `UNSTATED-PRECONDITION-SUSPECTED` (p ≤ α) when the residual concentrates on one offerer the
  framework calls *interchangeable*; `NO-NODE-STRUCTURE` when it does not; `NO-RESIDUAL` when
  nothing failed.
- `na` **with its n** below the minimum (default 20/cap) and when only one offerer has ever run the
  cap ("there is no interchangeability claim to test").
- `rc=255` on a remote route is broken out separately: reach failed **at use**, which the
  address check structurally cannot see.
- Malformed rows are **counted and dropped**, never defaulted to `rc=0`.
- Closing line: `NOT A CAUSE. … A concentrated residual names WHERE to look for the precondition
  nobody wrote down; it never names it.`

**3. The one semantic change, stated rather than slipped in.** Recording an outcome requires
outliving the capability, so the local `exec` became run-then-record-then-exit. The child's exit
code propagates byte for byte and the streams pass straight through, but a bash parent now stays
resident for the capability's lifetime and a SIGTERM aimed at the *router* pid no longer lands on
the capability (`[[killing-a-wrapper-does-not-reap-a-sudo-child]]`). `MESH_ORGAN_NO_RECORD=1`
restores `exec` exactly and writes nothing.

## Verification

`./mesh-organ --test` → `smoke-test: ok` (full suite, pre-existing legs included).

Six new legs, **each seen RED under its own mutant** — run from a scratch copy, not the tree:

| mutant | leg that caught it |
|---|---|
| `weighted_tv()` → constant `0.0` | concentrated fixture read `NO-NODE-STRUCTURE` |
| p-value hardcoded `0.001` | flat fixture read `UNSTATED-PRECONDITION-SUSPECTED` |
| min-n gate removed | verdict rendered on 19 routes |
| malformed row defaulted to `rc=0` | row swallowed into `n=31`, `malformed=0` |
| `run_recorded` reverted to `exec` | tape empty after a real route |
| `MESH_ORGAN_NO_RECORD` ignored | escape hatch wrote 130 bytes |

The load-bearing leg is the **vacuity pair**: two fixtures carrying the *identical* multiset (30
routes, 12 failures) differing only in which offerer the failures pair with. A lens that reads the
failure *rate* passes both, so the pair is the only thing that can tell "found node structure"
apart from "counted failures".

Live reading on this node right now, and it is the honest one:

```
$ mesh-organ --qualify
mesh-organ qualify: n/a — no route tape at ~/.mesh/organ-routes.log. This router recorded nothing
until the outcome tape landed, so the series starts empty BY CONSTRUCTION and is not a quiet fleet.
(exit 2)
```

That is the correct artifact for a lens whose tape begins the moment its writer does — an `na` that
is a claim about the node, not a shrug.

## What this does NOT do

It does not change routing. First-offered is still the whole tie-break. Making the router *prefer*
an offerer that has actually delivered is the obvious next commit, and it is deliberately not this
one: re-ordering a live capability router on an empty tape would be exactly the unmeasured change
the doctrine forbids. The measurement lands first; the policy earns its way in when
`UNSTATED-PRECONDITION-SUSPECTED` fires on real routes.

## Sources

- [Naturalizing relevance realization: why agency and cognition are fundamentally not computational — Jaeger, Riedl, Djedovic, Vervaeke & Walsh, Front. Psychol. 15:1362658 (2024)](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2024.1362658/full)
- [ConditionNET: Learning Preconditions and Effects for Execution Monitoring — arXiv:2502.01167 (2025)](https://arxiv.org/abs/2502.01167)
- [Language-Augmented Symbolic Planner for Open-World Task Planning — arXiv:2407.09792 (RSS 2024)](https://arxiv.org/abs/2407.09792)
- [Predictive processing and relevance realization: exploring convergent solutions to the frame problem — Andersen, Miller & Vervaeke, Phenom. Cogn. Sci. (2025)](https://link.springer.com/article/10.1007/s11097-022-09850-6)
