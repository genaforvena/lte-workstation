# Health warning triage: 86e2172e37803c554a2f

Checked 2026-09-15 12:48–12:50 UTC on `mesh-home` after the exact-owner
dispatch check passed and the row was taken as `health`.

## Finding

The dispatched chat-review is stale/duplicate. It claims that chronic
suppression roll-ups are still admitted as urgent errors, but the fix landed
before this triage completed:

- `git log -- scripts/mesh-health-warning-task` reports commit `4c6aa846`
  (`2026-09-15T12:49:25Z`, “Normalize chronic health roll-ups to one non-urgent trace chain”).
- Current `scripts/mesh-health-warning-task:97-105` detects `CHRONIC_ROLLUP`
  before `ERROR_MARKER` and returns `chronic:<subject>:<signature>`.
- Current `pending_error` at `scripts/mesh-health-warning-task:345-347` admits
  only `error:` and `error-task:` keys, so the chronic key is not urgent.
- `scripts/mesh-health-warning-task --test` and the deployed
  `~/.local/bin/mesh-health-warning-task --test` both pass.
- A direct current-code probe returns
  `key= chronic:imac-rozalia:35f22fafd26a` and `urgent=False` for the cited
  chronic roll-up shape.
- Source and deployed copies have identical SHA-256:
  `1c6bda88465375710016cb2c61d4991d054961725c6eff6704a766869a1238c7`.
- `mesh-health --once` at 12:49Z reported `mesh-home PASS` and
  `imac-rozalia PASS`; `mesh-dash --once check` reported current egress OK.

No code or substrate change is justified by this row. Reject it as stale
after recording this evidence; the landed fix is the artifact of the
underlying review.
