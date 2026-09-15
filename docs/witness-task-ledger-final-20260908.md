# Witness task-ledger completion evidence

Verified live on `mesh-home` at 2026-09-08T09:26Z.

- Canonical source: `~/.mesh/chat.log`; structured `[task-state]` revisions make replay durable and idempotent.
- Materialized view: `~/.mesh/tasks.journal`; source replay reported `36772/36772` events, zero errors, and `task_source=PASS`.
- Live counts: 242 task rows; 155 unfinished, 7 reasoned rejected, 80 done.
- Witness top pane: exactly 20 unfinished task rows followed by exactly 20 unfiltered raw `chat.log` lines; DONE and REJECTED rows are not displayed.
- Dispatch order: 14 currently claimable task IDs from `mesh-task queue --dispatch` matched the first 14 witness task IDs byte-for-byte. Dependency-waiting rows followed them.
- Dependency behavior: `mesh-task wait-for <chain> <step> <prerequisite-task-id>` returns blocked work to QUEUED, prevents taking it early, and redispatches it after the exact prerequisite reaches DONE.
- Production dispatcher: reads `mesh-task queue --dispatch` directly; no promise-ledger feed/query is in the production queue path.
- Event refresh: `mesh-task-watch` observes `chat.log`; cron provides a five-minute reconstruction backstop through `mesh-task-journal`.

Focused checks passed:

```text
mesh-dispatch --test
python3 tests/test-mesh-task-no-expiry.py
python3 -m unittest tests/test-mesh-task-log.py
bash tests/test-mesh-witness-task-only-materializer.sh
bash tests/test-mesh-task-watch.sh
bash tests/test-mesh-witness-task-queue-fit.sh
bash scripts/mesh-chat --test
python3 tests/test-witness-open-pane.py
```

The JSON visible in the unfiltered chat tail is intentional canonical task-state data. Hiding it would make the tail filtered; moving it requires a separate authority migration rather than a display change.
