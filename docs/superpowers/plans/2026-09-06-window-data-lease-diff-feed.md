# Window Data Lease and Conditional Diff Feed Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every live two-pane mesh channel use a top data pane with a visible liveness lease and feed its bottom mind only on meaningful top-pane diffs.

**Architecture:** Keep `mesh-dash` as the producer and its always-visible `pane live` footer as the renderer lease. Replace the stale consumer channel list with live discovery of two-pane windows whose top pane is a data renderer; `MESH_CONSUME_CHANNELS` supplies cadence/routing overrides but cannot remove a live channel. The existing `mesh-pane-consume` remains the conditional gate: it normalizes the top pane, applies prediction/refractory rules, and wakes the bottom mind through `mesh-tell` without copying stream content.

**Tech Stack:** Bash, tmux, mesh-dash, mesh-pane-consume smoke tests.

## Global Constraints

- Top pane is DATA and bottom pane is MIND for every channel built by `mesh-restore`.
- A data producer’s liveness must be visible as a lease; stale/unknown data must not appear current.
- The source remains ephemeral and unfiltered; only the consumer decides whether a diff wakes the mind.
- Preserve unrelated dirty worktree changes.

---

### Task 1: Cover live channel discovery

**Files:**
- Modify: `scripts/mesh-consume-all`
- Test: `scripts/mesh-consume-all --test`

**Interfaces:**
- Produces `channel_windows`, a newline-delimited live channel list used by ensure/status/kick/stop paths.
- Consumes tmux window and top-pane command state; does not inspect or mutate pane content.

- [x] **Step 1: Add a failing test** asserting the supervisor exposes live channel discovery and does not encode `tg` as an exclusion.
- [x] **Step 2: Run `scripts/mesh-consume-all --test` and observe the expected failure.**
- [x] **Step 3: Implement `channel_windows` and use it for all supervisor loops; preserve explicit `MESH_CONSUME_CHANNELS` cadence/routing overrides.**
- [x] **Step 4: Run the focused smoke test and shell syntax checks.**
- [x] **Step 5: Verify live wiring with `mesh-consume-all --status` and `tmux list-windows`.**

### Task 2: Verify lease/feed contract end-to-end

**Files:**
- Modify: `docs/mesh-architecture.md`
- Test: `scripts/mesh-dash --test-fast`, `scripts/mesh-pane-consume --test`, `scripts/mesh-consume-all --test`

**Interfaces:**
- Documents that the top pane’s `pane live` footer is the lease and that only normalized meaningful diffs wake the bottom mind.

- [x] **Step 1: Add the concise contract wording to the architecture section.**
- [x] **Step 2: Run all three focused smoke tests plus `bash -n` on changed scripts.**
- [x] **Step 3: Inspect the resulting diff and live status output for every discovered two-pane channel.**
