# Tiny Fleet operator-ideas reconciliation — 2026-09-12

## Verdict

The 2026-09-06 idea brief has no paired TSV in `docs/plans/`. Its proposals are not all covered by
the completed Tiny Fleet chains. The existing `docs/plans/tinyfleet-specialists.tsv` is the closest
plan, but it predates the enrichment: its `persona-and-code-plan` step is complete and its witness
step is complete, while the resulting small held-out sets do not establish corpus adequacy or the
new independent operator-style/code-culture boundary. The drift-methodology and 2026-09-12 expansion
chains cover parts of the project-DNA measurement method, but neither evaluates the proposed
same-base, across-snapshot 360M fossil experiment.

I created a six-step successor plan at `docs/plans/2026-09-12-tinyfleet-operator-ideas.tsv` and
registered it as chain `tinyfleet-operator-ideas-20260912`. Existing chains and historical receipts
remain unchanged. No model, corpus, training run, or route was changed in this audit.

## Proposal-by-proposal disposition

| Idea brief proposal | Current evidence/task | Reconciliation |
|---|---|---|
| Reproduce the exact BbyWVY-360M baseline with pinned identity and resource/latency record | `tinyfleet-specialists/audit-current-repo` closed with a 2026-09-06 non-reproduction: training dependencies/model run were absent and no download was started. The later `persona-and-code-plan` used pinned `HuggingFaceTB/SmolLM2-360M-Instruct`, a distinct model artifact. | Keep the old negative result; create `verify-bbywvy-baseline`. It must either produce the requested baseline artifact or an explicit typed block/failure. Do not infer BbyWVY reproduction from the separate SmolLM2 run. |
| Measure corpus and build disjoint operator-style and code-culture specialists | `tinyfleet-specialists/persona-and-code-plan` measured 815 Telegram rows and a code snapshot and planned separate persona/code artifacts; `verify-persona-and-code` reports separate adapters. But the plan allows mesh vocabulary in persona, the held-out sets are only four rows each, and no source/time independence or minimum adequacy result is established in the inspected witness receipt. | Do not retire the prior run. Add `reconcile-persona-code-evidence` to test the existing artifacts against the stricter separation and adequacy gates. It must publish `data-adequate` or `insufficient-data`; training stays conditional on that result. |
| Compare codebase “fossils” across pinned project snapshots using identical 360M controls | `tinyfleet-drift-methodology` is complete, while its study is blocked on external repository/license inputs and its roadmap proposes a temporal/generalization extension. `tinyfleet-expansion-20260912` covers structural/lexical and behavioral controls, but not the exact paired 360M base/retrieval/genuine-update snapshot comparison. | Reuse the expansion chain's manifests, fixtures, and controls; add `paired-project-dna-snapshots`, gated on the baseline and expansion's behavior/Lora preflight. Preserve blocked arms and raw outputs. |
| Select the smallest practical replacement candidate and shadow-test before routing | The completed specialist chain wired a mood pool and witness-verified fallback, but no inspected artifact ranks sound or another lane using narrowness/safety/fallback/cost, and the idea brief explicitly makes sound provisional. | Add `rank-and-shadow-replacement-lane`. It publishes route/hold/reject from evidence and has no routing mutation in scope. |
| Compare 1B/1.5B Linux-trained models only after 360M evidence | The prior promise says start with the shared 360M base; the drift roadmap includes snapshot extension but no capacity ladder or current-roster check. | Add `capacity-ladder-after-360m`, hard-gated on the 360M baseline and paired snapshot evidence. No evidence means a recorded block, not a larger-model substitution. |

No proposal is retired as irrelevant. The known overlaps are reuse points, not proof that the new
acceptance criteria have already passed. No new operator decision is required: the live operator
instruction says to choose Tiny Fleet inputs autonomously and record the choices/reasons; these tasks
retain that authority while keeping evidence gates explicit.

## Live-state checks and verification

- `mesh-task status tinyfleet-specialists`: complete (12/12); the persona/code plan and independent
  verification are complete, but the recorded evaluation contains four held-out rows per specialist.
- `mesh-task status tinyfleet-drift-methodology`: complete (7/7); the study status remains blocked,
  with one resolved repository and a failing six-duplicate leakage control in snapshot B.
- `mesh-task status tinyfleet-expansion-20260912`: open (0/5); its report says LoRA/QLoRA is blocked
  and keeps the study pilot-only.
- Read the source brief, its closest specialist plan, the persona/code plan and witness receipt, the
  deep-evaluation contract, current study status/roadmap, and the live task-chain summaries above.
- Confirmed no adjacent `tinyfleet-operator-ideas-20260906.tsv` exists under `docs/plans/`; the new
  plan above supplies explicit follow-through for uncovered criteria.

The successor chain is open (0/6) and its first row is
`tinyfleet-operator-ideas-20260912/verify-bbywvy-baseline`. The task descriptions spell out each
prerequisite. I attempted to encode those as `mesh-task wait-for` edges, but the ledger rejected the
write with `exact owner required: task owner=genome actor=tg`. I did not impersonate genome or
reassign its implementation work. Genome must add the corresponding ledger wait-for edges while
acting as the exact owner before taking later rows; until then, the task descriptions are the
available gate and the first row remains the intended next action.
