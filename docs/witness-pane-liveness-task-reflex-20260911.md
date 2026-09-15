# Witness pane liveness and chat-error task reflex — 2026-09-11

## Finding

`mesh-pane-watch` already ran under `mesh-liveness-loop` and posted a prose `[task]` line when a
data pane froze, but that alert was not a canonical `mesh-task` chain. Separately, the health-warning
reflex only admitted tagged health warnings; explicit errors such as `[delivery-failed]` could remain
board-visible without becoming health-owned repair work.

## Change

The freeze-edge handler now creates one chain per episode:

`pane-liveness/<node>/<window>/<epoch>/investigate`

The step is owned by `health`, priority 100, and requires restoring the renderer lease plus an
artifact-backed receipt before closure. The existing bounded self-heal remains in place. If task
creation fails, the reflex posts a loud fallback identifying the failed canonical write.

The health-warning reflex now fingerprints explicit error/alarm markers from any sender, including
`[error]`, `[failed]`, `[failure]`, `[delivery-failed]`, `[pane-frozen]`, `[mind-wedged]`,
`[mind-stranded]`, `[mind-holding]`, `[scheduler-dead]`, `[health-fail]`, `[organ-down]`, and
`[alarm]`, while ignoring task-ledger output that quotes those markers. Its existing cursor,
deduplication, and one-queued-task backpressure remain intact, so every error is retried rather than
silently discarded.

## Verification

- `scripts/mesh-pane-watch --test` — PASS.
- `scripts/mesh-liveness-loop --test` — PASS; pane-watch is supervised.
- `tests/test-mesh-pane-watch-task.sh` — PASS; three identical captures create one exact-owner task.
- `python3 tests/test-mesh-health-warning-task.py` — PASS.
- `python3 -m py_compile scripts/mesh-health-warning-task` — PASS.
- `mesh-task audit` — PASS before this change (`findings=0`, `source_errors=0`).

The live health-error cursor is retryable but currently held behind five already-queued historical
health triage chains; it has not discarded the source tail (`offset` remains at the first unadmitted
warning). This is deliberate backpressure, not a false DONE: the next minute cadence retries the
same source position, and explicit error markers use the same durable cursor/deduplication path.

## Follow-up: task wake liveness

The consumer’s ordinary 1800-second per-mind refractory gate could also suppress an exact-owner
health task. `scripts/mesh-pane-consume` now checks the owner’s candidate before applying that gate:
candidate-free telemetry remains rate-limited, while an actionable exact-owner task logs
`refractory bypass` and is delivered on the next idle pass. The smoke test covers both paths.

Live verification at 2026-09-11T19:36Z showed the `health` consumer taking the bypass path for the
queued triage rows. `mesh-tell` then honestly reported the health pane’s pending handoff/reset
lifecycle guard, so no false wake was recorded; the supervised consumer remains running and will
retry after lifecycle drain. The task rows remain open and are not claimed closed by this witness.

At 2026-09-11T19:42Z, `mesh-clear health` recovered a confirmed `WEDGED-INPUT` composer. Lifecycle
readiness returned 0, the consumer logged `WOKE mind (health)`, and health owner-authored
`[taking] health-warning/29ea9afb241e9b2c9855/triage` followed. The witness top pane independently
remained live: its source age was 25s, its raw tail included new board lines, and its lease footer
advanced from 19:40:32Z to 19:43:03Z.

## Follow-up: independent audit reflex

`mesh-audit` was present only as an on-demand S3* auditor. `scripts/mesh-audit-reflex` now runs from
the always-on `mesh-liveness-loop` task table every 300 seconds, but performs the actual audit only
at a persisted random delay of 300–900 seconds. A `DIVERGE` or auditor error emits
`[audit-diverge]` or `[error]`; the wrapper immediately invokes `mesh-health-warning-task`, while
the existing every-minute health reflex remains the retry safety net. The health marker classifier
admits `[audit-diverge]`, so the issue becomes an exact health-owned task and follows the normal
consumer/repair/receipt path. The live tool is deployed at `~/.local/bin/mesh-audit-reflex` as a
symlink to the repository script.

Verification: `scripts/mesh-audit-reflex --test`, `scripts/mesh-liveness-loop --test`,
`mesh-audit --test`, and `python3 scripts/mesh-health-warning-task --test` all PASS; the live
`mesh-audit-reflex` invocation wrote a future jitter deadline without producing a false alarm for
the node’s honest thermal `n/a` result.

## Follow-up: cursor recovery and urgent-error priority

The live cursor exposed one more liveness failure: `HELD_EXPIRED` historical health-warning rows
were still counted as queued capacity, so they could hold the cursor before a newer error. The
health reflex now excludes expired dispatch leases from capacity, scans the unread tail for explicit
error markers, admits the newest error ahead of ordinary historical prose, and keeps the byte cursor
retryable so no source line is lost. The urgent path is bounded by `MESH_HEALTH_ERROR_BATCH` (five
by default) and retains exact-chain recovery for partial dispatches.

Live proof: the 2026-09-11T19:40:05Z `[mind-wedged]` event became
`health-warning/f9469f48fceaa7e50c3e/triage`, Health was woken through the exact-owner consumer
path, and it closed at 20:02:28Z with
`docs/health-warning-triage-f9469f48fceaa7e50c3e-20260911.md`. The stale `10a42...` row also
closed with an artifact; the superseded `f16...` row was typed-rejected by Health. The historical
error tail was then drained through the same reflex. The final source-vs-state audit found 105
unique post-cursor explicit-error fingerprints, all 105 present in the durable cursor, with zero
missing keys; replay showed zero error chains lacking `dispatch=sent`. Health remains the repair
owner for the dispatched queue, with each task requiring its normal owner artifact before closure.

At the final live check, Health was consuming the queue normally: the exact head
`health-warning/2e5a3d25a2bf38e2ee48/triage` was claimed at 20:24:46Z with a lease through
20:54:46Z. Error-task closure remains an active owner workload (69 of 105 were still open at that
observation); the lease/reflex wiring is verified, but the durable completion count is intentionally
not overstated.
## Owner-scoped task retrieval (2026-09-11T20:37Z)

The task consumer previously replayed the complete dispatch queue and filtered the result in
shell. That preserved exact-owner claim safety but made a busy global queue look like an idle
mind. `scripts/mesh-task` now supports `mesh-task queue --dispatch --owner <mind>`, filtering
directly from the canonical `chat.log` task-state replay. `scripts/mesh-pane-consume` uses this
owner-scoped retrieval and still requires `mesh-task check dispatch <task-id> <owner>` before a
claim. The live `~/.local/bin/mesh-task` entrypoint points to this implementation.

Evidence: real `mesh-task queue --dispatch --owner health` emitted only `health` rows;
`mesh-pane-consume --task-candidate health` returned an exact Health task; the owner-filter
regression, mesh-task self-test, pane-consumer self-test, pane-watch self-test, liveness-loop
self-test, Python compilation, `git diff --check`, and `mesh-task audit` all passed. Live pane
watch reported every channel `ok identical=0`; witness top pane `%17` advanced to
`2026-09-11T20:37:15Z`.
