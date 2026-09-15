# Health warning triage — intermittent UVC metadata capture

Task: `health-warning/f877a0d0ee32e25f25bb/triage`

At 2026-09-12 16:00 UTC, the `check` pane reported `egress tailscale0`, 8/10
fleet nodes down, and all declared organs LIVE with none DARK. The pane also
reports high local load, so fleet reachability non-answers remain unreliable.

## UVC evidence

- `mesh-uvc-metadata --test` exited 0 after one two-second timeout, then read a
  real 7,546-byte `/dev/video1` metadata buffer containing 343 timestamped
  records. Test mode uses a private output.
- The deployed `~/.local/bin/mesh-uvc-metadata` is byte-identical to
  `scripts/mesh-uvc-metadata` (7,234 bytes).
- The production artifact `~/.mesh/uvc-metadata/latest.bin` was 8,954 bytes,
  mtime `2026-09-12 15:57:45 UTC`, SHA-256
  `5ec905c6f37799bdf97e71c4bd602c6d852b56e5d3787619e72f78f9f9798043`.
  `mesh-uvc-metadata --parse` exited 0 on that artifact and emitted 413
  timestamped records.
- `~/.mesh/reflexes.cron` still schedules the deployed wrapper every ten
  minutes (`*/10 * * * *`).

## Disposition

The organ is live and producing parseable production data, with a successful
fresh real-device read. The observed timeout confirms the known intermittent
startup/read blind; this does not establish continuous availability or its
cause. No camera, routing, or other substrate state was changed. Separately,
the current fleet pane still shows 8/10 nodes down and egress over `tailscale0`
with an exit-node SPOF; high local load makes probe non-answers unreliable.

## Verification

Ran `mesh-dash --once check`, `mesh-uvc-metadata --test`, production-artifact
stat/hash/parse, checked the ten-minute reflex entry, and compared the deployed
wrapper with the repository source. The interactive `mesh-organ --why`
inspection was stopped before returning an eligibility result, so no router
eligibility claim is made here.
