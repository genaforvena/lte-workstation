# Job autonomy recheck — 2026-09-12

Task: `design-spec-task-sweep-20260907/audit-job-autonomy` (owner `tg`; dispatch eligibility exited 0 before owner-authored take).
Prior end-to-end evidence: `docs/job-autonomy-audit-20260907.md` records repaired Getmatch submissions confirmed against the live applications page, including 36063, 36033, 36085, and 36113.

## Current verification

- `mesh-dash --once job` at 2026-09-12T05:33Z reports 6,439 seen, 356 sent, 42 viewed, 16 replied, 81 needs-human, and 18 interview rows. Gmail intake is dark for about 31.7 hours (65 runs since the last live read); the pane says the machine discharge path reaches only 13 of 139 incoming rows. The durable calendar query is empty, so no interview alert is due.
- Live crontab and `~/.mesh/reflexes.cron` agree on the bounded `mesh-job-apply-getmatch --top 1` schedule at 08:19 and 14:19. The other apply, scan, reply, mail, act, calendar, and confirmation entries remain wired.
- SHA-256 hashes match between source and deployed copies for `mesh-job-apply`, `mesh-job-apply-getmatch`, `mesh-job-confirm`, `mesh-job-cal`, and `mesh-job-reply`.
- `mesh-job-apply-getmatch --test`, `mesh-job-confirm --test`, and `mesh-job-cal --test` pass. `mesh-job-confirm --json` and `mesh-job-cal --agenda --json` both return `[]`.
- `mesh-job-apply-getmatch --dry-run --top 1 --json` prepared vacancy 36022 but submitted nothing. This verifies current selection/letter preparation only; the next live bounded cycle is not yet due.
- `mesh-job-apply --test` exits 2 because the HH driver is not running. `mesh-job-reply --test` exits 1: its DOM cases for logged-out, selector-drift, and readable-list control fail with `read=nav-failed`, and the pagination assertion raises `TypeError: 'NoneType' object is not iterable` at `_limited`.
- The deployed `~/.mesh/job/job-reply.log` contains `AttributeError: 'str' object has no attribute 'json'` at the final JSON branch. Source inspection found `_main` parses arguments into `a`, then assigns `a = bank_answer(s)` inside the blocker loop before evaluating `a.json`; this is variable shadowing, not an inferred driver symptom.
- The job pane and `~/.mesh/job/consume-20260912.md` identify a pending BPMSoft conversation (UID 18328, chat 5617701145) and a failed HH driver start. The discharge tape also retains operator-handling rows 18382 and 18401 for employer questions requiring facts or a decision. None were answered as part of this read-only audit.
- The prior audit records Getmatch IDs 35169, 35405, 35076, 35618, and 36109 as exact-ID-unconfirmed and retry-blocked. Their live status was not re-read because the browser lane is unavailable.

## Follow-up opened

Created exact-owner chain `job-autonomy-followups-20260912` with three sequential `job` steps: repair and isolate-test the reply failure; restore one safe HH driver and resolve the pending employer communications with read-back and operator input where needed; then exact-ID reconcile the five retry-blocked Getmatch records without retrying submissions. The first step is visible in `mesh-task queue --dispatch --owner job` and remains open for owner `job`.

No job source or deployed configuration was changed by this audit. The repaired application flow has historical end-to-end evidence, but current HH communication and live submission verification remain incomplete until the owner follow-ups run.
