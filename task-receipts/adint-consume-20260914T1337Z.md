# adint consume receipt — 2026-09-14 13:37 UTC

`mesh-dash --once adint` showed the pane `WORKING` on `step0d-hb-first-cell` and an open
room-camera resolver, `unblock/adint/3dd6562eb2e7cc86/resolve`. Its safe retry condition was
checked with `timeout 8s ssh -o BatchMode=yes -o ConnectTimeout=5 ilya@192.168.8.214 true`;
SSH timed out (exit 255), so no camera read or task resume was attempted.

`mesh-task queue --dispatch --owner 'adint'` exited 0 with no eligible rows after the retry.
No row was returned, so no dispatch check or take was applicable. Posted one board line:
`[adint] [idle] step0d-hb-first-cell remains open; camera SSH timed out; no eligible adint dispatch row.`

The parked genome snapshot `refs/wip/adint` is `80b8dba1`. The current genome worktree is dirty
and differs from that snapshot (`git diff --quiet refs/wip/adint --` exited 1; the diff stat
reported 884 changed paths and 47,696 deletions). The prescribed
`mesh-wip-commit --restore adint` correctly refused to overlay it and refreshed the recovery patch
at `/home/mesh-home/.mesh/wip/adint.patch` (5,600,275 bytes;
SHA-256 `832aee968317c8705b70ed842762b3bf134febcf32bd19554ecd07db46197484`). The working tree was
left untouched; the patch remains available for reconciliation in a clean worktree.

Operator update was sent in Russian over `mesh-voice-tx`; output confirmed both the voice note and
duplicated Telegram text were delivered. The clone socket was unavailable, and the documented
Piper/Russian fallback was used.

The next-pane prediction is bounded to 300 seconds and covers only the normalized periodic refresh
header and live-tick line:

```text
^== adint data \(refresh 30s\) — [0-9T:.-]+Z — all text ==$
^-- pane live [0-9T:.-]+Z · 30s · ticks every frame --$
```

Next real wake: run `mesh-dash --once adint`, then `mesh-task queue --dispatch --owner 'adint'`;
retry the camera SSH condition only as a fresh external-state check. Do not apply the parked WIP
patch over the current dirty genome worktree; reconcile it first.
