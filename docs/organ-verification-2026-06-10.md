# Organ Verification Table — 2026-06-10T10:40Z (phone+ds sections re-verified 2026-06-12)

## Legend
- ✅ WORKS — artifact produced, verified
- ⚠️ PARTIAL — present but limited/blocked
- ❌ FAILS — not working or inaccessible
- 🔒 BLOCKED — permission/consent/physical constraint

## IdeaPad (imozerov-IdeaPad-3-15IIL05)

| Organ | Status | Artifact/Proof | Blocker/Note |
|-------|--------|----------------|--------------|
| Camera /dev/video0 | ✅ | mesh-camera → /tmp/cam-*.jpg, real 640×480 JPEG (19.8KB, fswebcam backend), re-verified 2026-06-12T20:42Z | WORKS — per-user ACL `user:imozerov:rw-` grants access WITHOUT video group; fswebcam installed (no ffmpeg/v4l2-ctl needed) |
| Camera /dev/video1 | ✅ | same Integrated Camera, second interface; mesh-camera --test ok | WORKS via mesh-camera (see video0) |
| Mic (ALC236 card 0) | ✅ | /tmp/mic-test-ideapad.wav 345K, WAV PCM 44.1kHz stereo, peak=32768 (live signal, steward-verified) | WORKS |
| Speaker (ALC236 card 0) | ✅ | blessyou played bless-lessac.wav @ local 2026-06-10 01:16Z (prior artifact) | WORKS |
| Speaker (HDMI 0-3 card 0) | ⚠️ | aplay -l lists 4 HDMI devices | presence only, playback not tested |
| Bluetooth adapter | ✅ | bluetoothctl show: Powered=yes, Name=imozerov-IdeaPad | WORKS |
| BLE scan | ✅ | 5s scan: Bose LE, Samsung TV, 3 unknown devices | WORKS |
| Browser | ✅ | xdg-open/firefox/chromium available | WORKS |

## default-string (imozerov-Default-string)

| Organ | Status | Artifact/Proof | Blocker/Note |
|-------|--------|----------------|--------------|
| Bose speaker (Bluetooth) | ✅ | UPDATED 2026-06-12: Bose connected as DEFAULT PipeWire sink @74%; real TTS played via pw-play (tg mind) | WORKS — note: probes over ssh need `XDG_RUNTIME_DIR=/run/user/$(id -u)` or wpctl falsely reports PipeWire down |
| USB mic (card 1, USB Audio and HID) | ✅ | UPDATED 2026-06-12: real capture verified — 64044B WAV (2s@16kHz) 13:08Z; doctor PASS 'mic captures (plughw:1,0)'; card declares senses: mic | WORKS — the working mic is the USB card, found by device enumeration (mesh-card mic_real now probes all capture devices) |
| Zoran mic (card 0) | ❌ | /tmp/zoran-mono.wav: 96000 frames, peak=0 — absolute silence (steward-verified) | DEAF confirmed (card 0 only; see USB mic row — ds can hear via card 1) |
| CH340 serial /dev/ttyUSB0 | ⚠️ | device present, stty configured at 9600 | needs sudo; no data read (unknown device) |
| Bluetooth adapter | ✅ | bluetoothctl show: adapter present | WORKS |
| BLE scan | ✅ | 5s scan: 2 devices, Bose RSSI=-26 (close) | WORKS |

## Phone (Redmi 10, 100.103.99.16:8022)

| Organ | Status | Artifact/Proof | Blocker/Note |
|-------|--------|----------------|--------------|
| Battery | ✅ | 42%, DISCHARGING, 31.8°C, Li-poly, health=GOOD, 3.7V/907mA | WORKS |
| Camera 0 (back) | ✅ | UPDATED 2026-06-12: F-Droid reinstall (12:03Z) restored termux-api 0.59.1; camera-info live (4080×2304) | un-crippled; capture itself consent-gated by doctrine |
| Camera 1 (front) | ✅ | same — F-Droid build, specs live (3264×2448) | capture consent-gated |
| Audio out | ✅ | 48kHz, buffer 256 frames (512 low-latency), no BT/wired headset | WORKS |
| TTS | ✅ | termux-tts-speak "test" succeeded | WORKS |
| Sensors (accel/gyro/etc) | ✅ | UPDATED 2026-06-12: 20+ sensors live (bma420, akm09918, tmd2755…); light sensor exercised → real one-shot reading | WORKS (F-Droid fix) |
| Mic (termux-microphone-record) | 🔒 | not tested | needs consent + wake-lock |
| GPS (termux-location) | ✅ | UPDATED 2026-06-12: mesh-location → real fix lat 56.308/lon 44.031 ±29m in 4.9s (verify rotation ag) | WORKS — operator wired this deliberately (consent resolved) |
| IR transmitter | ✅ | UPDATED 2026-06-12: termux-infrared-frequencies → 6 real carriers 30–56kHz (capability sweep c) | transmit untested (consent territory — pointing IR at operator's devices) |
| SMS (send/receive) | ⚠️ | termux-sms-* present | not tested — privacy/cost-sensitive, declare-only |
| Telephony (cellinfo) | ✅ | UPDATED 2026-06-12: real registered WCDMA cell (cid 1826567, lac 45270, MegaFon, −105dBm) | WORKS; call actuator untested (cost/consent) |
| WiFi (scan/connection) | ✅ | UPDATED 2026-06-12: wifi-scaninfo → real AP survey w/ BSSID/RSSI/channel (sweep b) | WORKS — fills router's no-scan gap |

## Summary (re-verified 2026-06-12)

**Working (21):** IdeaPad mic, speaker, BT, BLE, browser, cameras ×2; default-string BT, BLE, Bose speaker (BT default sink), USB mic; phone battery, audio out, TTS, cameras ×2 (F-Droid fix), sensors, GPS, IR (enumerated), cellinfo, WiFi scan

**Partial (3):** IdeaPad HDMI out (presence only); default-string CH340 (operator must identify payload); phone SMS (declare-only)

**Blocked (1):** Phone mic (consent required for capture; mesh-hear deployed)

**Failed (1):** default-string Zoran mic card 0 (deaf — but ds hears via USB card 1)

## Next steps
1. ~~Investigate IdeaPad camera driver issue~~ ~~Fix: usermod -aG video~~ RESOLVED 2026-06-12: camera now WORKS via mesh-camera (fswebcam backend) + per-user ACL `user:imozerov:rw-` on /dev/video* — no video-group/v4l2-ctl needed.
2. ~~Phone JSON parsing~~ DONE: battery 42%/GOOD, audio 48kHz; camera capture found BROKEN (0-byte JPEG).
3. ~~Phone termux-api via F-Droid~~ DONE 2026-06-12 (operator reinstall 12:03Z) — sensors, cameras, location, IR, telephony, wifi-scan all restored/verified (capability sweeps b+c).
4. Ask operator: what is connected to CH340 on default-string? (still open)
5. ~~Test Bose playback~~ DONE 2026-06-12 — Bose is ds's default BT sink; real TTS played (pw-play; ssh probes need XDG_RUNTIME_DIR anchored).
6. ~~Test IdeaPad cameras after video group + tool install~~ DONE 2026-06-12 — cameras verified working (see #1).
7. ~~Test phone IR/SMS/telephony/WiFi organs~~ MOSTLY DONE 2026-06-12: IR frequencies + cellinfo + wifi-scan verified; SMS/call left declare-only (cost/privacy); IR transmit awaits operator consent.
8. Phone reliability (NEW, from sweep c): no sshd autostart + no mesh re-plant — body is one app-kill from dark (planner-claimed 12:03Z).
