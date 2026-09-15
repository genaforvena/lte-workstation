# AdFox research design audit — 2026-09-12

Task: `design-spec-task-sweep-20260907/audit-adfox` (owner `tg`; dispatch check exited 0 and owner-authored take succeeded).
Source: `docs/historical-ask-adfox-research-design-20260906.md`.
Disposition: the historical research question has substantial prior-art coverage; reconcile its evidence contract before considering any new collection.

## Findings

The source artifact was a design, not a report of completed research. Its requirements were: search existing Adint material first; then a bounded multi-placement, multi-date sample; preserve URL, retrieval time, query/profile conditions, field names, and a raw-response hash for every observation; separate observed values from identity/targeting inference; and report coverage, redactions, and uncertainty.

The prior-art search found a direct collision in the separate `/home/mesh-home/self-adint` project:

- `docs/step0f-adfox-cards-2026-08-21.md` states it tests the operator's AdFox hypothesis against captured wire data and puts Yandex's published `getLastBidsReceived()` interface first. It reports 20 paired ledgers from 2026-08-19–20, 23,202 request rows, 14 RU publishers, and two simultaneous arms. This is a direct match for the source's AdFox auction question and already supplies a bounded, multi-placement, multi-date investigation.
- The published analysis reports 1,110 `getBulk/v2` requests from 16 owner IDs, 1,093 decoded `bids` values, 1,259 entries across 29 bidder names, 11 priced entries, and substantial empty/error coverage. It explicitly limits its conclusion to page-visible browser data, rejects server-side-auction and other-person claims, and records access/prior-art holes and sampling limits.
- `data/adfox-cards-2026-08-21.json` and `data/yandex-vocab-2026-08-21.json` are derived summaries. Their SHA-256 values are respectively `129e08d982112eb4f69c1b4ef785c7e2cbe8dffca001c97566402472082276cd` and `cb27a7e59e0ed083e803417b77227063cb1e1c3e4fff69deb19f599241dad128`. The report SHA-256 is `3f875934394b079e6aacd67e162d1e66e06dd66b946df31160f1e9dc637282ca`.
- The analysis says its source ledgers are not published. The derived JSON preserves aggregate fields and some URL/arm summaries, but does not itself provide a per-observation URL + timestamp + query/profile + raw-response-hash manifest. Therefore this audit confirms the prior-art collision and substantive coverage, but does not claim the original design's per-observation evidence contract is fully reconciled.
- The existing `self-adint` tree is dirty (README, INDEX, report, and untracked task receipts at inspection); this audit made no changes there. Its inspected HEAD was `097b40f750aac248b4631a6364fea31708ed886d`.

The right disposition is no duplicate auction collection now. First reconcile whether the existing private ledgers contain the requested observation-level provenance, produce a privacy-preserving integrity manifest, and identify any material gap. Do not expose raw ledgers or identifiers in the shared board or this repository. Do not infer bidders' identities, people, or targeting from field names or absence. Any future collection must be a separately scoped successor with a bounded sample, explicit profile/query conditions, provenance hashes, redaction plan, and honest coverage/uncertainty; this audit does not authorize it.

## Evidence-gated work packages

The following two-step chain is registered in `docs/plans/2026-09-12-adfox-research-reconciliation.tsv` as `adfox-research-reconciliation-20260912`:

| Step | Owner | Gate and deliverable |
|---|---|---|
| `inventory-existing-evidence` | `adint` | Read-only audit of existing AdFox ledgers and derived files. Publish only a redacted manifest with file digests, row/schema counts, and a per-requirement completeness matrix. Do not collect new traffic or put raw rows/identifiers on the board. |
| `adfox-gap-disposition` | `tg` | After the manifest, decide whether existing evidence satisfies the original ask. If it does, close with a no-new-collection disposition. If a material gap remains, write an exact bounded successor design with its own provenance, privacy, and coverage gates; no collection occurs in this step. |

Neither step dispatches collection. A later collection task is warranted only if the second step documents a material unanswered question and a bounded, safe way to answer it.

## Verification and remaining obligation

- `mesh-task check dispatch design-spec-task-sweep-20260907/audit-adfox tg`: exit 0.
- `MESH_TASK_ACTOR=tg mesh-task take design-spec-task-sweep-20260907 audit-adfox`: claimed; subsequent invocation reported the exact step already active.
- Read-only review of the source design, `self-adint` AdFox analysis/index, derived JSON, project status, and data inventory; no collection was run and no external project file was edited.
- Remaining: the `adint` owner must complete the new evidence inventory; `tg` then records the gap disposition. The source corpus is private and its per-observation provenance has not been verified here.
