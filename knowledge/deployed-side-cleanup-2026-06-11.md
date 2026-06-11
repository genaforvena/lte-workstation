# Deployed-side cleanup — 2026-06-11

Scope: `mesh-breath`, `mesh-guardian`, `mesh-load`, `mesh-onboard`, `mesh-study`, `mesh-usage`.

| Tool | Verdict | Action |
| --- | --- | --- |
| `mesh-breath` | KEEP | Added to on-demand canon with purpose: read-only breathing probe for access-path and liveness verification. |
| `mesh-guardian` | KEEP | Added to on-demand canon with purpose: survival reflex for reachability, tmux restoration, and Telegram organ recovery. |
| `mesh-load` | KEEP | Added to on-demand canon with purpose: read-only agent load/quota reporter to `mesh-chat`. |
| `mesh-study` | KEEP | Added to on-demand canon with purpose: field-mining / study-brief helper. |
| `mesh-usage` | KEEP-AS-HELPER | Added to on-demand canon as the usage aggregator backing `mesh-load`. |
| `mesh-onboard` | ATTIC | Left out of canon. Treated as junk-posted / superseded onboarding wrapper; keep in history only. |

Checks:

- No files were deleted.
- `mesh-doctor` was re-run after the classification step; this shell currently shows unrelated FAILs (`mic declared but CAPTURE fails`, `cron MISSING mesh-supervise`).
- The board received the verdict via `mesh-chat`.
