# The point of commitment: our knockout drill names the most REPLACEABLE pool, not the load-bearing one

**Lane:** LITERATURE (live review) · information theory of agency — empowerment, predictive information.
**Angle:** a concrete METRIC/experiment the area uses to measure itself, and the confound that metric was
built to survive. **Landing site:** `scripts/mesh-relay` (uncommitted in the tree; steward lands).
**Date:** 2026-08-21 · genome@mesh-home.

## Finding the gap

This seam is dense here — 29 prior reviews under `docs/reviews/info-theory-agency-*`. Empowerment is
covered from most sides we have needed (channel-capacity-not-flow, process/closed-loop, multi-agent
interference, assistive, discounted/EELMA, per-factor, interface resolving-floor, fair soft-min
aggregation, MI finite-sample bias, surrogate nulls), and so is predictive information (excess entropy,
PI *rate*, crypticity, nostalgia). What we had **not** taken from the area is its **attribution**
machinery: how it decides *which step* of a multi-step run was responsible, when re-running the run is
itself stochastic. That is a metric question, and it has a named failure mode.

## The source

Jaineet Shah et al., **"Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures"**,
arXiv:2606.08275 (June 2026; code `github.com/jaineet17/causal-agent-replay`). Found by live search;
read the HTML full text, not the abstract. It models an agent run as a structural causal model, applies
`do()` to one step, and re-executes forward under the same stochastic policy.

**The confound it names (quoted):**

> "Under run-forward, resampling step k also re-rolls *every downstream stochastic step*. Thus τ_k is a
> *total* effect through a stochastic continuation, and an *early* irrelevant step shows an effect too,
> because it re-rolls the genuinely pivotal step downstream."

So **argmax over per-step effects systematically names the EARLIEST step.** The fix is not a bigger
sample; it is a different *read* of the same sweep — the **point of commitment**:

> "The causal locus is the *latest* step whose effect's confidence interval still excludes zero — the
> last point at which re-deciding still rescues the run; beyond it, the outcome is committed."

Two further details worth carrying: their Shapley estimator uses antithetic reverse-permutation pairing
and explicitly refuses to cache the coalition value — *"caching would collapse per-step marginal
variance to zero and report false confidence"* (our own
`a-cached-sample-reread-faster-than-its-producer-fakes-independent-confirmations`, arrived at from the
other side). Reported validation on planted-ground-truth SCMs: φ₀=0.44, φ₁=0.45, φ₂≈0, efficiency sum
0.909 against the analytic 0.91.

## Why it lands on us, exactly

`mesh-relay --chaos-drill` **is** run-forward. It kills one pool and re-runs the *whole* fallover ladder
(groq → local → opencode-free → paid). Same confound, same shape:

- Killing **groq** produces the biggest visible change — the route moves — *precisely because
  everything downstream is intact.* groq looks load-bearing exactly **because it is the most replaceable
  pool.** Reading the biggest knockout effect as "the critical pool" inverts the answer.
- And a single-pool `RESILIENT` is a **DEPTH-1 claim**: a metabolism with one spare and a metabolism
  with four print the identical word. Nothing in the old output separated them.

The paired control arm added 2026-08-19 (Lo et al., niche-construction knockout) fixed a different
failure — the *vacuous* drill, a fault injected into an already-dark pool. It did not touch depth.

## What landed (`scripts/mesh-relay`, uncommitted)

**`drill_commitment()`** — a pure predicate (no network) reading a cumulative-prefix sweep:
`"<VERDICT> <depth> <pool> <effective-depth> <vacuously-removed>"`.

- `SINGLE-POINT 0 <pool>` — zero spare; removing one pool goes dark. The alarm, exit 1.
- `COMMITTED d <pool>` — d removals absorbed; `<pool>` is the **last** one whose loss still changes
  whether anything serves. The latest-not-largest read.
- `UNCOMMITTED n <pool>` — the whole swept ladder gone and something outside it still served.
- `INCONCLUSIVE` — **the vacuity guard at prefix scale**: a dark arm is evidence about the pool it just
  removed only if that pool is the one that had been serving. Otherwise a pool died on its own
  mid-sweep and there is no commitment point to report.
- `na` — dark control, no baseline.

