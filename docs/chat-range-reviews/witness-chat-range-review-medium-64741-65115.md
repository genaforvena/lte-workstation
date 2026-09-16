# Witness review: physical lines 64741-65115

Task: `witness-chat-range-review-medium-64741-65115/review`  
Reviewed: 2026-09-16

## Scope

The production `MESSAGE_RE`/`is_source_message` predicate accepted exactly
**250** source messages from the 375 physical lines: first 64741, last 65115.
Structural `[task-state]`/`[task-ledger]` rows and reflex-self records were
excluded.

## Finding-to-ledger mapping

| Finding | Source lines | Ledger disposition and verification |
| --- | --- | --- |
| Repeat SSH-ban offender `159.223.225.140` | 64813 | **New task:** `fail2ban-repeat-offender-20260914-159-223-225-140/triage-repeat-offender`, owner `health`, `OPEN`, `dispatch=sent`. It requires a read-only log/current-jail disposition and receipt. |
| Shared-routing shadow evaluation must wait for real sample/time | 64760 and related follow-ups | **Existing blocker:** `self-review-routing-shadow-20260914/independently-evaluate-routing-shadow`, owner `witness`, `BLOCKED`; retry is after 2026-09-28 with 100 eligible tasks, otherwise terminal INCONCLUSIVE by 2026-10-14. The dependent adint rows are correctly queued behind it. |
| Repeated adint-resolver stalled alerts | 65017-65084, 65102 | **Covered terminal work:** `unblock/adint/9408d7f1f2f1225b/resolve`, owner `adint`, `DONE`; `health-warning/15755129219ff9786706/triage` is `DONE`, and `health-warning/dd1bf1d17c52d3cf8b0d/triage` plus `health-warning/bda387090d56d133ce40/triage` are evidence-backed `REJECTED` duplicates. No duplicate health task was created. |
| Parked Phaedra autostash blocks autoland | 64864, 65053 | **Covered terminal work:** `phaedra-autostash-steward-disposition-20260915/review-parked-object`, owner `steward`, `DONE`, artifact `docs/task-receipts/phaedra-autostash-steward-decision-20260915.md`; later `land-parked-autostash-20260915/fix-stale-autostash-alarm` is also `DONE`. Do not replay or drop user work from this review. |
| Doctor recovery and board-silence measurement limits | 64852, 64939 | **Non-actionable:** doctor reports `RECOVERED — 0 FAIL`; Phaedra board silence explicitly reports MESH-wide `UNKNOWN` because the feed is node-local and peers are stale. Neither provides a new failed obligation or safe substrate action. |
| Idle/handoff density | 64749-65115 | **Non-actionable:** 18 idle and 59 handoff rows are state reporting, not defects by themselves. The audit contract requiring a ledger disposition for any future actionable finding is implemented and verified by `witness-audit-ledger-routing-20260916/enforce-actionable-finding-routes`, owner `genome`, `DONE`, receipt `docs/task-receipts/witness-audit-ledger-routing-20260916.md`. |

## Verification

- `mesh-dash --once witness`, current `chat.log`, `tasks.journal`, and
  `mesh-task audit` were read before action.
- Canonical replay showed the prior near review complete while the disposable
  journal was stale; `mesh-task rebuild` corrected that row to `DONE`.
- `mesh-task check dispatch witness-chat-range-review-medium-64741-65115/review
  witness` returned exit 0 before the owner-authored claim.
- An independent worker was started for the range scan but returned no usable
  conclusion; its report was not relied on. The mappings above were checked
  directly against canonical replay and `tasks.journal`.
- Canonical replay confirms the new fail2ban task is health-owned and
  `dispatch=sent`.

