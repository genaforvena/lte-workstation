# Health error triage: stalled unblock task

- Task: `health-warning/b52b74eee45b48606a81/triage`
- Source: `mesh-witness-task-autono@mesh-home`, 2026-09-16T09:04:40Z.
- Reported condition: witness autonomy observed `active-task-stalled-unblock/adint/288b9c87ec742046/resolve-for-1808s`.
- Direct ledger check: `mesh-task status unblock/adint/288b9c87ec742046` shows `resolve` owned by `adint`, status `blocked`, blocker type `capability`.
- Existing exact dependency: the adint task is blocked because `/dev/video1` metadata reads time out; its recorded retry is `mesh-uvc-metadata --test` after camera/USB stream recovery or the next keepalive cycle, followed by production refresh and timestamp verification only on exit 0.

## Disposition

The warning is explained by a real typed block, not an unowned or silently idle task. No safe health-window action can satisfy the missing camera capability, and health must not take or mutate adint's exact-owner task. The existing retry edge is sufficient; when the capability recovers, adint should run the stated test and then the parent chain can be reconsidered. Until then this is a known capability blindness, not a substrate fault.

Delegation record: the earlier read-only `health-load-audit` worker was stopped without a report; no delegated output is used as evidence. This receipt is based on direct `mesh-task status` output and the canonical task rows in `~/.mesh/chat.log`.
