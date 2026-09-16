# Cleaner window implementation plan

Date: 2026-09-16
Owner: genome
Source task: `cleaner-window-planning-20260916/plan-cleaner-window`
Operator ask: `tg-d009a8585146f86c58cf7cc9`

## Outcome and boundary

Create a `cleaner` mesh window whose job is to make repository clutter visible,
classify it, and safely remove only explicitly approved disposable material. The
window owns inventory, age ordering, quarantine proposals, retention checks, and
receipts. It does not own git landing, public publication, secrets, another
window's state, or substrate configuration. `mesh-land` remains the sole landing
writer; `pub` remains the publication owner.

The first implementation must be report-only. A later delete/quarantine arm may
be enabled only after its safety gates have red-tested and green-tested against
fixtures. No command may infer that an old file is disposable from age alone.

## Window and top pane

Add `charter/cleaner.md` and register the window through the same uniform-channel
and enumerator path used by existing channels. Its charter should state:

* goal: reduce unowned, stale, duplicate, and generated repository clutter while
  preserving evidence and keeping documentation current;
* data pane: a dedicated `mesh-cleaner-dash` (or a clearly named cleaner section
  in `mesh-dash`) showing scan timestamp, repository HEAD, candidate count, the
  oldest eligible candidate, blocked/held counts, last receipt, and the next
  retry time;
* mind pane: receives only meaningful inventory/task changes plus the autonomous
  self-pick cadence; it must be quiet on unchanged normalized data;
* owed artifacts: every scan receipt, candidate manifest, disposition, and
  documentation handoff; `[task]` for a repair, `[fyi]` for a held risk, and
  `[done]` only with a verifiable artifact.

The top pane must retain the mesh convention: data above, mind below, full
unfiltered source stream available to the mind, and `--once` for one-shot reads.
The cleaner renderer must not hide failures behind an empty candidate list.

## Reflex cadences

Implement and wire separate reflexes, each with its own `# reflex-cadence:`
header, dry-run log, and real artifact check:

1. `mesh-cleaner-scan`: every 15 minutes, inventory tracked/untracked/ignored
   candidates using explicit enumerators and record a fresh manifest.
2. `mesh-cleaner-settle`: every 15 minutes, oldest-first evaluate mtime, active
   writers, git state, and retention rules; never mutate.
3. `mesh-cleaner-docs`: hourly, compare documentation references/owners/artifact
   links and create or advance an exact-owner `pub` review task.
4. `mesh-cleaner-receipt`: daily catch-up, ensure each run writes a run row and
   fresh receipt even when it finds zero candidates; use boot-aware catch-up for
   power-cycling nodes.

Teach every enumerator about any new `cleaner/` lane directory: `mesh-land`,
`mesh-sync-tools`, `mesh-doctor`, `mesh-autowire`, and `mesh-vitality`. A source
tool is not live until deployed to `~/.local/bin/`, and it is not mesh-live until
landed.

## Scan and oldest-first policy

The scan manifest is the source of truth for one run and contains path, git
classification, byte size, inode/device identity, mtime in UTC, scan id, and
reason codes. Sort by `(mtime, path)` ascending, never by directory listing order.
Use `git status --porcelain=v1 --untracked-files=all`, `git ls-files`, and explicit
allowlisted roots; do not use a broad `find /` or a glob that can cross the repo
boundary. Re-read the candidate immediately before any future disposition.

The initial read-only inventory found 64 untracked `docs/task-plans` entries, 38
untracked `docs/task-receipts` entries, 18 `docs/chat-range-reviews` entries, and
additional `.agents`, drafts, sense reports, systemd, TSV, and `.firecrawl`
material. These are inventory facts, not deletion approvals. The existing
manifest-enumerator contract at
`docs/superpowers/plans/2026-09-07-manifest-enumerator-contract.md` is the model:
deterministic traversal, explicit classification, fatal unknowns/collisions, and
report-only deployed parity. Preserve source cursors and distinguish stale
backlog from completed work, following
`docs/chat-range-review-backlog-cleanup-20260915.md`.

Oldest-first is a review order, not a deletion policy. Generated receipts,
findings manifests, task plans, memory, tests, source, lane tools, and operator
evidence are retained by default. A path with an unresolved owner, active task,
recent mtime, open process, symlink ambiguity, or unverified provenance is held.

## Safety and retention gates

Every candidate must pass all gates before quarantine is even proposed:

* repository-root containment after canonicalization; reject traversal and unsafe
  symlink targets;
* clean/known git classification and no active worktree/process touching it;
* settled mtime older than the configured threshold, with a second stat at action;
* no match in protected roots (`.git`, `memory/`, `docs/task-receipts/`,
  `docs/task-plans/`, `tests/`, `scripts/`, `charter/`, lane code, or config);
