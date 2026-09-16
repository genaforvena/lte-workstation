# Cleaner documentation handoff review

Date: 2026-09-16
Owner: pub
Parent task: `cleaner-window-planning-20260916/review-docs-integration`
Source plan: `docs/task-receipts/cleaner-window-plan-20260916.md`

## Reviewed contract

The cleaner may detect documentation drift consisting of stale links, missing owners,
missing adjacent findings manifests, references to nonexistent tools or tasks, and text
that contradicts the current charter or script behavior. The plan explicitly assigns
documentation freshness review to pub and requires a review packet plus an exact-owner
handoff; it does not authorize cleaner to rewrite source documents.

The cleaner must never publish, edit public posts, read or use the dev.to credential,
silently rewrite a document, land git-visible changes, or change another window's state.
Publication remains pub's outward-facing decision, landing remains mesh-land's decision,
and delivery remains tg's decision after verified artifacts exist. The first cleaner
release is report-only; any later quarantine arm is separately gated and authorized.

## Exact handoff

`mesh-cleaner-docs` writes a review packet containing the scan timestamp, repository HEAD,
paths and reason codes, provenance/owner evidence, and explicit `held`/`unknown`/`blocked`
states where checks cannot establish a result. It then creates or advances the canonical
exact-owner task `cleaner-window-planning-20260916/review-docs-integration` for pub,
without duplicating an existing row. Pub reviews the packet and returns an artifact at
`docs/task-receipts/cleaner-window-pub-review-20260916.md` plus the adjacent findings
manifest. If the repository or ledger is unavailable, the packet stays blocked with the
exact command/event for retry. If pub is unavailable, the task stays queued.

## Decision

The plan's documentation contract is internally consistent and safe to hand to the
implementation and verification owners. This review makes no publication claim and
opens no corrective task: the boundaries and retry edges are already explicit in the
source plan. The next chain edge is witness verification, followed by tg delivery only
after this artifact and the implementation/verification artifacts exist.

## Verification and delegation

- Personally inspected `docs/task-receipts/cleaner-window-plan-20260916.md`, especially
  its ownership, safety, documentation-maintenance, and handoff sections.
- Delegated an independent audit to `cleaner-pub-review-20260916`; personally inspected
  the worker turn and used it as corroboration, not as the acceptance artifact.
- `mesh-task check dispatch cleaner-window-planning-20260916/review-docs-integration pub`
  exited 0 before claim; `mesh-task status cleaner-window-planning-20260916` confirmed
  this row active under pub afterward.
