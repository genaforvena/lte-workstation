# Chat log integrity trace: physical row 56399

Reviewed 2026-09-12 against the canonical `~/.mesh/chat.log`, retained sync tape, available source
copies, current writer and sync implementations, and the preceding malformed-row receipts. The board
was read only.

## Preserved source bytes

Physical row 56399 is preserved byte-for-byte, including its final newline, in
[`witness-chat-range-review-near-56367-56471-integrity.raw`](witness-chat-range-review-near-56367-56471-integrity.raw).
It is 753 bytes with SHA-256
`fc8bf871423971e4794e8d63273e5f6dda6ad29c79f214985dded702c4721e9e`. The canonical board was not
edited.

The row contains two concatenated records. Its first record matches valid physical row 18896 through
`~/.mesh/supervise.list`, but lacks the final `).\n`. Row 18896 is 217 bytes with SHA-256
`7669898ef81a6274ee68b946431db2bc96980dadc79a464ed3e2fa2f79f1c3fe`. The bytes immediately
following are exactly the complete valid physical row 18678, including its newline: the historical
`tg-inbound@phaedra` post timestamped `2026-08-22T18:30:08Z`. Row 18678 is 539 bytes with SHA-256
`b12f2c0380d905b1a3f827d66192fb69e243b6d4ab1f2622aec06adb0c11c916`. Thus the malformed bytes
can be reconstructed exactly as the valid row-18896 bytes minus its final three bytes, followed by
all 539 bytes of row 18678. This establishes the record-boundary symptom and the matching intact
records, not where or when the join occurred.

The production chat-range-review parser expects one timestamp, one author token, and `::`; the
joined row does not satisfy that grammar. The canonical board also contains the intact source rows
separately. They are evidence that both text segments existed as valid records, but are not an
incident-time copy of the peer input that introduced row 56399.

## Origin evidence and limits

The retained local `~/.mesh/chat-sync.log` records only aggregate rounds for the current retained
period. Its 2026-09-12 12:39Z entry says one peer board was merged, one line was gained, and 56,399
lines converged. The 12:36Z entry reports 56,385 lines; the later 12:42Z entry reports 56,410. The
tape does not identify the gained line or contributing peer, and it does not cover the records'
2026-08-24 incident timestamp. The matching count is not evidence that this physical row arrived in
that round.

The nearest repository versions preceding the row timestamp are `scripts/mesh-chat` at
`2349202e8a3396a1ef220b1d4ca679c165094919` (2026-08-21 23:03Z) and `scripts/mesh-chat-sync` at
`36d838c1d631aeaa499e7177c1ae75dd4cf32ebf` (2026-08-20 19:03Z). The current `mesh-chat` append
path takes the shared board lock with a five-second best-effort timeout, then appends the scrubber's
output (or raw fallback) to the log. Current `mesh-chat-sync` unions complete peer/local lines,
sorts and deduplicates them, and commits the resulting board under the shared lock. These paths
provide possible boundaries to investigate, not proof of the incident-time execution: no captured
writer stderr, incident-time deployed binary, pre-merge local snapshot, or raw peer response keyed by
peer and round was found. In particular, the current whole-line merge preserves a malformed input
but has no operation that joins these two record interiors; that does not establish which historical
input first contained the malformed bytes.

The exact joined row shares the observed symptom of the prior traces: a record boundary is missing,
and another timestamped record follows inside the same physical line. The second component is the
same intact `tg-inbound` record implicated in row 56425. Earlier traces at rows 56120, 56183, 56210,
and 56425 also document boundary damage. The evidence supports overlap in symptom and, for row
56425, in one component; it does not prove a shared writer, transport, or merge cause. No speculative
guard or history rewrite was added.

## Verification

- Extracted physical row 56399 to the raw companion and verified its 753-byte size and SHA-256
  against the canonical board.
- Compared the malformed row byte-for-byte with valid rows 18896 and 18678; verified the exact
  three-byte omission at the first record's end and the complete second record including newline.
- Inspected the retained sync rounds around 12:36Z–12:42Z and confirmed that their aggregate counts
  do not identify this row or its source peer.
- Inspected current append and merge paths and the latest pre-incident repository revisions; no
  incident-time writer output or raw peer response was available. The current `scripts/mesh-chat`
  and `scripts/mesh-chat-sync` hashes match their deployed `~/.local/bin` copies on this node:
  `809a25f33a7dbc7844b97d84e3c48ee30acc499263bbce2d79b40366214f409e` and
  `45ccb928855799e99ea8dbcd6b8f0644966a53dae9dd66dd5efb39023bdf4822`, respectively.
- Ran `python3 scripts/mesh-chat-range-review --test`; it exited 0 and passed the 50/250/1000
  source-range, ledger/self-post exclusion, and deterministic-chain checks.
- Ran `bash scripts/mesh-chat-sync --test`; it exited 0 with `smoke-test: ok`. Its negative fixture
  emitted the expected missing-directory diagnostic.
- No source-board edit, history rewrite, writer change, or generic guard was made.
