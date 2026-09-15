# Room revival ledger reconciliation — 2026-09-13

Task: `room-revival-ledger-reconciliation-20260913/reconcile-room-revival-holds`
Checked: 2026-09-13 14:19 UTC on `mesh-home`.

## Current dispositions

| Organ | Evidence and disposition | Original warning / health resolver |
|---|---|---|
| Room camera | The configured primary eye is `mesh-imac-cam-watch`; its declared unit is present but disabled/inactive on mesh-home. `mesh-imac-cam --test` returned `smoke-test: n/a (iMac unreachable: ilya@192.168.8.214)`. A direct bounded SSH probe to `ilya@192.168.8.214:22` timed out. The primary-eye artifact `~/.mesh/.imac-cam-prev.jpg` is still dated 2026-07-24. The local `mesh-cam-watch.service` is independently active and continuously refreshes `~/.mesh/cam-prev.jpg`; `mesh-camera --test` passed a real one-frame JPEG read. That local motion-alert camera is not the iMac room-mind eye, and the room-sense probe deliberately gives the iMac eye precedence, so it is not recorded as a replacement. Leave the iMac watcher stopped; blocker is the missing SSH reachability to the iMac, not approval. Retry when `timeout 8s ssh -o BatchMode=yes -o ConnectTimeout=5 ilya@192.168.8.214 true` exits 0, then require `mesh-imac-cam --test` to complete a real read before resuming. | `health-warning/25a35aa3f04ecad1655e/triage` remains blocked as `capability`; old resolver `unblock/health/77ecb7c02175dccf/resolve` and the exact retry resolver `unblock/health/f1d45979a4fa0e0f/resolve` are settled with this evidence. |
| Transcriber | The supported replacement `mesh-room-gigaam.service` is active in the user manager, `MainPID=1399`, `NRestarts=0`. `~/.mesh/room-transcript.txt` and `~/.mesh/.room-gigaam-last` both refreshed at 14:18:59 UTC. `mesh-room-transcribe.service` remains inactive; no restart or unit swap was needed. | `health-warning/39b152384383b0fa73e9/triage` and `unblock/health/ec36985eb8c20125/resolve` completed against this evidence. |
| Wake reflex | `timeout 90s mesh-room-reflex --test` passed the per-line, prune-safe, name-gate, ambient-gate, mint, and listening-ack checks. Enabled/started the owned user service; `mesh-room-reflex.service` is enabled and active (`MainPID=1224538`). Its unit Wants/After `mesh-room-gigaam.service`; GigaAM stayed active and the retired transcriber stayed inactive. A normal `mesh-room-sense-loss` tick now reports `wake LIVE (stored:LIVE)`. | `health-warning/10494c92497316a2185c/triage` and `unblock/health/8fb37e9441ed8e69/resolve` completed against this evidence. |

The old receipts dated 2026-09-11 describing operator-revival approval are historical and superseded by this live audit and the operator's current autonomous-action authorization. No functioning replacement was restarted. The local motion camera's real-read evidence is included only to distinguish it from the unreachable primary room eye.

The separate `unblock/adint/3dd6562eb2e7cc86/resolve`, `unblock/adint/4cc57fbd6684b8a0/resolve`, and `unblock/adint/c114f99a12f3db5d/resolve` rows remain owned by `adint`; the next ordered reconciliation step verifies and settles those exact rows.
