# Relevance realization & the frame problem — the RAMIFICATION horn, operationalized: change-anchored supersession

**Lane:** LITERATURE (live review), genome window · **Date:** 2026-08-17 · **Landed in:** `scripts/mesh-doctor` (`--supersede`)

## Where we had already been

Seven `rr-*` reviews are in `docs/reviews/`: opponent processing, cognitive scope, efficiency/resiliency,
insight-at-impasse, ecological rationality, cognitive tempering, the diametric model, and (2026-08-15)
routines-vs-orientation-worlds. That last one already imports a **2026** Vervaeke paper (Chiappe &
Vervaeke, *Phenom. & Cog. Sci.*, doi:10.1007/s11097-026-10177-9) and already built
`mesh-reflex-health --routine-fit`. The canonical RR corpus is small and the mesh has eaten most of it:
Andersen, Miller & Vervaeke's PP↔RR convergence paper (*Phenom. & Cog. Sci.* 24:359–380, 2025) is the
diametric review; opponent processing is the 2012 Vervaeke/Lillicrap/Richards paper.

So this review deliberately did **not** land on RR-the-philosophy. It landed on the horn of the frame
problem that RR *names and declines to operationalize*, and on the live engineering literature that has
a partial mechanism for it.

## The concept we did not embody

**Implicit stale dependency, and the reverse-direction (change-anchored) pass that finds it.**

> Haofei Sun & Lin He, **"When Memory Updates but Behavior Does Not: Repairing Implicit Stale
> Dependencies in Personalized Agent Responses"**, arXiv:2608.01619v1, **3 Aug 2026**.
> Read in full at <https://arxiv.org/html/2608.01619>.

Their definition is the whole transfer:

> a draft `d` **depends** on attribute `a` if changing the current value of `a` would alter the
> response's substance, **"whether or not `d` mentions `a`"**.

That is a *counterfactual* definition of relevance — exactly the relation Jaeger, Riedl, Djedovic,
Vervaeke & Walsh ("Naturalizing relevance realization: why agency and cognition are fundamentally not
computational", *Front. Psychol.* 2024, doi:10.3389/fpsyg.2024.1362658, found via search, abstract +
secondary reading) argue cannot be pre-enumerated at all. Sun & He do not try to enumerate it. Their
move is to **invert the scan direction**, so the dependency never has to be declared:

- **Forward / product-anchored** (what everybody does): walk the product's own *stated* premises, check
  each against memory. Recall of stale premises **0.44–1.0** where the dependency is stated —
  **0.06–0.38** where it is merely implied. And the bottleneck is *extraction*, not judgement: few-shot
  prompting made implicit recall **worse** (0.38 → 0.13).
- **Reverse / change-anchored** (their "Temporal Role"): for each **changed attribute**, ask whether
  each product's substance still aligns with the *current* value. Isolated by a matched control that
  kept the evidence, the adapter and the budget and removed only the transition machinery, this is
  where their gain lives: implicit-policy adaptation **53:6**, the control adding a non-significant
  +0.6 (macro accuracy 0.736 vs 0.686 baseline, 95% CI [+2.9, +7.2]).
- Two guards they pay for: **provenance-verified transitions** (old→new both quoted from evidence,
  `t_new > t_old`) with **fail-open** when unverified — unverified repair costs them an 80%
  false-invalidation rate against 3% — and a **third state**, `unknown-current`, for a slot whose
  dependency moved but which has no settled replacement.

Related live reading, not landed: STALE (arXiv:2605.06527, May 2026) benchmarks whether agents notice
their memories expired; López-Díaz & Gershenson, "A Matter of Time: Towards a General Theory of Agency"
(arXiv:2606.23122, Jun 2026) — an agency-signature framework already adjacent to our
autopoiesis/semantic-closure reviews.

## Why it is not already embodied here

Every freshness instrument the mesh owns runs the **forward** direction and is **artifact-anchored**:

| instrument | question it asks |
|---|---|
| `eff_maxage` / `mesh-reflex-health` | is this artifact's **mtime** late against its cadence-derived lease? |
| `mesh-reflex-health --routine-fit` | does the **declared** cadence match the **enacted** cron? |
| `mesh-sync-tools` | does the **repo** copy match the **deployed** copy? |
| `mesh-doctor --sediment` | does this **knob** have any reader at all? |

All four ask "is this thing itself late / absent / unread". **None asks the reverse question**, and a
state file is the purest case of an unstated dependency in the mesh: **it records a verdict and never
records the threshold that produced it.** Such a file is fresh by mtime, on-cadence, honest in content,
and computed under a configuration that no longer holds — indistinguishable from a correct one at every
surface we have.

Measured before writing a line of code: **23 of 90** `~/.mesh/*.state` artifacts predate the last edit
of `~/.mesh/nodes` (13:29Z that day), and `grep` for `-nt`/`-ot` across `scripts/` finds the idiom only
in the audio pipeline — **no tool in the genome compares a derived artifact's mtime to its config's**.

## What shipped — `mesh-doctor --supersede` (report-only, on-demand, rc 3 on a finding)

1. **Snapshot + transition ledger (the provenance half).** Each run digests every `~/.mesh/nodes`
   assignment as `sha256(node-local-salt ‖ value)`, truncated to 12 chars, and diffs it against the
   previous snapshot. Three verbs, all real transitions: `changed`, `set` (a reader stops taking its
   default), `unset` (it resumes it). Appended to `~/.mesh/config-transitions.log` (0600, as are the
   snapshot and the salt). The digest proves a knob **is not what it was** and can never disclose what
   it is — `~/.mesh/nodes` is the node's secret-adjacent surface, the same reason `--sediment` refuses
   to print values. Here it is also never **stored**.
