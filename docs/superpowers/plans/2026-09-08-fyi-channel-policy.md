# FYI Channel Policy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `[fyi]` a typed, non-task event channel whose observations remain visible without creating hidden work, while converting every actionable conclusion into a canonical `[task]`.

**Architecture:** Keep `[fyi]` in the append-only raw board and out of task lifecycle state. Add one shared classifier/validator at the board-ingress boundary, then make producers either emit FYI with event fields or emit a separate task for action. Add deduplication and escalation rules so repetition is trace-level evidence until a measured threshold creates a real task. In parallel, materialize FYI into a separate `FYI`-commodity hledger event journal for counts and explicit `task:`-tag queries; never mix it into promise liabilities or let prose mentions infer task association.

**Tech Stack:** Bash and Python 3; `mesh-chat`, `mesh-task`, `mesh-workflow`, `mesh-trace`; shell integration tests; `~/.mesh/chat.log` as the live evidence source.

## Global Constraints

- `[fyi]` is an ordinary event, not a task or promise; an action derived from it is a separate canonical `[task]`.
- `[fyi]` must never create a task-ledger row, claim, dispatch, promise balance, or completion record by itself.
- Raw `[fyi]` lines remain in `~/.mesh/chat.log`; views may filter them, but the canonical source is never rewritten.
- A task requires a stable task ID, exact owner, actionable acceptance condition, and owner-authored `[taking]` before work is considered started.
- Repeated FYI is not silently discarded: retain the latest/first event according to a documented deduplication key and count suppressed repeats in trace evidence.
- No producer may encode an imperative (`owner:`, `priority:incident`, `Run:`, or equivalent action request) in FYI; emit the observation first and a separate task when work is required.

## Evidence and decision

The live corpus at 2026-09-08 contains 7,775 `[fyi]` rows, 1,308 `[task]` rows, 730 `[taking]` rows, and 4,380 `[done]` rows. The largest FYI producers are roll-call (1,215), device-churn (1,016), mesh-path-watch (679), and udev-stream (587). These are event/status streams with measurements, freshness, source, and tape references—not work items.

The corpus also contains action-shaped FYI. A recent example is `mind-control` repeatedly announcing an absent owner for a real open task. A bounded live review found 234 duplicate-looking rows before the cooldown race was fixed; the repair now emits one board FYI and trace-only repeats (`docs/mind-control-absent-owner-spam-fix-20260908.md`). Other examples report that a durable task was created or that a draft is ready. Those are useful receipts, but they must not become a second task protocol.

The decision is therefore “typed event, not noise; no blanket ban.” Ban `[fyi]` from the task lifecycle and promise semantics, not from the board. Keep it for measured observations, acknowledgements, state transitions, recovery notices, and receipts. Reject or relabel action-shaped FYI at ingress, and require a separate `[task]` for any requested work. Use `[design]`/`[chat-review]` for proposals and review findings, and `[done]` for completion.

### Reconsideration: hledger as a typed event view

The bounded experiment is recorded in `docs/fyi-hledger-event-experiment-20260908.md`.
It supports a separate FYI event journal, not FYI liabilities: 952 FYIs materialized as
balanced `events:fyi:<producer>` / `equity:fyi` postings and passed `hledger check`. The
same window contained 34 explicit `task:` tags but 278 prose mentions of current task
slugs, so association must use explicit tags only. The plan now adds this as a parallel
read/query surface while preserving `mesh-promises`'s existing commodity boundaries and
independent replay agreement.

## Planned event contract

An accepted FYI body must have this shape:

```text
[fyi] <event-kind> <subject>: <fact> · source=<producer> · observed_at=<ISO-8601> · evidence=<path-or-tape> · action=none
```

`event-kind` is descriptive (`observation`, `ack`, `state-change`, `recovery`, `receipt`, or `warning`). `action=none` is explicit for machine-produced lines. A warning may recommend where to look, but it cannot assign an owner, promise a change, or claim completion. If action is necessary, the producer emits a separate task containing the same subject and a concrete acceptance test.

## Implementation tasks

### Task 1: Freeze the classifier and migration inventory

**Files:**
- Create: `docs/fyi-channel-policy-20260908.md`
- Create: `tests/fixtures/fyi-channel-corpus-20260908.log`
- Test: `tests/test-fyi-channel-policy.sh`

**Interfaces:**
- Consumes: sampled raw lines from `~/.mesh/chat.log` and the existing marker grammar in `scripts/mesh-workflow`.
- Produces: a versioned fixture with representative accepted FYI, action-shaped FYI, ambient/no-action FYI, and task conversion pairs.

- [ ] Extract a reproducible sample by producer class, including the four largest producers, a sensor measurement, a recovery, an acknowledgement, a receipt, one imperative FYI, and the 234-row duplicate incident summary.
- [ ] Write the contract document with an explicit disposition for every sample: `event`, `task-conversion`, `design/review`, `done`, or `reject-as-malformed`.
- [ ] Add a failing shell test that asserts the fixture has all five classes and that FYI-only lines produce zero task IDs.
- [ ] Add an hledger fixture lane: balanced `FYI` event postings, explicit `task:` tag query, and an assertion that event postings never enter promise liabilities.
- [ ] Run `bash tests/test-fyi-channel-policy.sh`; expected initial failure until the classifier exists.

### Task 2: Add one ingress classifier and validator

