# Organ Verification Table — 2026-06-10T10:40Z

## Legend
- ✅ WORKS — artifact produced, verified
- ⚠️ PARTIAL — present but limited/blocked
- ❌ FAILS — not working or inaccessible
- 🔒 BLOCKED — permission/consent/physical constraint

## IdeaPad (imozerov-IdeaPad-3-15IIL05)

| Organ | Status | Artifact/Proof | Blocker/Note |
|-------|--------|----------------|--------------|
| Camera /dev/video0 | ❌ | v4l2-ctl: not a v4l2 device | driver issue or virtual device |
| Camera /dev/video1 | ❌ | v4l2-ctl: not a v4l2 device | driver issue or virtual device |
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
| Battery status | ⚠️ | termux-battery-status runs | no jq for parsing |
| Sensor list | ⚠️ | termux-sensor-list runs | no jq for parsing |
| Camera | ⚠️ | termux-camera-info runs | no jq for parsing |
| TTS | ✅ | termux-tts-speak "test" succeeded | WORKS |
| Mic (termux-microphone-record) | 🔒 | not tested | needs consent + wake-lock |
| GPS (termux-location) | 🔒 | not tested | needs consent |

## Summary (steward-reviewed 2026-06-10)

**Working (8):** IdeaPad mic, speaker, BT, BLE, browser; default-string BT, BLE; phone TTS

**Partial (6):** IdeaPad HDMI out (presence only); default-string Bose (needs GUI), CH340 (needs sudo+identification); phone battery/sensors/camera (need jq/python parsing)

**Blocked (2):** Phone mic, GPS (consent required)

**Failed (3):** IdeaPad cameras ×2 (not v4l2 devices), default-string Zoran mic (deaf — peak=0)

## Next steps
1. Investigate IdeaPad camera driver issue (udevadm info /dev/video0)
2. Install jq on phone or use python for JSON parsing
3. Ask operator: what is connected to CH340 on default-string?
4. Test Bose playback from graphical session (needs operator or X forwarding)
