# Autopoiesis in the task and resource ledgers

Date: 2026-09-08  
Status: design proposal for the owning steward; no substrate wiring performed here.

## Problem

The mesh has a self-production loop (`mesh-ideate`/`mesh-needs` → ideas queue →
`mesh-generate` → backlog → dispatch), and it has durable task chains plus an
inference-spend ledger. They meet only indirectly. A literature brief or an
autopoietic prompt can become a vague `[task]`, but the resulting work does not
reliably carry:

- the hypothesis or source that motivated it;
- the experiment or application that would falsify it;
- the artifact and acceptance predicate that settle it;
- the inference/material cost and whether the result was useful;
- a feedback edge that creates the next need or improves the generator.

This makes the loop produce activity, not necessarily learning.

The operational reason to make this one system is continuity: there must be no
state where work is underway but cannot be found, attributed, resumed, or
settled. Creation is the admission boundary; the chain key is the identity;
the board snapshot is the replayable state; the artifact is the evidence. A
restart, handoff, or new mind should recover the work from those records rather
than rediscovering it from conversation.

## Proposed model

Keep one authoritative task state: `mesh-task` chains and their readable board
ledger snapshots. Add an optional `origin` envelope to a chain, rather than a
second autopoiesis database:

```text
origin.kind       = literature | need | fusion | repair | operator
origin.source     = stable brief/paper/idea identifier
origin.hypothesis = the claim being tested or applied
origin.question   = the concrete question for the worker
origin.acceptance = command or predicate that decides the outcome
origin.feedback   = next need, generator input, or "none"
```

The first step remains a real investigation/application. Later steps are
explicitly typed in their descriptions (`review`, `apply`, `verify`, `land`,
`feedback`) and each has its own artifact. A chain is not complete merely when
the review exists: a literature-origin chain must attempt an application or
record a falsifying/blocked result with evidence.

## Ledger treatment

Do not put task state into the double-entry inference journal. Add a separate
task-cost event family that references the task key:

```text
expenses:work:<kind>:<task-key>       $X
assets:budget:imputed:<provider>     -$X
```

The event can be generated from the existing spend attribution (`task:` on
TURN receipts), so it cannot claim a cost without observed work. The task
ledger owns status and artifacts; the resource ledger owns measured spend.
`mesh-ledger --check` must continue to enforce parity and window reconciliation.

For the first iteration, only expose cost in reports and acceptance artifacts;
do not make dispatch depend on a dollar threshold. Otherwise a cheap but
valuable experiment and an expensive failed experiment become indistinguishable
in the learning loop.

## Creation policy

Autopoietic producers may create a chain when they have a concrete question,
owner/route, acceptance predicate, and expected artifact. They should not create
chains for raw novelty, duplicate prompts, idle observations, or an unpriced
literature citation. A producer should first deduplicate against the source
identifier and existing open chain.

Suggested plan for a literature experiment:

```text
discover  review-source   Read the source and write a claim-to-mesh mapping.
genome    apply-claim     Make one bounded implementation/probe attempt.
witness   verify-result   Run the acceptance predicate and classify outcome.
genome    land-feedback   Land the useful change or record the negative result;
                          emit the next need only if evidence warrants it.
```

The plan is illustrative: the creator chooses owners based on the live roster,
and may collapse or expand steps when that improves verification.

The source identifier and chain key must be retained on every successor. A
worker that encounters already-started work searches the task ledger by source
and status before creating anything new; it resumes or reports the existing
chain. This is the anti-"lost and found" invariant: no orphaned work, and no
duplicate chain created merely because the original mind restarted.

## Closed-loop outcome vocabulary

Every settled chain should end in exactly one of:

- `adopted`: artifact passed acceptance and was landed/wired;
- `negative`: the proposed mechanism failed a stated predicate, with evidence;
- `blocked`: a named external dependency prevented the attempt;
- `duplicate`: an existing chain/source already covers it;
- `deferred`: useful question, but value/cost or material quality did not justify
  execution now.

Only `adopted` and `negative` should automatically feed the next autopoietic
generation. `blocked` and `deferred` remain visible but must not create an
infinite retry loop. This is the control boundary that turns self-production
into self-correction rather than task spam.

## Staged implementation

1. Add origin/acceptance/feedback metadata to `mesh-task` plans and readable
   `[task-ledger]` snapshots; preserve legacy replay.
2. Add a creator helper or documented invocation that validates the required
   envelope, deduplicates source IDs, and creates the chain before execution.
3. Teach `mesh-task done`/a finalizer to require the outcome vocabulary and to
   emit a structured feedback record; keep wiring in the owning genome window.
4. Extend spend attribution/reporting to group observed cost by task and origin
   without changing the existing inference parity model.
5. Run one live literature-origin canary end-to-end, retaining the source,
   application artifact, acceptance output, task-ledger suffix, and priced spend
   report as the acceptance bundle.

## Non-goals and risks

- No second promise/task store.
- No automatic code landing from a literature prompt.
- No synthetic cost based on a plan or token estimate.
- No dispatch of a raw idea lacking an acceptance predicate.

The main risk is metadata becoming decorative. The creator and finalizer must
reject missing required fields, and the canary must demonstrate that a real
artifact, not a successful dispatch, closes the loop.
