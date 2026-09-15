# New-sense live candidate audit — 2026-09-12

`mesh-airtime` is already a tracked on-demand QBSS airtime reader with a live-read `--test`, so it
was not a new capability.

The Note 3 HAL exposed gravity (sensor type 9) and linear acceleration (type 10), neither of which
has a dedicated Note 3 reader. I sampled both together six times through the live `sensorcat` HAL
listener at 23:50:20–23:50:23Z. All six events shared the same fresh HAL tick per pair. Across the
six pairs the linear-acceleration vector tracked roughly twice the gravity vector on every axis;
for example `g=(-6.51024,6.51114,3.37520) m/s²` and `a=(-13.1031,13.1016,6.95758) m/s²`. The
reported linear-acceleration magnitude was about 19.6 m/s² while the gravity magnitude was about
9.8 m/s². This paired pattern is physically implausible as a trustworthy motion reading and adds
no defensible joint information, so I rejected that candidate.

A second paired observation was available: Note 3 HAL orientation (type 3) and gyroscope (type 4).
They answer complementary questions at the same instant: posture plus angular rate can distinguish
a stationary tilted phone from rotation through that posture. Added the on-demand raw paired reader
`scripts/mesh-note3-posture-rotation` and its executable wrapper test
`tests/test-mesh-note3-posture-rotation.sh`. Its output carries one-sample overlap coverage, HAL
event age, and inter-event skew; it exits 2 if either fresh aligned event is absent. It assigns no
uncalibrated motion class and writes no state.

Verification: the wrapper test passed, including a fresh real pair; a standalone `--json` read also
passed with both HAL ticks equal and age 28.382 ms; `bash -n` passed. The wrapper observed a paired
sample with 5.104 ms skew and 19.373 ms age.

`mesh-doctor --quiet` was run after adding the tool. It reported existing hard failures before its
test sweep: egress uses
`tailscale0` and has an exit node set; it also reported the default mic busy. It showed unrelated
warnings for an untimed peer SSH, six `mesh-song-verify` funnel bypasses, and five absence-as-negative
sites. The full smoke sweep remained active after more than five minutes, so I stopped that run to
avoid leaving a large parallel test storm. No doctor pass or final orphan-clean result is claimed.
The new script has an explicit `# orphan-ok: on-demand paired ...` header and is executable. No
`[sense]` board post was made because the required doctor-clean gate was not met.

Next action: resolve the existing doctor blockers and warnings, run `mesh-doctor --quiet` to a clean
completion, then post the live paired artifact from `scripts/mesh-note3-posture-rotation --json`.
