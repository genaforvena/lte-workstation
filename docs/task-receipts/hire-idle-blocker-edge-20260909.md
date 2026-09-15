# Hire idle blocker edge receipt — 2026-09-09

## Result

Implemented `scripts/mesh-hire-idle`, an on-demand hire idle reporter keyed by the normalized
blocker and the SHA-256 of its receipt. Every check is appended to
`~/.mesh/handoff/hire-idle-receipts.log`; only a blocker/receipt change or recovery calls
`mesh-chat`.

## Verification

- `./tests/test-mesh-hire-idle-edge.sh` passed: unchanged blocker deduplication, receipt-hash
  change, recovery edge, and retention of all five synthetic checks.
- `./scripts/mesh-hire-idle --test` passed.
- Live receipt checked: `docs/task-receipts/hire-trovu-391-submit-test-20260908-1711.md`.
- Two live checks at `2026-09-09T01:54:13Z` for the unchanged dedicated `GH_HIRE_TOKEN` gate
  appended two rows to `~/.mesh/handoff/hire-idle-receipts.log` and added zero board rows
  (`board_idle_before=1`, `board_idle_after=1`). The first check was the change edge; the
  second was logged as `unchanged`.

## Remaining funnel state

The hire funnel remains blocked on the operator-provided dedicated `ghIsPureTrash` public-repo
credential. No outward submission was attempted.
