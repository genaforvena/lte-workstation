# Corrected evidence-repair receipt — 2026-09-08

- Task: `recreated-rejected-20260908-06-corrected/evidence-repair`
- Owner: `hire`
- Captured: `2026-09-08T14:43:54Z`
- Disposition: replacement evidence is durable and independently hashable; historical bytes are
  missing and remain `UNKNOWN/unverifiable`.

## Historical evidence status

The predecessor cited these historical files, and each was checked at capture time:

```text
MISSING /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-10.md
MISSING /tmp/discover-upower-20260907T231541Z.txt
MISSING /tmp/discover-battery-20260907T214713Z.txt
```

Their contents were not reconstructed, re-created, or represented as recovered. The absence of
those bytes means the historical claims cannot be revalidated from this receipt.

## Durable replacement

The current replacement target is the existing bounded-fixture receipt:

```text
path: /home/mesh-home/lte-workstation/docs/task-receipts/05-bounded-test-fixture-20260908.md
size: 1552 bytes
sha256: 97ed951f840c692671be3c0c964b7b65de064e5ab85c18f36356f0379ef3a9da
mtime: 2026-09-08 12:18:14.819291255 +0000
```

Its durable promotion is also recorded by:

```text
path: /home/mesh-home/lte-workstation/docs/task-receipts/06-durable-evidence-receipt-20260908.md
sha256: 669e1a6ae14776e18442862dfb8f1d471bc42e9c1c50bc6a08676d27fd79d779
```

## Provenance and verification

```text
checkout_revision: d6db2f013cc52ea7908c66b0ee1b25f89bedbc1e
boot_id: b8fffc75-dd9b-41df-86cf-485c16bab89e
boot_time: 2026-09-07T23:18:36Z
```

At capture, `stat`, `sha256sum`, and existence checks were run against both durable receipt paths
and the three historical paths above. This receipt is a replacement observation, not a claim that
the vanished historical artifacts were recovered.
