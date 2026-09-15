# Crash-proof recovery audit — 2026-09-12

Audited `docs/superpowers/specs/2026-07-18-crash-proof-recovery.md` against the deployed commands,
current crontab, focused helper tests, and the task ledger. No live mind was killed.

| Prong | Evidence | Finding |
|---|---|---|
| P1 `mesh-wip-commit` | `mesh-wip-commit --test` passed: tracked and untracked capture, unchanged HEAD/branch/index/worktree, clean no-ref, repeat no-churn, restore behavior. Crontab line 175 runs it every 5 minutes. | Helper and cadence wiring are present; this is a helper test, not an engine crash drill. |
| P2 `mesh-handoff --snapshot` | `mesh-handoff --test` passed: snapshot extraction, fresh-manual no-clobber, bounded restore from 100× scrollback, clear coupling, and WIP-ref branches. Crontab line 176 runs it every 5 minutes. | Snapshot and cadence wiring are present; this is a helper test, not proof of recovery after a killed engine. |
| P3 `mesh-mind-recycle` | `mesh-mind-recycle --test` passed for decision branches, loop prevention, shadow/live action split, and unsafe model-down refusal. `mesh-mind-recycle --status` lists no active windows. No recycle invocation appears in crontab or the searched Codex/repository hook configuration. | Decision helper exists and its local tests pass; live busy→idle activation was not found, so the spec's every-idle-edge invariant is not established. |
| P4 actual recovery | No P4 recovery receipt or matching task existed in task replay. The spec requires an isolated SHADOW/test window and a real recovered session. | Not performed: no isolated test window was established, and killing a live mind would violate the spec. Do not claim crash-proof recovery from P1–P3 helper tests alone. |

Commands actually run:

```text
mesh-wip-commit --test       rc=0
mesh-handoff --test          rc=0
mesh-mind-recycle --test     rc=0
mesh-mind-recycle --status   rc=0; no rows
crontab -l                   P1 and P2 every 5 min; no P3 entry
```

Follow-up tasks were registered as chain `design-spec-crash-proof-followup-20260912` from
`docs/plans/2026-09-12-crash-proof-recovery-followup.tsv`:

- `verify-and-wire-mind-recycle-shadow` (genome): inspect actual deployment wiring and establish
  shadow-first busy→idle activation through `mesh-clear`, without enabling live clears before the
  unsafe-gate evidence passes.
- `p4-shadow-crash-drill` (pub): run the real dirty-work/no-manual-handoff recovery drill only in a
  proven isolated test window, and record actual recovery for engine kill, `/clear`, and simulated
  reboot. Stop if isolation cannot be proven.

This audit establishes green isolated helper tests and P1/P2 cron wiring only. It does not establish
live P3 activation or the P4 end-to-end recovery guarantee.
