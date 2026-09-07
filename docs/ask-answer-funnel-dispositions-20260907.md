# Ask→answer funnel disposition — 2026-09-07

Source: `docs/superpowers/specs/2026-07-15-ask-answer-funnel-design.md`.

The audit is complete at disposition level; implementation remains open and is admitted in
`ask-answer-funnel-implementation-20260907`.

| unit | disposition | evidence / next task |
|---|---|---|
| 1 explicit task/claim key | DONE | [unit-1 evidence](ask-answer-funnel-unit-1-explicit-key-20260907.md): explicit `task:<id>` survives task/dispatch/claim/claim-done/done joins; red-before-green and real-parser verification recorded |
| 2 delete inference scar tissue | OPEN | depends on Unit 1; remove only after regression corpus proves legacy rows render UNKNOWN |
| 3 witness resolution axis | OPEN | current `mesh-witness` search found no `ask_open`/`ask_resolve` implementation; add artifact-backed counters |
| 4 dispatch pane resolution view | OPEN | current `mesh-dash` search found no implemented resolution axis; add UNKNOWN-safe rendering after Unit 3 |
| 5 board canary | DEFERRED | explicitly sequenced after Units 1–4; no synthetic ask should run now |

No unit is falsely marked complete. Verification used direct source inspection and the existing
keyed claim implementation (`scripts/mesh-claim`); this is a disposition artifact, not a claim that
the funnel is implemented.
