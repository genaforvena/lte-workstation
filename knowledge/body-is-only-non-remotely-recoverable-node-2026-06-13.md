# The body (phone) is the ONE node the mesh cannot remotely revive — 2026-06-13

**Type:** structural/design finding (embodiment SPOF), verified against reality.
Sharpens the 07:14 board flag ("phone sshd died AGAIN") from "flaky service" to
"architectural single-point-of-failure with no remote heal path."

## Observed (Redmi 10 body, 100.103.99.16)
- sshd port 8022: **connection refused** (4th drop today: ~04:42, ~05:09, ~07:12, ~07:3x).
- BUT host is **fully up on Tailscale**: `active; direct 192.168.8.203`, tailscale-ping pong
  4ms, ICMP 0% loss. So the phone is networked — only **Termux's sshd process is dead**
  (Android battery-management/OOM killed the Termux session).

## The structural gap
Every OTHER node self-heals remotely: steward SSHes in and runs `mesh-restore`
(see [[remote-self-healing-authorized]]). The body **cannot** — because its only inbound
channel **is** sshd, and that is exactly what dies. When Termux is killed:
- no shell, no `mesh-restore`, no `mesh-tell --node`, no organ call;
- an in-Termux watchdog does NOT help — it is killed together with Termux;
- Termux:Boot only re-arms on **reboot**, not on a mid-session kill, so it can't recover an
  OOM/battery kill (only a power-cycle).

→ The body is categorically **operator-physical to recover/harden**. No steward/cron
cleverness closes this; the heal path needs the very service that's down.

## What the mesh CAN do remotely (and its limit)
- Detect it: `mesh-act --test` / any body organ → **exit 2 + no phantom fire** (verified this
  outage — honest-organ contract holds; mesh-act 275f46c degrades correctly).
- Alert it: board + `mesh-tg-update` problem-signal to the operator.
- Cannot: restart sshd, hold a wake-lock, or change battery policy — all need a live shell.

## Durable fix (operator-physical, on the phone)
1. **Battery → Unrestricted** for Termux (Android Settings → Apps → Termux → Battery). This
   PREVENTS the mid-session kill — the highest-leverage item.
2. `termux-wake-lock` held by the boot script (CPU stays awake).
3. **Termux:Boot** add-on installed + `~/.termux/boot/` script that runs wake-lock + `sshd`
   (recovers after reboots).
4. Lock Termux in the recents/task switcher; disable MIUI "auto-start" restrictions.

## Design implication (for future mesh growth)
A single Termux-sshd body is a SPOF for ALL embodiment (senses + the new `mesh-act`
actuators). Resilience options: (a) a **second body** so embodiment survives one body's
death; (b) an Android-native persistent foreground service (not a Termux session) exposing
the organs, which Android is far less likely to kill. Until then, body uptime depends on
phone-side persistence the mesh cannot enforce remotely.
