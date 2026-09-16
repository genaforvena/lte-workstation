# Health self-care clearance — 2026-09-16

Task: `witness-range-61067-61133-corrective/verify-selfcare-clearance`
Owner: `health`

## Fresh read-only verification

All timestamps are UTC and were collected during this turn.

| Check | Command | Exit | Verdict |
|---|---|---:|---|
| self-care smoke | `timeout -k 5 150 mesh-selfcare --test` | 0 | PASS — `smoke-test: ok` |
| egress probe | `timeout -k 5 45 mesh-egress-health` | 0 | PASS — no diagnostic output |
| exit-node/LAN card | `timeout -k 5 45 mesh-card --refresh --exit-node-lan` | 0 | PASS — default egress `enp42s0`, exit node `none`, exit-node-LAN `n/a` because no exit node, invariant `OK` |
| aggregate doctor | `timeout -k 5 120 mesh-doctor --cron` | 0 | UNKNOWN — skipped: another automated doctor holds `/home/mesh-home/.mesh/.doctor.lock`; no aggregate result was produced |

The card was live-refreshed at `2026-09-16T07:32:21Z`. The doctor lock was still held at
`2026-09-16T07:32:47Z` (mtime `2026-09-16 07:32:39.841984844 +0000`); a long-running
`mesh-doctor --cron` process was observed, so the lock was not removed or bypassed.

## Verdict

The corrected `mesh-selfcare` smoke path is independently clear, and the current egress and
exit-node/LAN topology checks are clear. Aggregate `mesh-doctor` clearance remains UNKNOWN until
the existing automated doctor run releases the lock and a fresh aggregate run completes. No route,
DNS, firewall, VPN, exit-node, or service state was changed.

Retry edge: rerun `mesh-doctor --cron` after the active doctor releases
`/home/mesh-home/.mesh/.doctor.lock`.
