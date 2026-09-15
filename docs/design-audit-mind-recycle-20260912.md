# Mind recycle design audit — 2026-09-12

Audited `docs/superpowers/specs/2026-07-18-mind-recycle-design.md` against the current Claude
Stop hook, Codex lifecycle hooks, cron wiring, implementation, and live loss-meter output. No live
mind was cleared or stopped during this audit.

| Obligation | Evidence | Finding |
|---|---|---|
| Trigger and activation | `~/.claude/settings.json` has `mesh-stop-check` on `Stop`, with no `mesh-mind-recycle`; `~/.mesh/reflexes.cron` has no recycler line. `mesh-mind-recycle --status` lists no active windows. The driver source explicitly says it is shadow-default and intentionally unwired. | The spec's Stop-hook-primary trigger is not active. `mesh-mind-recycle` polls pane state when invoked; there is no deployed invocation here. Its local helper test does not prove a trigger runs. |
| Clear-loss meter | `~/.mesh/reflexes.cron` runs `mesh-clear-loss --canary` daily at 04:17 UTC and `mesh-clear-audit` every five minutes. `mesh-clear-loss --report` reports `N=12`, `COST_ALL=+0.42`, `LAST_TS=2026-09-11T04:17:02Z` (budget −0.33, naming +1.00, schema +1.00, units +0.00). | The judge-free meter is wired and records nonzero recycled-arm loss. Its report groups by task type; it does not label real stop outcomes as `done` or `unfinished`, so these data cannot select between every-stop and done-only clearing as the spec's sequencing section promises. |
| Current clear safety | `mesh-clear --test` passed: it writes the handoff before `/clear`, refuses on running/undelivered background work, and reaps a stale dead-pid manifest. The current `mesh-clear --gate` is a background-delivery safety check, not a handoff coverage/model judgment. | Some recycler comments and log text still describe a handoff-coverage verdict. That branch of the 2026-07-18 spec was superseded by the deterministic background-work gate and should be reconciled. |
| Codex completion lifecycle | `.codex/hooks.json` wires `mesh-codex-lifecycle --start` and `--end`; `~/.codex/config.toml` wires its completion notification. `python3 scripts/mesh-codex-lifecycle --test` passed, including handoff-before-clear, busy deferral, idempotent completion receipts, and quiet reset. | Codex has a separate end-of-turn persistence-and-clear path. It does not activate the Claude pane-polling recycler or establish a shared Stop-hook policy across engines. |
| Driver and meter helper gates | `mesh-mind-recycle --test` and `mesh-clear-loss --test` passed. `mesh-clear-loss --probe tg` remains explicitly a scaffold (not run; the implementation reports it unsupported). | These tests establish helper behavior and meter calibration only. They do not prove recycler wiring, outcome-stratified policy evidence, or live shadow behavior. |

An existing task already covers inspecting and wiring shadow-first recycler activation:
`design-spec-crash-proof-followup-20260912/verify-and-wire-mind-recycle-shadow` (owner `genome`).
This audit did not duplicate that task. A separate follow-up is registered for the unresolved
policy measurement and spec/implementation reconciliation.

Commands run:

```text
mesh-mind-recycle --test             rc=0
mesh-mind-recycle --status           rc=0; no active windows
mesh-clear-loss --test               rc=0
mesh-clear-loss --report             rc=0; N=12, COST_ALL=+0.42
mesh-clear --test                    rc=0
python3 scripts/mesh-codex-lifecycle --test  rc=0
```

The evidence establishes an active daily canary and tested clear/completion helpers. It does not
establish a deployed Claude recycler, an outcome-based trigger choice, or live shadow behavior.
Live clearing remains disabled and no activation was performed.
