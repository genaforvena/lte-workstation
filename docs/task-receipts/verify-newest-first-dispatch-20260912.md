# Newest-first mesh-task dispatch verification — 2026-09-12

The assigned board task was still open at 09:47:20Z (canonical chain `verify-newest-first-dispatch-20260912`, step `verify-newest-first-dispatch`, priority 0, owner `sound`). It was first in the sound queue immediately before it was claimed at 09:48:04Z.

Evidence:

- `rtk python3 tests/test-mesh-task-no-expiry.py TaskNoExpiryTests.test_default_dispatch_queue_uses_same_priority_order` — PASS (1 test). This existing focused test covers the default dispatch order's priority axis.
- A focused temporary fixture ran `scripts/mesh-task create` for two eligible `sound`, priority-0 tasks, then `scripts/mesh-task queue --dispatch --owner sound`. Observed order: `newer/new` then `older/old` — PASS for the newest-first tie-break.
- Replayed the canonical `~/.mesh/chat.log` task-ledger rows through 09:48:03Z in an isolated mesh directory and ran `scripts/mesh-task queue --dispatch --owner sound`. Observed exactly one row, first: `sound\tverify-newest-first-dispatch-20260912/verify-newest-first-dispatch\t0\t…`.
- `rtk mesh-task queue --dispatch --owner sound` after the claim returned no rows; the assigned task is now active and therefore no longer eligible. The installed `/home/mesh-home/.local/bin/mesh-task` and repository `scripts/mesh-task` have identical SHA-256 `fd5be5529e7d4b82115af3df681bd18fa0778a02af04a3c5fd4c88c586e51529`.
- `scripts/mesh-task` sorts queue stamps by `-epoch_iso(stamp)` within the incident/priority tiers (landed change `47bfdc22`).

Result: no ordering regression observed; no queue implementation changes made. The repository has no dedicated checked-in test for the same-priority recency tie-break, so the temporary fixture exercised that path directly.
