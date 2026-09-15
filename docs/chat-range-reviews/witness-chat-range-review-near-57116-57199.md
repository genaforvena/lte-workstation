# Witness near chat-range review — 2026-09-15

## Scope

Reviewed `/home/mesh-home/.mesh/chat.log` physical lines 57116–57199 with the
production `MESSAGE_RE` and `is_source_message` predicate from
`scripts/mesh-chat-range-review`. The interval contains exactly 50 source
messages (first source line 57116, last 57199). Structural task-ledger/task-state
rows, malformed rows, and this reflex's own `witness-chat-range-review-` rows
were excluded.

## Findings and disposition

1. The slice contains repeated health and autoland coordination, but the exact
   health-warning rows have owner-authored receipts and the autoland rows are
   explicit genome follow-ups. Replay distinguishes those completed steps from
   their open landing successors; no duplicate health or landing task was
   created.

2. Lines 57137, 57153, and 57172 consistently record the unresolved route
   condition: `100.76.0.1` is captured by `tailscale0`/table 52 while VPN repair
   steps remain gated. Line 57172 explicitly retains this as a known condition
   with no substrate mutation. The existing `exit-node-lan-cgnat-repair-20260912`
   successor chain is the correct owner-routed follow-up; this review did not
   reopen or duplicate it.

3. The line-57070 sweep claim of `OPEN_UNOWNED=0` is historical and does not
   conflict with the later current dash, which shows newly accumulated open
   witness rows. The three idle posts are explicit owner-queue outcomes, not
   silent loss of work.

## Verification

- `rtk mesh-dash --once witness` returned the live unfiltered pane.
- Read live tails of `/home/mesh-home/.mesh/chat.log` and
  `/home/mesh-home/.mesh/tasks.journal`; `rtk mesh-task audit` ran and reported
  the current audit state.
- `rtk mesh-task queue --dispatch --owner witness` returned this exact row;
  `rtk mesh-task check dispatch witness-chat-range-review-near-57116-57199/review
  witness` passed, and the owner-authored take claimed it.
- Predicate recomputation returned `COUNT 50 FIRST 57116 LAST 57199`.
- `rtk mesh-task replay --json` confirmed the cited completed health rows and
  existing route successors; no duplicate task was created.

## Disposition

Receipt complete. Preserve the existing route-repair and autoland successors;
do not repeat completed warning triage.
