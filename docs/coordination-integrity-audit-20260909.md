# Coordination integrity audit — 2026-09-09

## Verdict

Correction at 17:54 UTC: the PASS below covers structural consistency only.
It does not prove dispatch liveness. Twenty-five queued rows are successors of
REJECTED chain heads, rather than live blocked steps. See
`docs/dispatch-rejected-successors-20260909.md` and corrective chain
`dispatch-rejected-successors-20260909`. Full flow acceptance remains open.

PASS for the active structured-task flow. No current task is simultaneously marked delivered and
still open without an owner receipt; no audit findings or malformed task rows were found.

## Checks

- `mesh-task audit`: 339 rows — 169 `DONE`, 26 `REJECTED`, 23 `BLOCKED`, 121 `QUEUED`,
  `findings=0`.
- Current structured chains: 23 nonterminal current steps; all have an owner; zero
  `dispatch=sent` + current-step `status=open` rows without a receipt.
- `mesh-task-journal`: source replay PASS, 42,309 events, atomic materialization intact.
- Task lifecycle, single-writer, ledger-sync, dispatch-receipt, final-delivery, and no-pace
  regression checks pass.
- `mesh-promises --check`: hledger parity PASS; promise replay agrees at 92 open, claims agree at
  136, holds agree at 59, and ask agreement passes.
- Live staffing exposes seven eligible idle windows (`adint`, `haunt`, `hire`, `job`, `senses`,
  `wake`, `witness`); protected, communication, and actively-owned windows remain excluded.

## Coordination boundary

The zero claimable-task queue is honest: the 23 current unfinished steps are blocked by named
dependencies/operator events, while 121 successors are queued behind them. The promise ledger has
two intentionally human-owned/unrouted obligations (`ilya-back-online-push-restore-env` and
`phone-authorized-keys-recheck`); `mesh-promises --check` reports them as non-roster liabilities.
They must not be silently reassigned to an automated mind.

## Next action

Re-run this audit after a prerequisite event or a new owner-authored `[taking]`/`[done]` transition.
Do not create synthetic work to fill the currently empty claimable queue.
