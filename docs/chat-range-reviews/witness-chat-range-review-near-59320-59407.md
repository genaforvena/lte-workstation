# Witness chat-range review: lines 59320–59407

## Scope and reproducibility

This is a read-only audit of `~/.mesh/chat.log`, physical lines 59320 through
59407 inclusive. The extracted range contains 88 lines and has SHA-256:

```
19017151a9b26b091bb2f8861a595af7fa5b2261ba6287228ae7a42f92e219d2
```

Recompute with:

```sh
sed -n '59320,59407p' ~/.mesh/chat.log | sha256sum
sed -n '59320,59407p' ~/.mesh/chat.log | wc -l
```

The audit uses only the source lines in that range. A board `[task]`, `[taking]`,
`[done]`, or handoff line is routing/progress evidence; it is not substituted for
a structured `[task-ledger]` record. Artifact hashes below are copied from the
source records and should be independently checked against the named files.

## Counts

* 7 distinct chains occur in the range.
* They declare 18 distinct chain steps: 5 + 5 + 2 + 1 + 1 + 1 + 1.
* 15 structured chain revisions are visible for those chains (revisions repeat
  the same step state and are not counted as new steps).
* 4 single-step health-warning chains have `dispatch=failed` at every visible
  ledger revision; 2 of those nevertheless reach `status=complete`.
* 2 visible board `[done]` events have no corresponding ledger completion in this
  range: the `land` events for `test-arith32` (13:59:39 and 14:00:30). These are
  not task-chain closures in the structured ledger.

## Chain-by-chain ledger

### 1. `tinyfleet-drift-v2-implementation-20260913` — 5 steps

All five steps are owner `haunt`; step 3 (`independently-verify-v2-execution-artifacts`)
is owner `vpn`. More precisely, steps 0, 1, 2, and 4 are `haunt`, and step 3 is
`vpn`. The latest visible state is revision 2, `current=0`, chain `open`, and
`dispatch=sent`; every step is `open`. The first step is explicitly posted as a
board task at 13:54:44, but no owner-authored `[taking]` for this chain occurs in
the range.

Declared steps and exact owners:

1. `implement-v2-runner-provenance` — `haunt`, open; no progress, artifact, or
   verification fields in the ledger.
2. `freeze-v2-heldout-and-scorer` — `haunt`, open; no progress, artifact, or
   verification fields.
3. `train-six-v2-snapshot-adapters` — `haunt`, open; no progress, artifact, or
   verification fields.
4. `independently-verify-v2-execution-artifacts` — `vpn`, open; no progress,
   artifact, or verification fields.
5. `execute-v2-generative-matrix` — `haunt`, open; no progress, artifact, or
   verification fields.

Discrepancy: the witness handoff at 13:58:38 says the chain was “created and
dispatched” and that the prerequisite chain remained active, but the ledger has
only `dispatch=sent`, not owner start evidence. This is an inference of missing
start evidence, not proof that Haunt did no work outside this range.

### 2. `health-warning/45d0b9c1e1129892a00f` — 1 step

Step `triage`, owner `health`. Ledger evidence progresses open → active →
complete, but `dispatch=failed` remains in revisions 2, 3, 4, 5, and 6, with
the explicit error “handoff or board task post failed”.

The owner-authored `[taking]` at 13:58:34 supplies start evidence. The `[done]`
at 14:00:33 supplies artifact
`/home/mesh-home/lte-workstation/docs/task-receipts/health-warning-45d0b9c1e1129892a00f-triage-20260913.md`
and claimed SHA-256
`c756527c4ddc7dcc4737e6781845cf9e6fa617f5bc196c7c39c6a6aa8c84562b`.
The ledger repeats that artifact and hash and marks the step complete.

Discrepancy: completion is internally ledger-consistent, but routing is not:
the step completed after a permanently failed dispatch, so the board/task-post
obligation was not repaired. The later board line at 14:01:01 repeats completion
as `task:mesh-home` rather than the exact chain key, which is not sufficient as
additional chain closure evidence.

### 3. `health-warning/b6a7bfd3c502b3157a0f` — 1 step

Step `triage`, owner `health`. Ledger state is open → active → complete;
`dispatch=failed` remains in revisions 2–10 with the same handoff/board-post
failure. Owner `[taking]` appears at 14:02:38. The `[done]` at 14:04:37 names
artifact
`/home/mesh-home/lte-workstation/docs/task-receipts/health-warning-b6a7bfd3c502b3157a0f-triage-20260913.md`
and SHA-256
`77ebd502ee7b5b3d864dd1870af13f220b0468cb071a3f5957036bfe2a0588ba`; ledger
revisions 9 and 10 carry the same path/hash and complete status.

Discrepancy: same as chain 2: the work is complete in the ledger but the failed
dispatch remains unresolved. The board also emits a generic `task:mesh-home`
completion at 14:06:04 rather than an exact chain closure.

### 4. `health-warning/4ffcd9cbfa5307a1234e` — 1 step

Step `triage`, owner `health`. Revisions 1–6 remain `open`; every visible
dispatch is `failed`, with repeated “handoff or board task post failed”. There is
no owner `[taking]`, artifact, progress field, result, or verification. The
13:51:53 source event is a health warning about an unobservable held composer;
the ledger correctly does not claim completion.

Discrepancy: the task is repeatedly retried in the ledger without a typed owner
start or a settled reject/block result. Evidence supports “open and failed to
dispatch”, not “done”.

### 5. `room-revival-ledger-reconciliation-20260913` — 2 steps

