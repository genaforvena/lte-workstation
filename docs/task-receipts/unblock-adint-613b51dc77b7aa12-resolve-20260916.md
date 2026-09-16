# UVC metadata unblock receipt — 2026-09-16

Task: `unblock/adint/613b51dc77b7aa12/resolve`

The blocker was a transient inability to read `/dev/video1` UVC metadata. No code
or wiring change was needed. The narrow retry was run locally after the camera/USB
stream became available:

```text
scripts/mesh-uvc-metadata --test
smoke-test: ok (real one-buffer metadata read: 5852 bytes, 266 timestamped records from /dev/video1)

scripts/mesh-uvc-metadata
mesh-uvc-metadata: captured 2530 bytes from /dev/video1 -> /home/mesh-home/.mesh/uvc-metadata/latest.bin and /home/mesh-home/.mesh/uvc-metadata/latest.jsonl (attempt 1/10)
```

Fresh retained artifacts:

```text
/home/mesh-home/.mesh/uvc-metadata/latest.bin     2530 bytes
/home/mesh-home/.mesh/uvc-metadata/latest.jsonl  13915 bytes
```

Independent parse verification produced 115 JSONL records from `latest.bin`.
SHA-256: `latest.bin` = `470e07951dcf6234c6c70a2cbd517b0ccdab5d32019c8c9e9d0272f5a9a052a1`;
`latest.jsonl` = `a9af65f40bd650b2f3262fc38117ed4e26575a498b79fc8b487e3331cef7f914`.

Delegation: none; this was a tightly coupled hardware retry plus ownership/ledger
settlement, kept in the adint mind. Personally inspected the executable, the fresh
artifact sizes/hashes, and the independent parser output.
