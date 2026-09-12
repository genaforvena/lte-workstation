# Chat log integrity review: physical line 56120

Reviewed 2026-09-12. The raw local row is preserved byte-for-byte in
[`witness-chat-range-review-near-56034-56125-log-integrity.raw`](witness-chat-range-review-near-56034-56125-log-integrity.raw): 734 bytes, SHA-256
`df10f734a615222fa866d36091287f8c60e4a64cc7551d9de3bcebd394bcd983`. The canonical
`~/.mesh/chat.log` was not edited. The row contains a phaedra `device-churn` message ending at
`device-age-vs-up`, immediately followed by a second timestamped phaedra `fail2ban-watch` record.

The nearest preserved local snapshot, `~/.mesh/board-snapshots/chat-20260912T114525.860322516Z.log`,
was written at 11:45:24Z with 56,080 rows; it contains no joined row. The current canonical row is
physical line 56,120. The sync tape records 56,109 converged rows and zero gained at 11:48Z, then
56,120 rows and one gained at 11:51Z, followed by zero gained at 11:54Z. This places the row's first
observed local appearance at the sync boundary, but `chat-sync.log` records counts rather than the
peer label or raw response, so it cannot identify which peer supplied these bytes.

At inspection time phaedra's current `~/.mesh/chat.log` contained the device-churn post as a valid
separate row (physical line 2,874) and no occurrence of the joined seam. That is current-state
evidence only; no retained local or phaedra snapshot preserving the malformed row at the 11:51Z pull
was found. The sync path in
`scripts/mesh-chat-sync` appends each peer response to its candidate, sorts rows, then retains any
line beginning with a board timestamp; it does not create or log peer-attributed raw rows. The
`scripts/mesh-chat` writer's `append_log` emits one newline-terminated row under its lock, but the
available evidence cannot rule out a malformed body supplied to that writer on some peer before
the sync.

Finding: the defect entered this node through a sync round; whether it was already malformed in the
peer's stored board or changed in transit cannot now be established. No historical source bytes
survive to prove a responsible writer or transport stage. No history was rewritten. No code guard was
added: the board body is free text and may legitimately quote another timestamped board row, so a
generic embedded-header rejection would change valid message behavior without a demonstrated source
contract. The bounded next diagnostic, if this recurs, is to preserve each successful peer response
before candidate concatenation, keyed by peer and round, and compare its hash/row with the local
snapshot. That will distinguish source corruption from merge-input corruption before a guard is
chosen.

Verification: compared the saved raw-row hash with the extracted canonical row; checked the 11:45Z
snapshot and 11:48Z–11:54Z sync records; read `scripts/mesh-chat`'s append path and
`scripts/mesh-chat-sync`'s peer-ingest path; queried phaedra read-only over SSH. The live board and
all existing snapshots remain intact.

The following code-block line is the 734-byte source row verbatim (including its final newline):
```
2026-09-11T10:30:07Z  device-churn@phaedra  ::  [fyi] device-churn on phaedra: 2026-09-11T10:30:04Z CHURN delta=6 interval=302s total-since-boot=16137 uptime=7844693s boot=e42f5e4e baseline=16131 candidates=none :: 6 device uevent(s) in the last 302s — the idle floor here is 0, so this is a real enumeration event, invisible to every level instrument (URB balance, xhci ring, rf_dump, runtime_*) which are all back to healthy by now. seqnum names NO device || candidates come from device-age-vs-up2026-08-22T17:50:22Z  fail2ban-watch@phaedra  ::  [fyi] mesh-fail2ban-watch: phaedra — repeat-offender 2.57.122.150: 3 bans in last 6h (scripted retry across ban/expiry cycles, not noise); jail=sshd. tape ~/.mesh/fail2ban-watch.log
```
