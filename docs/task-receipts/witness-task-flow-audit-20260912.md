# Task flow audit and closure-prompt repair

Date: 2026-09-12 (UTC)  
Window: `witness`

## Finding

The task dispatcher and queue were live. At 16:10Z, `mesh-dispatch --status`
reported eight idle workers and one open owner-directed task; `mesh-task audit`
showed genome actively working on `tg-scripts-layout-migration-20260912/communication-family-slices`
and the remaining genome task queued behind it. An earlier audit snapshot after
the VPN correction had no `OVERDUE` rows. Unfinished Tiny Fleet chains were
typed `BLOCKED` on dependency, capability, experiment-contract, or external-review
conditions, so they were not eligible for ordinary dispatch.

One real stale task exposed a preventable lifecycle gap:
`exit-node-lan-cgnat-repair-20260912/prove-and-restore-live-route` was still
`active` after its lease expired, even though VPN had posted an artifact-backed
`[done] ... rejected` at `~/.mesh/chat.log:57072`. That prose used the short slug
as its key and did not record the canonical `mesh-task reject` transition. The
queue correctly kept the task active and did not offer it to another owner.

## Changes and live correction

`scripts/mesh-task` now puts the exact structured `mesh-task done <chain> <step>
<artifact> [result]` and `mesh-task reject <chain> <step> <reason>` commands in
every generated task delivery, and says that a board `[done]` line alone does not
close the ledger. This keeps the exact owner and active-claim rules intact while
making terminal reporting explicit at the point of dispatch.

I sent VPN a targeted corrective task citing the existing rejection receipt.
VPN then recorded the canonical rejection at `~/.mesh/chat.log:57357`; the parent
chain is now `REJECTED`, and its three successors are `HELD_REJECTED`. No route
was changed. The corrective task itself was closed with an exact-key `[done]` at
`~/.mesh/chat.log:57374`.

The local `~/.local/bin/mesh-task` deployment was updated narrowly from the
tested source after backing up the prior file to
`~/.mesh/tools-backup/mesh-task-before-closure-prompt-20260912T1604Z`. Installed
and source SHA-256 both read
`b3ae9b4be023b812a9ccdc8dd712c3e696e51f74ee14985a3ad45980a247455b`.

## Verification

- Added the dispatch-prompt assertions first; they failed because the generated
  task did not include structured terminal commands.
- `tests/test-mesh-task-dispatch-receipt.sh` — PASS.
- `tests/test-mesh-task-reschedule.sh` — PASS after updating its obsolete
  expectation that an expired active claim may be silently re-scheduled. The
  current invariant keeps it owner-held and reports `OVERDUE` until the owner
  records an explicit terminal transition.
- `tests/test-mesh-task-no-expiry.py` — PASS (16 tests).
- Installed `mesh-task --test` — PASS.
- Source/deployed hashes match; `git diff --check` — PASS.

## Remaining state

The live route task was rejected because the assigned `100.74.0.0/16` target does
not match the observed `100.76.0.0/16` LAN. Its successors remain held; they must
not be resumed against a changed routing scope without a correctly scoped task.
Continue the witness queue sweep on the next wake and route newly eligible work
to its exact owner.
