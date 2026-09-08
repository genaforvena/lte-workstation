# One task lifecycle, one event source

Operator direction: keep coordination simple, use append-only chat.log as the
source of truth, retire stale work, and consider merging promises into tasks.

Decision: all actionable work is a task. A promise is an unfinished task viewed
through accounting, not another independently dispatchable object. A taking is
the task's owner-start event. A verification request is a task with verification
acceptance criteria, or a successor verification task when independently owned.
Observations, FYIs, and acknowledgments remain ordinary chat events.

Each task has one explicit task:<id>, description, optional owner, state, optional
dependencies, and completion evidence. State transitions are recorded in chat.log:
queued, running, blocked, done, cancelled, expired. Dispatch is delivery evidence;
only an owner receipt starts work. A completed task cites its artifact and check.
Expired means no longer scheduled and never means successfully completed.

Owner is optional at creation. An explicitly named owner is respected. Otherwise
dispatch chooses the least-busy eligible mind and records the assignment on that
same task ID before accepting its start receipt. Eligibility includes availability,
capability and any explicit scope constraints. Unknown load is not zero load.

Current evidence: mesh-task post_task already emits task:<chain/step>, take emits
the same ID, and mesh-promises creates a PROMISE for a task and a separate HOLD
for a taking. mesh-task load/save currently treat task-chains/*.json as authoritative.
That last path still contradicts the requested single source: it must become a
rebuildable projection, including ordered-step definitions and dependency state.

Implementation requirements for the ongoing dispatch repair:

- Use one explicit ID across creation, assignment, dispatch, start, progress,
  blocking, verification, retirement, and completion.
- Record enough structured task/plan facts in chat.log to rebuild task chains.
  Do not claim JSON caches are derived until a clean replay actually rebuilds them.
- Derive the dispatch queue, task state, and hledger balances from those events.
  Keep legacy CLI names as aliases only where useful; avoid a second mutable lifecycle.
- Preserve exact owner matching, human-owner holds, dependency ordering, duplicate
  delivery suppression, and artifact/verification checks during consolidation.
- Verify that deleting derived caches and replaying chat.log restores the same
  queue and task states. Verify restart between event append and cache update.

This document records the chosen design and completion criteria. Task lifecycle
consolidation is not yet implemented. Historical text is retained; consolidation
must not reopen old completed work or present expiration as completion.

Recovery groundwork: scripts/mesh_task_log.py and source `mesh-task replay --json`
read versioned task-state text records. Five tests verify preserved future steps,
duplicate/reordered delivery, conflicts/gaps/truncation, quoted-prose exclusion,
missing source, and optional-owner assignment before start. The writer and normal
chain readers are not switched yet. The installed ~/.local/bin/mesh-task is a
separate file, not a symlink; compare it with the source before deployment.

Optional-owner routing now survives the existing ledger queue: mesh-board marks
tasks without an explicit address/owner as unassigned, and mesh-dispatch omits
the synthetic owner tag for them. The poster's accounting attribution is not an
assignment. A live queue query showed 1 unassigned task among 44 open rows.

The router now receives the dispatcher's actual eligible-idle candidate list,
including an explicitly empty list, instead of reverting to its default pool.
Staffing currently admits only minds with zero open promises/holds; live state
must additionally be IDLE. These are tied at minimum workload; Codex/OpenCode
ties now use least-recent dispatch, as the Claude lane already did. UNKNOWN is
not treated as idle. Named-owner routing still precedes this selection.

Tests: test-mesh-board-snapshot.py (3), test-mesh-dispatch-unassigned.py, and
test-mesh-dispatch-query-failure.py pass. Source syntax and diff checks pass.
The bias regression expectation was updated because informative dispatch recency
now influences free-engine choice; the full control smoke suite passes.

Chain creation now accepts an empty owner column or `-` in plan TSV rows. Board
tasks omit owner tags when unassigned. The first successful owner-authored take
sets the owner under the coordinator lock; failed receipt emission leaves the
stored task unassigned, and a different actor cannot steal the active task.
Unassigned successors publish a board handoff and enter the ordinary free pool.

`tests/test-mesh-task-optional-owner.py` passes the complete two-step lifecycle,
including failed receipt rollback and owner exclusion. The chain smoke suite,
workspace-scope and ledger-sync tests pass. The installed executable was compared
with the source, backed up to ~/.mesh/task-deploy-backup.qfTPTO/mesh-task, and
replaced by a symlink to scripts/mesh-task. Installed help and smoke test pass.

Update 2026-09-08 04:54Z: normal chain saves now append validated, versioned
`[task-state]` records through `mesh-chat --task-state` before replacing JSON
caches. Normal load, audit, reschedule, and active-owner exclusion prefer those
records. Appends share the board lock, fsync their output, reject conflicting
revisions, and refuse any snapshot that the secret scrubber would alter.

Fresh checks: chain smoke test, workspace-scope, ledger-sync, unassigned dispatch,
and optional-owner lifecycle pass. Seven replay/append tests pass, including
duplicate/conflict handling and scrub refusal without changing the log. The
optional-owner test deletes both chain/context caches and verifies status, audit,
and owner exclusion; it also forces cache replacement to fail after the log append
and verifies the committed claim survives and can complete after recovery.

Still incomplete: existing chains without task-state records retain their legacy
JSON fallback; context-cache corruption recovery and direct cache consumers need
review. Human-readable receipts and structured snapshots are separate appends, so
their interruption interval still needs reconciliation. Next: explicit import and
verified replay of existing chains, then remove fallback and unify queue/lifecycle
consumers. This is not yet a verified single-source system across the whole mesh.

### Import and replay implementation checklist

- Add `mesh-task import` under the coordinator lock: validate all chain JSON
  files, append only chains not already represented in chat.log, and verify each
  imported payload using the normal replay reader. Reruns must be idempotent.
- Add `mesh-task rebuild`: regenerate chain and owner-context caches from replay,
  including completed/blocked state. Invalid caches must not override the log.
- Test an isolated legacy import, repeated import, corrupted/deleted caches,
  explicit rejection of unimported JSON, and full cache reconstruction.
- Run the import on the 38 current chains (19 complete, 16 blocked, 2 active,
  1 open at inspection), compare semantic payloads, then remove fallback reads.
- Update the witness prompt to query `mesh-task audit` instead of trusting JSON.
- Re-run task lifecycle, replay, ownership, workspace and ledger regression tests;
  record any remaining dispatch/lifecycle gaps separately.

### Live import result — 2026-09-08 05:02Z

`mesh-task import` appended all 38 existing chains and verified replay. A separate
semantic comparison reported `files 38 replayed 38 mismatches []`; repeating the
import reported `imported=0 verified=38`. `mesh-task rebuild` regenerated 38 chain
caches and nine owner-context files. Normal chain load/audit/reschedule and owner
exclusion now read only chat.log. Unimported JSON cannot create work implicitly.
Missing chat.log is a failure, not an empty queue. The original JSON caches remain
on disk as rebuildable views, not an alternative authority.

Two live-data issues were reproduced and repaired before import: a split Git
object hash in a description triggered the scrubber's generic secret rule; the
exact `.git/objects/<2 hex>/<38 or 62 hex>` position now survives, while bare,
wrong-width and prefixed-secret cases still reject. Old non-task prose contains
invalid UTF-8; replay now matches structured records as bytes and strictly decodes
only their payloads. Damaged structured records still fail loudly. No historical
board bytes were rewritten. The scrubber's existing UUID smoke assertion also
needed to distinguish the permitted board-id occurrence from the bare occurrence.

Fresh verification: nine replay/append cases; import/rebuild/absent-source test;
optional-owner cache-loss and write-failure test; mesh-task and mesh-log-scrub
smoke tests; task dispatch-receipt, reschedule (including held-receipt race), restart
continuity, complete-chain audit, identity, workspace-scope and ledger-sync tests.
All passed. The reschedule fixture now creates an expired lease through the actual
writer rather than mutating its cache; the audit fixture explicitly imports its
isolated chain. Live audit reads all imported chains. Diff whitespace check passes.

Remaining goal obligations: consolidate promise/hold/task accounting consumers onto
one task lifecycle; prevent stale prose tasks from dispatching blocked/completed
canonical work; reconcile interruption between prose receipt and task-state append;
verify the complete live dispatch-to-owner-start-to-artifact/verification path.
The import milestone does not prove the full dispatch repair complete.

### Canonical dispatch queue — 2026-09-08 05:06Z

`mesh-board open --dispatch` now reconciles legacy promise rows with replayed
task-state records. Exact chain IDs and their full historical account-normalized
aliases are replaced by the current chain state. Blocked, active/claimed, done,
complete and future steps are excluded; only the current open step is added,
including when its prose task receipt is absent. Its current owner and exact take
command come from the chain. Ambiguous normalized aliases fail loudly; incidental
mentions of another task in prose do not suppress independent work.

Human accounting debtors take precedence over the unassigned-poster marker, so
steward/operator obligations never fall into the free-mind pool. Four metadata
tests and six canonical-queue tests pass; the latter include the actual CLI with
real hledger, missing-source refusal and ambiguity. Unassigned dispatch and partial
query-failure tests pass, and diff whitespace check passes.

Compared source with installed board, backed up the latter at
`~/.mesh/board-deploy-backup.ObJ6aF/mesh-board`, and installed the source symlink.
An installed live query returned rc0, 33 candidates, zero forbidden chain steps,
and zero missing current-open steps. The only current-open chain step was
`token-usage-accounting-implementation-20260908/token-source-schema` (genome).
Both human tasks remained steward/operator-owned. `reflexes.cron` has the existing
five-minute dispatcher and board fsnotify dispatcher; both call the installed tool.

Next concrete gap: `mesh-mind-control::_open_taking_of` still reconstructs old
claims from prose taking/done/yield only, and its caller collapses scan errors to
no claim. It must consult canonical task states too, excluding blocked/completed
claims and refusing unreadable state. This was the stale resurface route observed
for hire at 04:28 and 04:37Z. Receipt/state append reconciliation and unified
promise/hold accounting remain open after that.

### Delivery-boundary and resurfacing repair — 2026-09-08 05:12Z

Live evidence changed the next action: at 05:06:24 an older dispatcher delivered
the blocked haunt-owned architecture sample step to senses, which posted taking
at 05:07:18. `mesh-task status` confirmed BLOCKED/haunt, so witness sent a direct
correction. Delivery was acknowledged; at 05:11:25/28 senses yielded, preserved its
partial files under `docs/tiny-fleet-artifacts-20260907/architecture-drift/02-external-sample/`,
handed them to haunt, and confirmed no completion or successor advancement.

`mesh-task check <dispatch|resume> <id> <owner>` now reads canonical text and returns
0 eligible, 2 refused, 3 independent/untracked, 1 unreadable. Exact IDs and full
legacy aliases are accepted; ambiguous aliases fail. Dispatch requires the current
open step and its owner (if assigned); resume requires a current active claim owned
by the target. Blocked, completed, future and foreign-owned steps are refused.

Mind-control uses this check before resurfacing an old taking and immediately
before delivery. Its caller no longer converts a failed claim scan to no claim.
The delivery check handles the old queue's leading normalized ID as well as exact
task tags. Full mind-control smoke passes; ten replay/eligibility tests, real
resurface-block/malformed-state tests, and the production final-gate test pass.
The final-gate test refuses stale state, owner redirection and missing source while
allowing the current open owner. Source syntax/diff checks pass.

Installed mind-control was compared, backed up to
`~/.mesh/control-deploy-backup.HbgPIQ/mesh-mind-control`, and replaced with its source
symlink. Installed live eligibility checks returned rc2 for both the senses sample
delivery and hire's blocked delivery-repair resume. That is refusal evidence, not a
claim that every future dispatch race is eliminated: state can still change after
the final read, and the owner's canonical take remains the exclusive claim gate.

Next: consolidate prose receipts and structured task transitions so interruption
cannot leave their consumers disagreeing; unify promise/hold/task accounting and
verify the full dispatch-to-start-to-artifact lifecycle. Goal remains open.

### Ledger reconciliation — 2026-09-08 05:20Z

For tasks represented by task-state records, mesh-promises now removes their
provisional prose lifecycle inputs and derives its accounting view from committed
snapshots. The in-memory projected events are not posted as invented board/start
receipts. Current open/blocked tasks remain obligations, only active current tasks
hold a worker, future steps do not hold workers, and completed steps stay closed.
Independent legacy tasks retain their existing text replay. PROMISE/HOLD remain
compatibility accounting views, not competing mutable state for structured tasks.

The regression drives open state plus provisional taking/done; active state with
no taking receipt; blocked state with old taking; and completion with stale task
and taking. It also proves completion cannot release an unrelated same-owner hold
or verification claim with similar prose. This exposed the scoped hold matcher's
explicit-key-to-prose fallback; explicit hold closures now stay keyed. Canonical
completion likewise cannot redeem an unrelated claim by prose. Legacy claim reply
semantics remain unchanged, as the full smoke suite verifies.

Full mesh-promises smoke, task-state regression, ten task-log tests, task-ledger
sync and diff check pass. Installed source symlink backup:
`~/.mesh/promises-deploy-backup.kKUeDp/mesh-promises`. Live installed JSON matched
all 19 canonical open obligations and both canonical active holds exactly, with
empty difference sets. `mesh-promises --feed` returned rc0 and regenerated the
journal; `hledger ... check` returned rc0. Increased legacy hold counts reflect
the removed false-closure fallback, not newly posted work. Imported snapshots
model one episode per step, not unavailable prior reopening history; the generated
journal now labels that limitation explicitly.

Remaining: early prose deduplication in mind-control can still treat a provisional
done/taking as authoritative before its final canonical check. Reconcile that
path, apply the chosen age retirement consistently across legacy work views,
and perform the full completion audit. No full dispatch-complete claim yet.

### Early dedup and legacy retirement — 2026-09-08 05:27Z

Mind-control's early cross-node scan now checks whether a structured task is still
pending. For a committed open task, provisional taking/done lines cannot suppress
dispatch; an actual dispatch receipt still enforces the delivery cooldown. A
non-pending or unreadable canonical state holds the task. The final owner/state
check remains in place. Production-block regression and full mind-control smoke
pass, as do the resurface and ten task-log cases.

The existing 336h legacy retirement horizon now applies to unstructured claims and
holds as well as tasks. Human-owned work and explicitly stateful canonical tasks
are not silently retired by this legacy cutoff. JSON reports retired counts by
kind, and journal comments distinguish retirement from completion. The isolated
test proves all three old legacy categories retire, human/recent holds survive,
and chat.log bytes are unchanged. Full promises smoke, structured-task accounting
regression, and diff check pass.

Completion audit found remaining DB assumptions, not new scope: roll-call's
`board_corpus` and respondent prompt still read board-store.db and report its
absence as a gap; board-weekly calls text history but falsely labels its output as
DB-backed. Next remove those readers/claims, replace their DB fixtures with text
tests, and continue the full completion audit. The store itself remains removed.

### Text-reader cleanup — 2026-09-08 05:34Z

Roll-call now reads only chat.log; its respondent prompt no longer asks minds to
query a deleted DB. Missing text yields explicit unknown rather than a fabricated
open/settled result. Weekly export selects dated lines directly from chat.log,
labels retained-local coverage, and refuses missing input before sending.
Both focused text-only regressions and both full smoke suites pass. Export sends
were isolated to a stub; no real Telegram export was sent. Installed paths resolve
to the source scripts and compare equal. Live `mesh-roll-call --settled witness`
returned `retired 2026-08-18T18:16:00Z` without a DB warning.

The operator contract now names optional ownership and chat.log authority.
Remaining audit: chat-sync's wipe/shrink diagnostic messages still recommend the
removed archive; correct those recovery instructions. The new task-log module
and focused regressions remain untracked and must be landed with their consumers.
Full dispatch completion is not claimed.

### Delivery scan and recovery audit — 2026-09-08 05:39Z

The remaining chat-sync wipe/shrink messages now identify text snapshots and
retained peer chat.log copies, with completeness explicitly UNKNOWN until checked.
Full chat-sync smoke passed. Installed copy differed only in these reviewed changes;
it was backed up to `~/.mesh/chat-sync-deploy-backup.4kBRYz/mesh-chat-sync` and replaced
with the source symlink. No live sync or recovery was invoked for this verification.

Two isolated regressions reproduced a dispatch bug: damaged historical prose
containing binary bytes made grep hide valid taking/completion records and bypass
the recent-delivery cooldown. Three receipt scans now force text mode. The resume
and final/early-delivery regressions went red then green; full mind-control smoke
passed. The installed mind-control source symlink already carries this fix.

A read-only review raised lifecycle-ordering, legacy fallback, optional assignment,
dependency/verification and explicit-import concerns. These require scoped
interpretation: ordered chains gate future steps; manual take is not dispatcher
selection; explicit import is an authorized recovery operation, not a normal cache
reader. Final canonical gates and accounting already reject provisional prose as
authority. Do not treat the review's broad conclusions or test claims as independent
completion evidence without reproducing each relevant path.

Durability is still open: `scripts/mesh_task_log.py` remains untracked although
committed consumers import it. Board task `task:task-text-source-landing` was filed
to genome with scoped commit, clean-tree checks and push evidence as acceptance.
Dispatch or acknowledgment alone is not an owner-start receipt or completion.
