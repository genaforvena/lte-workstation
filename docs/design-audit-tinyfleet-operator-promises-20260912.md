# Tiny Fleet operator-promises reconciliation — 2026-09-12

## Verdict

`docs/plans/tinyfleet-operator-promises-20260906.md` has no paired TSV. The nearest plan is
`docs/plans/tinyfleet-specialists.tsv`; its `tinyfleet-specialists` chain is marked complete (12/12),
but that status closes the listed implementation and witness steps, not every original operator
promise. The eight statements below reconcile to their closest chain rows, recorded artifacts,
owners, and remaining obligations. The old chain and receipts remain unchanged.

State tags describe the original promise: `[DONE]` means the bounded request has direct evidence;
`[PARTIAL]` means related work exists but a stated criterion remains unproved; `[OPEN]` means the
promise has no satisfying result yet. A ledger row marked `done` is not by itself proof that the
broader promise is done.

## Promise-by-promise audit

| Source promise | Closest task row(s), owner, and artifact | Reconciliation |
|---|---|---|
| Inspect and test `StarpowerTechnology/BbyWVY-360m` (03:01:11) | `tinyfleet-specialists/audit-current-repo` — genome — [`audit-current-repo-2026-09-06.md`](/home/mesh-home/tiny-fleet/docs/audit-current-repo-2026-09-06.md) | **[OPEN]** The audit explicitly records that the model/runtime dependencies were absent and no reproduction or download was attempted. Its task is done as an audit, not as a model test. `tinyfleet-operator-ideas-20260912/verify-bbywvy-baseline` is open, owner genome. |
| Determine whether one or three tiny models can replace an existing mesh means (04:05:42) | No completed row or artifact ranks one-vs-three replacements. New follow-up: `tinyfleet-promise-gaps-20260912/resolve-model-count-replacement` — genome. | **[OPEN]** The completed mood-pool wiring and the operator-ideas rank/shadow task do not settle the requested model count. The new follow-up asks for a bounded comparison and forbids routing changes. |
| Choose the first replaceable job from mesh context; sound was only a hypothesis (04:09:44) | `tinyfleet-specialists/wire-mood-pool` — genome — [`coordination-wire-mood-pool-20260907.md`](coordination-wire-mood-pool-20260907.md); `verify-mood-pool` — witness — [`coordination-verify-mood-pool-20260907.md`](coordination-verify-mood-pool-20260907.md) | **[PARTIAL]** A guarded Tiny Fleet pool was exercised with guitar/sourdough adapters and fallback/abstention evidence. That does not establish which mesh job is the best replacement or compare it with sound. The open `rank-and-shadow-replacement-lane` row is the required selection evidence. |
| Sentiment need not be the only specialist; use accumulated chat/log data (04:15:35) | `mood-corpus` — genome — [`mood-corpus-2026-09-06.md`](/home/mesh-home/tiny-fleet/docs/mood-corpus-2026-09-06.md); `persona-and-code-plan` — genome — [`persona-and-code-plan-2026-09-07.md`](/home/mesh-home/tiny-fleet/docs/persona-and-code-plan-2026-09-07.md); witness row — witness — [`coordination-verify-persona-code-20260907.md`](coordination-verify-persona-code-20260907.md) | **[PARTIAL]** There is evidence for more than sentiment: a code specialist was trained, and the mood corpus contains 36 train, 8 held-out, and 4 adversarial redacted semantic cases from the operator-mood ledger. The persona/code plan measured 815 Telegram records, but its witness reports only 12/10 training rows and four held-out rows per domain. This does not establish adequate use of the accumulated chat/log material. `tinyfleet-operator-ideas-20260912/reconcile-persona-code-evidence` is open, owner genome. |
| Start from the operator's spoken material to capture his style (04:17:43) | `persona-and-code-plan` — genome — [`persona-and-code-plan-2026-09-07.md`](/home/mesh-home/tiny-fleet/docs/persona-and-code-plan-2026-09-07.md); `verify-persona-and-code` — witness — [`coordination-verify-persona-code-20260907.md`](coordination-verify-persona-code-20260907.md); new follow-up `tinyfleet-promise-gaps-20260912/reconcile-spoken-style-source` — genome. | **[PARTIAL]** The measured source was `~/.mesh/tg-corpus.jsonl` (815 Telegram records); the plan explicitly excludes voice recordings and says voice transcription is future work. A persona adapter and small held-out evaluation exist, but neither proves a spoken-material run or corpus adequacy. The new follow-up resolves the source gap without publishing raw private material; `reconcile-persona-code-evidence` separately checks corpus adequacy. |
| Try a specialist trained on the mesh codebase and inspect what it learns (05:56:46) | `persona-and-code-plan` — genome — [`persona-and-code-plan-2026-09-07.md`](/home/mesh-home/tiny-fleet/docs/persona-and-code-plan-2026-09-07.md); `verify-persona-and-code` — witness — [`coordination-verify-persona-code-20260907.md`](coordination-verify-persona-code-20260907.md) | **[DONE]** The bounded trial produced a separate code adapter from the measured lte-workstation snapshot and a cross-domain held-out result; the witness records the pinned base, adapter, and evaluation artifact hashes. Its four held-out rows remain a limitation on strength, not absence of the requested trial. |
| Use the shared SmallLM2 360M base first, not a 1B model (05:59:28) | `mood-lora-bench` — genome — [`coordination-mood-lora-runtime-rerun-20260907.md`](coordination-mood-lora-runtime-rerun-20260907.md); `verify-persona-and-code` — witness — [`coordination-verify-persona-code-20260907.md`](coordination-verify-persona-code-20260907.md) | **[DONE]** The recorded mood run uses the shared SmolLM2 360M base; the persona/code witness records `HuggingFaceTB/SmolLM2-360M-Instruct` at pinned revision `a10cc1512eabd3dde888204e902eca88bddb4951`. No 1B substitution is claimed. |
| The compelling use is a compressed fossil of project idioms and conventions (06:11:15) | `persona-and-code-plan` and `verify-persona-and-code`, above; proposed successor `tinyfleet-operator-ideas-20260912/paired-project-dna-snapshots` — genome. | **[PARTIAL]** The code specialist is a bounded fossil of one measured repository snapshot, with a separate adapter and held-out output. It does not test across pinned project snapshots with identical controls; the paired-snapshot task is open. |

## Verification performed

- `mesh-task status tinyfleet-specialists` — complete (12/12); recorded owners and artifacts checked
  against the plan and receipts cited above.
- `mesh-task status tinyfleet-operator-ideas-20260912` — open (1/6); baseline, persona/code
  reconciliation, paired-snapshot, and replacement-ranking follow-ups remain open under genome.
- `docs/plans/2026-09-12-tinyfleet-promise-gaps.tsv` registers two additional exact-owner follow-ups
  for the original model-count and spoken-style-source gaps; the model-count question is distinct
  from the existing lane-ranking task.
- `mesh-task status tinyfleet-promise-gaps-20260912` — chain is open; both follow-ups are open and
  owned by genome.
- Confirmed that the named promise Markdown exists and that no
  `docs/plans/tinyfleet-operator-promises-20260906.tsv` exists; the specialists TSV is the only
  paired implementation plan identified for the completed `tinyfleet-specialists` chain.

No model, corpus, or route was changed during this reconciliation. The original chain's terminal
state remains intact; unresolved promises stay explicit in the successor chain rather than being
silently relabelled complete.
