# Idle-turn cost follow-through finding — 2026-09-11

## Evidence

- `mesh-task audit` passed at 383 total / 131 unfinished.
- `coordination-hledger-plan-20260908/communication-receipts` remains BLOCKED on a fresh operator inbound; witness-owned successors are correctly non-dispatchable.
- `~/.mesh/pane-consume.log` shows witness paid wakes at `12:53:26Z` and `13:23:31Z`, exactly one refractory interval apart, while intervening changes were repeatedly held by the 1800-second refractory.
- After the witness prediction was installed at `13:31:58Z`, the `13:32:31Z` change was correctly logged as fully predicted and held.
- `mesh-task queue --dispatch` nevertheless exposes exact-owner eligible rows, while recent idle handoffs do not provide an owner-authored `[taking]` transition. The existing prompt-delivery receipt explicitly stopped short of proving that transition.

## Finding

The prompt-only proactive pickup change proves instruction delivery but not task execution. Separately, an unchanged blocked/no-eligible state still pays a periodic turn when prediction expiry or the deaf guard meets the refractory boundary. This does not yet prove the requested outcome: tasks can remain eligible through an idle turn, and externally blocked lanes continue buying status-only turns.

Corrective chain: `idle-turn-cost-followthrough-20260911`.

## Independent pre-landing review

The first implementation revision correctly passed its focused test and deployed source/live SHA check, but did not yet meet the whole acceptance condition. With an absent expectation and no witness candidate, the real new interface returned:

```text
$ MESH_WAKE_EXPECT_DIR=/tmp/mesh-noexpect-witness-20260911 scripts/mesh-pane-consume --gate-check witness state=UP state=UP 0
WAKE:plain
```

Thus prediction expiry still spent a no-work wake; only the deaf-guard branch was suppressed. The initial symmetric candidate signature also treated eligible-to-empty disappearance as a wake edge, risking a follow-up idle turn after a successful take. Both cases were returned to the still-RUNNING genome owner at board time `2026-09-11T13:44:22Z`; witness verification remains queued.
