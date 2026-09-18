# Receipt: batch-test-forgery-filing (witness-chat-range-review-near-69444-69529-f1)

Task: file batched digests instead of one task per tool (5 [task] rows in 5s,
chat.log 694xx, plus 146 queued backlog).

## Finding
`scripts/mesh-test-forgery` already carried a per-sweep budget (`TASK_CAP=5`,
queue `$TASK_QUEUE`, drain-on-clean-pass) but still filed one `[task]` board
row PER TOOL. At 151 findings that is 30 sweeps of board-filling rows.

## Change (scripts/mesh-test-forgery only)
- Route section (B) now files ONE `[task] test-forgery/batch-N-tools-...`
  per sweep, naming up to `$TASK_CAP` tools inline with per-tool tape
  evidence (`tool[log1,log2]`), owned by `genome`, which fans out per-tool fixes.
- Queue/drain/backfill/edge-only semantics unchanged; pending-overflow `[fyi]`
  now says "the next sweep files the next batch".
- Digest `[fyi]` text updated ("one batched routed job ... follows per sweep").

## Verification
- `bash scripts/mesh-test-forgery --test` → rc=0, zero FAIL (log:
  /tmp/opencode/forgery-test2.log).
- Mutant (batch `[task]` emission muted): rc=1 with ROUTE + BUDGET + DRAIN(x4)
  + BACKFILL FAIL — gates are non-vacuous (log:
  /tmp/opencode/forgery-mutant.log).
- Landed as commit in main worktree; unrelated staged
  `scripts/mesh-chat.findings.json` left untouched.
