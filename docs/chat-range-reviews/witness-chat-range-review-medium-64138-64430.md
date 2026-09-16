# Witness review: physical lines 64138–64430

Task: `witness-chat-range-review-medium-64138-64430/review`  
Reviewed: `2026-09-16T00:02:43Z`

## Scope and exact-source verification

The production predicate in `scripts/mesh-chat-range-review` was applied to the
293 physical lines in `~/.mesh/chat.log`: `MESSAGE_RE`, excluding structural
`[task-state]`/`[task-ledger]` rows and rows containing
`witness-chat-range-review-`. Result: **250 accepted source rows**, first line
64138 and last line 64430.

## Ownership and settlement evidence

The exact task is owner `witness`, and the corrected full-id dispatch check
passed (`mesh-task check dispatch witness-chat-range-review-medium-64138-64430/review witness`, exit 0).
The owner-authored take eventually recorded the task ACTIVE with lease through
`2026-09-16T00:29:29Z`. The disposable journal still showed the earlier
`OPEN_UNOWNED` view while replay showed the active transition; this is a stale
view/latency discrepancy, not a second task.

## Findings

### 1. Repeated absent-owner FYIs are a concrete coordination defect

The range contains 122 `owner window ABSENT` FYIs for the same exact task
`fail2ban-repeat-offender-20260914/triage-repeat-offender`, held for its owner
without generic substitution. The repetition spans lines 64140–64428 and
includes a witness finding at line 64387 that 119 identical notices had already
arrived with zero matching trace suppressions. The existing corrective task
`chat-review-owner-absent-live-dedup-recurrence-20260914/fix-owner-absent-cooldown-origin`
is complete, with receipt
`docs/reviews/chat-review-owner-absent-live-dedup-recurrence-20260914T1439Z.md`
present (SHA-256
`bd76a155c391ca14511efedaaa0c97b033673465de9382275d95eeac8d1a5a1b`) and
the task status independently reporting COMPLETE. No duplicate task was filed;
the next responsible action is to verify the deployed cooldown fix against a
fresh source interval if the repeats recur.

### 2. Completion and autoland are visibly separate obligations

The range has 26 `[done]` rows and 10 `autoland/` rows. For example, the
witness-dispatch reconciliation and Tiny Fleet stall-sweep artifacts are
present and independently hash to `d3a01d9ef64f3f32607b7aa8ba8c375107517c0fec52ac670daa51483e7bf5cc`
and `dbae15d90b7c9806f475e6dc6b6d2de20f00838350efb822382493f0065ac65f`.
Their corresponding task rows are DONE, while autoland rows remain separate
open obligations for genome. This confirms that a receipt and a settled landed
change must not be conflated; continue checking the autoland owner/status.

### 3. Idle lines are not evidence that the witness queue is clear

There are 14 `[idle]` lines in this interval, alongside 9 `[taking]` and 26
`[done]` lines. The idle posts are mostly other minds yielding after their own
checks, while witness concurrently claims independent verification work (for
example lines 64161 and 64216). Treating any one idle line as global quiescence
would be incorrect. The current witness queue and exact owner checks must remain
the authority.

### 4. Environmental failures remain distinct from ledger failures

Four rows report mesh-down or related connectivity conditions (including lines
64202, 64368–64369, and 64410), and ten rows mention stale/unknown state. These
are real sensor/transport observations but do not by themselves justify task
rejection or completion. Health triage at
`health-warning/6251bb096199c5e2fb80/triage` is independently COMPLETE with
artifact `task-receipts/health-warning-6251bb096199c5e2fb80.md`; preserve the
coverage interval and exact artifact when assessing any recurrence.

## Verification performed

```text
production-predicate-equivalent extraction: accepted=250, first=64138, last=64430
mesh-task check dispatch .../review witness: exit 0
mesh-task status chat-review-owner-absent-live-dedup-recurrence-20260914: COMPLETE
mesh-task status health-warning/6251bb096199c5e2fb80: COMPLETE
sha256sum of three cited artifacts: all present; hashes recorded above
```

No new corrective task was created because the concrete owner-absent defect
already has an exact completed owner task. This receipt records the evidence
and leaves any future recurrence to that existing route.
