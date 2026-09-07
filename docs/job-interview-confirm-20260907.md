# Autonomous interview confirmation — 2026-09-07

## Design

`job/mesh-job-interview-confirm` is a narrow consumer of proposed calendar rows. Every 15 minutes
it reads only still-live `proposed` rows whose channel is an HH chat, reads that thread through the
single shared HH driver, and promotes a row only when the employer message contains all of:

1. explicit confirmation language;
2. a date/time matching one of the slots previously offered by the lane;
3. named participants; and
4. exactly one meeting link or physical place.

It then calls `mesh-job-cal --confirm` with the captured evidence and sends Telegram a structured
message containing company, role, date/time, link or place, participants, and preparation guidance.
Rows are compared with the last offered window: expired proposed rows are cancelled automatically,
while historical invitations cannot cause browser churn or accidental notifications. A live
non-confirmation leaves the row proposed.

## Wiring and verification

- Production wrapper: `~/.local/bin/mesh-job-confirm`.
- Reflex: `*/15 * * * * ... mesh-job-confirm --json` in the live crontab.
- Shared HH writer lock: `~/.mesh/job/.apply.lock`.
- Test-first parser coverage: `tests/test-job-interview-confirm.sh` plus `mesh-job-confirm --test`.
- Verified: parser test passed, Python compilation passed, `git diff --check` passed, and a live run
  returned `[]` for the current INКОМСИСТЕМ proposal (no employer confirmation yet).
- Current calendar remains `0 confirmed / 1 proposed`; no interview Telegram alert was sent.
