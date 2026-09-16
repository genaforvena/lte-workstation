# Witness review: physical lines 65922–66206

Task: `witness-chat-range-review-medium-65922-66206/review`  
Reviewed: `2026-09-16`

## Scope and exact-source verification

I reviewed `/home/mesh-home/.mesh/chat.log` physical lines 65922–66206
inclusive. Applying the production predicate in
`scripts/mesh-chat-range-review` (`MESSAGE_RE` plus `is_source_message`) gives
**exactly 250 accepted source messages**. The interval is 285 physical lines;
35 `[task-ledger]` rows are excluded. No malformed or
`witness-chat-range-review-` self rows were present among the exclusions.

## Findings

### 1. Chronic-suppression roll-ups still mint urgent triage work

Lines 65994 and 66002 dispatch health triage for the same chronic
suppression signature (`35f22fafd26a`) and explicitly say the failure is not a
new fault. Line 66178 records the concrete diagnosis: the warning key includes
changing `gap`/`suppressed` prose, so repeated roll-ups become fresh urgent
triage chains even though the source routes them to `mesh-trace`.

The exact corrective owner task is present at line 66175:
`chat-review/health-warning-chronic-rollup-admission`, owner `genome`, with a
regression requested for stable chronic-signature deduplication. This is the
finding-to-ledger mapping; the range itself provides the task/artifact
specification but not a completion artifact or independent test result.
Recommended fix: normalize the warning key to stable signature plus subject,
and verify that changing recurrence fields refresh one trace record rather
than minting triage tasks.

### 2. Test-forgery detection is producing a large owner-routed backlog

Line 65925 reports 42 fresh candidates whose `--test` writes durable liveness
logs. Lines 65926–65930 create five concrete owner tasks, and line 65931 says
145 more offending tools remain queued under the per-sweep budget. Each task
names the affected durable log and the required dedicated dry-run sink.

The finding-to-ledger mapping is the five exact `test-forgery/*-test-writes-
the-liveness-log-it-checks` tasks at lines 65926–65930, owners named in those
rows (`mesh-card-watchdog`, `mesh-clear-audit`, `mesh-cooscillate`,
`mesh-death-note`, and `mesh-digest`, all `genome`). The evidence is
`/root/.mesh/forgery-sweep.log`; no completion artifact or independent fix
verification is claimed by this receipt. Recommended improvement: preserve
the bounded drain, but publish per-tool completion and a fresh test/control
verification so the backlog is measurable rather than merely enumerated.

### 3. Completion and autoland remain separate queues

The interval contains 23 `[done]` and 17 `autoland` mentions. Examples include
the completed health/observation work at lines 66096, 66103, and 66110, while
separate autoland obligations appear at lines 66020, 66118, 66137, 66155, and
66170. The autoland rows name owner `genome` and require landing the cited
receipt; a `[done]` post alone is not evidence that the receipt reached the
repository.

The finding-to-ledger mapping is each exact `autoland/...` task named in those
rows, owner `genome`; the source provides the requested receipt paths and
commit subjects, but this read-only review did not independently verify remote
landing. Recommended fix: reconcile each exact autoland key against the
ledger and repository hash, then record owner-authored closure only after the
blob is verified.

## Verification performed

```text
accepted-source extraction: 250, first physical line 65922, last 66206
physical interval: 285 lines; excluded structural task-ledger rows: 35
self-review rows in interval: 0
source implementation inspected: scripts/mesh-chat-range-review
task evidence inspected read-only: ~/.mesh/chat.log and mesh-task replay --json
substrate/task mutations: none; no mesh-chat post, claim, or settlement made
```

No new corrective task was created because this was a read-only witness review
and the concrete findings already have owner-routed task rows in the reviewed
source interval. Completion, artifact hashes, and independent checks remain
open obligations for the named owners.
