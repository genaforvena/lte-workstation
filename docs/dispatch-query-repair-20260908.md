# Dispatch query repair

The text-only board exposed a query cost problem: `mesh-board` scanned the entire
35,000-line chat.log for each historical opening in the promise journal. A live
`mesh-board task next` exceeded a 15-second timeout. One source lookup measured
0.416 seconds; the hledger print itself measured 1.994 seconds.

The query now builds one in-memory timestamp index from chat.log and reads the
live window roster once per process. No persistent index or database is added.
The live `mesh-board open --dispatch` completed in 6.93 seconds after this change.

The queue also preserves human ownership when hledger quarantines the account as
unrouted, and recognizes the journal's `priority:incident` field. This preserves
the dispatcher’s human-owner gate and incident ordering.

Verification: `python3 tests/test-mesh-board-snapshot.py` passes both source-read
reuse and human-owner/incident cases. `test-mesh-dispatch-hledger-gate.sh` and
`test-mesh-task-dispatch-receipt.sh` pass. `git diff --check` passes.

The complete dispatch objective remains open: existing DB-specific disabled tests
and help text need reconciliation, and live task delivery through owner start and
artifact verification still needs a full audit. Queue success alone does not
prove that lifecycle.

## Resume and query failure follow-up

Live dispatch.log at 04:18:19 showed a failed cooldown write to
`.resurfaced-hire-ba260907-05-workspace/repair`. Resume state now percent-escapes
slashes and percent signs, preserving ordinary existing filenames and avoiding
collisions with literal encoded text. The resume scan also rejects the shared
parser's UNKNOWN sentinel as a claim ID.

Queue-query errors previously vanished inside mapfile process substitution.
Dispatch now checks the query pipeline status before accepting any rows, including
partial output from a failing query.

`python3 tests/test-mesh-resurface-path.py` passes cooldown persistence, repeat
suppression, percent-ID separation, UNKNOWN rejection, and explicit chain-ID
resume. `python3 tests/test-mesh-dispatch-query-failure.py` passes empty-success
and partial-failure cases. Bash syntax and diff whitespace checks pass.

The broader `mesh-mind-control --test` failed (12 assertions on the run preceding
the UNKNOWN guard). Its legacy untagged-identity fixtures conflict with the shared
parser's explicit-tag behavior; deduplication assertions also failed. These remain
to be reconciled and verified; the broad suite is not reported as passing.

## Identity reconciliation verified

The subsequent repair requires exact explicit IDs for both completion-race and
resume-close checks. A sibling ID with an extra suffix no longer suppresses work.
Failed-delivery announcements hash untagged messages independently rather than
sharing UNKNOWN; tagged chain IDs use safe filenames. Smoke fixtures now carry
explicit task tags on their task, dispatch, taking, done, and yield events.

After these changes, `mesh-mind-control --test` passed, including cross-node
deduplication, gossip presync, delivery acknowledgment, and resume/cooldown checks.
`tests/test-mesh-dispatch-identity.py` and `tests/test-mesh-resurface-path.py` pass
the exact-ID, UNKNOWN, slash-ID, and duplicate-notice regressions. Diff check passes.

Installed mesh-mind-control resolves to this repository script. Reflexes declare
mesh-dispatch on a five-minute schedule and through the chat.log watcher. Live
board lines at 04:26:50/51 confirm the human-owner gate executed after the queue
repair. The 04:28:17 resume line has no corresponding encoded cooldown file and
is therefore not accepted as runtime proof of the cooldown repair. Full owner
start/artifact/verification audit and DB-era test/help cleanup remain outstanding.
