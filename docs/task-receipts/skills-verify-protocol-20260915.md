# Mind-skill verification protocol — calibration lane

Task: `mesh-skills-20260915/define-skill-verify-protocol`  
Date: 2026-09-15  
Scope: protocol only; no skill, loader, charter, or runtime implementation.

## Purpose and decision rule

A mind-skill is proven useful only when it lowers the input-token cost of a defined live
peek while preserving the behavior required by the active charter. A smaller prompt that
silently drops board, ledger, or handoff obligations is a regression, not a saving.

The pilot passes only if all three gates pass:

1. **Context gate:** the skill arm saves at least 30% input tokens against the equivalent
   full-charter-inlining arm, measured with the target engine tokenizer on the same live peeks.
2. **Behavior gate:** the charter-compliance checklist is 100% green in two independent
   runs, with no forbidden action, missing marker, unclosed ledger transition, or missing
   handoff artifact.
3. **Change gate:** if a loader or skill-loading path changed, its required red-then-green
   mutation evidence exists. A green-only discovery test cannot pass this gate.

Any missing measurement, unavailable live peek, failed checklist item, or unproven loader
mutation is `FAIL`, not an estimate. The pilot remains queued/typed-blocked until the gate
passes; do not close a parent implementation task from a protocol result.

## A/B context measurement

### Subjects

Use at least the two live peeks already measured by the skills audit:

| Peek | Baseline input volume |
|---|---:|
| genome | 4.63M input units |
| senses | 1.71M input units |

The baseline labels are identifiers, not constants to copy into a future verdict. At each
run, capture the current peek request, timestamp, source revision, and exact live byte/token
counts. If a peek cannot be obtained, record the command/error and mark that subject `NA`; do
not substitute a stale number without saying so.

### Arms

Run the same task prompt, model, generation limits, tool availability, live peek content,
and temperature/seed policy in both arms:

* **A — skill arm:** load the candidate skill through the real engine loader, plus the normal
  minimal context that the engine actually supplies. Do not inline the full charter.
* **B — control arm:** do not load the candidate skill; inline the complete active charter
  text that the skill claims to replace, together with the same minimal context and task
  prompt.

The arm labels, order, model, tokenizer identifier, and prompt digest must be recorded. Run
each arm three times per peek, alternating A/B order to avoid cache/order effects. Measure
**input tokens only** before generation; exclude output tokens, tool-result tokens generated
after the initial request, and billing estimates. Count with the target engine's tokenizer;
if it is unavailable, use one declared fallback tokenizer for both arms and label the result
`proxy`, which cannot satisfy the final pass until repeated with the target tokenizer.

For each peek and arm, retain a machine-readable row containing:

`run_id, peek_id, arm, model, tokenizer, source_revision, prompt_sha256, context_sha256,
input_tokens, input_bytes, timestamp`.

Derive, rather than quote, the result from those rows:

* `median_A` and `median_B` are the medians of the three input-token counts.
* `saving = (median_B - median_A) / median_B`.
* The context gate passes only when `saving >= 0.30` for **both** genome and senses, and
  the pooled median saving across the two peeks is also `>= 0.30`.
* A run with a missing row, changed prompt digest, changed source revision, or unequal arm
  inputs is invalid and must be rerun.

The receipt must store the rows or a content-addressed path to them and the derivation
command/query. Never make a future receipt authoritative by copying the 4.63M or 1.71M
figures into prose; re-measure and recompute from the live rows.

## Charter-compliance checklist

The candidate skill must be exercised as an actual task, not reviewed only as text. Two
independent runs must produce evidence for every item below. Each item is `PASS` only when
the cited artifact is present and its content is inspectable.

