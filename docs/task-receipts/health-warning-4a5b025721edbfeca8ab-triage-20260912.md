# Health warning triage: intermittent UVC metadata capture

Task: `health-warning/4a5b025721edbfeca8ab/triage`

The warning repeats the known UVC metadata startup/read intermittency: an earlier real read
succeeded after one 2-second stream-start timeout, while the durable artifact was refreshed. The
current check pane reports all declared organs LIVE with none DARK.

## Current evidence

- `mesh-uvc-metadata --test` exited 0 against `/dev/video1`. It recorded two 2-second timeouts,
  then succeeded with a real 4,114-byte metadata buffer containing 187 timestamped records. Test
  mode uses a private temporary output, so it does not overwrite the durable capture.
- The deployed schedule remains present in `~/.mesh/reflexes.cron` at `*/10 * * * *` for
  `mesh-uvc-metadata`.
- At 2026-09-12 14:23:27 UTC, `~/.mesh/uvc-metadata/latest.bin` was 8,316 bytes with SHA-256
  `3c90fd4743aa691f01dbdcf698e9c6de9f26bfa12663e9d9be7b1c90152ff1af`. Independent
  `mesh-uvc-metadata --parse` validation produced 378 timestamped records.
- `mesh-organ --why uvc-metadata` resolves the local offer as eligible. This proves routing
  eligibility, while the scheduled capture and fresh parseable artifact provide the liveness
  evidence.

## Verdict

The organ is wired and producing parseable data, but the two timeouts before a successful read
confirm that individual stream starts remain intermittent. Classify it as **intermittently live
with a known startup/read blind**, not fixed and not currently DARK. Prior receipts document the
attribution limit when scheduled and manual captures overlap; this probe does not establish a
cause for the timeouts. No camera, routing, or other substrate state was changed.

## Verification

Observed the one-shot `check` pane, ran the real-device `--test`, independently statted, hashed,
and parsed the canonical artifact, confirmed the scheduled cron entry, and inspected the organ
router's current eligibility result. See also
[`health-warning-9acbe26cce46544962c3-20260912.md`](health-warning-9acbe26cce46544962c3-20260912.md)
for a prior failed normal capture and its attribution limit.
