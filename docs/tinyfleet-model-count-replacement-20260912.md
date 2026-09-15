# Tiny Fleet model-count replacement decision — 2026-09-12

## Verdict: BLOCKED — no replacement count is supported

The 2026-09-03 04:05:42 promise asks whether one or three tiny models could replace one
existing mesh means. The available artifacts do not identify a specific mesh lane that a tiny
model can safely replace, and they contain no paired comparison of one-model and three-model
configurations on that lane. Therefore the evidence supports neither count: **0 replacements
are currently justified**. This is an evidence block, not a finding that either design cannot work.

## What is actually available

| Candidate evidence | Observed artifact | What it establishes | What it does not establish |
|---|---|---|---|
| SmolLM2-360M-Instruct + `lora-guitar` and `lora-sourdough` | `docs/coordination-wire-mood-pool-20260907.md`; adapter hashes `68697b792b847d53945b43f502802735fb9243630c609cae16ef21f00505ebc1` and `ca02ca12cd773003a5b45be6f1a9fbf9dc10a614302f1723e3078f491cdd25be` | One shared 360M base with two verified adapter artifacts; guarded relay smoke, pool-0 fallback, and terminal abstention were exercised. | This is **one base plus two adapters**, not evidence for three independent models. Guitar/sourdough fixtures do not select or validate an existing mesh means as a replacement target. No one-vs-three shadow comparison was run. |
| `StarpowerTechnology/BbyWVY-360m` | `/home/mesh-home/tiny-fleet/docs/task-receipts/tinyfleet-operator-ideas-verify-bbywvy-baseline-20260912.md`; revision `154a243ffa13d3259a824c40a23d709d3ea42fa7`, weights SHA-256 `3e26b40ed65c3fcd53e2930c38e3c9b9a5912389e0a6924f047cafa8eaa68c14` | Exact 361,821,120-parameter model loaded and produced real GPU inference; baseline is available. | Its receipt explicitly limits the run to an inference/latency smoke, not completion-quality scoring. It does not test replacement of a mesh lane or a three-model configuration. |
| SmolLM2 persona/code adapters | `/home/mesh-home/tiny-fleet/adapters/persona-code-persona/` and `persona-code-code/`; reconciliation in `docs/design-audit-tinyfleet-operator-ideas-20260912.md` | Adapter directories exist on the shared base. | The operator-ideas audit found four held-out rows per specialist and unresolved provenance/source-time independence and corpus-adequacy gates. They are not eligible replacement evidence yet. |
| Mood-specific adapter | `docs/coordination-wire-mood-pool-20260907.md` | The verified live pool inventory names guitar and sourdough adapters. | No separate `lora-mood` weight is evidenced; the mood-pool label does not prove a third specialist. |

## Reconciliation with lane ranking

`tinyfleet-operator-ideas-20260912/rank-and-shadow-replacement-lane` is still open. Its plan
(`docs/plans/2026-09-12-tinyfleet-operator-ideas.tsv`) gates ranking and shadowing on
`reconcile-persona-code-evidence` and `paired-project-dna-snapshots`. The live chain status on
2026-09-12 reports only `verify-bbywvy-baseline` done (2/6 steps overall); those two prerequisites,
the rank/shadow step, and the independent review remain open. The operator-promises reconciliation
(`docs/design-audit-tinyfleet-operator-promises-20260912.md`) likewise marks the model-count promise
open and the first replaceable job partial. Thus the rank/shadow lane cannot currently supply the
missing target selection or comparison.

## Decision and next evidence

- Do not recommend one model, three models, or a route change from the present evidence.
- Keep the existing mesh path authoritative; this artifact changes no routing or runtime behavior.
- Resume the evidence chain in order: finish persona/code corpus and split reconciliation; complete
  the paired-snapshot controls; then rank actual mesh lanes and shadow the selected eligible 360M
  specialist against the current path. Only after that comparison should a one-vs-three count be
  tested on the same frozen cases and cost measures.

Sources checked: the original promise at `~/.mesh/voice-in.log:1173` (2026-09-03T04:05:42Z),
the current operator-promises and operator-ideas reconciliation artifacts cited above, the mood-pool
implementation/verification receipt, the BbyWVY baseline receipt, and live `mesh-task status`
for `tinyfleet-operator-ideas-20260912` and `tinyfleet-promise-gaps-20260912`.