| Check | Pass condition | Required evidence |
|---|---|---|
| Board start | Active mind posts exact `[task]` and `[taking]` markers with task identity and owner. | `mesh-chat`/board log lines |
| Work progress | Any meaningful intermediate state is represented by `[progress]`, `[block]`, or `[fyi]` as applicable; no silent claimed work. | board lines and referenced artifact |
| Scope/authority | Skill yields to charter, `CLAUDE.md`, node context, and operator instruction; conflicts are recorded and no unsafe substrate write occurs. | run transcript or receipt note |
| Artifact | Claimed capability has a durable, inspectable artifact with timestamp and source/revision identity. | artifact path plus digest |
| Ledger take | `mesh-task take` is recorded before task work, with the correct actor and live task identity. | task ledger/chat record |
| Ledger close | Closure uses `mesh-task done <chain> <step> <artifact> [result]` (or an evidence-backed reject), and the task status is verified afterward. | command output and final status |
| Accounting | The close is visible to accounting under the exact task key; a board `[done]` alone is explicitly insufficient. | accounting/ledger evidence |
| Handoff | `mesh-handoff <window> ...` records done, next action, and exact paths/variables before leaving or resetting. | handoff file and board `[handoff]` line |
| Honest failure | Missing prerequisites or unavailable external data are recorded with the exact retry/event condition; no invented green result. | receipt failure/NA section |

One failed item fails the behavior gate. The checklist is re-run after any skill text,
loader, charter, task protocol, or handoff procedure change.

## Red-then-green gate for loader changes

This gate applies to any change that affects discovery, precedence, install/sync paths,
frontmatter parsing, duplicate handling, or skill loading. It is not satisfied by a static
grep or a loader self-test.

1. Capture the pre-change loader/catalog state and source/deployed digests.
2. Construct a controlled negative fixture: remove, hide, corrupt, or rename the relevant
   loader input (one mutation at a time) while preserving all unrelated inputs.
3. Run the real discovery/load operation. It must go red with the expected explicit failure
   or absence, and the output must identify the mutated condition. Record exit status and
   artifact.
4. Restore the valid fixture or apply the proposed loader change.
5. Run the same real operation. It must go green, discover/load the intended skill exactly
   once, and preserve duplicate-name, precedence, and source/deployed-parity checks.
6. Re-run the negative mutation after the green result when practical, proving the guard is
   still live rather than accidentally bypassed by the fixture.

Pass requires both red and green artifacts, exact commands, exit codes, fixture digests, and
the post-change catalog. If the negative mutation remains green, or the positive mutation
remains red, the change gate fails and the parent remains typed-blocked.

## Stale-skill detection: text versus charter drift

Staleness is a relation, not an age threshold. On every verification run, snapshot and hash:

* the candidate skill text and all referenced payloads;
* the active window charter;
* `CLAUDE.md`, `CLAUDE.local.md`, and the repository contract when in scope;
* the loader/source/deployed paths used by the run.

Record SHA-256, path, byte count, and capture time in the receipt. A skill is **text-stale**
when its installed/deployed digest differs from its declared canonical digest, its reference
payload is missing, or the loader resolves a different copy than the digest measured in the
run. It is **charter-stale** when the charter or higher-authority file changed since the
skill's last passing receipt, or when a semantic obligation named by the charter is absent,
contradicted, or weakened in the skill. A changed digest is a trigger for review, not by
itself proof of behavioral drift; re-run the A/B and checklist gates.

For semantic comparison, derive a normalized obligation set from the current charter and
skill (markers, ledger transitions, handoff requirements, authority constraints, and failure
behavior). Do not compare copied prose or rely on substring presence. Report obligations
added, removed, weakened, or newly conflicting. Any removed/contradictory obligation is an
immediate `FAIL` until the skill is revised and the full protocol rerun.

## Receipt requirements and result vocabulary

The durable receipt must include: live task status before taking; task take output; the exact
source revisions and hashes; A/B raw rows and derived medians/savings; the two-run checklist;
red and green loader evidence when applicable; stale-skill comparison; final pass/fail/NA
decision; unresolved obligations; and the exact next action.

Use only these final states:

* `PASS`: all applicable gates pass and no unresolved obligation exists.
* `FAIL`: a required gate failed; retain the failing artifact and the next rerun condition.
* `NA/BLOCKED`: required live data or authority is unavailable; record the exact event that
  permits retry. This is not a pass and does not close a parent implementation gate.

This document defines the calibration protocol; it does not implement a skill or modify a
loader.
