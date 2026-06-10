# Organ Verification Table — 2026-06-10T10:40Z

## Legend
- ✅ WORKS — artifact produced, verified
- ⚠️ PARTIAL — present but limited/blocked
- ❌ FAILS — not working or inaccessible
- 🔒 BLOCKED — permission/consent/physical constraint

## IdeaPad (imozerov-IdeaPad-3-15IIL05)

| Organ | Status | Artifact/Proof | Blocker/Note |
|-------|--------|----------------|--------------|
| Camera /dev/video0 | ⚠️ | udevadm: Integrated Camera (uvcvideo driver, USB 1-5:1.0) — present but inaccessible | not in video group + v4l2-ctl/ffmpeg not installed |
| Camera /dev/video1 | ⚠️ | udevadm: same device, second interface — present but inaccessible | not in video group + v4l2-ctl/ffmpeg not installed |
| Mic (ALC236 card 0) | ✅ | /tmp/mic-test-ideapad.wav 345K, WAV PCM 44.1kHz stereo, peak=32768 (live signal, steward-verified) | WORKS |
| Speaker (ALC236 card 0) | ✅ | blessyou played bless-lessac.wav @ local 2026-06-10 01:16Z (prior artifact) | WORKS |
| Speaker (HDMI 0-3 card 0) | ⚠️ | aplay -l lists 4 HDMI devices | presence only, playback not tested |
| Bluetooth adapter | ✅ | bluetoothctl show: Powered=yes, Name=imozerov-IdeaPad | WORKS |
| BLE scan | ✅ | 5s scan: Bose LE, Samsung TV, 3 unknown devices | WORKS |
| Browser | ✅ | xdg-open/firefox/chromium available | WORKS |

## default-string (imozerov-Default-string)

| Organ | Status | Artifact/Proof | Blocker/Note |
|-------|--------|----------------|--------------|
| Bose USB audio (card 1) | ⚠️ | aplay -l: card 1 present; playback command accepted but terminated | needs graphical session for full control |
| Zoran mic (card 0) | ❌ | /tmp/zoran-mono.wav: 96000 frames, peak=0 — absolute silence (steward-verified) | DEAF confirmed; matches blessyou self-test 2026-06-10 01:16Z |
| CH340 serial /dev/ttyUSB0 | ⚠️ | device present, stty configured at 9600 | needs sudo; no data read (unknown device) |
| Bluetooth adapter | ✅ | bluetoothctl show: adapter present | WORKS |
| BLE scan | ✅ | 5s scan: 2 devices, Bose RSSI=-26 (close) | WORKS |

## Phone (Redmi 10, 100.103.99.16:8022)

| Organ | Status | Artifact/Proof | Blocker/Note |
|-------|--------|----------------|--------------|
| Battery | ✅ | 42%, DISCHARGING, 31.8°C, Li-poly, health=GOOD, 3.7V/907mA | WORKS |
| Camera 0 (back) | ❌ | camera-info shows specs (4080×2304, RAW+manual) BUT capture broken: termux-camera-photo → 0-byte file, "not yet available on Google Play" (steward-verified) | REGRESSION — worked before (CLAUDE.md); Play Store build crippled, needs F-Droid |
| Camera 1 (front) | ❌ | same Play Store cripple (specs visible: 3264×2448, capture untested-presumed-broken) | same fix: F-Droid termux-api |
| Audio out | ✅ | 48kHz, buffer 256 frames (512 low-latency), no BT/wired headset | WORKS |
| TTS | ✅ | termux-tts-speak "test" succeeded | WORKS |
| Sensors (accel/gyro/etc) | ❌ | termux-sensor returns "not yet available on Google Play" | Play Store build crippled — needs F-Droid |
| Mic (termux-microphone-record) | 🔒 | not tested | needs consent + wake-lock |
| GPS (termux-location) | 🔒 | not tested | needs consent |
| IR transmitter | ⚠️ | termux-infrared-* present | not tested |
| SMS (send/receive) | ⚠️ | termux-sms-* present | not tested |
| Telephony (call/cellinfo) | ⚠️ | termux-telephony-* present | not tested |
| WiFi (scan/connection) | ⚠️ | termux-wifi-* present | not tested |

## Summary (steward-reviewed 2026-06-10)

**Working (10):** IdeaPad mic, speaker, BT, BLE, browser; default-string BT, BLE; phone battery, audio out, TTS

**Partial (10):** IdeaPad cameras ×2 (present but inaccessible: not in video group, no v4l2-ctl/ffmpeg), HDMI out (presence only); default-string Bose (needs GUI), CH340 (needs sudo+identification); phone IR, SMS, telephony, WiFi (present, not tested)

**Blocked (2):** Phone mic, GPS (consent required)

**Failed (4):** default-string Zoran mic (deaf — peak=0); phone sensors + cameras ×2 (Play Store termux build crippled — REGRESSION, capture worked before per CLAUDE.md)

## Next steps
1. ~~Investigate IdeaPad camera driver issue~~ DONE: uvcvideo driver, present but inaccessible (not in video group, no v4l2-ctl/ffmpeg). Fix: `sudo usermod -aG video $USER` + install v4l-utils.
2. ~~Phone JSON parsing~~ DONE: battery 42%/GOOD, audio 48kHz; camera capture found BROKEN (0-byte JPEG).
3. **Phone termux-api via F-Droid** (PRIORITY — restores sensors AND cameras; Play Store build is crippled: https://github.com/termux-play-store/termux-apps/issues/29).
4. Ask operator: what is connected to CH340 on default-string?
5. Test Bose playback from graphical session (needs operator or X forwarding).
6. Test IdeaPad cameras after video group + tool install (operator decision).
7. Test phone IR/SMS/telephony/WiFi organs (need consent where applicable).
