# Blocked self-unblock landing correction — implementation receipt

Task: `blocked-self-unblock-landing-correction-20260911/finish-prompt-land-and-migration-remediation`  
Date: 2026-09-11 UTC · owner: genome

The resolver prompt in the landed `scripts/mesh-task` now tells the owner to diagnose the blocker,
create or implement the narrowest safe in-scope prerequisite/fix first, and park or reject only when
an artifact proves the required authority or external state is irreducible. The dedicated regression
`tests/test-mesh-task-blocked-self-unblock.py` asserts that wording. The protected dirty
`tests/test-mesh-task-no-expiry.py` was not touched.

The initial 19 generic resolver prompts from the migration sweep are immutable canonical history and
were not rewritten or silently rescheduled. They were supplemented operationally by direct owner
tells to hire, tg, haunt, and health. The bounded code remediation applies the strengthened prompt
to every new blocker epoch and any future re-block; existing resolver records retain their original
wording and direct tells are the only safe supplemental correction for them.

Landing and verification:

- `mesh-land --apply` landed/pushed the scoped implementation, test, contract, implementation
  receipt, and this correction receipt (no `tests/test-mesh-task-no-expiry.py`): PASS;
- `python3 -m unittest tests/test-mesh-task-blocked-self-unblock.py` — PASS, 9 tests;
- `python3 scripts/mesh-task --test` — PASS;
- `bash scripts/mesh-task-unblock-sweep --test` — PASS;
- source/deployed SHA-256 parity — PASS for `mesh-task`:
  `8813b29560c7cdd2ce1b86e7e520c65016508c17bf7cc70a9f66c4922111b4cb`, and
  `mesh-task-unblock-sweep`:
  `892a197a7c244c20e2668d71ffda5479655cfba0ee180b82fc394fe02958addb`;
- live cron wiring — PASS: `*/5 * * * * .../.local/bin/mesh-task-unblock-sweep --run` is present
  in both `~/.mesh/reflexes.cron` and the crontab;
- live sweep idempotency — PASS: post-migration run returned `unblock-sweep owner=all created=0`;
- owner taking — PASS: this correction step is active under exact owner `genome`.

Origin verification is recorded by the landing push; the landed commit is the repository `HEAD` and
the remote fast-forward was accepted by `mesh-land`.
