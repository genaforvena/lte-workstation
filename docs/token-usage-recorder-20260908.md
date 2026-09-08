# Token usage recorder — implementation receipt (2026-09-08)

Task: `token-usage-accounting-implementation-20260908/token-recorder`

The recorder is now implemented at `scripts/mesh-token-usage-recorder` and deployed by
`mesh-land` to `~/.local/bin/mesh-token-usage-recorder`. Lifecycle completion events hand off to it
with `subprocess.Popen(..., start_new_session=True)` after the completion receipt is written, so
collection is asynchronous and cannot hold the completion callback.

The recorder writes mode-0700 store directories and mode-0600 JSONL/lock files. It retains only the
raw whitelist (`type`, attribution, identity, timestamps, and usage fields), plus the normalized
row. Message bodies, cwd, and unknown input fields are discarded. Rows are append-only and keyed by
`engine:thread-id:turn-id`; exact replays are duplicates, changed payloads are conflicts in
`conflicts.jsonl`, and missing identity is quarantined in `quarantine.jsonl`.

Evidence commands and outputs:

```text
scripts/mesh-codex-lifecycle --test
=> lifecycle-test: ok (durable artifact, handoff before clear, busy deferral, idempotent turn count, quiet reset)

tests/test-mesh-token-usage-recorder.sh
=> token-recorder-test: ok (record, privacy, permissions, duplicate, conflict, replay, quarantine)

20 concurrent recorder processes against one store
=> token-recorder-concurrency: ok (20/20 unique records)
```

The focused test is `tests/test-mesh-token-usage-recorder.sh`. The recorder is observation-only;
token values have no control-plane consumer in this change.

Next action: witness runs the bounded live canary and replay audit for the downstream
`token-live-canary` step.
