# Phone blocker resolver backlog reconciliation

- Checked: 2026-09-12 (UTC)
- Parent: `coordination-hledger-identity-phone-20260908/phone-authorized-keys-recheck`
- Blocker key: `88dbdd74fbfeb7323a72f801f1096e9d`
- Result: 43 stale resolver attempts rejected; attempt 45 retained and completed with an unresolved external prerequisite. Parent remains blocked.

## Audit and disposition

Before changing these rows, the task ledger contained exactly 44 pending `unblock/genome/*` chains for the parent, numbered attempts 2–45. Every row had the same `unblock_for` key, an empty `unblock_epoch`, owner `genome`, and an open current `resolve` task. Each had no `last_progress`, `progress_artifact`, `artifact`, or `result`. Their descriptions and prerequisite were identical. No row had distinct owner progress or evidence, so attempts 2–44 were safe to reject as pre-fix duplicates of the unchanged blocker epoch. Attempt 45 is the sole retained resolver.

The same rejection reason was recorded on every attempt 2–44:

> superseded duplicate resolver: the pre-fix sweep duplicated the same unchanged blocker epoch 88dbdd74fbfeb7323a72f801f1096e9d; this exact row had no owner progress or artifact, and attempt 45 is retained as the sole current resolver

| Attempt | Settled task ID | Disposition |
|---:|---|---|
| 2 | `unblock/genome/7d586c6d331aaa97/resolve` | Rejected; reason above |
| 3 | `unblock/genome/1676885757272015/resolve` | Rejected; reason above |
| 4 | `unblock/genome/cd9f690ed051e7df/resolve` | Rejected; reason above |
| 5 | `unblock/genome/ca5d163633da3d59/resolve` | Rejected; reason above |
| 6 | `unblock/genome/31e27722ec623090/resolve` | Rejected; reason above |
| 7 | `unblock/genome/0046aa25b2d4577d/resolve` | Rejected; reason above |
| 8 | `unblock/genome/4eea9f5fb1dcb079/resolve` | Rejected; reason above |
| 9 | `unblock/genome/46f98f2a4336a0fe/resolve` | Rejected; reason above |
| 10 | `unblock/genome/d1d5ba032a7a9003/resolve` | Rejected; reason above |
| 11 | `unblock/genome/96dd47b7ec4e45ad/resolve` | Rejected; reason above |
| 12 | `unblock/genome/29584579e98da751/resolve` | Rejected; reason above |
| 13 | `unblock/genome/236a2ee19a997cd7/resolve` | Rejected; reason above |
| 14 | `unblock/genome/e3bb77ed51b5aba9/resolve` | Rejected; reason above |
| 15 | `unblock/genome/607e31b6dc994243/resolve` | Rejected; reason above |
| 16 | `unblock/genome/3e984f2f1c3e129f/resolve` | Rejected; reason above |
| 17 | `unblock/genome/d1cfa3aa9a30c5d4/resolve` | Rejected; reason above |
| 18 | `unblock/genome/c64d76cf0de8ca78/resolve` | Rejected; reason above |
| 19 | `unblock/genome/72ad6202e73656f9/resolve` | Rejected; reason above |
| 20 | `unblock/genome/4d142199b051deb7/resolve` | Rejected; reason above |
| 21 | `unblock/genome/5db584ca4da227f2/resolve` | Rejected; reason above |
| 22 | `unblock/genome/d7474788f946dea1/resolve` | Rejected; reason above |
| 23 | `unblock/genome/7b2e3ee80e2a1e36/resolve` | Rejected; reason above |
| 24 | `unblock/genome/1345e7a2c0c5d5fd/resolve` | Rejected; reason above |
| 25 | `unblock/genome/884b53c6d53b1c28/resolve` | Rejected; reason above |
| 26 | `unblock/genome/e5063ec72a282802/resolve` | Rejected; reason above |
| 27 | `unblock/genome/c346ded18779cf36/resolve` | Rejected; reason above |
| 28 | `unblock/genome/d2c2e9737d86c6ba/resolve` | Rejected; reason above |
| 29 | `unblock/genome/fedb3634111d6287/resolve` | Rejected; reason above |
| 30 | `unblock/genome/b3b655b1df989e87/resolve` | Rejected; reason above |
| 31 | `unblock/genome/594a3a56f4d0b1dc/resolve` | Rejected; reason above |
| 32 | `unblock/genome/98e5f11ad454b3b3/resolve` | Rejected; reason above |
| 33 | `unblock/genome/9bb8545f25976415/resolve` | Rejected; reason above |
| 34 | `unblock/genome/c069ba364c8e33fd/resolve` | Rejected; reason above |
| 35 | `unblock/genome/64e88167f9c44ce3/resolve` | Rejected; reason above |
| 36 | `unblock/genome/ef750a96c3797794/resolve` | Rejected; reason above |
| 37 | `unblock/genome/a1591afb854d83df/resolve` | Rejected; reason above |
| 38 | `unblock/genome/b166c340a91c6af9/resolve` | Rejected; reason above |
| 39 | `unblock/genome/03bdf3d91296e47b/resolve` | Rejected; reason above |
| 40 | `unblock/genome/8aab682698da5130/resolve` | Rejected; reason above |
| 41 | `unblock/genome/ec9e2fe8cdf5b6d6/resolve` | Rejected; reason above |
| 42 | `unblock/genome/3f93a0092f8a9126/resolve` | Rejected; reason above |
| 43 | `unblock/genome/a9423a6456fbfd32/resolve` | Rejected; reason above |
| 44 | `unblock/genome/1cdc28c209ca9dc0/resolve` | Rejected; reason above |
| 45 | `unblock/genome/9e5a9a65af12087f/resolve` | Retained as the sole current resolver; completed below |

## Retained resolver result

The fresh read-only SSH check was `timeout 10 ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=4 -o StrictHostKeyChecking=accept-new u0_a380@100.103.99.16 termux-battery-status`. It timed out (`ssh_rc=255`, `Connection timed out`). `mesh-phone-ip` returned its last-good address and explicitly skipped its ADB fallback because `PHONE_ADB_SERIAL` is unset. Neither result confirms phone reachability. The earlier receipt [unblock-operator-2f17619fc508be96-resolve-20260911.md](unblock-operator-2f17619fc508be96-resolve-20260911.md) likewise records all then-known candidates closed or timed out and no operator reachability confirmation.

The actionable prerequisite remains operator confirmation that the phone is reachable over SSH at the recorded endpoint; only then can `phone-authorized-keys-recheck` safely recheck the phone's `authorized_keys`. The retained resolver is completed as an artifact-backed unresolved result. The parent remains `blocked` on `operator-input`, with retry `retry after operator reachability confirmation`; no resume was issued.

## Verification

- `mesh-task replay --json`: attempts 2–44 are `rejected` with the exact reason above; attempt 45 has this artifact as its completion evidence.
- `mesh-task audit`: run after closure; see recorded result in the completion handoff.
- `mesh-task queue --dispatch --owner genome`: run after closure; verify the settled duplicates are absent from dispatch and the parent remains blocked.
- Parent `mesh-task status coordination-hledger-identity-phone-20260908`: must remain blocked unless new, actual phone reachability evidence appears.
