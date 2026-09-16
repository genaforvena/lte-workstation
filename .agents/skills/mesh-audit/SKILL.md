---
name: mesh-audit
description: Run an audit, review, or reconciliation that promises downstream task creation, with every finding mapped to an exact owner or a reasoned disposition. The audit enforces mesh rules strictly — it fails work that does not meet them, it never waives them. Use when a task carries the audit-followthrough tag.
---

This skill is the strict one. Where other skills describe how to work, this one
decides whether the work counted. When in doubt, fail the item: a wrong pass is
worse than a loud fail, because a pass stops every downstream check.

ENFORCE, in this order — stop at the first failure and record it:

1. **Artifact exists.** The claimed file, ref, receipt, or reading is on disk (or
   in the ledger) and you have personally inspected it. A subagent's report, a
   board line, or a memory of it is not the artifact. No artifact → FAIL.
2. **Verification is real.** The claimed check ran against the live thing and was
   seen red-then-green where the gate matters: `--test` green on the changed path,
   a mutant or fixture proving the gate can fail, a hardware read for a sensor, a
   transport receipt for a delivery. Green-only, offline-only, or self-reported
   verification → FAIL.
3. **Done means done.** Match the work against the definition of done: delivery
   lane owes a receipt with destination + transport proof; code lane owes verified
   behavior; sensor lane owes a fresh real reading; every lane owes a settled
   ledger row and a written handoff. Partial work presented as complete → FAIL,
   and say exactly which clause failed.
4. **Observability holds.** The change's state renders on a top pane and the owning
   mind observes it there — the receipt names the pane/role. Deterministic gates
   must wire into `mesh-doctor` so `.doctor-fails` carries them to the health pane.
   A verdict visible only in chat.log, in a receipt file, or in this pane → FAIL:
   it is a blind change.
5. **Mesh rules were obeyed.** Single-writer substrate discipline (claim held,
   rollback planned, verified from a vantage the change cannot sever); board voice
   in the mind's own window (no subagent impersonation); no silent fallbacks
   (`cmd || default` that renders failure as success); no prose that satisfies its
   own source-text gate; coverage published beside every ambiguous zero. If the
   work failed any of these BEFORE the audit, the audit enforces them now — it
   does not grandfather the violation because it already happened. Rule broken →
   FAIL with the rule named.

DISPOSITION. Every finding from this audit must result in an exact-owner
corrective task before the audit settles. First search for an existing active task
that covers the finding and cite it; otherwise create a corrective task naming the
owner, acceptance condition, retry edge, and durable artifact path. A finding
recorded only in a receipt is incomplete.

DETERMINIZE. For every check this audit performed by judgement, ask whether a
deterministic gate could perform it instead — a script, a lint, a `--test` arm, a
`mesh-doctor` check. Judgement rots; a gate runs every tick. If the answer is yes,
the audit owes an exact-owner task to build it (script path, red-then-green proof,
wiring into the doctor/pane path). If the answer is no, write the one sentence
saying why this check is irreducibly judgement — "needs a human eye" without the
reason is not the sentence. An audit that leaves a determinable check as judgement
is itself a finding (against this audit, actionable, owner: whoever can build the
gate).

Canonical task plans use `owner<TAB>step-slug<TAB>description` (or the four-column
form with priority); verify the created ledger row and dispatch eligibility. Mark
every task that performs an audit, review, reconciliation, or other work promising
downstream task creation with the plan header `#tags=audit-followthrough`. Its
completion artifact must have an adjacent `<artifact>.findings.json` file with
`version: 1` and a nonempty `findings` array. Each unique finding is either
`actionable: true` with exact `task` (`chain/step`) and `owner`, or
`actionable: false` with a nonempty `reason`. `mesh-task done` verifies these
mappings against canonical replay; tagged work cannot use `reject` to bypass
disposition, so block it with an exact retry edge or complete it with a reasoned
non-actionable disposition. This tag is explicit metadata, never inferred from a
task name or prose.
