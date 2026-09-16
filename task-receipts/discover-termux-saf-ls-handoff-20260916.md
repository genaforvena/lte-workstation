# Discover handoff receipt — Redmi `termux-saf-ls`

Date: 2026-09-16
Owner: `discover`

## Evidence inspected

- Source capability artifact: `/home/mesh-home/.mesh/knowledge/capability-termux-saf-ls-redmi-20260916.md`
- Fresh end-to-end sample: `192.168.8.203:8022`, `termux-saf-dirs`, exit `0`, stdout `[]`.
- Acceptance predicate: SSH reaches the Redmi, command exits `0`, stdout parses as a JSON array; sample pass rate `1/1 = 100%`.
- Contract boundary: zero-argument `termux-saf-ls` returns an argument-count error; no SAF folder is currently authorized, so `[]` is valid empty data rather than failure.

## Delegation and duplicate check

Delegated independently verifiable artifact review to `discover-saf-review` via the shared CSD relay. I personally inspected the source artifact and replayed the canonical task ledger. The worker's report matched the inspected evidence and proposed the same narrow steward handoff.

Read-only checks found the probe task complete and no existing active, queued, or blocked SAF-list handoff. The new exact-owner row is:

`discover-termux-saf-ls-handoff-20260916/wire-termux-saf-ls-consumer`, owner `senses`, dispatch check exit `0` when checked as `senses`.

## Handoff

`senses` should implement or document a narrow consumer accepting `folder-uri`, parsing the JSON-array response, treating `[]` as valid empty data, and preserving SSH timeout/no-route failures as `UNKNOWN`. Do not grant phone permissions or mutate substrate. Retry after a SAF folder URI is granted or the Redmi endpoint changes state.
