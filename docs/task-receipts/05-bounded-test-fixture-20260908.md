# Bounded test-isolation fixture — 2026-09-08

- Task: `hire-ledger-correction-prereqs-20260908/05-bounded-test-fixture`
- Owner: `hire`
- Captured: `2026-09-08T12:18:02Z`
- Scope: one current, bounded fixture for reassessing test isolation; no historical leaking variant was run against live tapes.

## Fixture and source target

The canary target is the repository fixture `tests/test-mesh-promises-isolation.py` run against
the current `scripts/mesh-promises` source at revision
`1d265f0a76fdefa96d564abf6a5fa5e6b9682628`.

Source hashes at capture:

```text
scripts/mesh-promises                 0ccc09f34a69fe512ab8608a17dfbf3c170633f2
tests/test-mesh-promises-isolation.py b1704f4f421ee8c45e06ef4dd71b528c7e03b056
```

The fixture creates separate temporary `HOME/.mesh` and `MESH_DIR` trees, places a sentinel in
the default summary, feeds a task from the custom chat log, and asserts that the sentinel remains
unchanged while the custom summary and custom promises journal are created. Its environment also
redirects the chat log, promises directory, voice input, and TG sent marker into the temporary
fixture tree.

## Verification

```text
python3 tests/test-mesh-promises-isolation.py
PASS: custom mesh feed leaves default HOME summary untouched

bash -n scripts/mesh-promises
PASS (exit 0)
```

This is a hermetic source/canary artifact: it proves the current custom-directory path without
claiming a live feed or replay of historical variants. The next task remains
`hire-ledger-correction-prereqs-20260908/06-durable-evidence-receipt`.
