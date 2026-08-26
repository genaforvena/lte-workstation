# Pask's Prune: two topics derived the same way are one topic

**Lane:** LITERATURE (live review) · second-order cybernetics · 2026-08-26 · genome@mesh-home
**Subject organ:** `scripts/mesh-health-state`
**Status:** implemented + gated, uncommitted in the tree (steward lands)

---

## The source

Francis Heylighen, *"Bootstrapping knowledge representations: from entailment meshes via semantic
nets to learning webs"*, **Kybernetes 30 (5/6), 2001**, pp. 6–8 —
<https://pespmc1.vub.ac.be/Papers/Pask-Bootstrapping.pdf> (fetched and read in full, 1535 lines of
extracted text). It is the clearest surviving operational write-up of Gordon Pask's **entailment
meshes** and their implementation **THOUGHTSTICKER**, because Pask's own papers state the algebra and
skip the procedure.

Cross-checked against the live secondary literature: the Wikipedia *Conversation theory* /
*Interactions of actors theory* entries, `cybernetics.coexplorer.org/pask.html`, and Mancilla's
*Paskian Algebra* (philarchive.org/archive/MANPAA-8) — all of which recite the *structure* (topics,
coherences) and none of which state the **Prune procedure** this review is about.

## The mechanism, and why it is operational rather than philosophical

An entailment mesh is a set of **topics** grouped into **coherences**; a coherence is a cluster in
which *"the meaning of any topic of the coherence can be derived from the meaning of the relation
among the other topics"*. Every topic must belong to at least one coherence and be *"unambiguously
derivable from the other topics in the mesh"*.

**Prune** is the operation that checks this, and its job is stated in one sentence (p. 6, verbatim):

> "The main function of the Prune operation is to discover structural ambiguities or conflicts in a
> mesh. **An ambiguity arises when different topics are derived in the same way. In that case, there
> is no way to distinguish the topics within the mesh.**"

Pask gives four mechanical repairs, and exactly four (p. 7): **merge topics** (they were the same
thing under two names) · **add topic** (extend one coherence so the derivations differ) · **split
topic** (bifurcate a shared premise into two, keeping them linked by *analogy*) · **merge
coherences**. A fifth, separate illegality: **nested coherences** (one coherence a subset of
another) have no determinate derivation at all and must be **condensed** into a generalised topic.

This is a check on the **representation**, not on the measurement, and that is the whole value: it
runs *before* any incident, and it is indifferent to whether each individual probe is correct.
Write down, for every verdict a tool can emit, the premise set it is derived from. Any two distinct
verdicts sharing a premise set are structurally ambiguous — the tool cannot separate them however
well it measures.

## Why this is not something we already embody

The mesh has 309 reviews, thirteen of them `second-order-cyb-*` (including
`second-order-cyb-pask-teachback-agreement-vs-understanding`, which takes Pask's *conversational*
criterion, not his *representational* one) and seventeen `vsm-*`. None takes Prune.

More to the point, we keep finding this class **one incident at a time, after the fact**. From the
memory index alone: `a-collapsed-reason-makes-blind-and-quiet-identical` ·
`a-fixed-verdict-standing-in-for-four-different-failures` ·
`a-queue-deduped-by-question-text-collapses-two-employers-obligations` ·
`a-redaction-placeholder-used-as-a-key-is-a-self-erasing-collision` ·
`a-byte-exact-dedupe-cannot-express-the-same-performance` ·
`a-short-sense-name-is-shared-by-two-different-organs`; and in CLAUDE.md, *"a fallback keyed on the
FAILED text collapses every distinct obligation that failed the same way onto one row."*

Every one of those is Pask's sentence. What we lack is the **prospective** form: enumerate the
derivations and look for a collision, instead of waiting for the collision to cost something.

