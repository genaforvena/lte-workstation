# Health warning triage: held job composer

- Warning: `channel-keepalive@mesh-home` reported at 2026-09-14T14:39:31Z that `mesh-home:job` held `/model ...` text for 12 minutes without a matching `mesh-tell` delivery. The warning explicitly left the composer alone because it could have been a hand mid-sentence.
- Live check at 2026-09-14T15:08Z: `mesh-mind-state job` returned `IDLE` (`ready prompt, no turn running`). Read-only capture of `mesh-home:job.1` showed the Codex ready prompt, with no text in the composer. The held text is no longer present.
- Delivery evidence: `~/.mesh/tell-wal.log` has job intent/sent records at 14:17:38Z and 14:48:10Z, with no record at the warning time. `~/.mesh/channel-keepalive.log` has no matching event at 14:39Z; its latest job relaunch record is 02:05:37Z. The warning's original composer text and how it cleared cannot be attributed from these artifacts.
- Action: no pane or substrate change. The alert is no longer current and the job mind-state agrees with the visible pane; clearing or resending an unknown in-progress composer would have been unsafe. Historical cause remains an attribution blind spot.
- Verification: `mesh-mind-state job` exit 0; read-only `tmux capture-pane -t mesh-home:job.1` exit 0.
