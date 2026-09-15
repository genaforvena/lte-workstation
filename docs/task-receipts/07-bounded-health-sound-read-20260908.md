# Bounded health/sound observation — 2026-09-08

- Task: `hire-ledger-correction-prereqs-20260908/07-bounded-health-sound-read`
- Owner: `hire`
- Captured: `2026-09-08T12:20:44Z`
- Repository revision: `10ac36b9b30ac01b33d7b5975523965db7027508`

## Health read

Command: `timeout 30s mesh-health`

```text
rc=0 elapsed_ms=12765 stdout_bytes=815 stderr_bytes=0
=== mesh-health 2026-09-08T12:20:25Z ===
PASS  mesh-home                        100.81.222.19 (self)
OFFLINE GL-MT3000                        100.105.241.84 (tailnet: last-seen 81d ago, active=True)
OFFLINE Redmi 10                         100.103.99.16 (tailnet: last-seen 5d ago, active=True)
OFFLINE ilya                             100.107.198.111 (tailnet: last-seen 19d ago, active=True)
SKIP  imac-rozalia                     100.121.88.110 — SSH unreachable
OFFLINE imozerov-Default-string          100.125.157.75 (tailnet: last-seen 55d ago, active=True)
OFFLINE imozerov-IdeaPad-3-15IIL05       100.73.170.56 (tailnet: last-seen 9d ago, active=True)
PASS  phaedra                          100.94.116.17
OFFLINE rip                              100.116.125.102 (tailnet: last-seen 5d ago, active=False)
stderr: empty
```

The first 8-second bounded attempt timed out with partial output (`rc=124`); the 30-second
bounded retry completed (`rc=0`). The final read preserves measured `last-seen` ages and the
SSH-unreachable `SKIP`; it does not turn silence into a healthy or unhealthy claim.

## Sound read

Command: `mesh-audio --verbose`

```text
rc=0 elapsed_ms=28 stdout_bytes=784 stderr_bytes=0
=== mesh-audio @ 2026-09-08T12:20:38Z — mesh-home ===
cards: NVidia Generic Camera
capture_devices: 3
playback_devices: 6
audio_group: 1 (1=member)
pulseaudio: 1 (1=found)
pipewire: 1 (1=found)
ALSA capture: card 1 Generic, devices 0 ALC897 Analog and 2 ALC897 Alt Analog
ALSA playback: card 0 NVidia, HDMI devices enumerated
stderr: empty
```

The direct producer read is fresh at the command timestamp and enumerates three capture and six
playback PCM devices. `mesh-audio --test` independently returned `rc=0`, `smoke-test: ok` in
5 ms. This is an inventory/freshness observation, not a claim that audio was recorded; no
recording producer artifact was present in this bounded read, so recorded-audio freshness is
`UNKNOWN`, not inferred from quiet output.