**Second dated instance, from today, four hours before this review.** The board task
`health-fail-blames-the-far-end-for-this-nodes-own-uplink-and-both-verdicts-are-false-together`
({#507f5ad0}, closed 00:14Z) was precisely a derivational collision: `[health-fail] phaedra — SSH
unreachable` and `[health-fail] mesh-home — no internet` were both derived from *"a probe failed"*,
so a far end's death and our own uplink wedging were indistinguishable — and the fix I applied,
before reading this paper, was Pask's **add topic** (the self-leg's own state joined the coherence).
Two independent arrivals at the same repair, on the same day, is the argument that the rule is live
here.

## The application: `scripts/mesh-health-state`

`mesh-health-state` fuses eight per-aspect state files into one `~/.mesh/.mesh-health` verdict
(`reflex-cadence: */3`). Its `agg_verdict` derived **three distinct topics in the same way**:

| topic | premise, before | verdict |
|---|---|---|
| an aspect genuinely DEGRADED | value not in the acceptable set | WARN |
| an aspect **never measured** (file absent / organ not on this node) | value not in the acceptable set | WARN |
| an aspect reporting a token the **registry never learned** | value not in the acceptable set | WARN |

**MEASURED on this node, 2026-08-26T00:33Z**, with the whole node reading WARN:
`stress=WARM`, `mind=IDLE` — both *healthy* words this registry does not know — and
`router_thermal=unreachable-down`, a router we could not reach, which is a **coverage** fact and not
a health fact. **Zero aspects were actually degraded**, and the one word could not say so. A WARN
that can never resolve is the standing-accusation shape
(`a-suite-gate-on-a-node-fact-becomes-a-standing-accusation`).

**The repair taken is ADD TOPIC**, the minimal of Pask's four. Each `DECLARE` entry may now carry a
fourth field — the tokens meaning UNMEASURED *for that aspect* (`router_thermal|…|cool OK|unreachable`)
— so "unmeasured" acquires a derivation of its own instead of borrowing "degraded"'s. `check_class`
returns `good | fail | unmeasured | unrecognized`, and the reading publishes a per-check `class`, a
`coverage` term (`measured/declared`), and the NAMES in `unmeasured` / `unrecognized` / `failing`.
The same node now reads:

```
mesh-health-state: WARN — mesh-home @ 2026-08-26T00:35:54Z
  coverage: 7/8 aspects measured | unmeasured: router_thermal | token-not-in-registry: stress,mind | failing: none
  router_thermal: unreachable-down [unmeasured] (.router-thermal-state)
  mind: IDLE [unrecognized] (.mind-state-health)
```

Three deliberate restraints, each of which is a doctrine already on the wall:

- **The aggregate word is byte-identical in behaviour** — OK|WARN|FAIL, same mapping (unmeasured and
  unrecognized still WARN, absence still WARN, `FAIL*` still FAIL). A new top-level word would
  outrun every consumer's alphabet (`a-new-verdict-word-must-be-in-the-consumers-alphabet`) for no
  gain: grepped 2026-08-26, **nothing in the genome parses this file's `verdict` string** — the
  readers are a human, a mind, and `mesh-pulse`, which reads *freshness* only (`mesh-pulse:113`). So
  the ambiguity is resolved where it is actually read.
- **An unknown token is never folded into the acceptable set.** `WARM`/`IDLE` are probably healthy;
  quietly widening the good-set on that hunch is the guard-widening this doctrine refuses
  (`an-exclusion-allowlist-fails-toward-silence-so-invert-the-polarity`). They are named as a
  **registry gap**, which is the true statement, and the gap is now visible instead of wearing WARN.
- **A declaration can never outrank a hard fail.** `check_class` tests the fail patterns *before*
  the declared unmeasured tokens, so a state reading `FAIL: unreachable …` is `fail`, not
  `unmeasured` — the one ordering whose failure direction is loud.

**Two sub-fixes fell out of the same rule, one ring down:**

1. **Absence is decided from the filesystem, never from the sentinel string.** The old code derived
   absence via `cat … || echo MISSING`, so a state file whose *content* was the word `MISSING` was
   indistinguishable from a file that does not exist — the very ambiguity, recreated inside the fix
   for it. `check_class` now tests `[ -r … ]`; the rendered value stays `MISSING` for compatibility.
2. **`--check` no longer writes `~/.mesh/.mesh-health`.** It is documented read-only (`:9`) and wrote
   the artifact anyway — and `mesh-pulse` watches that file's mtime for liveness, so a hand-run
   `--check` refreshed the very evidence it claims only to inspect
   (`a-dry-run-that-writes-the-liveness-log-forges-its-own-evidence`).

## The gate, and it was seen to fail

Six arms in `mesh-health-state --test`, each mutated to confirm it is not vacuous:

| arm | mutation | result |
|---|---|---|
| absent vs unknown-token are distinct topics | collapse `unmeasured` → `unrecognized` | RED: *"absent=unrecognized unknown=unrecognized"* |
| the 4th DECLARE field is what does the work | ignore the declared unmeasured set | RED |
| a declaration cannot outrank a hard fail | move the unmeasured test before the fail patterns | RED |
| absence is a filesystem fact, not a string | decide absence by `= MISSING` | RED |
| coverage is published and counts | rename the `coverage` key | RED |
| no faked all-clear (unmeasured holds WARN) | — control, green with all-good fixture | — |

One process note worth keeping: the first mutation run reported a red for an arm whose
`str.replace` had **silently not matched**, and the runner then re-tested the *previous* mutant's
leftover file. A failed fixture mutation reads exactly like a surviving gate
(`a-failed-fixture-mutation-looks-like-a-passing-gate`) — every mutation here asserts it applied.

## What I did NOT take, and why

- **Split topic / analogy relation** — Pask keeps two bifurcated topics linked by an explicit
  *analogy* edge. We have no representation of "these two verdicts came from one idea", and inventing
  one for a single organ would be a private notation nobody else reads.
- **Nested coherences are illegal → condense.** A real second candidate (our DECLARE-style registries
  do nest), but it needs a survey of registries before it means anything, not an edit. Filed as the
  next step, not claimed.
- **Prune as a mesh-wide lint.** Tempting and refused: a lint whose predicate is not the parser's own
  predicate is not a guard on that parser (`a-lint-that-tests-a-different-predicate-than-the-parser-is-blind`).
  Prune belongs *inside* each organ's own vocabulary, which is where it went.

## Sources

- Heylighen, F. (2001). *Bootstrapping knowledge representations: from entailment meshes via semantic nets to learning webs.* Kybernetes 30(5/6). <https://pespmc1.vub.ac.be/Papers/Pask-Bootstrapping.pdf>
- <https://en.wikipedia.org/wiki/Conversation_theory>
- <https://cybernetics.coexplorer.org/pask.html>
- Mancilla, R. *Paskian Algebra: A discursive approach to conversational multi-agent systems.* <https://philarchive.org/archive/MANPAA-8>
- <https://en.wikipedia.org/wiki/Second-order_cybernetics>
