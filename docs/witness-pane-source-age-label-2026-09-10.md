# Witness pane source-age label — 2026-09-10

`scripts/mesh-dash` now labels the materialized `tasks.journal` mtime as
`source age=<N>s`, matching `charter/witness.md`. The existing renderer still
limits unfinished task rows to 20 and emits the last 20 raw `chat.log` lines.

Verification:

- Focused isolated fixture: `PASS: witness source age and 20/20 pane contract`
- Existing queue-fit contract: `PASS: witness chat.log tail fits the pane and reports coverage`
- Existing Python renderer fixture: `witness open pane: PASS`
- `bash -n scripts/mesh-dash`: exit 0
- `git diff --check -- scripts/mesh-dash`: exit 0

The broader `mesh-dash --test-fast` run was attempted on the live node but did
not finish within approximately 90 seconds; it was terminated and is not
claimed as passing.
