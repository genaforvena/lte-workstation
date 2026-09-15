# Discover UVC metadata find verification

Checked 2026-09-12 10:57–10:59 UTC for the health stage of the discover → health loop.

The finding did appear as a real artifact. The retained discovery sample
`~/.mesh/knowledge/capability-uvc-metadata-stream-vid1871-0142-mesh-home-20260909.bin`
exists at 5,874 bytes with SHA-256
`81aac71c51cb19921bf039bccfffd188d80a59eddab564c4eccc9d686b1dce94`. This matches the
historical board evidence. A separate retained runtime sample was 5,852 bytes at 10:57 UTC.

A live `mesh-organ --node mesh-home uvc-metadata --test` reached `/dev/video1`. Two one-buffer
attempts timed out; a later attempt succeeded with a 616-byte real read, and the command exited 0.
This proves the stream can produce a buffer now, but not steady availability. The next `mesh-dash
--once check` at 10:59 UTC still listed `mesh-home:uvc-metadata — DARK` (14 live organs, 1 dark),
and its probe warning said local load was high, making reachability probes unreliable. The separate
wiring assessment also documents intermittent read failures. Verdict: **APPEARED and presently
readable on retry; health is intermittent/degraded, not continuously green.**

No substrate or sensor configuration was changed. The probe used the organ's private temporary
output, so it did not overwrite the retained discovery sample.
