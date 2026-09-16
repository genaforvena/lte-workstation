# Witness review: physical lines 65534–65921

Task: `witness-chat-range-review-medium-65534-65921/review`  
Scope: read-only review of `~/.mesh/chat.log` physical lines 65534–65921 using the production predicate in `scripts/mesh-chat-range-review`.

## Scope and predicate result

The production predicate is `MESSAGE_RE` plus `is_source_message`: a row must match the timestamp/author/`::` format, must not start with `[task-state]` or `[task-ledger]`, and must not contain `witness-chat-range-review-`. Running the equivalent extraction over the requested physical interval returned exactly 250 accepted source messages, with first accepted line 65534 and last accepted line 65921. The interval therefore satisfies the task's “exactly 250 source messages” constraint.

## Current ownership and task state

The task journal records the chain as `OPEN_UNOWNED` with owner `witness` and `dispatch=sent` (the journal is a historical intake record). A fresh `mesh-task replay --json` read at review time is authoritative for current state: the chain is `status=active`, `owner=witness`, `current=0`, `started=2026-09-15T23:20:42Z`, and leased through `2026-09-15T23:50:42Z`. No claim, reassignment, completion, rejection, or board post was performed by this review.

## Findings

### 1. Observation/autonomy backlog is repeatedly failing while work remains unfinished

Evidence: the range contains 15 `mesh-witness-task-autono` health-fail rows, including lines 65534 (`unfinished=98`, `blocked=59`, `dispatchable=3`), 65881 (`unfinished=114`, `blocked=59`, `dispatchable=4`), 65893 (`unfinished=115`), and 65902 (`unfinished=116`). The reported errors repeatedly include `analyze-observation-for-*` (for example lines 65818, 65820, 65823, 65825, 65829, 65831, 65833, 65835, 65838, 65840, 65842, 65844, 65847, 65849, 65854, 65856, 65861, 65868, 65872, 65874, 65878, 65881, 65883, 65893, 65895, 65902, and 65905).

The range also has 32 observation-related task/error references and three explicit `OPEN_UNOWNED` task observations (65566, 65573, 65581). This is evidence of a repeated queue/ownership or dispatch-follow-through problem, not proof that every referenced task is invalid. The appropriate owner should reconcile the exact observation chains against the task ledger, publish a bounded backlog inventory, and verify dispatch/lease transitions independently; do not infer completion from a `[done]` board line alone.

### 2. Completion artifacts are present, but autoland creates a second open obligation

Evidence: lines 65541/65546/65558/65568 show completed health or genome work with receipt paths and SHA-256 values; lines 65543, 65548, 65560, 65570, and many later lines create `autoland/...` tasks for genome. The same pattern is visible at lines 65909, 65916, and 65920 where `land@phaedra` reports autoland refusal because a parked autostash blocks rebase.

Independent artifact checks performed during this review found these referenced receipts present:

| Artifact | SHA-256 observed | Source evidence |
|---|---|---|
| `docs/task-receipts/health-warning-099c6d7b9da9ea96921e-triage-20260914.md` | `0f734beb65d9f2339a8c98adb3f56db7a53bb513eeeee961e859b873e64b6ed8` | line 65541 |
| `docs/task-receipts/genome-file-table-live-verification-20260914.md` | `5e8cdabdb7034e0ac238c429e4f5ba92775784e266dc7224412c42fd4bb886f7` | line 65546 |
| `docs/task-receipts/health-warning-c3fa3f92ca12a525ee97-triage-20260914.md` | `c555dd368cce3afe75c308147e59e11fabae58fba5729d6cc84f2525036d84fe` | line 65558 |
| `docs/task-receipts/health-warning-39c87c2ae290326e29c6-triage-20260914.md` | `dd85b8002b62f2fba2957e3cd7675a5214c3c58f95441028fe04d4c8218c056b` | line 65568 |

The artifact side is therefore verifiable for these examples. The unresolved risk is the landing path: repeated autoland tasks and explicit stale-autostash refusals show that “receipt exists” and “receipt is landed/settled” are separate states. Genome/land should reconcile the exact open autoland chain and parked stash before creating more duplicate landing work.

### 3. Connectivity and sensor evidence has genuine gaps and must remain distinct from task backlog claims

Evidence: lines 65535 and 65557 record phaedra mesh-down transitions; lines 65577, 65584, 65592, 65799, 65912, and 65913 report unreachable peers/nodes. Line 65789 records another mesh-down transition. Lines 65907 and 65914 independently report mesh-home off-tailnet and witness sensing stale/unknown values. These are concrete environmental/observability conditions, not sufficient evidence that the task system itself is broken.

The review recommendation is to preserve the distinction in future triage: cite the exact health/sensor artifact and its coverage interval, then separately cite task ownership and ledger state. Do not convert a partial sensor window or an unavailable host into a task completion or rejection verdict.

## Verification performed

Commands and results:

```text
python3 <production-predicate-equivalent-extractor>  # accepted=250, first=65534, last=65921
mesh-task replay --json | ...                       # chain status=active, owner=witness, current=0, dispatch=sent
sha256sum docs/task-receipts/{four referenced receipts}  # all four files present; hashes match source rows
```

The exact extractor used was an inline Python read-only check implementing the `MESSAGE_RE`, structural-row exclusion, and chain-prefix exclusion from `scripts/mesh-chat-range-review`; it reported `count 250`. The replay and checksum commands were read-only. No `mesh-task take`, `done`, `reject`, dispatch, `mesh-chat`, or board write was run.

## Receipt status

This receipt is the requested evidence artifact. Findings are recommendations only; no mesh task was claimed or settled, and no new task or board line was created.
