# Task dispatch completion audit — 2026-09-08

Operator requirements: simple text-only coordination; chat.log sole source;
optional task ownership; least-busy eligible dispatch; stale legacy work may
expire; promises are views of work rather than independently mutable task state.

## Fresh evidence at 05:43Z

| Requirement | Evidence | Result |
| --- | --- | --- |
| No board database | Exact live `~/.mesh/board-store.db` absent; source search finds only historical comments | Pass |
| Rebuild state from text | task-log, import, optional-owner cache-loss/write-failure, restart-continuity tests | Pass |
| Unassigned work and named owners | optional-owner, unassigned-dispatch, staffing, TG exclusion tests | Pass |
| Exact identity and owner exclusion | task-identity, promises-identity-integrity, task-workspace-scope tests | Pass |
| Dispatch is not start | dispatch-receipt, reschedule receipt-race, final-state, resurface tests | Pass |
| Dependency ordering and no stale canonical work | board-task-state tests; live replay compared to actual queue | Pass: 38 chains; exactly 3 current open steps; no missing/forbidden rows or owner mismatches |
| Derived promise accounting and age retirement | promises-task-state, work-retirement, addressed-task tests | Pass; retirement preserves historical source bytes and human/canonical work |
| Read errors cannot become empty-success | dispatch-query-failure, board-task-state, roll-call-text, board-weekly-text tests | Pass |
| Real scheduling and installed code | Actual crontab has five-minute dispatch and chat.log fsnotify triggers; dispatch.log records current passes; nine installed consumers compare equal to source | Pass |
| Durable clean-checkout implementation | New replay helper and focused regressions still being landed by genome | Pending |

All 13 Python scripts in the focused set and all 9 shell lifecycle/accounting
scripts passed in this audit turn. The separate staffing and TG policy scripts
also passed. Full router and sync smoke tests passed in the preceding turn after
the final receipt-scan and recovery-message edits; they are not represented here
as rerun during this audit.

The live legacy `next` reminder still scheduled completed staffing work because
the owner's stale-dispatch reply did not carry its exact reminder key. Witness
verified the original genome completion at 2026-09-07T21:32:15Z, the complete
five-step canonical chain, and both fresh staffing checks, then posted a scoped
`[done] ... task:next owner:genome` reconciliation at 05:42:19Z. Feed regenerated
the journal and a fresh queue check confirmed that reminder absent. No new
implementation or owner impersonation is claimed by that reconciliation.

## Remaining completion gate

Board task `task:task-text-source-landing` is owned by genome. Its live pane at
05:40–05:42Z showed review and staging of the requested source/helper/tests: this
is task-loaded start evidence beyond its acknowledgment. Require the resulting
commit, clean-tree executable/import and focused test checks, and push evidence
before declaring the implementation durable. Do not mistake a staging list or a
green dirty-checkout test for this gate.

Historical prose reminders remain compatibility inputs from the same chat.log.
Explicit `mesh-task import` is a manual recovery operation, not a normal cache
fallback. Completion checks attest recorded owner evidence and artifact scope;
they do not prove arbitrary human claims true. These limits are not hidden by a
second database or synthetic owner-start receipt.

## Clean archive check at 05:44Z

Genome committed the helper and consumers in `fd00ec3f`. Witness extracted that
exact commit with `git archive` into `/tmp/task-dispatch-clean.CDQfmJ`, without
borrowing untracked files. Replay (10 cases), import/rebuild, optional-owner
cache-recovery, board-state (6 cases), and final/early dispatch checks passed.
The next command failed because `tests/test-mesh-resurface-path.py` was absent.
`tests/test-mesh-work-retirement.py` was also omitted from the commit, so the full
committed regression set remains incomplete. Genome was notified at 05:44:41Z
to land those required tests and the audit/design evidence before closure.

Live hledger journal integrity check returned rc0. The required follow-up
regressions and design evidence were landed in `1d9281c7`: resurface-path,
work-retirement, board-snapshot, addressed-task, and promise-identity-integrity
tests passed, and the two design/audit documents were added. The follow-up was
pushed to `origin/main`; a fresh fetch confirmed `HEAD == origin/main`, with no
tracked or staged changes. The unrelated untracked worktree artifacts remain
untouched.

## Witness verification and isolation repair at 05:48Z

An exact archive of `1d9281c7` at `/tmp/task-dispatch-clean.0XHurh` passed all
13 Python and 9 shell focused scripts. Shell tests were run with an isolated
HOME to keep their output away from the live mesh.

The live pane exposed a separate test-isolation bug: `mesh-promises` hardcoded
its mesh directory to HOME/.mesh, ignoring MESH_DIR. A custom-input feed fixture
therefore overwrote the live promise summary with two fixture tasks, even though
live JSON still contained real tasks. `tests/test-mesh-promises-isolation.py`
reproduced this against a sentinel under a fake HOME (red), then passed after the
one-line MESH_DIR fix. Addressed-task, retirement, and full promises smoke passed.
No task source records were lost. A live feed restored 50 open / 1010 kept and
the hledger integrity check passed.

This newly discovered fix is not covered by the prior landing closure. Separate
owner task `task:task-text-isolation-landing` was filed to genome at 05:48:07Z for
the source line, regression, scoped commit/push and clean-commit verification.
The overall goal remains open until that final fix is durable and verified.