* no live task, board claim, handoff, or artifact reference requiring the path;
* duplicate/reproducibility proof where deletion is proposed; preserve a hash and
  reversible quarantine location;
* bounded batch size and an interruptible cursor, claiming each irreversible item
  before its side effect;
* explicit human/steward `mesh-land --apply` for any git-visible deletion or
  change. The cleaner may prepare a patch/manifest but never land it.

The first release has no delete arm. A later arm must prove a red gate by mutation,
then restore it, and verify before/after `git status`, manifest, and quarantine
contents. Failure states are `held`, `unknown`, or `blocked` with a reason, never
an implicit clean verdict.

## Ownership and task flow

`cleaner` owns discovery and receipts. The owning mind owns its source and active
work. `witness` owns task-ledger reconciliation. `genome` owns source changes and
landing. `pub` reviews documentation freshness and decides whether a measured
case is publishable. `tg` delivers only after artifacts and transport receipts
exist.

Exact next tasks and artifacts:

| Owner | Task | Acceptance artifact |
|---|---|---|
| genome | `cleaner-window-implementation-20260916/implement-cleaner-window` | `docs/task-receipts/cleaner-window-implementation-20260916.md` plus tests and `.findings.json` |
| pub | `cleaner-window-planning-20260916/review-docs-integration` | `docs/task-receipts/cleaner-window-pub-review-20260916.md` plus `.findings.json` |
| witness | `cleaner-window-verification-20260916/verify-cleaner-wiring` | `docs/task-receipts/cleaner-window-verification-20260916.md` plus `.findings.json` |
| tg | `cleaner-window-planning-20260916/deliver-cleaner-plan` | `docs/task-receipts/cleaner-window-delivery-20260916.md` with transport receipt |

The implementation task must create the charter, renderer, scan/reflex tools,
enumerator registrations, fixtures, and tests; it must not delete existing user
files. The pub task is already in the parent chain and must remain the handoff
edge. The witness task verifies live wiring rather than trusting `--test` output.

## Verification artifacts

Each run writes:

* `docs/task-receipts/cleaner-scan-<timestamp>.json` — schema-versioned inventory;
* `docs/task-receipts/cleaner-scan-<timestamp>.md` — human-readable decision/holds;
* adjacent `.findings.json` with `version: 1` and a disposition for every finding;
* a run ledger row containing attempt health even when no candidate was found;
* a test-only log separate from the liveness log.

Acceptance checks must cover: oldest-first ordering, root containment, protected
paths, active-writer hold, mtime race, cursor recovery, zero-candidate run rows,
documentation task deduplication, `--once` renderer behavior, all enumerator
registrations, deployment drift, and a real scheduled/reflex invocation. The
verification receipt must include command, exit status, timestamp, and artifact
path for each check.

The baseline commands for the verification task are:
`git status --short`, `git ls-files --others --exclude-standard`,
`scripts/mesh-pane-watch --status`, `scripts/mesh-window-check --check`,
`scripts/mesh-reflex-census --check`, `scripts/mesh-reflexes --check`, and
`mesh-task audit`. A baseline run observed all 15 pane-watch windows advancing;
`mesh-window-check --check` also exposed a missing task heading in `witness`, so
the cleaner must report such a defect and route it rather than rewrite the pane.
`mesh-reflex-census --check` reported 362 scheduled reflexes but exceeded a
20-second read-only timeout while continuing its multi-substrate census; the
cleaner must preserve timeout/failure as `unknown` evidence, not render zero.

## Documentation maintenance and `pub`

`mesh-cleaner-docs` may detect stale links, missing owners, absent adjacent
findings manifests, references to nonexistent tools/tasks, and documentation that
contradicts current charter or script behavior. It writes a review packet and
queues the exact `pub` owner task. It must never publish, edit public posts, use
the dev.to credential, or silently rewrite a document. `pub` reviews the packet,
chooses draft/revise/hold, and returns its review artifact to the parent chain.

The retry edge is explicit: if the repository or ledger is unavailable, retain the
packet as `blocked` with the exact command/event to retry; if `pub` is unavailable,
leave the exact-owner task queued and do not duplicate it. `tg` delivers only the
verified plan plus pub review and records the actual `mesh-tg` receipt.

## Documentation-maintenance path

1. Land this plan and its findings manifest.
2. `genome` implements the cleaner window and registers every reader.
3. `witness` verifies task transitions, pane fit, and live reflex wiring.
4. `pub` reviews the documentation contract and any measured case.
5. `tg` delivers the verified packet to the operator.
6. Only after those artifacts exist may a separate task propose a bounded,
   reversible quarantine arm; deletion remains a separately authorized change.
