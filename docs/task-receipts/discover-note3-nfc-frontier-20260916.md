# Discover receipt: Note3 NFC frontier

- Task: `discover-note3-nfc-frontier-20260916/probe-note3-nfc-frontier`
- Probe time: 2026-09-16 UTC
- Target: attached ADB device `SM-N900` (Samsung Note3)
- Acceptance predicate: a usable NFC capability is proven if Android exposes the NFC feature and the live NFC service reports enabled state; a Termux bridge would additionally require an installed `termux-*` package/command.

## Raw live readings

```text
$ adb shell getprop ro.product.model
SM-N900

$ adb shell pm list features | grep -i nfc
feature:android.hardware.nfc
feature:android.hardware.nfc.hce

$ adb shell pm list packages | grep -i termux
(no output; rc=1)

$ adb shell dumpsys nfc
mState=on
mScreenState=ON_LOCKED
mEnableReader=false
mEnableHostRouting=true
mIsSendEnabled=true
mIsReceiveEnabled=true
mLinkState=LINK_STATE_DOWN
libnfc llc error_count=0
```

## Verdict

**PROVEN hardware capability, not yet a mesh-readable organ.** The Note3 has NFC and its Android NFC service is on, but no Termux package/bridge is installed. This is distinct from the blocked Redmi Termux frontier: it is an ADB-reachable Note3 hardware path, not a Redmi `:8022` probe. No outward NFC action was attempted.

Next owner: `senses` if a read-only NFC organ is desired; it would need an Android-side bridge or an operator-approved tag fixture before it can produce a tag-read artifact.
