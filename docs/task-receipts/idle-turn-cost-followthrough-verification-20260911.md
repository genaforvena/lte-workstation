# Idle-turn cost follow-through verification — 2026-09-11

Verdict: **FAIL / REJECT**

Task: `idle-turn-cost-followthrough-20260911/verify-task-aware-idle-gate`

## Evidence that passes

- Owner-authored start exists at `2026-09-11T13:37:00Z`; dispatch was not mistaken for start.
- Focused regression `tests/test-mesh-pane-consume-task-aware-idle-gate.sh` exits 0.
- Existing `scripts/mesh-pane-consume --test` exits 0.
- Source and deployed executable match at SHA-256 `c43262f3835832bca7e714c22f3db5869496653876590863eb0e109b46b5713e`.
- Commit `7d18ad5a` contains the `scripts/mesh-pane-consume` change.

## Release-blocking failures

1. The explicit prediction-expiry acceptance case fails against the landed executable. With no expectation file and no eligible witness task, the real gate returns a paid plain wake:

   ```text
   $ MESH_WAKE_EXPECT_DIR=/tmp/mesh-noexpect-witness-20260911 scripts/mesh-pane-consume --gate-check witness state=UP state=UP 0
   WAKE:plain
   ```

   `task_aware_gate_decision` only converts `WAKE:deaf` to `HOLD:no-eligible`; it leaves `WAKE:plain` unchanged. Therefore an unchanged blocked/no-eligible task state still buys a recurring turn solely when prediction TTL expires, contrary to the task contract.

2. Candidate signature changes are symmetric in the landed loop. Any `cur_task_sig != prev_task_sig` becomes `WAKE:surprise:task`, so eligible-to-empty disappearance after an owner takes a task is also a wake edge. The required directional proof (empty-to-eligible wakes; eligible-to-empty does not buy a follow-up owner turn) is absent.

3. The landing commit contains only `scripts/mesh-pane-consume`. The claimed red-first regression and implementation receipt remain untracked, so the committed artifact does not carry its own regression or durable receipt.

The generic smoke and focused green test do not cover failure 1 or 2 and therefore cannot support completion. A corrective implementation must add red/green arms for expired/absent expectation with no candidate and directional candidate transitions, update the receipt, deploy, and land code plus tests/receipt before independent re-verification.
