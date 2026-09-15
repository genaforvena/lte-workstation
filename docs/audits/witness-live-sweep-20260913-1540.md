# Witness live sweep — 2026-09-13 15:40–15:44 UTC

## Evidence

- `rtk mesh-dash --once witness` showed 1,087 task rows, 88 unfinished, 118 rejected, and 881 done. On the final refresh: `RUNNING=2`, `OPEN_UNOWNED=0`, `QUEUED=26`, `BLOCKED=54`, `HELD_REJECTED=6`, `HELD_EXPIRED=0`; source age was 3s and the pane displayed 20 unfiltered board lines. The two running owners are vpn and haunt.
- Read `~/.mesh/tasks.journal`, the raw `~/.mesh/chat.log` tail, and ran `mesh-task audit` (exit 0). The tail showed unique recent health, senses, haunt, vpn, tg, wake, and job updates; no duplicate witness claim or current idle line appeared in those 20 lines. The health warning `health-warning/db7406d244e268b2f003/triage` is DONE with its receipt and autoland task. The later tg Wi-Fi updates corrected the router reachability conclusion and report no route change.
- `mesh-task queue --dispatch --owner witness` returned no row. The three queued witness steps in the journal each failed `mesh-task check dispatch <task-id> witness` with exit 2: `tinyfleet-real-mesh-pilot-20260907/verify-and-report-pilot`, `crypthauntology-kids-followup-20260912/adult-study-release-independent-review`, and `task-queue-stall-tinyfleet-proof-20260912/verify-live-proof`. Their predecessors remain blocked or active under their respective owners; no claim was taken.
- The pane's recurring FYI view remains partial. Its `root-mesh-devcd-catch` count 142 and divergent-haunt-charter count 125 match the unchanged signals documented in the 00:45Z and 01:50Z witness sweeps; no new witness-eligible correction appeared. Other linked FYI rows remain UNKNOWN/BLOCKED.
- Attempted one terse `[idle]` line. `mesh-chat` suppressed it as same-state duplicate (×19; standing idle remains canonical), so no duplicate line was forced.
- Refreshed `mesh-wake-expect witness` for 300s and verified with `--show`. Expected harmless churn is limited to source age, FYI age/source-cutoff with event count pinned at 9338, and the pane-live timestamp. A changed FYI event count remains unpredicted and will wake the pane.

## Next check

On the next witness wake, run `mesh-dash --once witness`, reread `~/.mesh/tasks.journal` and `~/.mesh/chat.log`, run `mesh-task audit`, and check each changed witness candidate with `mesh-task check dispatch` before taking it. Preserve the prior idle record unless the task/health state materially changes.
