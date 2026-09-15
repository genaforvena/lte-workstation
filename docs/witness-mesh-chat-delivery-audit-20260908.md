# mesh-chat-deliver delivery audit — 2026-09-08

Audit task: `witness-mesh-chat-deliver-sweep-20260908/delivery-audit`
Audited at: 2026-09-08T15:28Z (UTC), on `mesh-home`

## Verdict

The task was live and correctly specified. The delivery reflex is live and
executing, but its failure records have an evidence-quality defect: the board
failure edge says `attempts:3` (the configured maximum) while the durable
ledger records the actual attempt count. Of 445 terminal `failed` ledger rows,
403 have zero attempts, 25 have one, 5 have two, and 12 have three. This is
not a stale task and is not repaired by this audit; the mismatch must remain
visible for a corrective implementation task.

## Reconciliation

The append-only `~/.mesh/chat.log` contains 273 messages emitted by
`mesh-home/mesh-chat-deliver@mesh-home` with `[delivery-failed]`; all 273
message IDs are unique and every ID exists in
`~/.mesh/chat-deliver-ledger.json`. The failure edges cover targets as
follows: witness 118, genome 44, tg 40, job 29, hire 24, discover 8, haunt 6,
sound 3, wake 1. In the current 14:00Z–15:28Z window there are 27 edges (hire
15, job 12); since 15:00Z there are 6 (job 4, hire 2).

For target `witness`, the source/ledger reconciliation is 426 historical
targeted records: 261 `acked`, 159 `failed`, and 4 `expired-preledger`.
The two current audit task posts are intentionally absent from the delivery
ledger because they are the newly-created task lines, not delivery attempts.
The receipt evidence is the 261 matching `[ack] ack:<message-id>` records in
`chat.log`; the live witness pane showed the task as `RUNNING` with lease
until 2026-09-08T15:57:28Z and a live footer at 15:27:37Z.

The latest failure example is for `msg:f95259f27dd134ae`, emitted at
15:26:02Z with board text `attempts:3`; its ledger row has status `failed` and
`attempts:0`. The same pattern holds for the other latest failure edges,
except rows that had genuinely received one or more delivery attempts.

## Live wiring and code identity

* `crontab -l` contains `* * * * * $HOME/.local/bin/mesh-chat-deliver >>
  $HOME/.mesh/chat-deliver.log 2>&1` (autowired 2026-07-14).
* `cron` is active, and `~/.mesh/chat-deliver.log` mtime was
  `2026-09-08 15:26:42Z`, with a successful delivery at that time.
* `command -v mesh-chat-deliver` resolves to
  `~/.local/bin/mesh-chat-deliver`, whose realpath is
  `scripts/mesh-chat-deliver`; both copies have SHA-256
  `aa18b68f654f6e91a85eb801c20636da75d906d6caba682bc739161e129b4907`.
* The source reflex declares `reflex-cadence: * * * * *`, uses an exclusive
  lock, persists its ledger atomically with `os.replace`, emits delivery
  attempts to `chat-deliver.log`, and writes terminal failure edges only after
  `mesh-chat --to <sender>` succeeds.

## Independent verification

The following checks were run after the reconciliation:

```text
scripts/mesh-chat-deliver --test
mesh-chat-deliver smoke-test ok (stable message id, terminal controls, bounded ledger contract)

tests/test-mesh-chat-deliver.sh
PASS (3 attempts, one failure edge, terminal ack, spaced terminal ack, duplicate suppression, fresh id reopen)

systemctl is-active cron
active
```

The artifact was then checked independently against the live files: all 273
failure IDs resolved in the ledger, the source/deployed hashes matched, and
the target/status counts above were recomputed from fresh reads of
`chat.log` and `chat-deliver-ledger.json`.

Evidence inputs at audit time:

```text
chat.log sha256       8523583de2115117d1d6ae8a8d22d1f52ec2e509260387026ec26fe6273e5617
chat-deliver-ledger   aa1327a330804262a8c7163feac25b019224225b992da43b3829206733e2578f
chat-deliver.log      5fc129dcc1f0670bff07d82de0840ec7c71e88f7ce5bc1c57681e0387e3c6a48
```

Next action: open a corrective implementation/audit task for the misleading
failure `attempts` field, preserving the distinction between attempted
delivery and age/idle expiry.
