# Mesh capability census — 2026-09-16

## Scope and method

This is the first live pass for `literature-capability-frontier-20260916/census-and-evidence`.
Reachability was read from `tailscale status --json`; device claims were checked with direct
commands, not inferred from the registry. The pass covered every currently online tagged peer and
the physically attached Note3.

## Live node matrix

| node | live evidence | capabilities established | gaps / interpretation |
|---|---|---|---|
| mesh-home | `mesh-card --refresh` at 2026-09-16T14:04:32Z; RTX 3060 12,288 MiB; USB camera + USB audio; active mesh services | primary compute; Claude/OpenCode/Codex/Ollama; camera, display-link, IRQ, light, link-flap, mic, UVC metadata; speaker, TV/DLNA, Docker compute, iMac notify/say, Shadowsocks | card reports identity-coherence conflict (27); this is an improvement target because capability attribution is currently noisy |
| Note3 / SM-N900 (attached to mesh-home) | `adb devices -l` found serial `4d00553d61ab90b7`; `pm list features`; `dumpsys sensorservice` | camera + autofocus + flash/torch; microphone + speaker; GPS/network location; Bluetooth/BLE; NFC/HCE; telephony/GSM; accelerometer, gyro, magnetometer/compass, barometer, proximity, light, humidity, ambient temperature, step detector/counter, significant motion, rotation/gravity/linear-acceleration; consumer IR | Many features are only Android declarations. Existing verified paths include barometer, camera, light/proximity/motion, speaker playback; IR is declared but not yet end-to-end proven. The sensor dump showed significant-motion and accelerometer clients active, so contention/ownership must be modeled. |
| imac-rozalia | SSH to `ilya@100.121.88.110` succeeded; Darwin 17.7.0; 4-core i5/16 GB; `/usr/bin/say` present | macOS speech actuator; possible camera/mic/BLE surface not yet probed in this pass | Need explicit artifact-backed probes for camera, microphone, screen, notifications, and local-network services before declaring them. |
| phaedra | SSH to `root@100.94.116.17` succeeded; Linux 7.0.0-22, 2 cores; running `mesh-loc-collector.service`, Tailscale, port-80 fallback | always-on compute/relay role; location-collector service; network fallback transport | `docker`, GPU, presence, and camera commands were absent or not resolved in the bounded probe; inspect service inputs/outputs and storage next. |
| Redmi 10 | Tailscale peer currently `online=true`, but SSH 8022 refused at 100.103.99.16 and 192.168.8.203; 192.168.8.146 timed out | no fresh device capability claim in this pass | This is a sleepy-body/sample reachability condition, not proof of absence. Retry on the next awake/SSH-success event; then census Termux API, camera, mic, location, SMS, telephony, sensors, and notification surfaces. |

## Immediate capability hypotheses

1. **Note3 multimodal event body:** fuse significant-motion, barometer, humidity/temperature,
   light/proximity, camera, microphone, and location into event-triggered context. The device
   exposes substantially more than the currently wired sensor subset.
2. **Note3 IR actuator:** consumer-IR is a declared hardware capability and the mesh has a root
   backend declaration, but it needs one safe frame-emission artifact before becoming a capability.
3. **iMac social/output edge:** `say` is live; camera/mic/notification probing could turn the iMac
   into a second human-facing, geographically distinct observation/output vantage.
4. **Phaedra durable relay:** its always-on location collector and port-80 fallback suggest a
   resilient store-and-forward/egress role; inspect the actual artifacts before designing around it.
5. **Identity-aware capability registry:** the mesh-home card's 27-field identity conflict is itself
   a capability-discovery problem: the registry must distinguish declared, live, wired, and verified
   capabilities rather than presenting all four as one state.

## Acceptance rule for the next pass

Every promoted capability needs a real artifact from the device or actuator, freshness and coverage
metadata, a named owner, and a literature/design mapping. A declaration, reachable SSH session, or
successful self-test alone remains `declared`/`unmeasured`.
