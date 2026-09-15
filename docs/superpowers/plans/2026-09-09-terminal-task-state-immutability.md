# Terminal task-state immutability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A structured task-state record that has reached DONE, REJECTED, or IGNORED cannot be replaced by a later mutation of that same terminal step, and rebuilding the ledger retains the valid receipt. A documented recovery may advance from a rejected predecessor to a distinct held successor only when it preserves the predecessor receipt byte-for-field.

**Architecture:** Validate transition legality while replaying the append-only task-state history, not only in `mesh-task` command handlers. `mesh_task_log.append()` calls replay while holding the log lock, so it rejects a newly supplied malformed post-terminal payload before it reaches `chat.log`. Historical malformed records cannot be erased and must be quarantined during replay: retain the last valid terminal state, continue validating later records against it, and keep unrelated chains available. `mesh-task rebuild` materializes only that valid canonical state.

**Tech Stack:** Python 3 standard library; `scripts/mesh_task_log.py`; `scripts/mesh-task`; unittest.

## Global Constraints

- `~/.mesh/chat.log` structured task-state records are authoritative; cache JSON is disposable.
- Keep DONE receipts immutable; do not rewrite or erase historical board evidence.
- BLOCKED remains retryable only from an ACTIVE current step; REJECTED is the only non-DONE terminal disposition.
- The pre-existing `recover` contract is valid: an artifact-backed `recovery_action` may move `current` from a rejected predecessor to a distinct successor while the predecessor snapshot remains unchanged. It is not a post-terminal mutation.
- Add red-before-green regression and verify historical-record quarantine, append rejection, unrelated-chain append, and cache rebuild.

---

### Task 1: Reject post-terminal revisions at the authoritative log boundary

**Files:**

- Modify: `scripts/mesh_task_log.py:replay` and `append`
- Modify: `tests/test-mesh-task-log.py`
- Test: `tests/test-mesh-task-log.py`

**Interfaces:**

- Consumes: decoded records shaped as `{revision: int, data: {chain, status, current, steps}}`.
- Produces: `replay(path) -> dict[str, dict]` that retains the valid terminal snapshot while quarantining a terminal-to-nonterminal historical revision; `append()` rejects a newly supplied invalid transition and leaves the log byte-identical on that error.

- [ ] **Step 1: Write the failing replay and append tests**

```python
def test_replay_quarantines_done_step_replaced_by_blocked_revision(self):
    self.write_record(revision=1, status="complete", step_status="done",
                      finished="2026-09-09T19:06:35Z", artifact="/receipt.md")
    self.write_record(revision=2, status="blocked", step_status="blocked")
    self.assertEqual(replay(self.path)["plan"]["data"]["status"], "complete")

def test_append_refuses_post_done_block_without_writing_bytes(self):
    append(self.mesh, "tg@mesh-home", self.done_payload)
    before = (self.mesh / "chat.log").read_bytes()
    with self.assertRaisesRegex(ReplayError, "terminal task-state regression"):
        append(self.mesh, "tg@mesh-home", self.blocked_payload)
    self.assertEqual((self.mesh / "chat.log").read_bytes(), before)
```

- [ ] **Step 2: Run the focused tests and verify red**

Run: `rtk proxy python3 tests/test-mesh-task-log.py`

Expected: FAIL because replay currently selects revision 2 without checking the prior terminal snapshot.

- [ ] **Step 3: Implement the transition validator**

```python
TERMINAL_STEP_STATUSES = {"done", "ignored", "rejected"}
TERMINAL_CHAIN_STATUSES = {"complete", "ignored", "rejected"}

def validate_transition(previous: dict, candidate: dict) -> None:
    previous_step = previous["data"]["steps"][previous["data"]["current"]]
    candidate_step = candidate["data"]["steps"][candidate["data"]["current"]]
    previous_terminal = (previous["data"].get("status") in TERMINAL_CHAIN_STATUSES
                         or previous_step.get("status") in TERMINAL_STEP_STATUSES)
    candidate_terminal = (candidate["data"].get("status") in TERMINAL_CHAIN_STATUSES
                          or candidate_step.get("status") in TERMINAL_STEP_STATUSES)
    if previous_terminal and not candidate_terminal:
        raise ReplayError("terminal task-state regression")
```

