# Evidentiary adequacy: a record answers a determination only if it carries the TYPING and the RELATION

**Area:** second-order cybernetics (von Foerster / Pask / Beer lineage) — the observer's *record*, not
the observed system. **Landed:** 2026-08-04, `scripts/mesh-promises --evidence` (report-only,
uncommitted — steward lands). **Angle:** a result one month old.

## The source

Jeroen Janssen (Apparens), *From Runtime Records to Legal Findings: An Evidentiary-Adequacy Criterion
for Agentic AI Oversight*, **arXiv:2607.00941v1 [cs.CY], 1 July 2026** (technical report, 12pp).
Found via the arXiv API sorted by submission date; **PDF read in full** (`pdftotext`).

Its own framing is squarely in this area: keywords list *requisite variety* and *Good Regulator
Theorem*, and §4.2 states the move that makes it second-order rather than first — it **inverts
model-dependence onto the overseer**:

> "The report uses this result only under its coupling condition: it applies to a supervisory system
> that senses, decides, and can affect future states. A purely retrospective evaluator is outside that
> theorem. The theorem supports model-dependence, not the legal content of the model."

That is Conant–Ashby turned on the observer — von Foerster's question ("what must be true of the
*observing* system?") made into a checkable condition on its records.

### The criterion

> **Definition 1 (answerability).** "E answers D when there exists a decision procedure f such that
> f(E) recovers the truth value of D, soundly, for the cases in the determination's scope. E fails to
> answer D when no such procedure exists over E, that is, **when the truth value of D is not a
> function of the content of E**."

> **Criterion 1 (evidentiary adequacy).** Let D be of the form: *did event-type X, of legal category
> C, stand in relation R to event-type Y?* Then E answers D **only if** E represents, explicitly or in
> functionally equivalent form, both: (1) **a typing** that maps the recorded events to the category
> C; and (2) **the relation R** — provenance, derivation, authority, or temporal validity — on which
> the truth of D depends.

And the sentence that makes it operational rather than rhetorical:

> "A representation carrying neither the typing nor the relation **can raise a suspicion, but it
> cannot establish the finding**."

Two further points matter for us. The claim is **necessity, not sufficiency** — a typed record is not
thereby correct, only *answerable*. And §2.2 argues the pair is **minimal**: "If typing is dropped, a
record can show a boundary crossing without showing that the content was of a protected legal
category. If the relation is dropped, a record can type two events without showing whether one derived
from the other… Neither feature is redundant."

§4.3 gives the same boundary in security vocabulary: a **relational** property "cannot generally be
evidenced from a single black-box trace" (Clarkson–Schneider hyperproperties); gray-box monitoring
lifts the limit only when the monitor is *given* the system knowledge — "that condition is the security
vocabulary version of the criterion."

## Why this is new ground for us

We have mined this area hard (see `second-order-cybernetics-coverage`, `vsm-beer-review-coverage`).
Checked and **already embodied**, so deliberately not re-landed:

- **Good Regulator Theorem** — `scripts/mesh-homeostasis:94-114` already cites *both* 2025 papers
  (arXiv:2506.23032, arXiv:2508.06326). Covered.
- **Requisite variety on the regulator** — `mesh-relay metabolism_variety()`, `mesh-vitality
  channel_variety()`. Covered.
- **Well-founded meta-observation** — `mesh-liveness-loop --audit-watchdog` (2026-08-04). Covered.
- **S3\* independent audit** — `mesh-liveness-loop --audit-cron`. Covered.

None of those asks the criterion's question. Every one of them is about *whether an observation
happened*. This is about **whether the record that resulted can bear the finding placed on it** — and
we have exactly one place that makes findings of fact from runtime records at scale.

## The gap: the leak detector's determinations are mostly not answerable from the record

`mesh-promises` replays the board into a double-entry ledger. Its determination is
**D = "did this `[done]` discharge that `[task]`?"** — precisely an in-scope binary finding of fact
about specific events *and their relation*.

- **Typing:** carried. The `[task]`/`[done]` markers map each line to its category.
- **Relation:** *usually not carried.* Which task a done closes is decided by `best_match()`
  (`scripts/mesh-promises:437`): leading-slug equality, else **distinctive-token overlap over prose**.

The mesh already *has* the explicit relation — `mesh-dispatch`'s `claim_id_of()` prefers a
`task:<id>` tag "over all derivation", and the board task that opened this very review carried
`task:mesh-rfkill` as its stated machine close-key. **`mesh-promises` never read that tag at all**
(verified: the only `task:` occurrences in the file were an internal bookkeeping string and two test
strings). The ledger that computes the mesh's standing liabilities was inferring a relation the record
was, in some cases, already carrying.

`mesh-dispatch`'s own test suite is an unwitting catalogue of Definition 1 failures — a done citing
*another* task's slug; a hostname fragment (`ad-3-15` out of `IdeaPad-3-15IIL05`) shadowing the real
subject; a bare tool-name mention beating the ns/slug subject. Each is the same shape: the record did
not carry the relation, so derivation supplied one, and supplied it wrong. Each was patched
individually. Nothing ever asked **what fraction of the ledger's determinations rest on inference**.