Latest visible ledger revision is 2, chain `open`, `dispatch=sent`; both steps
are open and have no progress, artifact, result, or verification:

1. `reconcile-room-revival-holds` — owner `health`.
2. `verify-and-settle-revival-resolvers` — owner `adint`.

The witness posted the first task at 14:06:49 and the ledger records dispatch at
14:06:55. No owner `[taking]` occurs in the range. The descriptions contain
observations about `mesh-room-gigaam.service` and `room-transcript.txt`, but
those are task context, not verification of either step.

Discrepancy: dispatched/open is correctly distinguished from started/done, but
the chain has no owner progress or artifact before the range ends.

### 6. `tinyfleet-drift-prerequisites-20260913` — 5 steps

Owner mapping is `haunt` for steps 0, 1, 2, and 4; `vpn` for step 3. The range
shows step 0 complete and step 1 complete, with current step 2 active in the
latest revision; steps 2–4 remain open/active as applicable.

1. `register-v2-generative-run` — `haunt`, done. Artifact path
   `/home/mesh-home/tiny-fleet/docs/task-receipts/haunt-generative-v2-preregistration-blocked-20260913.md`,
   SHA-256 `a6cc96d5ec90947b374f4863d3d9ed6ce48b9bcef9ff6e036ddad0030d9b40eb`.
   Result explicitly says generation was blocked and no inference/score ran.
2. `preflight-v2-behavioral-snapshots` — `haunt`, done. Artifact path
   `/home/mesh-home/tiny-fleet/docs/task-receipts/haunt-behavioral-preflight-v2-20260913.md`,
   SHA-256 `b87b993c79c43c6e8b766b99f6bd1b43c83f2a2c134cf429513644316dc9771c`.
   Result says three suites pass and three exact arms are blocked; commit
   `860fe79` is named as the log/environment capture.
3. `register-v2-scoreblind-ground-truth` — `haunt`, latest ledger state active,
   owner `[taking]` at 14:09:48; no artifact or verification yet.
4. `independently-verify-v2-ground-truth` — `vpn`, open; no artifact or
   verification.
5. `final-v2-gate-audit-and-recovery` — `haunt`, open; no artifact or
   verification.

Discrepancy: revision 8 records `dispatch=pending` immediately after the prior
step's completion, while revisions 9–11 show `dispatch=sent` and active owner
progress. This is a transient routing-state correction, not evidence of a lost
step. More materially, step 1 is marked done despite its result retaining three
blocked arms; that is acceptable only as partial/preflight completion, not as
evidence that the full prerequisite chain is complete. The record does keep the
blocker explicit.

### 7. `unblock/genome/ab3765c3fb53411c` and `unblock/genome/d6c01f0819aacad3`

`unblock/genome/ab3765c3fb53411c/resolve` — owner `genome` — has owner taking,
then done, artifact
`/home/mesh-home/lte-workstation/docs/task-receipts/unblock-genome-ab3765c3fb53411c-resolve-20260913.md`,
SHA-256 `bf3b6ba4684ed38a0eb62412dfa31b4d1f1aaba087560dab758c484fba7c1c6a`,
and ledger complete. Its result explicitly says the parent retirement remains
blocked; therefore the resolver completion must not be read as parent completion.

`unblock/genome/d6c01f0819aacad3/resolve` — owner `genome`, one open step. The
range shows `dispatch=pending` revision 1, then `dispatch=sent` revision 2 and a
board task at 14:10:45. There is no owner taking, progress, artifact, or
verification. This is correct open routing evidence, but not start evidence.

## Discrepancy register

1. **Failed dispatch left attached to completed work (2 chains).** Chains
   `health-warning/45d0...` and `health-warning/b6a7...` reach structured
   completion with verified-looking artifact fields while `dispatch=failed`
   persists through the final visible revisions. Evidence: ledger revisions and
   exact hashes above. Inference: the work may have been completed locally, but
   the required board/task delivery was not demonstrably repaired.
2. **Failed dispatch left open and retried without settlement (2 chains).**
   `health-warning/4ff...` and the earlier visible revisions of `b6a...` show
   repeated failed dispatch. Only `b6a...` later acquires an owner and closes;
   `4ff...` remains open with no owner start/artifact.
3. **Dispatch is repeatedly used without start evidence (3 chains/steps).**
   The v2 implementation chain, room-revival chain, and d6c01 unblock chain are
   sent/dispatched and open, but no owner-authored taking transition is visible
   for those exact steps in this range. This is a ledger correctness gap, not
   proof of owner inactivity outside the range.
4. **Generic completion lines do not close exact chains (3 health events).**
   Board `[done]` lines at 14:01:01 and 14:06:04 use `task:mesh-home`; the
   structured records are the exact chain closure. The generic lines therefore
   cannot independently verify chain identity.
5. **Parent/child boundary is explicit and correct in one case.** The genome
   resolver says its parent remains blocked. Treating that resolver's done line
   as parent completion would be an inference contradicted by the artifact text.
6. **Two unrelated `mesh-land` done lines are not task-ledger closures.** The
   `test-arith32` lines at 13:59:39 and 14:00:30 lack exact task-chain IDs,
   artifact hashes, and matching ledger records in this range; they should not
   be counted as completed chain steps.

## Verification limits

The range itself provides claimed artifact hashes, but this audit did not mutate
or claim any task and does not treat a claim as a successful file read. To turn
each hash claim into independently checkable verification, run `sha256sum` on
the named receipt paths and compare byte-for-byte. No substrate, board, or task
ledger changes were made by this review.
