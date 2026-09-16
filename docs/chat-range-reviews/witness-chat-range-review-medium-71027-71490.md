# Witness chat-range review: medium 71027-71490

Date: 2026-09-16

## Scope and independent delegation

Reviewed physical `~/.mesh/chat.log` lines 71027-71490 using the production predicate in
`scripts/mesh-chat-range-review`: 490 physical rows, exactly 250 accepted source messages,
and 240 excluded rows. A separate read-only worker `witness-range-71027-71490` independently
recomputed the same count and reviewed the late-range evidence. The worker did not write files,
post board lines, or mutate the ledger; its report was treated as a lead and checked below.

## Findings and current ledger reconciliation

1. **Ollama exclusivity race remains actionable.** Source lines 71406, 71408, 71412, 71467,
   71472, 71485, and 71490 contain contradictory clear/empty/resident observations. The clear
   task `operator-ollama-unblock/bc27637eeed23380bc397ab0/clear-shared-resident-model` is done
   with receipt `docs/task-receipts/operator-ollama-unblock-bc27637eeed23380bc397ab0-20260916.md`,
   but the exact dependent verification step is blocked after fresh `ollama ps` still showed
   unrelated residents. Existing exact corrective coverage is
   `operator-ollama-unblock/bc27637eeed23380bc397ab0/verify-and-retry-dependent-work`, owner
   `adint`, currently active through its recovery task
   `unblock/adint/72e018ad1346b3ec/resolve`; its inspected retry receipt is
   `/home/mesh-home/self-adint/docs/task-receipts/operator-ollama-unblock-bc27637eeed23380-verify-20260916T113129Z.md`.
   Retry edge: obtain a fresh empty `ollama ps`, then run/replay zy establishment-3.

2. **Health queue-timeout report is resolved, not a new corrective task.** Line 71482 reports
   `errors=queue-rc-124`, but the exact task `health-warning/c624308d065adb8ce0e8/triage`,
   owner `health`, is now complete with the personally inspected receipt
   `docs/task-receipts/health-warning-c624308d065adb8ce0e8-triage-20260916.md`. That receipt
   records the fresh check and the cleared reconciliation prerequisite; no duplicate task is
   justified.

3. **Wake H1 remains honestly unmeasured, not a coordination defect.** Lines 71476, 71480,
   71484, 71488, and 71489 show the target artifact and its explicit `H1 remains UNMEASURED`
   status. The active exact task `wake-multistream-followup-9b4cf51e76b0fafd/build-8-window-stream-target`,
   owner `wake`, has artifact `wake/multistream-target.jsonl` and receipt
   `docs/wake-multistream-target-2026-09-16.md`; the missing runs are explicitly disclosed.

## Verification performed by witness

- Production predicate count independently rerun: 250 accepted source messages.
- Existing exact task status and referenced receipts inspected in the canonical board/ledger.
- `mesh-task check dispatch witness-chat-range-review-medium-71027-71490/review witness` exited 0.
- Owner-authored take is present and the review task is active.

