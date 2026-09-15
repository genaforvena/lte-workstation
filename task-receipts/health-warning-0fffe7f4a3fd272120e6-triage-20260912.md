# Health warning triage: Tiny Fleet smoke-test failures

Chain: `health-warning/0fffe7f4a3fd272120e6/triage`  
Checked: 2026-09-12 (UTC)  
Source warning: the 2026-09-09 08:23Z doctor report added smoke-test failures for `mesh-tiny-fleet`, `mesh-tiny-fleet-snapshot`, and `mesh-tmp-guard`; LAN/router remained unknown and egress still used `tailscale0` with an exit node.

## Current state and checks

- The consumed check pane at `2026-09-12T05:36:00Z` showed 10 nodes (2 SSH, 0 LAN, 8 down), egress via `tailscale0`, and a cached doctor result of 3 FAIL/33 WARN. Its displayed failures were egress over the overlay, an exit-node SPOF, and `scripts/tinyfleet_split_audit.py` lacking its execute bit. The pane also showed 26 alarm and 35 stale states; no substrate action was taken.
- From the repository root, `mesh-tiny-fleet --test` exited 0 (1889 files extracted; no live inference asserted), and `mesh-tiny-fleet-snapshot --test` exited 0.
- From `/home/mesh-home`, the same tests failed: `mesh-tiny-fleet --test` exited 1 (“not in a git repo”), and `mesh-tiny-fleet-snapshot --test` exited 128 (“not a git repository”). This isolates the two failures to caller working directory. Cron invokes `mesh-doctor --cron` from `~/.mesh/reflexes.cron:32`; its smoke runner executes deployed tools by absolute path (`~/.local/bin/mesh-doctor:5334, 5371`) without changing to the genome directory. The cron smoke-test result is therefore a harness-context false positive for these repo-dependent tests, not evidence that their repository-root smoke tests fail.
- `timeout 90 mesh-tmp-guard --test` from the repository exited 1 with a real current finding: six shell traps could not be parsed (shell-leg verdict UNKNOWN), and twelve Python temp producers have cleanup paths but no SIGTERM handler: `mesh-board-query`, `mesh-chat-deliver`, `mesh-codex-lifecycle`, `mesh-contact-name`, `mesh-edit-validate`, `mesh-health-warning-task`, `mesh-secret-cut`, `mesh-task`, `mesh-tv-dlna`, `strip-head`, `test-fleet-refresh`, and `wake_eval_fixtures.py`.
- A full fresh `mesh-doctor` verdict was not obtained in this pass; the pane's cached result is the current report. An accidental `mesh-doctor --help` invocation launched the full scan (there is no help branch) and was terminated as a process group after it continued running for several minutes. Its partial output is not treated as a verdict.

## Disposition

The Tiny Fleet failures are reproducible only from the doctor/cron working-directory context and need the smoke runner or those tests to resolve the repository root. The `mesh-tmp-guard` failure is current and names unhandled producer work plus an unparsed shell-trap blind; its prior known owner is the tmp-guard/genome lane, so this health triage does not edit those producer scripts. LAN/router state remains UNKNOWN. Egress and exit-node failures remain reported by the live pane. No routing, DNS, firewall, VPN, or other substrate state was changed.
