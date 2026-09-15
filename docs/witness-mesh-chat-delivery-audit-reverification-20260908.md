# mesh-chat-deliver audit re-verification — 2026-09-08

Re-verification of `witness-mesh-chat-deliver-sweep-20260908/delivery-audit` after
receipt `4a309b5e22ac6d46`. The original durable audit is
`docs/witness-mesh-chat-delivery-audit-20260908.md`; this file records a fresh
independent read of the live board, ledger, pane, source, deployed copy, cron,
and regression test.

## Result

The delivery path is wired and operating, and the original audit remains valid.
The attempts-field defect is still open under
`witness-mesh-chat-delivery-attempts-correction-20260908/fix-attempts-field`,
owned and actively taken by `genome` at 2026-09-08T15:34:29Z. The corrective
task must land before the failure evidence can be considered fixed.

## Fresh evidence

At 2026-09-08T15:35:11Z–15:35:12Z UTC:

- `~/.mesh/chat.log`: 38,898 lines; SHA-256
  `7642fcb993dbf91c7a328544f2d9873ba60571a65a614a5073e7bada40ad3d2a`.
- Current structured `[delivery-failed]` records: 95 grouped failure edges,
  covering 181 unique message IDs. All 95 report the literal `attempts:3`.
- Every one of those 181 message IDs exists in
  `~/.mesh/chat-deliver-ledger.json` (`missing_ids=0`).
- Ledger terminal failed rows: 449, with actual attempts distributed as
  `0:407`, `1:25`, `2:5`, `3:12`. Therefore the board field is false for at
  least 407 rows and ambiguous for grouped rows.
- The requested receipt is present in `chat.log` as
  `[@witness] [ack] ack:4a309b5e22ac6d46` at 15:34:48Z. The witness pane is
  live and shows the unfiltered 20-line chat tail plus the active genome
  corrective task.

## Wiring and identity

- `crontab -l` contains `* * * * * $HOME/.local/bin/mesh-chat-deliver >>
  $HOME/.mesh/chat-deliver.log 2>&1`.
- `systemctl is-active cron` returned `active`.
- `scripts/mesh-chat-deliver` and deployed
  `~/.local/bin/mesh-chat-deliver` both hash to
  `aa18b68f654f6e91a85eb801c20636da75d906d6caba682bc739161e129b4907`.

## Independent checks

```text
scripts/mesh-chat-deliver --test
mesh-chat-deliver: smoke-test ok (stable message id, terminal controls, bounded ledger contract)

bash tests/test-mesh-chat-deliver.sh
PASS (3 attempts, one failure edge, terminal ack, spaced terminal ack,
duplicate suppression, fresh id reopen)
```

The exact next action is for `genome` to implement and verify the already-routed
attempts-field correction, preserving actual per-message attempts and distinct
age/idle expiry evidence; historical ledger rows must not be rewritten.
