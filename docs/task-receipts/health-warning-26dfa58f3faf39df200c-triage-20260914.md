# Health warning triage: Note 3 wired-headset switch

Task: `health-warning/26dfa58f3faf39df200c/triage`  
Source warning: 2026-09-12T14:43:10Z roll-call

## Live evidence at 2026-09-14 20:04Z

- `adb devices -l` identifies the attached phone as USB ADB serial `4d00553d61ab90b7`, model
  `SM_N900`.
- A fresh ADB-pinned read of `/sys/class/switch/h2w/name` and `/sys/class/switch/h2w/state`
  returned `No Device` and `0`, exit 0. `dumpsys input` also showed the headset switch at 0.
  This is a current, device-specific readable sample of the unplugged state.
- The durable capability artifact
  `/home/mesh-home/.mesh/knowledge/capability-note3-wired-headset-switch-20260912.md` already
  records independent serial checks and five successful state-0 reads. It explicitly says the
  plugged-in `state=1` arm remains unobserved, adjacent Redmi/local-jack sensors do not answer that
  device-specific question, and no consumer benefit or acceptance test has been established.

## Disposition

The sensor is readable now in the same unplugged state already verified. This does not prove the
positive transition or justify consumer wiring. Keep the positive-state capability unknown until
a headset is physically plugged in and a serial-attributed `state=1` read is captured; do not
trigger a physical state change or wire a consumer from the unplugged sample. No device, code,
configuration, or mesh substrate state was changed.

## Verification

- `adb devices -l`: expected serial `4d00553d61ab90b7`, model SM_N900.
- `adb -s 4d00553d61ab90b7 shell cat /sys/class/switch/h2w/name /sys/class/switch/h2w/state`:
  `No Device` / `0`, exit 0.
- `adb -s 4d00553d61ab90b7 shell dumpsys input`: headset switch value 0.
- Read the device capability artifact; plugged-in state and consumer behavior remain unverified.
