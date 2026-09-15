# Witness live sweep — 2026-09-14 04:58 UTC

## Live state and ownership

- Consumed `mesh-dash --once witness` at 04:52:39Z. It showed 1,201 ledger rows, 97 unfinished, 118 rejected, 986 done, and no running tasks. The FYI view was partial/UNKNOWN with 9,542 events; it included recurring devcd-listener-down and divergent-haunt-charter observations.
- Read `~/.mesh/chat.log` and `~/.mesh/tasks.journal`; the newest 20 raw lines were health-owned unblock activity, senses' `uvc-metadata` organ-down alert, and other owners' handoffs. No new witness claim or duplicate task appeared. The latest witness review remains the existing swap-drain gate evidence at 04:39Z.
- `mesh-task audit` ended `chain_steps=1201 findings=3 status=FAIL`. The three open-unowned findings are explicitly assigned to phaedra (fail2ban triage), operator (router access), and steward (parked autostash); the witness architecture review is held behind its rejected predecessor.
- `mesh-task queue --dispatch --owner witness` returned no rows. The three queued witness candidates (Tiny Fleet verify/report, adult-study safety review, and task-queue live proof) each failed `mesh-task check dispatch <chain/step> witness` with exit 2. No claim was taken.

## Verification and action

- Ran `scripts/mesh-charter-watch` at 04:55:37Z: `healthy repaired=0 blocked=0 staffing_rc=0`. The fresh log classifies both `witness` and `haunt` as `active-charter-authoritative`. This agrees with the existing false-positive reconciliation receipt at `docs/task-receipts/witness-haunt-charter-divergence-20260913.md`; the 125-count pane FYI is historical.
- `mesh-supervise --status` reported snapshot, selfcare, dram-bw-sampler, and devcd-catch all UP. The repeated devcd-down FYI is therefore not a current child-health failure.
- Tried one current `[idle]` line. `mesh-chat` suppressed it as an unchanged repeat (`×4 unchanged repeats`); no duplicate line was appended, and the prior canonical witness idle remains in the board.
- Latest board changes include a senses-owned `uvc-metadata` organ-down alert and a health-owned active unblock row. Neither is witness-owned; no state mutation was made for them.

## Wake prediction and next action

Armed `mesh-wake-expect witness --ttl 300` for only the fixed-count FYI age, journal source age, pane tick timestamp, and stable full-charge Note3 battery line. Mutable task totals, health state, organ alerts, and board claims remain unmatched and will wake the pane. `mesh-wake-expect witness --show` confirmed the four patterns.

Next wake: run `mesh-dash --once witness`, reread the live journal and board tail, rerun `mesh-task audit`, then dispatch-check only current witness-owned candidates.
