# UVC metadata runtime retry

The health-stage verification in [discover-uvc-find-verification-20260912.md](discover-uvc-find-verification-20260912.md)
found `/dev/video1` time out twice, then return a real 616-byte metadata buffer on retry, while
`mesh-dash` still classified the organ as DARK. The runtime wrapper previously made one read per
10-minute fire, so a transient miss could leave the last artifact stale until the next cadence.

`scripts/mesh-uvc-metadata` now makes up to ten bounded reads by default (each retains the existing
2-second timeout), matching the real-device test window. It truncates the private temporary output
before each attempt and replaces the retained artifact only after a successful, nonempty read. The installed
`~/.local/bin/mesh-uvc-metadata` resolves to this source file.

The regression test first reproduced the failure: its fake device returned partial bytes and failed
twice, then returned a complete payload; the old runtime exited on attempt one. After the change,
`bash tests/test-mesh-uvc-metadata.sh` passed, including that retry fixture, the missing-device gate,
the bounded-hang check, and a live `/dev/video1` read. The first live run timed out twice, then read
5,852 bytes; a later verification timed out nine times, then read 1,628 bytes on attempt ten; the
final verification timed out once, then read 572 bytes. `bash -n` passed for the wrapper and test.

Source SHA-256: `32875b11711eb7b038b4c8f192bf4daa7d7c9ffe3e83cc78acfaf66abefd342a`.
Test SHA-256: `5f1a48bad80518d3fadb68d488e71aa4b19910d583d4ec5af3a7caf6af77e29f`.