Call it while replaying each chain before selecting the canonical latest valid revision. Preserve the existing same-revision conflict and contiguous-revision checks. A historical invalid record is retained as evidence but quarantined: it cannot replace the last valid state or make another chain unavailable; a later record must validate against the last valid predecessor. Do not allow a changed terminal artifact/status either: compare the terminal chain status, current step id/status, artifact, artifact_sha256, and finished/rejected/ignored fields.

Allow exactly the existing recovery transition from a rejected current step when the candidate moves `current` to a distinct successor carrying `recovery_action` and its artifact-backed recovery fields, while preserving the formerly current rejected step exactly. A missing recovery marker, changed predecessor receipt, or in-place rejected-to-blocked mutation remains `ReplayError("terminal task-state regression")`. `append()` must still raise that error for a fresh invalid payload.

- [ ] **Step 4: Run focused and command-level verification**

Run: `rtk proxy python3 tests/test-mesh-task-log.py && rtk proxy python3 tests/test-mesh-task-no-expiry.py && rtk proxy scripts/mesh-task --test`

Expected: all exit 0.

### Task 1b: Preserve legitimate rejected-successor recovery

**Files:**

- Modify: `tests/test-mesh-task-log.py`
- Modify: `scripts/mesh_task_log.py`

- [ ] **Step 1: Write the recovery regression**

Build a chain with r7 current A02-V `status=rejected`, then r8 current A06 `status=blocked`, `recovery_action=hold`, `recovery_artifact`, and unchanged A02-V terminal fields. Assert replay selects r8; a later release/open/done progression remains canonical. Add a control that changes A02-V or omits `recovery_action` and is quarantined.

- [ ] **Step 2: Verify the live counterpart**

Run `rtk proxy scripts/mesh-task replay --json` and assert TinyFleet selects r44/current A07 DONE after replay. This is the gate for requesting A07-V; no later task may be dispatched merely because raw board messages exist.

### Task 2: Prove rebuild retains the terminal snapshot and publish the correction receipt

**Files:**

- Modify: `tests/test-mesh-task-no-expiry.py`
- Create: `docs/task-receipts/terminal-task-state-immutability-20260909.md`

**Interfaces:**

- Consumes: a chat log whose valid revision is DONE and whose next revision attempts BLOCKED.
- Produces: a rebuild that preserves/materializes the valid DONE cache while quarantining the bad historical revision; receipt records source/deployed hashes and commands.

- [ ] **Step 1: Write the failing rebuild fixture**

```python
def test_rebuild_quarantines_postterminal_mutation_and_preserves_done_cache(self):
    self.command("done", "no-expiry", "inspect", str(self.artifact))
    before = (self.mesh / "task-chains" / "no-expiry.json").read_bytes()
    self.append_invalid_blocked_revision()
    rebuilt = self.command("rebuild")
    self.assertIn("rebuild", rebuilt.stdout)
    self.assertEqual((self.mesh / "task-chains" / "no-expiry.json").read_bytes(), before)
```

- [ ] **Step 2: Run it red, implement only through Task 1 validator, then run green**

Run: `rtk proxy python3 tests/test-mesh-task-no-expiry.py`

Expected after Task 1: exit 0; the invalid historical record cannot overwrite the valid terminal cache.

- [ ] **Step 3: Verify deployed parity and an isolated fixture**

Run: `rtk proxy sha256sum scripts/mesh_task_log.py ~/.local/bin/mesh_task_log.py scripts/mesh-task ~/.local/bin/mesh-task`

Run: `rtk proxy python3 tests/test-mesh-task-log.py && rtk proxy python3 tests/test-mesh-task-no-expiry.py && rtk proxy scripts/mesh-task --test`

Expected: source/deployed pairs have equal hashes and all commands exit 0.

- [ ] **Step 4: Write the receipt**

Record the quarantined terminal-regression payload, the exact first terminal revision and artifact hash, focused command exit codes, source/deployed hashes, and the recovery action for the already-corrupted TG chain. Do not claim its recovery until replay/rebuild produces the original DONE state from valid evidence and an unrelated chain can append.
