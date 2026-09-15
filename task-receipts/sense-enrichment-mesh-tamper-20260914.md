# Sense enrichment: mesh-tamper — 2026-09-14

## Change

`scripts/mesh-tamper` now reads the numeric `TAMPER_EOF` status. With no sensor event object,
only the known empty-return (`0`) and bounded timeout (`124`) outcomes classify as quiet; tool
errors such as command-not-found (`127`) and permission failure (`1`) classify as hollow and flow
to the existing OFFLINE/exit-2 path.

`mesh-tamper --test` now performs the same bounded three-second `SIGNIFICANT_MOTION` watch as the
runtime through shared `run_watch`. It reports a real moved/quiet artifact or exits 2 when the
phone is unreachable or the read is hollow. The test path does not write `.tamper-state` or
`.tamper-events`.

## Verification

- Test-first regression was red before the classifier change: missing-executable and sensor-error
  sentinels were incorrectly `quiet`.
- `bash -n scripts/mesh-tamper tests/test-mesh-tamper-test-real-read.sh` — PASS.
- `bash tests/test-mesh-tamper-test-real-read.sh` — PASS: bounded hardware command is invoked,
  valid no-event output is reported as an artifact, tool errors degrade, and liveness files remain
  untouched in the isolated test home.
- `git diff --check` — PASS.
- Live `scripts/mesh-tamper --test` — exit 2 with
  `86 classifier assertions passed; real sensor read unreachable, no trustworthy hardware artifact`.
  The phone was unreachable; this is the expected degraded result, not a successful hardware read.
- Live `scripts/mesh-tamper --window 3` — exit 2 with
  `phone unreachable / watch did not run — tamper read n/a (NOT 'quiet')`. The real runtime artifact
  in `~/.mesh/.tamper-state` was `OFFLINE|1789377535|3|COLD|0|UNKNOWN|NONE|NA` (mtime
  `2026-09-14 09:18:55 UTC`).

No commit was made. Re-run `scripts/mesh-tamper --test` when the phone is reachable to verify a live
`body-moved` or `body-quiet` sensor artifact.
