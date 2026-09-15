# Blocked self-unblock landing correction — witness verification — 2026-09-11

## Verdict

PASS. Blocked rows now generate bounded, exact-owner self-unblock work instead of becoming an idle
dead end.

## Independent code and deployment evidence

- `python3 -m unittest tests/test-mesh-task-blocked-self-unblock.py` — PASS, 9/9.
- `python3 scripts/mesh-task --test` — PASS.
- `bash scripts/mesh-task-unblock-sweep --test` — PASS.
- Python syntax compilation — PASS.
- `scripts/mesh-task` and its deployed executable both hash to
  `8813b29560c7cdd2ce1b86e7e520c65016508c17bf7cc70a9f66c4922111b4cb`.
- `scripts/mesh-task-unblock-sweep` and its deployed executable both hash to
  `892a197a7c244c20e2668d71ffda5479655cfba0ee180b82fc394fe02958addb`.
- Landed correction receipt commit `82855dba` is on `origin/main`; it descends from the scoped
  source, sweep, contract, receipt, and dedicated-test commits.
- The live crontab drives the dynamic all-owner sweep every five minutes.
- Protected user work `tests/test-mesh-task-no-expiry.py` remains mode 0644 with blob
  `da3708dcf59110854cdaf1ad451b31895dde1631`.

## Independent behavior evidence

- The landed prompt explicitly requires diagnosing and creating/implementing the narrowest safe
  in-scope prerequisite first. Parking/rejection requires evidence of irreducible authority or
  external state.
- Tests cover parked blocker classes, same-text parent separation, blocker epochs, seeded legacy
  terminal-resolver migration, dynamic all-owner sweep, exact-parent-only resume, idempotency, and
  stale blocker metadata removal from active/terminal status.
- The initial live migration created 19 resolver chains. A post-land live sweep returned
  `unblock-sweep owner=all created=0`.
- Canonical replay currently has 17 blocked parents and exactly 17 matching current-epoch resolvers:
  zero missing and zero duplicate mappings.
- Owner-authored takes were observed for newly migrated work, including
  `unblock/hire/d5564913a610215e/resolve` and
  `unblock/health/4b42a991b6458d80/resolve`.
- The concrete health self-unblock restored and enabled `mesh-room-gigaam.service`; independent
  evidence showed continued transcript/cursor advancement. The exact original blocked parent
  `health-warning/bcc69eeef277b22e47e9/triage` was then resumed and completed, and its terminal
  status no longer renders stale blocker metadata.

The 19 first-migration descriptions are immutable history and retain the earlier generic wording.
Active mind owners received direct supplemental instructions; all newly created blocker epochs use
the strengthened landed prompt. Unchanged epochs do not regenerate work, preserving the no-paid-loop
constraint.
