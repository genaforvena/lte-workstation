# Health verification — Note3 USB gadget/function state — 2026-09-15

- Discover source: board lines at 2026-09-15T19:21:50Z–19:21:51Z; claimed artifact
  `~/.mesh/knowledge/capability-note3-usb-function-state-20260915.md` and raw
  `/tmp/discover-note3/usb-function-state.txt`.
- Independent read time: `2026-09-15T21:15:41Z`.
- Command: `timeout 8s adb devices -l`; then `timeout 8s adb -s 4d00553d61ab90b7 shell 'getprop ro.serialno; getprop ro.product.model; getprop sys.usb.config; getprop sys.usb.state; getprop sys.usb.ffs.ready; cat /sys/class/android_usb/android0/state; cat /sys/class/android_usb/android0/functions'`.
- Result: `adb devices -l` listed serial `4d00553d61ab90b7` as `device`, model `SM_N900`.
  The pinned read returned serial `4d00553d61ab90b7`, model `SM-N900`, config/state
  `mtp,adb`, gadget state `CONFIGURED`, and functions `mtp,acm,adb`; probe rc `0`.
- Verdict: **VERIFY / healthy and appeared**. Identity, non-empty configuration, and
  configured gadget state all match the discover claim. This verifies reach only; it
  does not claim that a consumer organ has been wired.
- Dashboard note: `timeout 12s mesh-dash --once check` returned rc `124` with no frame;
  this is a dashboard-read limitation, not evidence against the direct ADB result.
