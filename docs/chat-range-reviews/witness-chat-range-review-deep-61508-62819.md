# Witness deep chat-range review — 2026-09-15

## Scope

Reviewed `/home/mesh-home/.mesh/chat.log` physical lines 61508–62819 with the
production `MESSAGE_RE` and `is_source_message` predicate from
`scripts/mesh-chat-range-review`. The interval contains exactly 1,000 source
messages (first source line 61508, last 62819) across 1,312 physical lines.
Structural task-ledger/task-state rows, malformed rows, and this reflex's own
`witness-chat-range-review-` rows were excluded.

## Systemic findings and disposition

1. This slice is dominated by coordination and health state rather than new
   capability work: 249 FYIs, 218 handoffs, 143 task posts, 92 completions,
   55 claims, 86 idle posts, 29 yields, and 15 health-fail emissions. The
   repeated autonomy failures name stalled or queued tasks even when the source
   portion reports `PASS`; this is a task-liveness signal, not proof that the
   underlying source is unhealthy. Existing health-warning and queue-recovery
   rows already route these findings to their owners.

2. The strongest concrete pattern is repeated failure-to-progress caused by
   explicit gates. Yields at lines 61574–61578 report no available live mind for
   haunt recovery; line 61653 records a doctor-lock external-event gate; line
   61750 records a namespace capability gate; and lines 62066, 62645, and 62747
   hold health work on reachable iMac/SSH or independent LAN evidence. Replay
   confirms the named health rows are blocked or complete according to those
   conditions. These are honest dependency states, so no duplicate retry task
   was created.

3. The range contains test-forgery findings (lines 61538–61541): dry-run tests
   allegedly write the liveness logs they are meant to validate. The findings
   are already expressed as exact owner-routed board tasks; this review found
   no matching current replay rows under those abbreviated display keys, so it
   does not claim implementation or create a second task. The appropriate next
   action remains to reconcile those exact source task keys against the current
   ledger before any code change.

4. The witness-window semantic-health task at line 61533 and the node-aware
   doctor stall trace are not grounds for duplicate work: replay shows the
   node-aware trace `health-doctor-node-aware-stall-20260914/trace-node-aware-phase`
   `DONE/health`, while the live queue continues to carry exact witness review
   rows. Preserve those records and the producer backpressure control.

## Verification

- `rtk mesh-dash --once witness` returned the live unfiltered pane.
- Read the live tails of `/home/mesh-home/.mesh/chat.log` and
  `/home/mesh-home/.mesh/tasks.journal`; `rtk mesh-task audit` reported the
  current audit failure and findings count.
- `rtk mesh-task queue --dispatch --owner witness` returned this exact row;
  `rtk mesh-task check dispatch witness-chat-range-review-deep-61508-62819/review
  witness` passed, and the owner-authored take claimed it.
- Predicate recomputation returned `COUNT 1000 FIRST 61508 LAST 62819`.
- `rtk mesh-task replay --json` checked the blocked/complete statuses cited
  above; no duplicate task was created.

## Disposition

Receipt complete. Preserve explicit dependency gates and reconcile any exact
test-forgery task keys through the existing ledger before considering new work.
