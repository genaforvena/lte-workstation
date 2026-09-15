# Job autonomy and repository synchronization audit — 2026-09-12

Task: `design-audit-task-sweep-20260907/design-audit-job-and-sync` (owner `tg`; dispatch check exited 0 before claim).
Sources: `docs/job-autonomy-audit-20260907.md` and `docs/repo-sync-audit-20260907.md`.

## Job autonomy

The repaired bounded Getmatch path remains installed and wired. Both the node-local desired set
(`~/.mesh/reflexes.cron`) and live crontab have exactly one Getmatch apply line:
`19 8,14 * * * ... mesh-job-apply-getmatch --top 1`. The source declares the same
`# reflex-cadence: 19 8,14 * * *` and `# reflex-args: --top 1`. No unbounded duplicate is present.

The five audited job tools (`mesh-job-apply`, `mesh-job-apply-getmatch`, `mesh-job-confirm`,
`mesh-job-cal`, and `mesh-job-reply`) match their deployed `~/.local/bin` copies byte-for-byte by
SHA-256. The current confirmation query returns `[]`; the calendar agenda is empty. These are fresh
observations, not a claim that the historic Getmatch application outcomes were re-reconciled.

Focused checks passed: `tests/test-job-apply-tg-policy.py`, `tests/test-job-hh-serialization.sh`,
`tests/test-job-reply-parser.sh`, `tests/test-job-dispatch-ownership.sh`, and deployed
`mesh-job-apply-getmatch --test`, `mesh-job-confirm --test`, and `mesh-job-cal --test`. The
interview-confirm test script has one stale fixture: it expects `current_proposed()` to treat
`2026-01-01` as current, while the implementation intentionally accepts only appointments live or
within 90 minutes of the present. On 2026-09-12 the assertion correctly returns false. The
confirmation parser's physical-place extraction itself returned the expected value. This audit left
the existing test file unchanged.

`mesh-reflexes --check` remains non-zero because `/home/mesh-home/.local/bin/mesh-clear-loss
--canary` is missing. This is an unrelated global reflex parity issue; the targeted job entries are
present in both desired and live schedules.

## Repository synchronization

Fresh bounded fetches found clean upstream advances in `.fzf` (8 commits) and
`prebid-local/prebid-server` (1 commit). Both trees were clean and strictly behind, so each was
fast-forwarded. Post-update status is clean and aligned with the fetched branch. `.mesh/gigaam-src`
remains clean and aligned.

The `src/llama.cpp-prism` fetch succeeded and advanced `origin/prism`; the local `prism` branch is
still clean but divergent, now 43 ahead / 1131 behind. It was left untouched because this still
requires an explicit merge/rebase choice. Fetching `.mesh/knowledge` exceeded the 20-second bound;
its tree was left untouched and still reports 85 commits ahead of `default-string/main`, so its
remote freshness is unknown.

## Remaining obligations

- Refresh or replace the stale January date fixture in `tests/test-job-interview-confirm.sh` before
  using that script as a current regression gate.
- Restore the missing deployed `mesh-clear-loss --canary` reflex parity; it is outside the job lane
  and needs its own repair.
- Decide explicitly whether and how to reconcile the 43/1131 `prism` divergence.
- Retry a bounded fetch for `.mesh/knowledge`, then compare before choosing any synchronization.

## Verification evidence

- `mesh-job-confirm --json` → `[]`; `mesh-job-cal --agenda --json` → `[]`.
- Desired and live schedules each contain one `mesh-job-apply-getmatch --top 1` line at 08:19 and
  14:19; no unlimited duplicate was found.
- SHA-256 comparison matched all five source/deployed job-tool pairs.
- All job checks listed above passed except the single stale date assertion in
  `tests/test-job-interview-confirm.sh`.
- `mesh-reflexes --check` reported 242 reflexes verified firing and 104 not decidable in its
  3600-second window, but exited 1 for the missing `mesh-clear-loss --canary` line.
- Post-fetch repository status: `.fzf`, `gigaam-src`, and `prebid-server` clean/aligned;
  `llama.cpp-prism` clean/divergent at 43/1131; `knowledge` clean locally/ahead 85 with remote fetch
  timed out.

No job source, configuration, or dirty repository content was edited. The only repository
synchronization changes were the two clean fast-forwards above.
