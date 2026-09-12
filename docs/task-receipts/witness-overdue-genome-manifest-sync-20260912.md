# Overdue manifest sync/doctor witness — 2026-09-12

Disposition: stale; the parent slice completed after this witness task was created and before it was dispatched to genome.

Evidence:

- `~/.mesh/chat.log:55752-55754` records this witness task created at 10:44:01Z and dispatched at 10:44:09Z, originally while the parent had no completion artifact.
- `~/.mesh/chat.log:55766-55767` records the parent autoland request at 10:47:21Z and the authoritative chain ledger at 10:47:24Z. The ledger marks `tg-scripts-layout-migration-20260912/manifest-sync-doctor` `done`, finished at 10:47:18Z, with result and artifact `/home/mesh-home/lte-workstation/docs/task-receipts/manifest-sync-doctor-20260912.md` (SHA-256 `72c7165a20f14c83d43fe34b693175d298c3f370d91e62c889e1068b596b16b6`). This is after the witness was created but before the current owner-direct dispatch at 10:56:35Z (`chat.log:55816`).
- `rtk mesh-task status tg-scripts-layout-migration-20260912` independently reports the parent step done and the successor step open.
- The parent receipt exists and records focused consumer tests, manifest validation, outside-repository `--test` runs, and rollback scope.
- Current source/deployed SHA-256 matches for `mesh-sync-tools` (`583833af39aab4d5bae8969efee27eb4f627ec9e689d545bb321f9dec0fbd4dc`) and `mesh-doctor` (`0002973c57b27e17683aa686964170722d089074fd8bb236ddf1c062941424e4`). The shared manifest reader is source-only, as expected.

The overdue lease was real, but it does not justify renewing a completed parent task. No parent progress update was issued. The witness task itself was still open at audit time and is being closed as stale using its required exact close tag.

Recheck at 10:59Z confirmed the source/deployed hashes above and the parent ledger remains done. The retained board already has an exact `[done]` line for this witness at `~/.mesh/chat.log:55823`, but `mesh-task status witness-overdue-genome-manifest-sync-20260912` still showed the row open before this owner take. This pass records the terminal state through `mesh-task done` as well, rather than treating the chat line alone as ledger closure.
