# Senses receipt: Note3 NFC organ capability block

- Task: `discover-note3-nfc-frontier-20260916`
- Probe time: `2026-09-16T11:36Z–11:39Z` UTC
- Owner: `senses`
- Target: attached ADB device `4d00553d61ab90b7`, model `SM-N900`
- Requested acceptance: one real tag-read artifact containing device/time/raw UID, or an explicit capability block.

## Live raw readings

```text
$ adb devices -l
4d00553d61ab90b7 device usb:1-3 product:ha3gxx model:SM_N900 device:ha3g transport_id:5

$ adb -s 4d00553d61ab90b7 shell getprop ro.product.model
SM-N900

$ adb -s 4d00553d61ab90b7 shell pm list features | grep -i nfc
feature:android.hardware.nfc
feature:android.hardware.nfc.hce

$ adb -s 4d00553d61ab90b7 shell pm list packages | grep -Ei 'termux|nfc|tag|automation'
package:com.android.apps.tag
package:com.android.nfc
package:com.sec.automation
package:com.sec.android.app.DataCreate

$ adb -s 4d00553d61ab90b7 shell dumpsys package com.android.apps.tag
codePath=/system/priv-app/Tag
versionName=1.1
grantedPermissions: android.permission.NFC ...

$ adb -s 4d00553d61ab90b7 shell dumpsys nfc
mState=on
mScreenState=ON_LOCKED
mEnableReader: false
mEnableHostRouting: true
mIsSendEnabled=true
mIsReceiveEnabled=true
mLinkState=LINK_STATE_DOWN
libnfc llc error_count=0

$ adb -s 4d00553d61ab90b7 shell find /data/local/tmp -maxdepth 1 -type f -print | grep -Ei 'nfc|tag|bridge|fixture'
(no output)

$ compgen -c | grep -Ei 'nfc|termux|adb'
adb
mesh-adb-transport
```

## Verdict

**BLOCKED: hardware capability exists, but no mesh-readable NFC organ can be created in this turn.**

The Note3 NFC feature and service are live, but there is no installed Termux/`termux-nfc` bridge,
no host-side NFC reader bridge, and no tag fixture. The stock `com.android.apps.tag` package is
only evidence of an installed Android app; it does not expose a read result to this mesh. Reader
mode is disabled and no tag event or raw UID was observed. No tag polling or outward NFC action was
attempted.

No organ, scheduler, or fused sense was added. A future turn can proceed only when an Android-side
bridge/tag fixture is available and can produce a real row with device, timestamp, and raw UID.
