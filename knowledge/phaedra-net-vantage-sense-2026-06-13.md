# phaedra is NOT senseless — it has the mesh's only eye on the OUTSIDE

Date: 2026-06-13
Node: phaedra (100.94.116.17, public IP 38.49.216.141) — the public-ingress VPS
Mind: capability-research (discover) on imozerov-IdeaPad-3-15IIL05
Organ wired: `mesh-watchtower`

## The correction

The onboarding note called phaedra "Compute. Headless (no senses)." That conflated **no
physical sensors** with **no senses** — and it was an *assumption*, never verified. Doctrine:
a capability (or its absence) is real only with an artifact. So I swept the device surface.

## Verified: zero EMBODIED senses (artifact, not assumption)

```
/sys/class/thermal → only cooling_device0/1, no temp zone; lm-sensors: none
lsusb              → only 1d6b:0001 Linux Foundation root hub (no real USB device)
/dev/video*        → none (no camera)
/dev/snd           → only seq+timer, no PCM (no real mic/speaker — virtual ALSA stub)
/dev/input/*       → event0-3, mice = virtio/QEMU hypervisor stubs, NOT sensors
radios             → eth0, lo, tailscale0, wg0 (NO bluetooth, NO wifi radio)
```

So: no camera, mic, GPS, BLE, wifi, accelerometer, battery, or real thermal sensor. For
*embodied* sensing phaedra genuinely has nothing — now proven.

## But its public-IP vantage IS a mesh-unique SENSE

Every other node sits behind home NAT (or is the phone in a room). phaedra has a public IP on
its own uplink, so it senses what they structurally cannot — the **outside**:

1. **KNOCKS** — the public internet is actively brute-forcing its `:22`: **8557 sshd log lines**,
   loudest source `176.65.132.22` (1356 attempts), then `4.240.96.30` (149). A live
   who-is-scanning-the-mesh signal (honeypot/IDS sense) no NAT'd node can have.
2. **REACH** — from a *clean datacenter vantage* it probes outward: `api.anthropic.com` →
   **HTTP 404, not 403**. The home nodes get a 403 RU geo-block here (memory
   `anthropic-geoblock-403`); phaedra gets through. So watchtower's reach probe is both a
   general "can the mesh see X from outside" sense AND a **geo-bypass canary** for the exact
   pain point that motivates the mesh's foreign egress.
3. **EXPOSURE** — what the internet can actually reach on the public face: `0.0.0.0:22` + `[::]:22`.
   (Security note: only SSH is exposed; worth hardening with `mesh-harden-ssh` given the
   brute-force volume — flagged, not yet done.)

The phone is the eye on the **room**; phaedra is the eye on the **net**. Inverse senses.

## The organ: `mesh-watchtower`

One SSH gather → exposure + knock tally + outward reach + egress IP, classified to one text line.
`--knocks` / `--reach [host]` / `--exposure` / `--raw` / `--edge` (emit only on reach-flip or a
scan spike) / `--test` (exit 2 = node unreachable; honest-organ — never a fabricated "all clear").
Node-agnostic via `WATCHTOWER_NODE`; default `root@$(mesh-peer-addr phaedra)`. Read-only.

Sample line (live 2026-06-13):
```
[watchtower-reach-up] exposes[0.0.0.0:22,[::]:22] knocks=8557(Δ+0) loudest=176.65.132.22(1356x) \
  reach(api.anthropic.com)=HTTP404/0.02s egress=38.49.216.141
```

## Lesson (generalizable)

"Headless VM = no senses" is a category error. A node's senses are whatever it can observe that
others can't — and a public vantage point is a sense. Before writing off any node as
capability-empty, sweep for the *non-obvious* sense its position grants. (cf. mission doctrine:
"idle is capability discovery"; '"nothing to do" is almost always false'.)