2. **The reverse pass.** For each state artifact declared in the genome (via `umwelt_slug`, deduped to
   one row per artifact, ownership preferring the declarer whose own name is the artifact's stem — a
   dash that merely *names* `.climate-state` is a consumer, not its writer), collect the knobs its
   producer actually **reads** (literal name, outside an assignment, comments and the `--test` block
   stripped by `um_body`), take the latest transition over those knobs, and compare to the artifact's
   mtime.
3. **Four verdicts.** `SUPERSEDED` (artifact predates a change to a knob its producer reads) ·
   `UNKNOWN-CURRENT` (older than the ledger's own coverage — a knob may have moved unwatched) ·
   `CURRENT` · `INDEPENDENT` (reads no knob this node sets).
4. **The refusal to certify.** Coverage opens **once**, stamped as the ledger's first line, and nothing
   written before it can be certified. On a node that has never run this, that is *everything*, and the
   first run says `BASELINE RUN` instead of issuing a clean bill it has no basis for. The stamp is
   pinned in the ledger precisely so coverage does not slide with the clock — an unpinned fallback makes
   `CURRENT` unreachable, and a check that can only ever answer "I cannot tell" is not a check.

**What makes the verdict sound is the liveness-touch convention.** A change-gated reflex rewrites its
state only when the value changes, so content alone could never say whether it re-evaluated;
`mesh-state-touch` on every successful eval decouples ran-live from value-changed, and that touch is
exactly the evidence this pass needs — mtime *after* a transition means the reflex evaluated under the
new knob and (perhaps) found the same answer. Where a producer does **not** touch, mtime-before-transition
is genuinely ambiguous, which is why `SUPERSEDED` is written as a **LEAD, not a verdict**.

## Artifacts

Live on mesh-home, repo copy (deployed copy untouched — steward lands and syncs):

```
$ mesh-doctor --supersede
BASELINE RUN — no prior snapshot. 39 knobs recorded; no transition can be claimed yet.
ledger: ~/.mesh/config-transitions.log — 0 transition(s), coverage begins 2026-08-17T21:39:29Z (+0 this run)
producers declaring a state artifact: 217 · distinct artifacts: 193 · present here: 155
verdicts: CURRENT 0 · SUPERSEDED 0 · UNKNOWN-CURRENT 36 · INDEPENDENT 119 (reads no knob this node sets)
UNKNOWN-CURRENT 36 — written before the ledger opened; a knob may have moved unwatched, so they are NOT certified CURRENT.
```

Driven over the **real** corpus against a *copy* of the real `~/.mesh/nodes` with the knob values
edited (live config untouched), the reverse pass fires:

```
verdicts: CURRENT 0 · SUPERSEDED 2 · UNKNOWN-CURRENT 34 · INDEPENDENT 119
SUPERSEDED — the artifact predates a change to a knob its producer reads (a LEAD, not a verdict:
a producer that does not mesh-state-touch may have run and declined to rewrite):
  mesh-room                  .room-contact.state        written 2026-07-23T10:13Z · ROOM_NODE changed 2026-08-17T21:39Z
  mesh-voice-count           .voice-count.state         written 2026-08-17T21:35Z · ROOM_NODE changed 2026-08-17T21:39Z
```

**Gate:** 11 legs inside `mesh-doctor --test`, every one driving the real script as a child process
against a fixture config + fixture producers + fixture artifact dir. **11 mutants, all seen RED**, each
for its own reason:

| mutant | leg that caught it |
|---|---|
| reverse pass removed (deps always empty) | a real supersession must exit 3 |
| raw source instead of `um_body` | a comment/`--test` mention counted as a dependency |
| pre-ledger artifacts certified CURRENT | must read UNKNOWN-CURRENT, not CURRENT |
| accuse on the baseline run | the first run must declare itself a baseline |
| sticky accusation (ignore artifact mtime) | a re-written artifact must clear |
| value printed instead of the knob name | (row assertion) |
| raw value stored in the snapshot | a config value was written to the snapshot/ledger |
| coverage stamp not written | the ledger must carry exactly one COVERAGE-OPEN |
| coverage stamp written but ignored | coverage slid between two runs |
| ownership preference removed | the consumer owned the row → rc 0 |
| dedup removed | one artifact judged twice → CURRENT census wrong |

## Boundaries (stated in the code, repeated here)

1. **Report-only, on-demand, no repair.** Reconciling means re-running someone else's reflex, which
   belongs to that reflex — the same boundary `--routine-fit` and `--sediment` keep.
2. **The dependency edge is SYNTACTIC.** It understates exactly where `--sediment` does (a knob whose
   name is *built* at runtime is invisible to a literal-name scan) and overstates where a knob is read
   on a branch never taken.
3. **It compares a CONFIG to an ARTIFACT, not a config to behaviour.** A producer that rewrites every
   tick clears itself on its next run, so a *standing* `SUPERSEDED` line is a statement about the
   change-gated family specifically.
4. **Coverage is a real limit, not a formality.** Until the ledger accumulates, the honest answer for
   most artifacts is `UNKNOWN-CURRENT`, and the report says so rather than reporting green.

## Not a duplicate of

`--sediment` (knob→reader **reachability**, no time axis) · `--routine-fit` (declared vs enacted
*cadence*, not artifacts) · `mesh-reflex-health` staleness (mtime vs a cadence lease — the forward,
age-based question) · `mesh-sync-tools` (repo vs deployed, a different supersession axis, also forward)
· `mesh-doctor`'s umwelt check (does a producer's artifact have a *reader* — the dead-vehicle question).
