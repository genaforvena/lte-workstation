# Idle-turn follow-through mislanding recovery verification — 2026-09-11

## Verdict

PASS. The false-scope commit `8c0481eb4250946308835ab5e11e3e9cfed4fee5` was recovered without
history rewriting or loss of the pre-existing resolver-test work.

## Independent evidence

- `HEAD`, cached `origin/main`, and server `refs/heads/main` all resolve to normal revert
  `6d87ae8018ef522fb15e1ffadf868034b213f16d`.
- `git show --name-status 6d87ae80` contains only
  `tests/test-mesh-task-no-expiry.py`; the revert restores its tracked mode from `100755` to
  `100644` and removes the 32 lines falsely landed by `8c0481e`.
- The working file is preserved dirty at mode `644`. Its blob
  `da3708dcf59110854cdaf1ad451b31895dde1631` exactly equals
  `8c0481e:tests/test-mesh-task-no-expiry.py`, proving the resolver-test edits survived outside
  canonical history for their real owner.
- The actual idle-turn regression remains tracked in commit `025ef766`; corrected
  `scripts/mesh-pane-consume` remains in commit `41e9da17`, and source/deployed SHA-256 still matches
  at `44a44dd490c31a44dda3bed0ca681d61be638f26a222b063a33778647dd20c3a`.
- Correction implementation and prelanding-review receipts remain in commits `9e512c6c` and
  `83644e60` respectively.

Owner recovery receipt:
`docs/task-receipts/idle-turn-cost-followthrough-mislanding-recovery-20260911.md`.

