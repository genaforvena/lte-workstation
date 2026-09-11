# Blocked self-unblock follow-through — implementation receipt

Task: `blocked-self-unblock-followthrough-20260911/make-every-block-actionable`  
Date: 2026-09-11 UTC

Implemented in `scripts/mesh-task` and `scripts/mesh-task-unblock-sweep`:

- every owner-bearing blocker class now materializes one exact-owner resolver;
- resolver descriptions explicitly direct diagnosis and the narrowest safe in-scope prerequisite/fix,
  with evidence required before parking/rejection;
- resolver identity is scoped to parent chain/step and block epoch, with a short ledger-safe key
  plus parent metadata, so same-text parents and new epochs cannot alias;
- `unblock-sweep` without an owner discovers all blocked owners dynamically;
- resume clears transient blocker metadata and exact cleared results resume only their parent;
- status output renders blocker/retry only for currently blocked steps, including legacy terminal rows.

New scoped coverage is in `tests/test-mesh-task-blocked-self-unblock.py` (the pre-existing dirty
`tests/test-mesh-task-no-expiry.py` was not edited).

Verification:

- `python3 -m unittest tests/test-mesh-task-blocked-self-unblock.py` — PASS, 9 tests;
- `python3 scripts/mesh-task --test` — PASS;
- `bash scripts/mesh-task-unblock-sweep --test` — PASS;
- `mesh-sync-tools --apply` — PASS;
- source/deployed SHA-256 parity — PASS: `mesh-task`=`e2985bf3edb3689779ebc8aa0c7dcdd2fd1b0c8ab76c461ad10b930f6d845f32`,
  `mesh-task-unblock-sweep`=`892a197a7c244c20e2668d71ffda5479655cfba0ee180b82fc394fe02958addb`;
- live migration sweep — PASS: `unblock-sweep owner=all created=19` on first run;
- live idempotent sweep after deployment — PASS: `unblock-sweep owner=all created=0`.

Bounded migration decision: the 19 resolver chains created by the first migration sweep retain their
immutable historical descriptions; they are not silently rewritten or rescheduled. Their parent
epochs are already represented by exact resolver keys. The strengthened instruction applies to all
new blocker epochs; a future re-block creates a new resolver with the canonical wording.

The implementation is present in the genome and deployed locally. Scoped landing uses the explicit
settle override and exact path allowlist; the protected pre-existing
`tests/test-mesh-task-no-expiry.py` is excluded.
