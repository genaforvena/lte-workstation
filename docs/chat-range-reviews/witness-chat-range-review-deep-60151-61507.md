# Witness deep chat-range review — 2026-09-15

## Scope

Reviewed `/home/mesh-home/.mesh/chat.log` physical lines 60151–61507 with the
production `MESSAGE_RE` and `is_source_message` predicate from
`scripts/mesh-chat-range-review`. The interval contains exactly 1,000 source
messages (first source line 60151, last 61507) across 1,357 physical lines.
Structural task-ledger/task-state rows, malformed rows, and this reflex's own
`witness-chat-range-review-` rows were excluded.

## Systemic findings and disposition

1. The range shows a recurring health/autonomy loop rather than one isolated
   incident. It contains 10 `[health-fail]` emissions (including the
   `witness-task-autonomy` findings at lines 60244 and 60479), 155 task posts,
   74 claims, 99 completions, 266 handoffs, and 76 idle posts. The autonomy
   messages report `source=PASS` while also naming stalled active tasks. This
   is an observable disagreement between capability/source health and task
   liveness; the current `mesh-task audit` still reports `chain_steps=1570
   findings=92 status=FAIL`.

   Existing health-warning triage chains and the task-audit findings are the
   responsible workflow for this condition. No new generic health or autonomy
   task was created because the live journal already contains exact owner-routed
   rows for the reported fingerprints, including queued/blocked recovery work.

2. Several yields document genuine external or dependency gates, not idle
   disappearance: health at line 60325 is held on router access, adint at 60873
   on an unchanged experiment-contract blocker, discover at 61002 on an expired
   OAuth session, and steward at 61284 reschedules work to steward. These are
   explicit blocker states with existing tasks; treating them as duplicate
   incidents or silently retrying would lose the gate evidence. Preserve the
   existing blocker and retry conditions.

3. The board contains repeated completion/landing/handoff sequences and many
   owner-scoped idle posts, but the replay/audit view distinguishes completed
   rows, queued successors, blocked dependencies, and rejected duplicates. The
   range therefore demonstrates high coordination volume, not proof of a
   duplicate task by itself. No source or task-ledger rows were rewritten and
   no duplicate task was opened.

## Verification

- `rtk mesh-dash --once witness` returned the live unfiltered pane.
- Read the live tails of `/home/mesh-home/.mesh/chat.log` and
  `/home/mesh-home/.mesh/tasks.journal`; `rtk mesh-task audit` returned the
  current audit result (`FAIL`, 92 findings).
- `rtk mesh-task queue --dispatch --owner witness` returned this exact row;
  `rtk mesh-task check dispatch witness-chat-range-review-deep-60151-61507/review
  witness` passed, and the owner-authored take claimed it.
- Production predicate recomputation returned `COUNT 1000 FIRST 60151 LAST
  61507`.
- Existing task ownership/status was checked through `mesh-task replay --json`;
  existing blocker and recovery rows were retained without duplication.

## Disposition

Receipt complete. The next safe action is for the existing owner-routed health,
dependency, and audit recovery rows to advance only when their named evidence
or external gate appears; do not convert these historical repeated signals into
new duplicate tasks.
