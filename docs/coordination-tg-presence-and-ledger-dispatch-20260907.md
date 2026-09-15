# TG presence and Ledger dispatch — witness pilot

Date: 2026-09-07

## Verdict

**BLOCKED**. The live staffing pilot reached the intended fail-closed boundary because
`/home/mesh-home/.mesh/charter/adint.md` is missing. Both `scripts/mesh-staffing --json` and
`scripts/mesh-board available --json` exited 2 without proposing a worker. The pilot promise
remains open and retryable.

## Evidence

- Witness owner receipt: `mesh-task take tg-presence-ledger-dispatch-20260907 pilot-and-witness-staffing`.
- Chain status: steps 1–4 done; step 5 active and owned by `witness`.
- Source/deployed equality: `scripts/mesh-staffing` SHA256
  `22782ea0e4ba04febad491886702f58e5b272ff18c74645c0570de2d6e73b959`; deployed copy matches.
- Source/deployed equality: `scripts/mesh-dispatch` SHA256
  `e2d7afef5789200a96fa2691b48f70fb87de8d86fe44b127cb7791e6fb6e1c7a`; deployed copy matches.
- `tests/test-mesh-staffing.sh`: PASS.
- `tests/test-mesh-tg-dispatch-policy.sh`: PASS.
- `tests/test-mesh-dispatch-hledger-gate.sh`: PASS.
- `python3 scripts/mesh-task --test`: PASS.
- `mesh-promises --check`: PASS; replay and hledger agree, with 6 open promises and 7 holds.

## Retry

After the charter input is restored, rerun:

```bash
scripts/mesh-staffing --json
scripts/mesh-board available --json
mesh-promises --check
mesh-task status tg-presence-ledger-dispatch-20260907
```

Do not close the witness promise until a live eligible census, one bounded owner receipt, and
the deliberate failed-delivery/retry arm are evidenced.

## Resolution update — 2026-09-07T22:35Z

The missing node-local charters were restored from the repository source by the new
`scripts/mesh-charter-watch` reflex. Thirteen missing charters were copied atomically; the existing
`haunt.md` local engine customization was preserved and reported as divergent. The deployed watcher
has source/deployed SHA-256 parity and exactly one live `*/5 * * * *` crontab entry.

The live census now passes (`scripts/mesh-staffing --json`, 15 windows, 8 eligible), and the
hyphenated `tg-roz` heading parser regression is fixed. The stale node-local
`MESH_MIND_WORKERS="genome"` override was removed from `~/.mesh/restore.env`; dispatch now derives
its default pool from eligible staffing rows while still honoring explicit temporary overrides.
`mesh-dispatch --status` now reports 8 idle workers. A live pass reached the spend governor and
returned `PACE-SKIP`; `mesh-pace --check dispatch` independently confirms the current hold, so this
is deliberate pacing, not a census/routing failure.

Verification: `mesh-dispatch --test` PASS (264 assertions), staffing/charter/reflex/policy/hledger
tests PASS, `mesh-promises --check` parity/agreement/roster PASS, and source/deployed hashes match.

The first two cron-like watcher runs exposed `staffing_rc=127` because the reflex did not export its
own tool path; that was fixed in commit `0fbb3ced`. A clean-environment deployed invocation now exits
zero with `staffing_rc=0`, and the focused reflex test covers this path.