**Files:**
- Modify: `scripts/mesh-chat`
- Create: `scripts/mesh-fyi-policy`
- Test: `tests/test-fyi-channel-policy.sh`

**Interfaces:**
- Consumes: a candidate marker/body and optional producer metadata.
- Produces: `event`, `task-required`, or `reject`, plus a reason and normalized event fields; it must not write `chat.log`.

- [ ] Implement `scripts/mesh-fyi-policy --classify '<marker/body>'` with body-start marker parsing, not substring matching.
- [ ] Return `event` for facts/status/measurements/receipts with no imperative; return `task-required` for owner/priority/action/acceptance language; return `reject` for malformed or ambiguous marker syntax.
- [ ] Make `mesh-chat` call the validator for new `[fyi]` posts while preserving raw append-only behavior and returning a loud non-zero result for rejected input.
- [ ] Add mutation tests: remove the action detector and assert the imperative fixture goes red; change `[fyi]` to prose containing `[task]` and assert it remains an FYI event.
- [ ] Run `bash tests/test-fyi-channel-policy.sh` and `bash -n scripts/mesh-chat scripts/mesh-fyi-policy`; expected result: PASS.

### Task 3: Separate escalation and deduplication from FYI semantics

**Files:**
- Modify: `scripts/mesh-mind-control`
- Modify: `scripts/mesh-ledger`
- Modify: `scripts/mesh-dispatch`
- Test: `tests/test-fyi-channel-policy.sh`

**Interfaces:**
- Consumes: the classifier result and a producer/subject/evidence deduplication key.
- Produces: one bounded FYI board line, trace-only suppressed repeats, or a new canonical task when an explicit escalation threshold is crossed.

- [ ] Preserve the owner-absent repair’s per-task cooldown and add an integration assertion for concurrent dispatches: one FYI row, remaining attempts in trace, no duplicate task.
- [ ] Ensure `mesh-ledger` escalates only through `[task]` after its measured consecutive-failure threshold; recovery remains `[fyi]` or `[done]` according to whether work was performed.
- [ ] Ensure `mesh-dispatch` never treats FYI text as an opener, claim, settlement, priority, or evaporation exemption.
- [ ] Keep any FYI event materializer separate from `mesh-promises`; require replay/count parity and explicit-tag-only task association.
- [ ] Run the focused tests plus `bash scripts/mesh-ledger --test`, `bash scripts/mesh-dispatch --test`, and `bash scripts/mesh-mind-control --test`.

### Task 4: Update views, producer guidance, and live wiring

**Files:**
- Modify: `scripts/mesh-workflow`
- Modify: `docs/mesh-architecture.md`
- Modify: `docs/coordination.md`
- Modify: producer headers that currently describe FYI behavior (`scripts/mesh-path-watch`, `scripts/mesh-fail2ban-watch`, `scripts/mesh-udev-stream`, and any producer found by the inventory)
- Test: `tests/test-fyi-channel-policy.sh`

**Interfaces:**
- Consumes: the shared event classification and task lifecycle markers.
- Produces: truthful views where FYI is visible as context but cannot appear as workflow progress.

- [ ] Keep `mesh-workflow`’s explicit FYI exclusion and add a fixture assertion that an FYI citing a task slug does not open, claim, or settle that task.
- [ ] Document the marker decision table and the conversion rule in the architecture/coordination docs.
- [ ] Update each producer’s usage text to say whether it emits event, warning, recovery, or receipt FYI and where action is escalated.
- [ ] Run `bash scripts/mesh-workflow --test` and the full focused FYI test.

### Task 5: Prove the live migration and audit the remaining exceptions

**Files:**
- Create: `docs/fyi-channel-policy-verification-20260908.md`
- Test: `tests/test-fyi-channel-policy.sh`

**Interfaces:**
- Consumes: live `~/.mesh/chat.log`, `tasks.journal`, `mesh-task audit`, and deployed script paths.
- Produces: an independent receipt with before/after counts, rejected candidates, conversion pairs, dedup evidence, and unresolved exceptions.

- [ ] Run the classifier against a bounded recent window and record counts by producer and disposition; do not claim whole-history conformance from a sample.
- [ ] Create one disposable live event and one disposable action-shaped candidate; verify the first is retained as FYI and the second becomes a separate task or is rejected loudly.
- [ ] Run `mesh-task audit`, confirm no FYI-only row is open/owned/closed as task work, and inspect `mesh-dash --once witness` for truthful unfinished rows and the unfiltered 20-line tail.
- [ ] Record any historical exceptions as migration debt with owner and exact next command; do not rewrite historical `chat.log`.

## Acceptance gates

- A fact-only FYI remains visible and never enters `tasks.journal`.
- An FYI with an imperative or owner/priority assignment is rejected or paired with a distinct `[task]`; it cannot itself satisfy start or completion.
- A task-citing FYI does not close or claim the cited task.
- Repeated FYI is bounded on the board and measurable in trace; it is not silently lost.
- A sustained warning escalates through a real task with owner and acceptance evidence.
- Live checks cover both ingress wiring and task-ledger/workflow exclusion; unit tests alone are insufficient.

## Self-review

The plan covers the requested classification, rejects the false choice between “all task” and “noise,” preserves useful event visibility, and provides a concrete no-blanket-ban policy. It does not alter historical logs or create a duplicate implementation task before the classifier design is accepted. No placeholder steps or unspecified test commands remain.
