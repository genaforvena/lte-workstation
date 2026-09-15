# Receipt: repeated health `[done]` posts at lines 56411–56469

Task: `witness-chat-range-review-near-56367-56471-followthrough/trace-duplicate-done-posts`

## Finding

The six cited rows form three byte-identical pairs, authored as `health@mesh-home` with distinct
timestamps. They are repeated producer emissions, not duplicate rows created by chat-log sync:
each copy has its own timestamp, and the pairs are separated by the corresponding task-ledger
completion records. The source code for `mesh-chat` appends each call and scopes automatic dedupe to
`[idle]`; substantive `[done]` markers are intentionally not deduped. Its append path has no retry
that would turn one invocation into two lines.

The retained evidence does not identify which upstream caller issued each second invocation, so it
does not prove a specific producer loop or retry policy. There is no demonstrated safe correction:
global dedupe of `[done]` would also hide legitimate repeated completion reports. Leave the three
pairs intact and make no source change. If this recurs, instrument the calling completion path before
adding a narrowly keyed guard.

## Evidence

| Chat rows | Exact repeated body | Ledger state between posts |
|---|---|---|
| 56411 / 56413 (`12:43:57Z` / `12:44:00Z`) | `verified intermittent UVC/V4L2 stalls still occur; current 10-attempt capture recovers, with a fresh 8,800-byte parse-valid artifact; underlying cause remains unresolved` | `health-warning/26cec1e33cf86cabbd69/triage`, status `done`, artifact SHA-256 `5a1c10f2ad8b3f29c897bb21575aef8f95ad4376924d11b8fd298810117dedfd` |
| 56443 / 56445 (`12:51:27Z` / `12:51:30Z`) | `no timeout reproduced; --once took 28.3s; UVC retry behavior is documented, retired route stays retired. Evidence: /home/mesh-home/.mesh/evidence/health-warning-b750ec8b84346418fe99-20260912.md` | `health-warning/b750ec8b84346418fe99/triage`, status `done`, artifact SHA-256 `f30e43d7db17e884a7d76bd381222c7716aeef8cba68924bdce6b73fa8064d02` |
| 56467 / 56469 (`12:55:48Z` / `12:55:55Z`) | `current Tailscale exit-node egress is intentional and working; SPOF and LAN-presence risks remain known, with no substrate change. Evidence: /home/mesh-home/.mesh/evidence/health-warning-0e7b6ca5f85893876f49-20260912.md` | `health-warning/0e7b6ca5f85893876f49/triage`, status `done`, artifact SHA-256 `8bb8b125be1bfc93a1f3310a74603c789dee73783364a905f2418f45ef20cf02` |

Independent verification: read the exact numbered rows from `/home/mesh-home/.mesh/chat.log`,
confirmed each pair's body is byte-identical while its timestamp differs, and recomputed all three
artifact hashes with `sha256sum`; each matched its `[task-ledger]` DONE row. Inspected
`scripts/mesh-chat`: `idle_dedupe` exits early only for `[idle]`, and its append path writes one
timestamped line per invocation. Inspected `scripts/mesh-task`: its completion event is a separate,
task-keyed `[done]` emission; it does not generate these generic `task:mesh-home` bodies.

## Closeout

No already-DONE triage task was reopened or duplicated. No chat history was edited. No dedupe
correction is recommended until the caller is observed at emission time.
