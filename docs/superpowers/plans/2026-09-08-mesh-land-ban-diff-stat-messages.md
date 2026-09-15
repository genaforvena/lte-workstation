# MeshLand Diff-Stat Message Ban Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent MeshLand from committing a diff statistic as a semantic change description.

**Architecture:** Treat `change N additions, M deletions` as invalid in both the commit subject and `Why/context:` field. The existing deterministic fallback will then fail loudly rather than inventing semantic intent; a worker must provide a path-linked board completion description or an explicit meaningful subject.

**Tech Stack:** Bash, Git, `scripts/mesh-land --test` hermetic fixtures.

## Global Constraints

- Keep steward-centralized, path-limited landing intact.
- A missing semantic description must hold the candidate loudly; it must never silently degrade to diff statistics.
- Drive the shared `commit_message_informative` predicate and an actual temporary-repository landing path.

### Task 1: Add the regression first

**Files:**

- Modify: `scripts/mesh-land` in the existing `--test` message-contract fixture.

- [ ] Add a commit message whose subject and context are `change 11 additions, 0 deletions`.
- [ ] Run `bash scripts/mesh-land --test`; expected result before implementation: `smoke-test: FAIL` because the current predicate accepts that message.

### Task 2: Reject non-semantic diff-stat descriptions

**Files:**

- Modify: `scripts/mesh-land:497-535`.

- [ ] Add one predicate rejection for `change <number> additions, <number> deletions` in the subject and `Why/context:` field.
- [ ] Run `bash scripts/mesh-land --test` and `bash -n scripts/mesh-land`; expected: both exit 0.

### Task 3: Verify the real fallback edge

**Files:**

- Modify: `scripts/mesh-land` existing temporary-repository fixture only if Task 1 does not exercise the real fallback path.

- [ ] Verify a candidate with no semantic board completion does not create a commit and emits a refusal naming opaque context.
- [ ] Restore a semantic board completion in the fixture and verify its commit is still accepted.

### Task 4: Record and land safely

**Files:**

- Modify: `scripts/mesh-land`.
- Create: `docs/meshland-ban-diff-stat-messages-2026-09-08.md`.

- [ ] Record red/green commands and their results.
- [ ] Run `git diff --check`, `bash -n scripts/mesh-land`, and `bash scripts/mesh-land --test` immediately before landing.
- [ ] Post a path-linked semantic board result before `mesh-land --apply`, so this change itself demonstrates the enforced contract.
