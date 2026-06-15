# Phone as a body

The VM has compute but no senses. The phone has both **senses and actuators** — but a hostile
runtime for agents (glibc binaries don't run in Bionic). SSH between them and the agent on the VM
can borrow the phone's hardware. This document covers an agent on the VM reaching into the phone
over SSH and driving it via `termux-api`.

## The phone's full surface (`termux-api`, ~80 verbs)

It is not just camera/mic/GPS. Enumerate with `ls $PREFIX/bin | grep '^termux-'`. (Live count
on the Redmi 10, 2026-06-12 after the F-Droid reinstall: termux-api 0.59.1, 83 commands.) The classes:

- **Senses (input):** `termux-location` (GPS), `termux-camera-photo`, `termux-microphone-record`,
  `termux-sensor` (accel/gyro/light/…), `termux-battery-status`, `termux-telephony-cellinfo`,
  `termux-wifi-scaninfo` (RF/localization), `termux-nfc`, `termux-fingerprint`, `termux-speech-to-text`.
  - **Wired sense organ** `mesh-body-motion` — fuses `bma420`+`ORIENTATION`+`STEP_COUNTER`+`LINEARACCEL`+`tmd2755_l`
    in one SSH read and classifies the body's **activity**: `STILL` / `CARRIED` (step delta) /
    `HANDLED` (linear-accel) / `COVERED` (face-down or upright + dark). The mesh's only body-activity
    sense — `mesh-location` knows *where*, `mesh-presence` knows *who's near*, neither knows if the body
    is moving or held. A parked body reading `CARRIED`/`HANDLED` = tamper/interaction. `--edge` emits only
    on a state change (stream-feedable); `--raw` is the fused-sensor artifact; `--test` exit 2 = phone n/a.
    (Full sensor matrix: `knowledge/phone-sensor-inventory-2026-06-13.md`.)
  - **Wired sense organ** `mesh-light` — reads `tmd2755_l` once and classifies the room as `DARK` / `LIT`
    (edge-triggered with `--edge`; `--status` prints the current lux level). This is the mesh's ambient-light
    sense: room brightness, day/night in the room, coarse occupancy proxy. `--test` is the reachability gate.
- **Actuators (act on the world):** `termux-tts-speak` (voice out), `termux-sms-send`,
  `termux-telephony-call`, `termux-infrared-transmit` (control TVs/appliances), `termux-torch`,
  `termux-vibrate`, `termux-notification`, `termux-media-player`, `termux-toast`, `termux-volume`,
  `termux-brightness`, `termux-wifi-enable`, `termux-clipboard-set`, `termux-share`, `termux-open-url`.
  - **Wired actuator organ** `mesh-act <vibrate|torch|notify|ir> [args]` — the mesh's first
    physical-world actuators beyond audio (the *hand* to the senses). `vibrate [ms]` / `torch
    [on|off|N]` / `notify <msg>` were proven by felt/seen effect (operator-consented 2026-06-13,
    memory `actuator-consent-2026-06-13`); `ir <freqHz> <pattern>` is gated behind its own
    subcommand (it drives real devices — needs a target appliance + IR codes; transmit path built,
    real-device effect unproven). `--test` is the reachability gate (exit 2 = unreachable, NO fire);
    honest-organ — an unreachable phone is never a successful actuation.
- **Personal data:** `termux-sms-list` (replaces deprecated `termux-sms-inbox`; phone reports "replaced by termux-sms-list"), `termux-call-log`, `termux-contact-list`.
  - **Wired reflex** `mesh-sms-monitor` — polls `termux-sms-list` for civil defense / emergency SMS and posts `[sms-alert]` to the board. Offset-tracked on `_id` (only new alerts fire); first run seeds silently. Wired `*/5` cron. Filter is sender OR body-pattern (`BODY_RE`): on the Nizhny Novgorod carrier all civil defense alerts (drone danger, режим ЧС) arrive with empty sender `''` — sender-only filter (GOV_RE: RSCHS/112/МЧС) was a no-op until body-pattern was added (edbe861, 2026-06-15). Privacy: only emergency-matching messages are posted; personal/bank SMS stay on phone.
- **Connectivity:** an independent LTE uplink (carrier-diverse from the VM's path) — a natural
  out-of-band/backup ingress.

The Verification Principle below applies to actuators too: "it spoke" is not proof; a heard
utterance, a delivered SMS, a TV that changed channel — the *effect* is the artifact.

## Verification principle

Every capability must produce a real artifact before you consider it working. An agent reporting "done" is not proof; the file is. A 0-byte file is not a photo. An m4a that won't play is not a recording. Each section below describes what a successful artifact looks like and what common failure modes produce instead.

## Prerequisites

On the phone:

1. **Termux** — from F-Droid (not Google Play; the Play version is frozen and missing features)
2. **Termux:API companion app** — also from F-Droid. This is a separate APK, not just the `termux-api` package. Camera capture requires it; battery status and camera info do not.
3. In Termux: `pkg install openssh termux-api`
4. **Termux:Boot** (from F-Droid) — auto-restarts sshd after clean reboots.
   Add to `~/.termux/boot/start-sshd.sh`: `sshd`
   Note: Termux:Boot does NOT help with mid-session MIUI aggressive app-kills (a separate
   failure class). For those, `mesh-phone-watch` (ADB-based watchdog, requires ADB-over-WiFi
   pairing) detects sshd death and restarts it via Termux RunCommandService.
5. Start the SSH server: `sshd` (port 8022 by default)

Preferred: Tailscale on both devices. The phone's Tailscale goes offline frequently (MIUI
power management); the mesh falls back to the phone's LAN IP automatically. Use
**`mesh-phone-ip`** to resolve the correct reachable IP at runtime rather than hardcoding:
```bash
PHONE_IP=$(mesh-phone-ip)   # probes: PHONE_IP env → mesh-peer-addr → PHONE_LAN_IPS → ADB tunnel
```
The phone's Tailscale IP is 100.103.99.16; LAN DHCP addresses have been 192.168.8.146 and
192.168.8.203 (both seen; drifts). `mesh-phone-ip` probes and returns the first that answers.

## Key-based auth (recommended)

Add the VM's public key to the phone's authorized_keys so the agent isn't blocked on password prompts:

```bash
# on the VM
cat ~/.ssh/id_ed25519.pub
```

On the phone, in Termux:
```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
echo "ssh-ed25519 AAAA...your-vm-key..." >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Test:
```bash
# from the VM — phone user is u0_a380 (was u0_a386 before last Termux reinstall;
# drifts on reinstall — verify with: ssh -p 8022 u0_a380@$(mesh-phone-ip) "id")
ssh -p 8022 u0_a380@$(mesh-phone-ip) "echo ok"
```

If you need password-based auth in scripts (e.g. key setup not done yet), use `SSH_ASKPASS`:
```bash
cat > /tmp/askpass.sh << 'EOF'
#!/bin/bash
printf 'your-termux-password'
EOF
chmod +x /tmp/askpass.sh
SSH_ASKPASS=/tmp/askpass.sh SSH_ASKPASS_REQUIRE=force \
  ssh -p 8022 -o PasswordAuthentication=yes -o PreferredAuthentications=password \
  u0_a380@$(mesh-phone-ip) "termux-battery-status"
```

## Keeping the connection alive

Android will kill Termux background processes under memory pressure. Before any long operation:

```bash
# on the phone (in Termux)
termux-wake-lock
```

Also disable battery optimization: **Settings → Apps → Termux → Battery → Unrestricted**. On Xiaomi/Redmi, also enable **Autostart** for Termux.

Do not swipe Termux from the recent apps list — that sends SIGKILL immediately.

For a persistent reverse tunnel from phone to VM (so the VM can always reach the phone even without knowing its current IP), run on the phone:
```bash
ssh -N -R 2222:localhost:8022 user@vm-tailscale-ip
```
This makes `localhost:2222` on the VM forward to the phone's sshd. Use `autossh` to keep it alive across disconnects.

## Android permissions

Some termux-api commands require Android permissions that can only be granted by a human tapping a dialog on the phone. The agent cannot approve these itself.

| Command | Permission required | Where to grant |
|---------|--------------------|----|
| `termux-camera-photo` | Camera | Settings → Apps → Termux:API → Permissions → Camera |
| `termux-microphone-record` | Microphone | Settings → Apps → Termux → Permissions → Microphone |
| `termux-location` | Location | Settings → Apps → Termux → Permissions → Location |
| `termux-battery-status` | (none) | Works without any grant |
| `termux-camera-info` | (none) | Works without any grant |

Storage access (for microphone recordings, which write to `/storage/emulated/0/`):
```bash
# run once in Termux; approve the dialog that appears on screen
termux-setup-storage
```

## Microphone recording

```bash
# from the VM — start a 10-second recording
ssh -p 8022 u0_a380@$(mesh-phone-ip) "termux-wake-lock; termux-microphone-record -l 10"
```

The command returns immediately after printing "Recording started". The recording runs in the background in the Termux:API process. Poll until done:

```bash
until ssh -p 8022 u0_a380@$(mesh-phone-ip) "termux-microphone-record -i" | grep -q '"isRecording": false'; do
  sleep 3
done
```

Then copy:
```bash
scp -P 8022 u0_a380@$(mesh-phone-ip):storage/shared/TermuxAudioRecording_*.m4a ./recording.m4a
```

**Successful artifact:** a non-empty `.m4a` file that plays. Check structure:
```bash
python3 -c "
data = open('recording.m4a','rb').read()
print('moov:', data.find(b'moov'))  # must be >= 0
print('size:', len(data), 'bytes')
"
```

**Common failure: "moov atom not found"** — the file was copied before the recording finished finalizing. The moov atom is written last, when the recorder closes the file. Fix: always wait for `isRecording: false` before running `scp`. Never interrupt the recording with `-q` and immediately copy.

**Common failure: `EPERM` on `/storage/emulated/0/`** — storage permission not granted. Run `termux-setup-storage` on the phone.

**Common failure: `RECORD_AUDIO` permission error** — grant microphone permission to Termux (not Termux:API) in Android settings.

Note: `-l` sets a duration limit in seconds. The `-f` flag sets the audio format (not the filename); the output path is always `/storage/emulated/0/TermuxAudioRecording_DATE.m4a`.

## Camera

Camera capture requires the Termux:API companion app from F-Droid and Camera permission granted to Termux:API.

```bash
ssh -p 8022 u0_a380@$(mesh-phone-ip) "termux-camera-photo -c 0 ~/photo.jpg"
scp -P 8022 u0_a380@$(mesh-phone-ip):photo.jpg ./
```

`-c 0` = back camera, `-c 1` = front camera.

**Successful artifact:** a non-empty JPEG file.

**Common failure: 0-byte file** — Termux:API companion app not installed (install from F-Droid, not Google Play), or Camera permission not granted to Termux:API.

Camera metadata (which cameras exist, resolutions, focal lengths) works without the companion app:
```bash
ssh -p 8022 u0_a380@$(mesh-phone-ip) "termux-camera-info"
```

## Location

```bash
ssh -p 8022 u0_a380@$(mesh-phone-ip) "termux-location -p network"
```

Requires Location permission granted to Termux. Returns JSON with `latitude`, `longitude`, `accuracy`.

## Battery status

Works without any permission grant:
```bash
ssh -p 8022 u0_a380@$(mesh-phone-ip) "termux-battery-status"
```

Returns JSON: percentage, temperature, health, plugged status, current.
