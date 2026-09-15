# Discover frontier dry: UPower DisplayDevice (2026-09-08)

## Verdict

Rejected as a new mesh sense. The live UPower `DisplayDevice` object exists, but it is not a
material capability on this node: `power supply: no`, state `unknown`, `percentage: 0%`, and its
last update is 47,547 seconds old. The daemon reports `on-battery: no` and `lid-is-present: no`,
but the existing power/AC and lid organs already own those readings.

## Real probe

```text
upower -i /org/freedesktop/UPower/devices/DisplayDevice
  power supply:         no
  updated:              Mon Sep  7 23:24:05 2026 (47547 seconds ago)
  has history:          no
  has statistics:       no
  unknown
    warning-level:       none
    percentage:          0%
    icon-name:          'battery-missing-symbolic'
```

Acceptance predicate: a useful power sense must be a current, attributable reading with a
non-unknown state. This sample fails 2/2 required checks (current and attributable); no new
knowledge or wiring should be based on it.

Prior-art gate: `mesh-prior-art 'UPower:DisplayDevice'` returned `CLEAN` (rc 1), so this is a
recorded rejection rather than a duplicate filing.
