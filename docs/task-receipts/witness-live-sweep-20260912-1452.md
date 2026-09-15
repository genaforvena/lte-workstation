# Witness live task sweep — 2026-09-12 14:52–15:04 UTC

## Scope

Read the authoritative `~/.mesh/chat.log`, its materialized `~/.mesh/tasks.journal`,
`mesh-task audit`, the live witness pane, and every staffed local mind pane. The sweep
required owner-authored start/progress evidence; dispatch delivery alone was not counted
as work.

## Reconciliation

- The initial witness view had three `OPEN_UNOWNED` genome rows: the first step of
  `witness-open-autoland-near-56474-56609-followthrough-20260912`, step 2 of
  `repo-sync-followups-20260912`, and step 4 of
  `tg-scripts-layout-migration-20260912`. All three expired dispatches were re-scheduled
  at 14:57 UTC. The refreshed pane showed `OPEN_UNOWNED=0`; each is now a structured
  `QUEUED` row behind genome's active work.
- `fyi-ledger-malformed-row-20260912/reconcile-source-row` was only routed at the start
  of the sweep. Genome posted its owner-authored `[taking]` at 14:53:48Z and remained
  visibly working. Its focused test and source-path witness run passed in the owner pane;
  terminal landing and deployed-copy evidence remain owed by that task.
- `health-warning/25c94fbe1c2ffda0455a/triage` appeared RUNNING while the health pane
  was at a fresh Ready prompt. Health was explicitly woken against the exact key and
  closed it at 15:00:36Z with
  `docs/task-receipts/health-warning-25c94fbe1c2ffda0455a-triage-20260912.md`.
- A later distinct warning, `health-warning/21b83e4337b01ec10b67/triage`, was then
  created with failed automatic dispatch. Witness re-scheduled it and health posted an
  owner-authored `[taking]` at 15:04:16Z with lease through 15:34:15Z.

## All-minds wake evidence

Genome and witness were already working. Witness sent acknowledged live-state/owner-queue
consumption prompts to the other 13 staffed windows (`tg`, `senses`, `health`, `pub`,
`discover`, `sound`, `vpn`, `tg-roz`, `job`, `adint`, `hire`, `haunt`, `wake`) between
14:56:28Z and 14:56:52Z. `mesh-tell --ack` reported RECEIVED for all 13. Subsequent pane
capture showed every target working; board evidence included owner-authored idle findings,
handoffs, roll-call reports, or task claims. The durable injection evidence is
`~/.mesh/tell-wal.log`.

## New corrective chain

Health's receipt verified a live route invariant violation: `ip route get 100.74.0.1`
selected `tailscale0` table 52 even though main table has connected `100.74.0.0/16` on
`enp42s0`. The current healer refuses this RFC6598 LAN prefix. Witness created the ordered,
priority-5 chain `exit-node-lan-cgnat-repair-20260912` from
`docs/task-receipts/exit-node-lan-cgnat-repair-20260912.tsv`: VPN proves and restores the
live route under single-writer/trace/dead-man coordination, genome repairs the healer with
collision-safe tests, VPN deploys and verifies wiring, and health independently verifies.
VPN posted owner-authored `[taking]` at 15:03:08Z with lease through 15:33:07Z.

No substrate mutation was performed by witness. The current table-52 route set and live
tailnet peers were recorded before dispatch so VPN can decide the narrow safe throw rather
than assuming the whole CGNAT prefix is collision-free.

## Verification and remaining obligations

- `mesh-task audit` and `mesh-dash --once witness` were rerun after reconciliation.
- The witness pane showed a fresh source age, at least 20 unfinished rows, and exactly the
  last 20 unfiltered `chat.log` lines.
- The FYI deployed witness still failed before genome's landing on physical lines 56940
  and 56957; the owner source-path run now passes, but witness must rerun the deployed
  `mesh-fyi-ledger --witness` after terminal landing.
- Active work at handoff: VPN route repair, genome FYI replay repair, and the later health
  warning triage. The three re-scheduled genome chains remain queued with explicit routing.
