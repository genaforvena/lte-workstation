# MeshLand Semantic Commits Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `mesh-land` create one independently revertible commit per settled semantic landing unit, with an imperative path-naming subject and a concise why/scope/verification body.

**Architecture:** Preserve candidate enumeration, settle/parse/rollback/substrate/autoland gates, path-limited staging, push healing, deployment, autowiring, and board outcome handling. Replace the single batch commit with a per-unit loop; an ordinary candidate is one unit, while a detected rename remains one add+remove unit so it cannot half-land. Generate deterministic imperative subjects (`Add`, `Update`, `Remove`, or `Move`) from the actual unit paths.

**Tech Stack:** Bash, Git, existing `scripts/mesh-land --test` hermetic fixtures.

## Global Constraints

- Keep steward-centralised landing and all existing gates unchanged.
- Keep push, deploy, autowire, and board reporting behavior unchanged in meaning.
- Do not commit unrelated staged paths; leave them staged and explain the deferral.
- Every generated commit body must explain why/context, scope, and verification.
- Use the existing self-test as the focused regression artifact; no live repository mutation is needed for the fixture.

---

### Task 1: Lock the new commit contract with failing tests

**Files:**
- Modify: `scripts/mesh-land` in the existing `--test` block and commit-message helper tests

- [ ] Add assertions that a generated message with an imperative subject and `Why/context:`, `Scope:`, and `Verification:` is accepted, while the old `mesh-land: land N changed:` shape is rejected.
- [ ] Add an end-to-end fixture with two settled candidates and assert that landing produces two commits, each names exactly one candidate, and each has the three body fields.
- [ ] Run `bash scripts/mesh-land --test`; expect failure because the current implementation creates one batch commit and only accepts the old message contract.

### Task 2: Implement semantic-unit message generation

**Files:**
- Modify: `scripts/mesh-land` commit-message helpers and landing message construction

- [ ] Replace the old count-based validator/fallback with validation for an imperative subject naming the unit path and body fields for why/context, scope, and verification.
- [ ] Generate `Add <path>`, `Update <path>`, `Remove <path>`, or `Move <old> to <new>` subjects from the unit’s actual index/worktree state.
- [ ] Keep path-specific context/citations and verification details in the body; never include a generic batch claim.
- [ ] Run the focused self-test and confirm the message assertions pass.

### Task 3: Land one semantic unit per commit

**Files:**
- Modify: `scripts/mesh-land` `--apply` commit/push/deploy/board path

- [ ] Build units from candidates, pairing a rename’s removal with its addition and leaving lone removals as their own unit.
- [ ] For each unit, stage only its paths, commit with its generated message, run the existing push-heal logic, deploy only that unit’s deployable files, and retain existing deployed-deletion warnings and autowire behavior.
- [ ] Preserve explicit deferral of unrelated staged paths and retain aggregate landed/strand reporting without claiming a batch commit.
- [ ] Run the end-to-end fixture and verify two candidate files produce two independent commits with no interloper.

### Task 4: Verify and record the artifact

**Files:**
- Create: `docs/mesh-land-semantic-commits-20260907.md`

- [ ] Run `bash scripts/mesh-land --test` and `bash -n scripts/mesh-land`.
- [ ] Record the exact fixture commit subjects/bodies, test output, and preserved behaviors in the verification artifact.
- [ ] Inspect `git diff --check` and the final diff, then report exact commit examples and any unresolved limitation.
