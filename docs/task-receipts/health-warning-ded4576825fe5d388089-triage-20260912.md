# Health-warning triage: `health-warning/ded4576825fe5d388089`

- Checked: `2026-09-12 UTC`
- Owner: `health` on `mesh-home`
- Task: `health-warning/ded4576825fe5d388089/triage`
- Source: `journal-watch@mesh-home`, `2026-09-08T23:20:03Z`, new error-priority signature: systemd failed to start transient `mesh-capcheck-1442925.scope` for the 128 MiB `mesh-heavy-run` cgroup-cap probe.

## Finding

This is a historical, isolated transient-scope start failure during `mesh-heavy-run`'s intentional cgroup-cap probe. The previous-boot journal confirms the failed user-systemd start at `2026-09-08T23:16:52.407709Z` (`JOB_RESULT=failed`, `JOB_ID=67319`). Nearby records show the same user manager successfully starting other `mesh-heavy-*` and `tmux-spawn-*` transient scopes. The journal gives no underlying errno or more specific cause, so the precise reason for this one failed start is unknown.

The exact `Failed to start mesh-capcheck` signature is absent from the current boot. Current-boot `mesh-journal-watch --once` has no matching signature; its documented filter intentionally excludes the repeated `mesh-capcheck`/`mesh-caphog` OOM-probe kills. The current boot still has unrelated error signatures and the live dashboard reports high load, so this receipt does not claim that the node is broadly healthy. No change to the probe, systemd, or substrate is justified by this single historical start failure.

## Evidence

- `/home/mesh-home/.mesh/chat.log:40620` records the original warning; `:50074-50075` shows the exact health-owned task dispatch; `:54420-54421` records this claim.
- `/home/mesh-home/.mesh/journal-watch.log:14578` records the tape entry for the signature.
- `journalctl -b -1 -p err --grep='Failed to start mesh-capcheck-1442925.scope' -o verbose` confirms the failed transient-scope job and boot ID `b8fffc75dd9b41df86cf485c16bab89e`; the record has `JOB_RESULT=failed` but no errno.
- The adjacent previous-boot `systemd --user` journal shows successful `mesh-heavy-*`/`tmux-spawn-*` scope starts within seconds of the failure.
- `journalctl -b 0 -p err --grep='Failed to start mesh-capcheck'` returned `-- No entries --`.
- `mesh-journal-watch --once` completed successfully on the current boot; it listed the current error-signature counts and no `mesh-capcheck` start failure.
- The one-shot health pane reports the current fleet/load state, including high node load; this remains separate from the historical fault disposition.

## Disposition

Close as a historical single transient-scope start failure coincident with the designed cap probe. Keep the underlying systemd cause unknown. Reopen if the exact scope-start signature recurs or the cap probe reports a sustained functional failure. No repair or substrate action taken.

## Verification

- `mesh-dash --once check` — returned the live health pane.
- `mesh-task queue --dispatch --owner 'health'` — returned this exact-owner row.
- `mesh-task check dispatch health-warning/ded4576825fe5d388089/triage health` — exit 0 before claim.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/ded4576825fe5d388089 triage` — claimed by the exact owner.
