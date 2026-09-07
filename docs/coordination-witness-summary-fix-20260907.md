# Witness coordination summary repair — 2026-09-07

## Finding

The witness dashboard showed an old seven-step coordination summary while the
durable tiny-fleet chain had advanced to 10/12. The installed five-minute
`mesh-witness-promises` reflex was exiting at its `mesh-board unavailable` gate
under cron because cron's PATH omitted both `~/.local/bin` and the repository
`scripts/` directory. Additionally, `mesh-task audit` emitted only unfinished
steps, despite the summary contract saying it audited every chain step.

## Repair

- `scripts/mesh-witness-promises` now resolves its sibling/installed tools when
  `mesh-board` is absent, while preserving fixture-provided PATH overrides.
- `scripts/mesh-task audit` now emits `DONE` rows with artifact paths for every
  completed step.
- The witness summary counts only `OPEN_UNOWNED`, `BLOCKED`, `EXPIRED`, and
  `ABANDONED` as findings; `DONE`, `QUEUED`, and `RUNNING` are healthy states.
- Summary field rendering preserves the blocked step's type and retry timestamp
  as real tab-separated fields.
- Updated deployed copies of `mesh-task` and `mesh-witness-promises` are
  byte-identical to source.

## Verification

- `python3 scripts/mesh-task --test` — PASS.
- `bash tests/test-mesh-witness-lifecycle.sh` — PASS.
- `bash tests/test-mesh-witness-promises.sh` — PASS.
- `bash -n scripts/mesh-witness-promises` — PASS.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile scripts/mesh-task` — PASS.
- Live installed reflex under a bounded run — exit 0, `promise_ledger=PASS`.
- Live summary now records all 12 chain steps: 10 `DONE`, one `BLOCKED`, one
  `QUEUED`, with `chain_steps=12 findings=1 status=FAIL`.

The remaining FAIL is substantive and intentional: persona/code verification
is blocked on missing runner, redacted corpora, adapters, and held-out evidence;
it is not a dashboard freshness failure.