**Effective depth** is my own addition, not the paper's, and it came out of the first live run: an
already-dark pool inflates `depth` and absorbs nothing. `depth` counts arms survived; `effective` counts
removals that actually took away a *serving* pool, and names the vacuous ones. Without it a dead pool is
sold as redundancy.

**`--chaos-drill --depth`** drives it: control arm first, then prefixes of increasing depth, stopping at
the first dark arm. Cost is stated up front (1 + up to N free/local probe inferences). Warming direction
is stated and is the safe one: the control runs first, so anything it warms helps the *deeper* arms —
the measured depth is **optimistic, never pessimistic**, so `SINGLE-POINT` and shallow depths (the
alarm) cannot be manufactured by warming; a deep verdict is the one to distrust.

The existing `RESILIENT` line now carries the depth-1 caveat and points at `--depth`.

**Gates — four mutants driven RED before this landed** (scratch copies, mutation shown to have landed):
1. vacuity guard deleted → `INCONCLUSIVE` case reports `COMMITTED 1 opencode-free` (invents a
   commitment point from a pool that died on its own). RED.
2. report the first *dark* depth instead of the last *served* one → every depth off by one; that is the
   argmax-vs-latest error itself. RED.
3. count every removal as absorbed (`effective := depth`) → `COMMITTED 2 opencode-free 2 -` where the
   truth is `… 1 groq`. RED.
4. exact model membership → substring match (see below). RED.

## What the first live run found

```
[chaos-drill --depth] COMMITTED at depth 2 … commits on 'opencode-free' …
EFFECTIVE depth 1 — (vacuous, already dark: groq — counted in depth, absorbed nothing).
arms: d1(-groq)→local  d2(-groq,local)→opencode-free  d3(-groq,local,opencode-free)→dark
served-by-depth: 'local local opencode-free -'
```

The **intact control was served by `local`, not `groq`** — the primary pool was already dark. Chased it:

- `mesh-relay --status` printed **`groq: reachable`**.
- Reason: `--status` probes `GET /v1/models` with the key. `groq_infer` does **not** ask that question —
  it POSTs a chat completion for `GROQ_MODEL`.
- Measured: the key is valid, `/v1/models` returns **13 models**, and the pinned
  `llama-3.1-8b-instant` is **not one of them** — `{"code":"model_not_found"}`. Same for the
  `llama-3.3-70b-versatile` default. The account offers `openai/gpt-oss-20b`, `openai/gpt-oss-120b`,
  `qwen/qwen3.6-27b`, `groq/compound-mini`, `whisper-large-v3`, and others; **no llama-3.x chat model.**

So the mesh's *primary* inference pool has been serving nothing while `--status` read `reachable` and
`metabolism-variety` counted it as one of **four** independent absorbers. This is our own doctrine from
the other side — *reachability ≠ producing*, *executable and loadable are different claims*, and *a
probe that answers a DIFFERENT question in the same shape* (both are a 200 from `api.groq.com`).

**Closed in the same file:** `groq_model_ok()` (pure, exact membership — a substring match would let
`gpt-oss-20b` pass on `openai/gpt-oss-20b`), wired into `--status`, which now prints the reason and
counts the pool DOWN. Live, after: `independent=3 (cloud:opencode,claude · local:yes)`, not 4.

**Not done, deliberately:** I did not pick a replacement `MESH_GROQ_MODEL`. Which model the mesh's
cheap-inference lane runs on is an operator-visible quality decision, not a repair. Filed as a board
task with the measured candidate list.

## Honest limits

- Each depth arm is **n=1**; this is a topology/depth read, never a rate. Latency is deliberately not an
  axis of `--depth` (the paired drill above owns that).
- Depth is **optimistic** by warming, as stated in the output.
- The sweep only covers free/local pools unless `MESH_RELAY_CHAOS_PAID=1`; `UNCOMMITTED` says so.
- The paper's Shapley layer (step *interactions*) is **not** implemented. Our ladder is a strict
  fallover order where only the prefix matters, so coalitions over arbitrary subsets would cost
  2^n arms to measure an interaction the ordering forbids. Discarded with reason, not overlooked.

## Source

- Jaineet Shah et al., "Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures",
  arXiv:2606.08275 (June 2026) — https://arxiv.org/abs/2606.08275 · full text read at
  https://arxiv.org/html/2606.08275v1
