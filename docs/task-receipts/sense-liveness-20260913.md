# Sense liveness audit — 2026-09-13

## Selected organ: `lan-newdevice`

`mesh-reflex-health` reports the organ as **BLIND**, while its scheduled caller is still firing. At
2026-09-13 11:53Z, the last real LAN beat was `~/.mesh/.lan-newdevice.beat` at 2026-09-02
20:24:22Z (zero bytes); `~/.mesh/.lan-newdevice-blind` was touched at 11:48:54Z. The marker records
an attempted read, not a LAN observation.

The 24-hour window is 2026-09-12 11:45Z–2026-09-13 11:45Z; the 7-day window is 2026-09-06
11:45Z–2026-09-13 11:45Z. System syslog records **66** and **634** starts, respectively, of the
15-minute `mesh-perimeter --edge` caller. Its code invokes `mesh-lan-newdevice --status` in the
NETWORK axis. There is no independent timestamped child-attempt tape, so the caller-start counts
are an upper bound on completed child reads, not a fabricated exact child denominator. The
nominal schedules are 96 and 672 slots; missed slots are not evidence of a clean LAN.

Across both windows, fresh real LAN artifacts are **0**: the beat predates both windows. Thus the
observed fresh-beat coverage against caller starts is 0/66 (24h) and 0/634 (7d); exact child-level
coverage is UNKNOWN because child attempts are not recorded per run. Per-run empty/unreachable
counts are also absent: the perimeter log is transition-only and the blind marker overwrites its
mtime. The live probe at 11:48Z returned `router DHCP + LAN ARP both unreachable — can't assess
(not an alarm)`. This confirms unreachable now, not for every historical attempt.

`mesh-lan-newdevice --test` passes its fixture assertions, but it does not make a live LAN read.
The source currently marks this axis `DECAYED 2026-09-13`; the live probe and stale beat support
keeping that honest disposition. `mesh-wifi-link` is independently blind: its direct cron command
started 196 times (24h) and 1,901 times (7d), while `.wifi-link.state` remains at 2026-09-03
09:47:02Z and the offline marker was refreshed at 11:48:30Z. Its real result mix is not retained
per run; `--test` currently returns n/a/exit 2 because SSH to the phone is unreachable.

## Live sensor survey and post-disposition artifact

`mesh-sensorium` completed at 11:52Z. Its real local readings included CPU 74.6°C, GPU 49.0°C,
NVMe temperatures, a Wi-Fi scan of 0 APs, and ALSA device enumeration. It reported no Bluetooth
adapter. These are current sensor results; no radio silence was reinterpreted as a calm reading.
The individual LAN probe above and the Wi-Fi link probe both remain unreachable.

After confirming the decay disposition, `mesh-note3-battery --edge` read the connected Note3 at
11:53:22Z: `present=true level=100/100 temperature=28.1°C power=USB status=5 voltage=4303mV`.
The fresh 81-byte artifact is `~/.mesh/.note3-battery-state`. This verifies a real post-disposition
hardware read without claiming that the LAN organ recovered.

No commit was made. Existing unrelated dirty worktree changes were preserved.
