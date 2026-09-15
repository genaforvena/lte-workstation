# Synthetic effort commodity evaluation — 2026-09-09

Task: `coordination-hledger-reconciliation-extension-20260909/synthetic-effort-commodity`

Decision: **NO-GO for a new ledger commodity now; retain `TURN` and expose any future
effort weighting as a derived, report-only view until attribution is materially better.**

## Live-state audit

The task was still live at 2026-09-09T00:41:54Z: the task ledger marked this step `open`,
and no receipt with this path existed. The completed sibling `reconcile-protocol` is not
this task and does not settle it.

Current accounting is already split into distinct axes:

| question | current source | boundary |
| --- | --- | --- |
| provider/mind work quanta | `mesh-labor`, commodity `TURN` | one provider round-trip; report-only unless a TURN cap is explicitly armed |
| imputed compute price | `mesh-ledger`, commodity `USD` | inference/energy/depreciation; not cash |
| obligations | `mesh-promises`, commodities `PROMISE`, `CLAIM`, `HOLD`, `ASK` | board lifecycle; not labor or quality |

The live checks were all green for their own scopes: `mesh-labor --check` (parity and
replay agreement), `mesh-ledger --check` (parity and 609 non-overlapping feed windows),
and `mesh-promises --check` (parity and promise/claim/hold/ask replay agreement). The
labor journal contained 5,725 TURN against 6,108 spend-log rows; the difference is
unfed tail, not evidence for another commodity. The live branch query reported 3 TURN,
but explicitly labels its owner-window interval attribution as a proximity estimate,
not per-turn proof.

## Does a weighted effort measure answer a question beyond unit counts?

Yes, in principle, one real coordination question is:

> With equal open-task counts, which owner/window is carrying more expected coordination
> burden because tasks have different declared effort weights?

That could help a human inspect load balance when ten small tasks should not be treated as
ten large investigations. It is not a quality score, completion score, cash price, or
routing denominator. However, the current evidence does not support minting it: only
176 of 6,108 live spend turns (28.8%) carried a task tag, while `mesh-labor --branch`
assigns the owner window's turns by the task's open interval and calls the result a
first-order estimate. A second commodity would therefore give weighted-looking numbers
with less provenance than the existing TURN count.

The useful next step, if the question becomes operationally important, is a derived
`effort_points` report over explicitly declared task weights—not an independent feed
that duplicates every TURN. It must show both raw task count and weighted sum, plus
coverage and unknowns, so missing attribution cannot look like low effort.

## Proposed invariants if a future `EFFORT` commodity is justified

1. `EFFORT` is synthetic ordinal capacity, not USD, cash, outcome quality, or route
   relevance. No exchange rate to USD or TURN is permitted.
2. A task has one positive declared integer weight in a bounded scale (for example
   1–5), immutable for the frozen reporting interval. Missing, conflicting, or
   out-of-range weights are `UNKNOWN`, never zero.
3. Every counted unit has exactly one task/owner attribution or is reported in a separate
   `unattributed` bucket. A weighted total is not presented as complete without its
   attribution coverage denominator.
4. A task's weight is counted once per task interval/report cohort, not once per chat
   line, wake-up, provider, or duplicate replay. Reopens are separate intervals and are
   visible rather than silently netted away.
5. Every double-entry transaction balances in `EFFORT` itself. The balancing account is
   synthetic capacity (for example `equity:synthetic-effort`), never `assets:budget`,
   USD, PROMISE, or a routing account.
6. The view is report-only until a separate acceptance proves that its attribution is
   stable across task replay, board/chat, and artifact cutoffs. It must not alter task
   liabilities, routing, dispatch order, or any quality verdict.

## Attribution coverage and adjustment semantics

Publish, at the same frozen UTC cutoff:

`weighted_known / weighted_expected`, `tasks_known / tasks_expected`,
`unattributed`, `conflicting`, `late`, and `source_age`.

Coverage is a property of the answer, not a footnote. If task replay, owner identity,
weight declaration, or the artifact source is unavailable or stale, emit `UNKNOWN` with
the source and watermark; do not impute zero effort.

Corrections are append-only and explicit. A future journal entry would use this shape:

```hledger
2026-09-09 = ADJUSTMENT ; task:<exact-id> ; source:<watermark> ; reason:<bounded reason>
    expenses:synthetic-effort:correction:<owner>    2 EFFORT
    equity:synthetic-effort-adjustment              -2 EFFORT
```

The entry must cite the superseded observation, frozen cutoff, author, and reason. It
corrects a derived balance in a later period; it never edits or deletes the original
transaction, closes a PROMISE, changes USD, or changes routing. If the correction cannot
be attributed to a unique task and owner, it remains `UNKNOWN`/`PROPOSE_ONLY` rather than
being booked.

## Negative case — when not to use it

Do **not** use `EFFORT` to decide that one mind produced better outcomes, to rank or route
tasks, to infer cash cost, or to declare a task complete. In particular, two tasks with
weights 1 and 5 can both be equally successful, and a high-weight open task can reflect
uncertainty rather than poor performance. Use PROMISE/CLAIM lifecycle, outcome evidence,
TURN/interval labor, and USD inference for those separate questions.

## Verification and unresolved obligation

Verified against the live board/task ledger, current `mesh-labor`/`mesh-ledger`/
`mesh-promises` checks, `mesh-labor --balance`, and the live branch attribution output.
No code path, journal, routing rule, or historical entry was changed. The unresolved
obligation is an independent acceptance experiment: replay missing/delayed/conflicting
weights and show that the proposed report says `UNKNOWN` and leaves existing ledgers
unchanged before any `EFFORT` commodity is implemented.

## Corrective live-state verification — 2026-09-09T03:20Z

The step was claimed by `genome` after the dispatch-reconciliation finding. The requested
artifact now exists at this path. Repeated live checks produced:

- `mesh-promises --check`: parity PASS and replay/hledger agreement PASS for PROMISE,
  CLAIM, HOLD, and ASK; it reports two existing non-roster promises as unrouted.
- `mesh-ledger --check`: parity PASS; 611 feed windows, zero overlaps or gaps.
- `mesh-labor --check`: parity PASS; journal 5,795 TURN is within the 6,185 TURN spend log.
- `mesh-labor --balance`: current TURN balance rendered successfully, including `genome`'s
  existing provider rows.

These checks do not justify minting `EFFORT`; they confirm the report-only NO-GO boundary and
leave journals, routing, and quality decisions unchanged.
