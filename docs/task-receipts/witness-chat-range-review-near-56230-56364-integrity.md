# Chat log integrity trace: physical row 56425

Reviewed 2026-09-12 against the canonical `~/.mesh/chat.log`, the local chat-sync tape, the current
`mesh-chat-sync` source, and the preceding malformed-row investigation. The board was read only.

## Preserved source bytes

Physical row 56425 is preserved byte-for-byte, including its final newline, in
[`witness-chat-range-review-near-56230-56364-integrity.raw`](witness-chat-range-review-near-56230-56364-integrity.raw).
It is 566 bytes with SHA-256
`f50de7c2a5b57c9ccff60a8c02d914e6672b3ac8a5e16e298b5ac1ba7b787fb2`. The source board was not
modified.

The row begins `2026-08-23T17:20:06Z  tg-in2026-08-22T18:30:08Z  tg-inbound@phaedra`. The first
record's sender is truncated at `tg-in` and directly joined to a second timestamp; the next sender
then appears as another token before `::`. This fails the production message grammar in
`scripts/mesh-chat-range-review` (`MESSAGE_RE`), which expects one timestamp, one author token, then
`::`.

## Comparison and origin evidence

The task-provided comparison hash for valid physical row 18820,
`3cdc92b4be7d8b186e8d800440172c2c584b476033c364cdc8b9cb92c72cd6aa`, matches that row's bytes
without its final newline. Including the newline, row 18820 is 539 bytes and hashes to
`8f7ca309d6e3a51158842d1c1ca84adf2d67d45d1829a43e8b52e702fe8db494`. It is a valid 2026-08-23
NOEAR post from `tg-inbound@phaedra` with the same leading timestamp and same first-message text;
row 56425 diverges at the sender, before its second timestamp and the later 2026-08-22 NOEAR post.
This is evidence of the same record-boundary symptom as the earlier joined/truncated row 56120 and
the timestamp-prefix defects at rows 56183 and 56210.

`~/.mesh/chat-sync.log` records 56,410 converged lines at 12:42Z, then one peer board merged and
one new line gained at 12:45Z, with 56,425 lines converged. The next recorded round, 12:48Z, ends
at 56,431 lines. These aggregate counters show a possible observation window, but do not identify
row 56425 as the gained line or identify which peer supplied it. The tape records neither raw peer
responses keyed by peer and round nor a pre-round source snapshot containing the row. Thus it cannot
establish whether this row was already malformed upstream or was damaged during a source append,
transport, or an earlier merge. The current sync path pulls peer output, unions whole lines, and
sorts/deduplicates; no current operation edits bytes within a retained row. That does not establish
the incident-time path.

The prior receipt, [`witness-chat-range-review-near-56126-56227-integrity.md`](witness-chat-range-review-near-56126-56227-integrity.md),
reached the same evidentiary limit for the three earlier defects: they appeared at sync-round
boundaries, but the historical peer response and incident-time writer bytes were not retained. Row
56425 supports the same *symptom* (record-boundary truncation/join); the available evidence does not
prove the same underlying cause. No history rewrite or regression guard was added because no
corrupting ingestion boundary is proven. For a future occurrence, retain each successful peer
response under its peer and sync-round identity alongside the pre-round local snapshot before merge.

## Verification

- Extracted source row 56425 byte-for-byte and verified the companion's size and SHA-256 against the
  canonical board.
- Verified row 18820 with and without its final newline; the supplied task hash is the no-newline
  digest.
- Confirmed row 56425 fails `MESSAGE_RE` and inspected the current merge path and sync summaries.
- No source-board edit, history rewrite, or source-code change was made.
