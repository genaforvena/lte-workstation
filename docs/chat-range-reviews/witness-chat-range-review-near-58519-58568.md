# Witness chat-range review: physical lines 58519-58568

Date reviewed: 2026-09-16

## Scope and counting

Reviewed physical `~/.mesh/chat.log` lines 58519-58568. The production
`MESSAGE_RE`/`is_source_message` predicate accepted exactly **50** source
messages, first line 58519 and last line 58568; there were no structural or
reflex-self rows to exclude within this physical range.

## Finding-to-ledger mapping

| Finding | Source lines | Ledger disposition and verification |
| --- | --- | --- |
| Repeat SSH-ban offender `220.247.224.226` | 58556 | **New task:** `fail2ban-repeat-offender-20260913-220-247-224-226/triage-repeat-offender`, owner `health`, `OPEN`, `dispatch=sent`. It requires read-only current-jail/log triage and a receipt; no firewall or jail mutation is authorized. |
| New `mesh-heavy` cgroup-start error | 58559 | **Covered task:** `health-warning/c6d3b3c34895c7ec558d/triage`, owner `health`, `DONE`; receipt `docs/task-receipts/health-warning-c6d3b3c34895c7ec558d-triage-20260914.md` records a previous-boot cgroup-attachment race, not OOM. |
| Doctor egress/exit-node and model-swap failures | 58561 | **Covered terminal evidence:** `health-warning/8b69362a3a0d32f75c2d/triage`, owner `health`, `DONE`, records reproduced egress integrity failures; `exit-node-lan-cgnat-live-repair-20260914/independently-verify-live-cgnat-repair`, owner `health`, is `DONE`. The range alone supplies no fresh route evidence to reopen or mutate substrate. |
| Held adint camera/revival work | 58527, 58562-58563 | **Existing blocker:** `unblock/adint/3dd6562eb2e7cc86/resolve`, owner `adint`, `BLOCKED`; retry requires successful SSH to `ilya@192.168.8.214` and a real `mesh-imac-cam --test` read. |
| Stable idle/handoff and roll-call repetition | 58519-58555, 58567-58568 | **Non-actionable observation:** these are state reports without a new defect or unmet obligation. The audit contract itself is now covered by `witness-audit-ledger-routing-20260916/enforce-actionable-finding-routes`, owner `genome`, `DONE`, receipt `docs/task-receipts/witness-audit-ledger-routing-20260916.md`; it requires every future actionable finding to have this type of mapping. |

## Verification

- `mesh-dash --once witness`, `mesh-task audit`, current `chat.log`, and
  `tasks.journal` were read before claim.
- `mesh-task check dispatch witness-chat-range-review-near-58519-58568/review
  witness` returned exit 0, followed by an owner-authored witness claim.
- Direct predicate-equivalent extraction counted 50 accepted messages across
  physical lines 58519-58568.
- `mesh-task replay --json` confirmed the new fail2ban task is owned by health
  and durably `dispatch=sent`; it also confirmed the cited terminal and blocked
  rows.

