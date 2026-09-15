# adint room revival resolver reconciliation — 2026-09-13

Task: `room-revival-ledger-reconciliation-20260913/verify-and-settle-revival-resolvers`
Checked: 2026-09-13 14:33 UTC on `mesh-home`.

Health's preceding receipt, `health-room-revival-ledger-reconciliation-20260913.md`, was read
and its three dispositions were independently checked against live service and artifact output.
The historic adint receipts that asked for an operator revival decision are superseded by the
operator's current authorization for autonomous mesh operation. That authorization does not create
missing iMac reachability.

| Original adint resolver | Current evidence | Final state |
|---|---|---|
| `unblock/adint/3dd6562eb2e7cc86/resolve` (room camera) | `timeout 8s ssh -o BatchMode=yes -o ConnectTimeout=5 ilya@192.168.8.214 true` exited 255 with connection timeout. Health identifies `mesh-imac-cam --test` as the required real-read verification after SSH returns. The local motion camera is not a replacement for this primary iMac room eye. | Remains blocked as a capability dependency. Retry event: the bounded SSH command exits 0; then require `mesh-imac-cam --test` to complete a real read before resuming. No camera service was started. |
| `unblock/adint/4cc57fbd6684b8a0/resolve` (wake reflex) | `mesh-room-reflex.service` is enabled and active/running (`MainPID=1224538`, `NRestarts=0`). `timeout 90s mesh-room-reflex --test` passed its per-line, prune-safe, no-replay, name, ambient, mint, and listening-ack checks. | Done against this receipt; supported service already works, so no restart or unit change was needed. |
| `unblock/adint/c114f99a12f3db5d/resolve` (transcriber) | `mesh-room-gigaam.service` is active/running (`MainPID=1399`, `NRestarts=0`); retired `mesh-room-transcribe.service` remains inactive/dead. Both `~/.mesh/room-transcript.txt` and `~/.mesh/.room-gigaam-last` were nonempty and refreshed at 14:32:36 UTC. `timeout 90s mesh-room-gigaam --test` passed the real-read fixture, RMS gate, and prune checks. | Done against this receipt; current supported GigaAM replacement produces fresh output. No retired service was started. |

The camera retry remains tied to an observable network result and a real-read gate, not a generic
permission wait. The local motion camera's artifact was not substituted for the iMac eye.
