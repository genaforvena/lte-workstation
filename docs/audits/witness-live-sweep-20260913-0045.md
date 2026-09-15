# Witness live sweep — 2026-09-13 00:45Z

## Evidence

- `mesh-dash --once witness` showed 1,040 task rows, 97 unfinished, 116 rejected, 827 done; source age 12s; 20/58,577 unfiltered chat lines shown.
- `mesh-task audit` reported `task_source=PASS`, 58,576 replayed events, and 0 source errors. It identified two genome-owned discrepancies: `tg-layout-migration-owner-receipt-20260912/settle-expired-owner-receipt` is `OPEN_UNOWNED`, and `tg-scripts-layout-migration-20260912/retire-layout-shims` is overdue. Neither is witness-owned.
- `mesh-task queue --dispatch --owner witness` returned no eligible row. The four queued witness candidates in the journal all failed `mesh-task check dispatch <chain/step> witness` with exit 2: `tinyfleet-real-mesh-pilot-20260907/verify-and-report-pilot`, `tinyfleet-architecture-drift-review-20260907/critical-publishability-review`, `crypthauntology-kids-followup-20260912/adult-study-release-independent-review`, and `task-queue-stall-tinyfleet-proof-20260912/verify-live-proof`.
- The live pane reported `root-mesh-devcd-catch` down (count 142), a divergent haunt charter watch (count 125), FYI replay coverage partial, and the 00:31Z doctor line at 3 FAIL / 33 WARN. The doctor line reports egress on `tailscale0`, a configured exit node, and a `mesh-model-swap` smoke-test failure. These are observations; this sweep did not change substrate state.
- Attempted the required terse `[idle]` update. `mesh-chat` suppressed it as same-state duplicate (×14); the standing idle record remains canonical.
- Refreshed `mesh-wake-expect witness` for 300s to cover only journal source-age churn, FYI age/source-cutoff refresh, the pane-live timestamp, and the recurring Note3 battery line. Mutable task/health counts remain unpredicted and should wake the pane.
- Final live recheck at 00:47Z: the hire preflight completed, changing the materialized totals to 1,040 rows, 96 unfinished, 116 rejected, 828 done, and zero running; both genome-owned discrepancies remain. The owner-scoped queue still returned no row (exit 0), and the four witness candidates remain dispatch-ineligible.

## Next check

On the next witness wake, run `mesh-dash --once witness`, reread `~/.mesh/tasks.journal` and `~/.mesh/chat.log`, run `mesh-task audit`, and re-check any changed witness candidate with `mesh-task check dispatch` before taking it.
