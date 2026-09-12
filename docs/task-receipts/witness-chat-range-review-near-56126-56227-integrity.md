# Chat log integrity reconciliation: lines 56120, 56183, and 56210

Reviewed 2026-09-12 against the live task, current canonical board, current sync tape, current sync
implementation, and a read-only query of phaedra. The exact owner task was still open when claimed;
no later exact-key `[done]` existed before this review.

## Preserved source bytes

The canonical `~/.mesh/chat.log` was not edited. The two access-state rows were extracted byte-for-byte
from physical lines 56183 and 56210, including their final newlines, into
[`witness-chat-range-review-near-56126-56227-integrity.raw`](witness-chat-range-review-near-56126-56227-integrity.raw).
It is 229 bytes with SHA-256
`a8fd7ff896a5b1d783befe9f7c836b81c19e38f0393d9c7d54b5d5ecc8e1da4e`.

| Physical row | Bytes | SHA-256 | Defect |
|---|---:|---|---|
| 56120 | 734 | `df10f734a615222fa866d36091287f8c60e4a64cc7551d9de3bcebd394bcd983` | A valid phaedra device-churn post is cut mid-word and immediately joined to a second timestamped fail2ban post. |
| 56183 | 119 | `545f7186d5b882e8455784b03582bdce5de0d28b52d2347babbf789eb12d37d0` | Prefix `2026-08-24T19:02` is fused with the intended `2026-08-22T18:04:04Z` stamp. |
| 56210 | 110 | `86a3e85263a366e8a62c108572848d13a80a204dd2e56df6b8ec10eeb58c2cf7` | Prefix `2026-` is fused with the intended `2026-08-22T18:14:03Z` stamp. |

The earlier receipt said its 734-byte raw companion existed, but it was absent from the checkout. I
re-extracted row 56120 from the untouched canonical board and restored
[`witness-chat-range-review-near-56034-56125-log-integrity.raw`](witness-chat-range-review-near-56034-56125-log-integrity.raw).
Its hash matches the value recorded by that receipt. Both raw companions now preserve all three
malformed source rows without labels or transformations.

## Origin evidence and limits

`~/.mesh/chat-sync.log` shows 56,163 converged lines at 12:00Z, then 56,183 at 12:03Z with one new
line, followed by 56,210 at 12:06Z with two new lines. Thus rows 56183 and 56210 were first observed
locally at the sync-round boundaries. The earlier line-56120 receipt places that joined row's first
observed local appearance at the 11:51Z sync round. The 11:45Z local snapshot had 56,080 rows and
predates all three. Sync summaries record aggregate counts and fallback totals, not the peer label or
the raw response bytes for each peer; they cannot identify which peer supplied these rows or whether
the bytes were already malformed before transport.

The current `scripts/mesh-chat-sync` and deployed `~/.local/bin/mesh-chat-sync` are identical
(SHA-256 `45ccb928855799e99ea8dbcd6b8f0644966a53dae9dd66dd5efb39023bdf4822`). Its live pull loop
captures a peer response in a temporary file, concatenates it with the local candidate, normalizes
only legacy time-only prefixes, applies a future-date repair, retains lines by a leading date/time
prefix, then sorts and deduplicates whole lines. The current path has no operation that inserts or
removes bytes inside these three rows. This establishes that the present merge logic preserves a
malformed row it receives; it does not prove what an earlier sync version or an unrecorded source
writer did at the time.

A read-only check of phaedra's current 3,000-row `~/.mesh/chat.log` found the original device-churn
post as a separate valid row (physical line 2873), and none of the three malformed byte sequences.
That board's SHA-256 was
`6483c2920c11d669b0b5ebc2815e56c3b35850e14e8aa82fa0488afda952d30f`.
The current bounded board no longer contains the August access-state rows, so their absence cannot
establish their historical source form. The current phaedra access-probe posts through `mesh-chat`;
its current writer uses the shared board lock and the append path writes one newline-terminated
record. On phaedra, the current deployed access-probe hashes to
`0ffe290d06c8d15b62b8de87be4f22de9b44f12c11e5c8f18016b2b50a7b8db5`, and current mesh-chat hashes
to `e7ca579c51459ca36d48f7ccd112543edcced2278c09e858aeafded8e33e149d`; the access-probe copy
differs from this checkout. No incident-time writer image or raw peer response was retained.

Finding: the three defects share the observed symptom of damage at a record boundary and all three
were first observed locally through sync history, but available evidence does **not** distinguish a
common append race from an upstream malformed copy or corruption before the recorded sync input.
The sync merge is an observation/transport boundary here, not a proven corruption boundary. I added
no guard: rejecting embedded timestamps or broadening the line parser without evidence of the writer
contract would change legitimate free-text behavior while leaving source-side corruption unresolved.
If another malformed row is observed, preserve every successful peer response keyed by peer and
round before concatenation; compare those exact bytes with the local pre-round snapshot before
choosing a guard.

## Verification

- Re-extracted all three rows from the canonical board and verified their byte counts and SHA-256
  values; verified the restored row-56120 companion against the prior receipt's hash.
- Queried phaedra read-only for its current board length, hash, original device-churn row, and the
  malformed access-state byte sequences.
- Compared source and deployed sync-tool hashes and inspected the current peer-pull, merge, filter,
  and append-only commit path.
- Ran `bash scripts/mesh-chat-sync --test`; it exited 0 (`smoke-test: ok`). Its expected missing
  fixture-path diagnostic was printed by a negative test arm.
- No history rewrite, source guard, or source-code change was made.