## What landed

`mesh-promises --evidence` — **report-only**, grades each closure by which feature of the record made
the determination. It never re-grades a balance; it says what the balance *rests on*. Verified
verdict-preserving: `--report`, `--json`, `--mttr`, `--collisions` byte-identical to the deployed copy.

| basis | meaning |
|---|---|
| `typed` | the done carries `task:<slug>` agreeing with the closed promise — **E answers D** |
| `lead` | no tag; closed by the `[done] <slug>:` lead convention — answerable only while the convention holds |
| `inferred` | closed by token overlap — the relation came from the matcher, not the record |
| `misbound` | the record's explicit relation and the matcher's inference **disagree**; the matcher won |
| `orphan-key` | a done asserted `task:<id>` that bound to no open promise |

Reported as `answerable` (typed / closures) and `structural` (typed+lead / closures), with verdicts
`TYPED-LEDGER` / `CONVENTION-BORNE` / `INFERRED-LEDGER`.

### Live reading

```
promise-evidence: closures=53 typed=35 lead=10 inferred=6 misbound=2 · answerable=0.660 structural=0.849
  VERDICT: TYPED-LEDGER
  orphan close-key ×20
  MISBOUND ×2:
    close-key says 'stale-propose-65fe2036' · matcher closed 'devto-hledger-coordination-piece'
    close-key says 'mesh-rfkill'            · matcher closed 'bluetooth-controller-s-own-pairable-disc'
```

**The second misbound is this session's own previous `[done]`.** The dispatcher stamped the close-key
`task:mesh-rfkill`; the promise ledger closed a promise slugged from the task's prose lead
(`bluetooth-controller-s-own-pairable-disc`). Two subsystems, two names for one obligation, and until
now nothing compared them. That is the criterion producing a live defect on the first run, from the
observer's own record.

`orphan-key ×20` is the other half: twenty dones asserted a relation the ledger could not bind at all.

### One correction the implementation forced

The first draft graded **22 of 53** closures `misbound` and read `INFERRED-LEDGER`. Nearly all were
artifacts: `pub-242370` vs `route-orphan-pub-242370`, `mark-completed-pairings` vs
`ideate-queue-mark-completed-pairings` — *one* value under two derivations (dispatch's `claim_id_of`
vs `sanitize(lead(...))`), differing by a namespace prefix. A third was a `SLUG_CAP` **truncation**
(`mesh-stress-voice-rx-functional-blindspo`, cut at 40). Grading those as disagreements manufactures
defects. `keys_agree()` canonicalizes first — boundary-anchored containment, a length floor, and an
explicit truncation branch — and `SLUG_CAP` is now a named constant because `keys_agree()` must reason
about truncation at exactly the value `sanitize()` cuts at, and two readers of a literal `40` drift.
This is [[two-renderings-of-a-value-must-be-canonicalized]] hit again, and it moved the headline
verdict from `INFERRED-LEDGER` to `TYPED-LEDGER` — a detector's verdict is a claim too.

### Gates (six mutants, each seen red from a scratch copy; control green)

| mutant | result |
|---|---|
| close-key ignored (`ck = None`) | RED — four bases not distinguished |
| `misbound` collapsed into `typed` | RED |
| canonicalization removed | RED — two renderings read as a disagreement |
| length floor removed | RED — *only after* fixture 26b was added |
| truncation branch removed | RED |
| n/a fabricated as `0.000` instead of exit 2 | RED |

The floor mutant is the honest one: it stayed **green** against the original fixture. `pub` inside
`republish-…` is rejected by the *boundary* guard alone, so the assertion I had labelled as covering
the length floor covered nothing. Fixture 26b puts a 3-char key exactly *on* a boundary, where only
the floor can reject it. Same shape as the `mesh-bt-link` field-anchoring gate earlier today —
**an assertion whose target is already caught by a different guard is not a gate.**

## Not claimed

The criterion is about **necessity**. A `typed` closure is not thereby correct — `answerable=0.660`
says two thirds of closures *could* be checked against the record, not that two thirds are right. The
paper's legal framing (EU AI Act obligations) is not imported; only the structural criterion is. And
`--evidence` deliberately does **not** make `best_match()` prefer the close-key: that would change
every balance, and the report exists to measure the gap before anyone decides to close it.

## Suggested next (not done here)

Make `best_match()` prefer an agreeing close-key over token overlap, then re-run `--evidence` and
`--report` and diff the balances. `misbound=2` and `orphan-key=20` are the pre-registered
expectation of what that change would move.

Related: [[second-order-cybernetics-coverage]], [[vsm-beer-review-coverage]],
[[mesh-promises-leak-detector]], [[dispatch-close-key-prose-poison]],
[[promise-best-match-prose-mention-hijack]], [[done-lead-must-be-the-slug]].
