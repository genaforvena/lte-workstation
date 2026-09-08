# Token usage live canary (2026-09-08)

Task: `token-usage-accounting-implementation-20260908/token-live-canary`

## Evidence

- `tests/test-mesh-token-usage-recorder.sh`: passed (privacy whitelist, permissions,
  duplicate, conflict, replay, quarantine).
- `tests/test-mesh-token-usage-reconciliation.sh`: passed.
- `tests/test-mesh-token-usage-report.sh`: passed.
- `scripts/mesh-codex-lifecycle --test`: passed.
- `scripts/mesh-codex-lifecycle` and `~/.local/bin/mesh-codex-lifecycle` have identical
  SHA-256 `78702cf1fe363454ad7f41db293446633f0511517eb36a7d975e5999e8baabd6`.
- `scripts/mesh-token-usage-recorder` and `~/.local/bin/mesh-token-usage-recorder` have
  identical SHA-256 `d54ab7df5aef7a86d900f13dd5a1b2774216f164503a4efe8f84e582e39a671a`.
- A current `agent-turn-complete` lifecycle receipt was recorded with five explicit
  `missing` usage states; replay produced `duplicate`, and the store contained one row.
  Message content and `cwd` were absent from the retained raw whitelist.
- A bounded provider fixture with `total=12`, `input=8`, `output=4`,
  `cached_input=2`, and `reasoning=1` reconciled as `pass`; reporting produced one
  row with zero missing fields.
- No runtime reference to `mesh-token-usage-report` or `mesh-token-usage-reconcile` was
  found outside their own source/tests; they are read-only source tools, not control-plane
  consumers. The lifecycle runtime consumer is the deployed recorder only.

## Failed gate

The recorder is not idempotent for a valid identity when both `received_at` and
`observed_at` are absent. On first record it fills `observed_at` with the current time;
replaying the identical JSON event fills it with a new time and returns `conflict`.
Therefore the required general replay/idempotency acceptance is not met. The focused
test passes only because its fixture supplies a fixed `received_at`.

Required correction: make the normalized observation timestamp deterministic for a
missing timestamp (or otherwise exclude the generated receipt time from the identity
comparison), add a regression fixture for timestamp-free replay, rerun this canary, and
publish a replacement artifact before closing the task.

Verdict: `REJECTED` pending the recorder idempotence correction. No production store was
modified; all canary stores were temporary test fixtures.
