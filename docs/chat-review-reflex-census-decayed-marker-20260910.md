# Reflex census DECAYED marker repair

Date: 2026-09-10 08:15Z
Task: `chat-review/reflex-census-decayed-marker-20260910`

## Change

`scripts/mesh-reflex-census` now treats an explicit commented `DECAYED` cron marker as a
deliberate schedule removal, alongside `DISABLED` and `HELD`. Ordinary commented cron lines,
freshness-expired `PAUSED` markers, and live schedule removals remain visible to the census.

## Verification

- Red regression before the production edit: `mesh-reflex-census --test` rejected the fixture
  because `mesh-decayed-tool` was missing from `disabled_set`.
- Source test: `bash scripts/mesh-reflex-census --test` — PASS.
- Deployed test: `~/.local/bin/mesh-reflex-census --test` — PASS.
- Syntax: `bash -n scripts/mesh-reflex-census` — PASS.
- Source/deployed SHA-256: `febc2c40cc81fa15f607ea1e578a03bfea1d38d5498019a4d836a0223e4487ae` — identical.
- Live `~/.local/bin/mesh-reflex-census --check`: `vanished vs baseline: none`; `declared-but-unscheduled: none`.

The deployed copy is byte-identical and includes the regression fixture.
