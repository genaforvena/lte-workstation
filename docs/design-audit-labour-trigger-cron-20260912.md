# Labour trigger-vs-cron audit — 2026-09-12

Task: `design-spec-task-sweep-20260907/audit-labour-trigger-cron`  
Source: `docs/labour-audit-trigger-vs-cron-2026-07-24.md`  
Disposition: all findings reconciled; no new follow-up task created.

## Findings and dispositions

1. **The 17% idle-flagged result is not a cron-burn rate.** The source audit traced five
   flags to two false positives (pane/git work absent from the board proxy and an 8-minute
   timestamp offset) and three near-boundary liveness ticks. Preserve the 25/30 paired count
only as a one-window historical observation. It does not support a fleet-wide rate or a
current measurement task; the original sample was small, minute-granular, and from one
quiet five-hour window.

2. **Board proximity is not a complete turn-output record.** This remains a methodological
limit, not a repair request: a board-only match can miss code work and mispair delayed posts.
No current claim should use it alone to classify a turn as idle.

3. **The proposed output-based idle detector is explicitly declined as superseded and
unidentifiable from the available evidence.** The later corrective work addresses the
operational failure directly: `mesh-pane-consume` holds unchanged no-candidate state across
absent or expired predictions, wakes for newly eligible exact-owner work, and retains wakes
for genuinely unpredicted changes. A retrospective union of commits and board posts would
still be an incomplete output inventory and cannot identify whether a wake came from cron
or an event without a recorded wake-source field. Building such a classifier from the July
snapshot would therefore risk presenting an attribution guess as a measurement.

4. **The low-yield periodic-wake case has a current corrective artifact.** The completed
`idle-turn-cost-followthrough-correction-20260911` chain records the behavior, regression,
deployment, and independent verification in:
   - `docs/task-receipts/idle-turn-cost-followthrough-correction-implementation-20260911.md`
   - `docs/task-receipts/idle-turn-cost-followthrough-correction-verification-20260911.md`

   This audit reran `bash tests/test-mesh-pane-consume-task-aware-idle-gate.sh` and
   `bash scripts/mesh-pane-consume --test`; both passed. Current source and installed
   `~/.local/bin/mesh-pane-consume` have identical SHA-256:
   `c84d8b3dc49a17b547afb8e52f49ce3a43d23227c0df3dd8883d9ffd426253d9`.
   The focused test file was already modified in the worktree at audit time; it was not
   changed by this audit, and the current contents passed.

## Closure

The historical board-correlation result stays explicitly non-causal. Its proposed detector
is declined for the reasons above; the actionable no-work wake issue is already covered by
the later corrective chain and verified live. No duplicate implementation or measurement
task is warranted from this source artifact.
