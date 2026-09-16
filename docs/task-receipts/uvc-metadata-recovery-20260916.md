# UVC metadata recovery — 2026-09-16

Parent task: `uvc-metadata-recovery-20260916/recover-uvc-metadata`
Retry edge: `event:adint-receipt-20260916T0952Z`

The dependent unblock receipt
`docs/task-receipts/unblock-adint-613b51dc77b7aa12-resolve-20260916.md` supplied a
fresh real `/dev/video1` read and justified this retry. The parent was resumed at
2026-09-16T09:56:13Z.

Verification:

```text
timeout 100s scripts/mesh-uvc-metadata --test
exit=0
smoke-test: ok (real one-buffer metadata read: 5852 bytes, 266 timestamped records from /dev/video1)

timeout 100s scripts/mesh-uvc-metadata
exit=0
mesh-uvc-metadata: captured 5852 bytes from /dev/video1 -> ~/.mesh/uvc-metadata/latest.bin and ~/.mesh/uvc-metadata/latest.jsonl (attempt 1/10)

independent JSONL parse of ~/.mesh/uvc-metadata/latest.jsonl
exit=0; records=266

mesh-card --refresh
exit=0; capability map includes uvc-metadata
```

Fresh production artifacts at 2026-09-16T09:57:01Z:

```text
~/.mesh/uvc-metadata/latest.bin     5852 bytes  sha256=55183af580826ca613e1cdacb4d7246be2af93a577ff7cd805dc52091abbb86b
~/.mesh/uvc-metadata/latest.jsonl  32452 bytes  sha256=6005d25f9cfb8b723084c703fd38b748bcfb0bd1a519aee75a735d9686c84ce3
```

Result: PASS — the real hardware read and production refresh both succeeded,
and the retained JSONL parses into 266 records. The prior UVC capability block is
resolved; no code, routing, or substrate change was made.
