# Unblock receipt: Note 3 HH harvest

- Task: `unblock/job/bb7e667f603dbd9e/resolve`
- Owner: `job`
- Decision: typed machine-only capability block remains; no external authority was requested.
- Delegation decision: no subagent was launched. The work is one tightly coupled live-driver
  diagnosis/retry on the single-writer HH session; splitting it would risk competing writes.

## Evidence

- Live process check at 2026-09-16T12:10Z: PID `687073` was running
  `scripts/mesh-hh-drive.py`.
- `mesh-hh-drive --alive` returned `up` (`rc=0`), but that was not sufficient evidence of service
  responsiveness.
- Fresh read probe queued with `mesh-hh-drive --send` using marker
  `job-unblock-health-20260916T121012Z`. The driver returned a real JSON result after the bounded
  wait: URL `https://nn.hh.ru/applicant/negotiations?page=4`, `ready=interactive`, and a non-empty
  body beginning `Chats / Resume and profile / Applications`.
- The required retry was run as:
  `timeout 100s job/mesh-job-apply --reopen --harvest --json`.
- Retry artifact: `/tmp/job-unblock-harvest-20260916.json`, SHA-256
  `ee68066621074a6f46385ff10366e92de3bfdb2e0d2ed151f7172b3ea3cf9141`.
- Retry result: started `2026-09-16T12:10:44Z`, ended `2026-09-16T12:12:24Z`, `rc=143`, elapsed
  `99.8s`; no harvest result or target transition was produced.
- Personally inspected target rows in `~/.mesh/job-board.tsv`:
  - line 8082: vacancy `137369624`, X5 Tech, state `needs-human`, form `form`.
  - line 8101: vacancy `137329739`, БУРГЕР КИНГ РОССИЯ, state `needs-human`, form `questions`.

## Retry edge

Keep the parent harvest task typed-blocked. Re-check the live Note 3 driver with a fresh bounded
non-empty read after PID `687073` exits or the driver completes a responsive command promptly; then
rerun the same 100-second harvest and reread vacancies `137369624` and `137329739`. Do not kill the
driver or remove `.apply.lock`: the HH account is single-writer scoped, and the lock currently names
`mode=confirm`.
