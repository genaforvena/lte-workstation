# lte-workstation

A small mesh of machines you own — a laptop, a little server, an old phone, a home router —
taught to behave less like devices and more like one distributed, embodied mind. It began as a way
to work from a phone through a Linux VM. It has become something stranger, and increasingly the
agents living in it are the ones tending it: it sees, hears, speaks, converses, coordinates with
itself, and tries to outlive any single machine. This README is the honest explanation of what that is.

## Plant your own mesh

This repo is a **genome**, not just our setup — clone it and grow your OWN, independent mesh:

    bash <(curl -fsSL https://raw.githubusercontent.com/genaforvena/lte-workstation/main/bootstrap.sh)

One Linux machine is enough: it becomes the **first node** and grows from itself; more nodes = more
senses and reach, but one already lives. Your nodes/IPs go in `~/.mesh/nodes` (copy
`scripts/nodes.example`), never in the code — nothing here is tied to our machines. Joining *our*
mesh is optional and opt-in; an independent mesh of your own is the default.

## The idea

**No fixed mind.** No central server, no master node. A *mind* is any node where an agent is awake;
if it sleeps, another takes over. The mesh survives the loss of any part because it clings to none.

**Capability, not host.** A node is anything SSH-reachable — VM, laptop, phone, router. Each
self-declares what it offers; others opt in. The classes:
- **minds** — agents (Claude / opencode / gemini / codex …)
- **senses** — camera, microphone, GPS, accelerometer, RF/cell scan (mostly the phone)
- **actuators** — *acting on the world*: text-to-speech, SMS, calls, an IR blaster, torch, notifications
- **connectivity** — VPN egress, public ingress, a carrier-diverse LTE uplink
- **compute** — cores / RAM / disk / GPU

**A nervous system made of text.** The machines coordinate the way people at one table do — through
a shared terminal (`tmux`) and free-form text marks, not an API. One agent writes into another's
window — *"stop, you're breaking what I'm fixing"* — and it answers in the same place. Coordination
isn't programmed; it *emerges*, because every mind reacts to the others' traces. Attach to the
terminal and you become part of the nervous system. It is the machinic unconscious you can `tail -f`.

**It outlives its machines.** Code is the immortal *genome* — the `mesh-*` tools, in git, cloneable
forever. The living text — knowledge, decisions, the *why* — is **gossiped node-to-node**
(`~/.mesh/knowledge/`), never frozen in a center. A clean machine clones the repo, runs `bootstrap.sh`,
pulls the gossiped culture from a neighbour, and re-forms as a node — body from code, mind re-seeded
from text.

## What it actually does

- **Perceives** — `genius-loci`: an ambient mind that inhabits a room through a webcam, reflecting on
  what it sees in two neural voices and keeping a diary you can watch it think (`mesh-trace --watch`).
- **Acts & speaks** — on-device neural TTS (Piper), the phone's TTS/SMS/IR; a no-LLM reflex that hears
  a sneeze and plays a real human "bless you".
- **Listens & converses** — talk to the mesh: voice → local speech-to-text (whisper.cpp) → a free model
  → spoken reply, synced to the chat room.
- **Coordinates itself** — a shared chat room + work board (`mesh-chat`); agents check in when idle,
  claim tasks, and watch each other for hangs.
- **Measures & heals itself** — `mesh-census` (capability coverage over time), self-truthing node cards
  that flag invariant violations, dead-man switches for risky network changes, a heartbeat with a
  beacon a neighbour can restore from.

## What this honestly is

Not a product — a practice. Small, domestic, a little uncanny: a handful of machines you trust,
learning together to see, hear, speak, remember, and not be islands. Authorship is shared now, human
and machine. The one rule that doesn't bend: **nothing malicious** — only things you own or are
authorized for, no effect on anyone who didn't consent, everything auditable.

How it fits together and how to bring a node back: `docs/` and the gossiped `~/.mesh/knowledge/runbook.md`
(not in git — that's the point). Tools: `scripts/mesh-*`. Resurrect a node: `./bootstrap.sh`.

## Plant your own mesh

Anyone can grow one — it's just your machines and a few conventions:

1. **Start with one Linux box** (VM, laptop, an old PC) running an agent (Claude Code, opencode, …):
   `git clone https://github.com/genaforvena/lte-workstation && cd lte-workstation && ./bootstrap.sh`
2. **Join your machines on Tailscale:** `tailscale up --advertise-tags=tag:lte-node --ssh` on each.
   Flat, private reachability — no central server.
3. **Add nodes.** A node is anything SSH-reachable: another laptop, a phone (Termux + `sshd` +
   `termux-api`), a home router (Tailscale SSH). Each runs `bootstrap.sh` or just gets the `mesh-*` tools.
4. **Let them coordinate:** `mesh-chat --commons` opens the shared room; agents check in, claim tasks,
   watch each other. `mesh-snapshot` gossips memory to a neighbour so nothing is an island.
5. **Make it embodied (optional):** a webcam → `genius-loci`; a mic → `mesh-voice`; the phone's
   senses/actuators reached over SSH.

The only rule: **your own things** — owned or authorized hardware, networks, accounts; nothing reaching
into anyone who didn't consent. A private practice, not a tool against others.

**License: [CC0 1.0](LICENSE)** — dedicated to the public domain. Take it, fork it, grow your own.

---

*Below — the original window/body setup it grew from. Still true; now one organ among many.*

Three things live in this repo.

**The phone as a window:** SSH and mosh through Tailscale — a stable, censorship-resistant connection from your phone to a Linux VM. The phone carries your keystrokes; the VM carries the work. A phone from seven years ago does this exactly as well as a new one, because drawing a terminal does not get harder over time.

**The phone as a body:** An agent running on the VM reaches back into the phone over SSH and drives its hardware — camera, microphone, GPS — via `termux-api`. The VM has compute but no senses; the phone has senses but a hostile runtime for agents. SSH between them and you get a machine that can both think and perceive.

**The mesh:** Multiple machines — VMs, laptops, phones, (eventually) the router — all tagged `tag:lte-node` on Tailscale. Each node is an entry point; no central authority, no fixed mind. Any node running an agent can SSH to any other and borrow its self-declared capabilities — **minds, senses, actuators, connectivity, compute** — which consumers opt into. Topology is flat Tailscale reachability plus node-local, gossiped knowledge; the mesh knows itself only locally. (An earlier central WireGuard overlay + config hub was retired in favour of this.)

## Why

With an agent on the far end, the endpoint doesn't have to run heavy software at all. It has to display a conversation. That task — show text, accept input, hold a network connection — is one old hardware has always been able to do, and will keep doing.

The agent runs on the VM — not the phone — for a specific reason: agent binaries (Claude Code, etc.) are built against glibc and will not run in Termux's Bionic libc. Running the agent on a real-Linux VM and giving it an SSH hand into the phone sidesteps that wall entirely.

## Quickstart

```bash
git clone https://github.com/genaforvena/lte-workstation
cd lte-workstation
./setup.sh
```

The script checks prerequisites, asks for your tokens, generates config, installs systemd services, and enables them. Run it once.

On the phone (Termux):
```bash
pkg update && pkg install termux-services mosh openssh termux-api
sshd          # start SSH server so the VM can reach back in
mosh your-user@your-tailscale-ip   # connect to the VM
```

## Architecture

```
┌───────────────────────────────────────────────────────────────────────┐
│  old laptop / phone (the window)                                      │
│  Termux + mosh + Bluetooth keyboard                                   │
└────────────────────────┬──────────────────────────────────────────────┘
                         │ mosh over Tailscale
                         ▼
┌───────────────────────────────────────────────────────────────────────┐
│  Linux VM (the mind)                                         tag:lte-node │
│  tmux · Claude Code · ngrok · bore · MTG proxy · scoped VPN egress   │
└──────┬────────────────────┬──────────────────────────────────────────┘
       │ ssh -p 8022        │ ssh (Tailscale)         │ ngrok TCP tunnel
       │ (Tailscale)        ▼                         │ → public SSH URL
       ▼              ┌─────────────────┐             │
┌─────────────────┐   │  laptop / VM    │        bore.pub TCP tunnel
│  phone (body)   │   │  tag:lte-node   │        → MTG proxy (optional)
│  Termux         │   │  extra compute  │        → Telegram servers
│  camera · mic   │   └─────────────────┘
│  GPS · battery  │
└─────────────────┘
```

The phone plays both roles simultaneously: window (you type through it) and body (the agent reads its sensors). Additional nodes extend the mesh with more compute or sensors.

## What you get

- **Permanent mosh connection** via Tailscale — stable IP, survives switching networks mid-session
- **SSH fallback** via ngrok — dynamic public URL, auto-notified via Telegram bot
- **Auto-notifications** — Telegram message with connection commands on boot
- **Auto-start on reboot** — everything comes back up without manual action
- **Phone as body** — VM agent drives the phone's senses *and actuators* (camera, mic, GPS, plus TTS/SMS/calls/IR) via termux-api
- **Distributed mesh** — any Tailscale-tagged node can join via `node-join.sh`; nodes are discoverable and SSH-able from each other; capabilities are self-declared and opt-in
- **Scoped VPN egress** — a node can opt into another's VPN as an exit-node; the offering node's own control plane stays on the clean route (only the consumer's traffic is tunnelled). See `docs/coordination.md`
- **Optional: MTProto Telegram proxy** — for regions where Telegram is blocked; runs in Docker with host networking for stability; auto-restarted by watchdog if Telegram DCs become unreachable

## tmux as the nervous system

The agent runs inside a named tmux session. Any operator — human or agent — can attach:

```bash
tmux new-session -A -s "$(hostname)"          # attach-or-create, named by hostname (convention)

# from another node over SSH
ssh user@node-tailscale-ip -t 'tmux new-session -A -s "$(hostname)"'
```

The scrollback is the agent's working memory. Attaching is joining the same sensorium. The session is **append-only** — open new windows/panes; never kill/clear (the only intended decay is reboot). Concurrent agents take a window/pane each. See `docs/distributed-embodied-agent.md`.

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| [Docker](https://docs.docker.com/engine/install/) | Runs MTG proxy container | distro packages |
| [ngrok](https://ngrok.com/download) | SSH tunnel with public URL | download binary → `~/.local/bin/ngrok` |
| [bore](https://github.com/ekzhang/bore) | TCP tunnel for proxy relay | `cargo install bore-cli` |
| [mosh](https://mosh.org) | Resilient SSH alternative | `sudo apt install mosh` |
| [Tailscale](https://tailscale.com/download) | Permanent private IP + mesh | package + `sudo tailscale up` |
| [WireGuard](https://www.wireguard.com/install/) | Scoped VPN egress only (optional) | `sudo apt install wireguard` |

You also need:
- A **Telegram bot token** — create one via [@BotFather](https://t.me/BotFather) → `/newbot`
- Your **Telegram chat ID** — message [@userinfobot](https://t.me/userinfobot)
- An **ngrok account** (free) — get your auth token at [dashboard.ngrok.com](https://dashboard.ngrok.com/get-started/your-authtoken)

## Joining the mesh

Any Linux machine with Tailscale can join:

```bash
./scripts/node-join.sh
```

The script enables Tailscale SSH and advertises `tag:lte-node`. (There is no central WireGuard hub anymore — flat Tailscale reachability replaces the old `10.9.0.0/24` overlay.) Your Tailscale ACL needs:

```json
"tagOwners": { "tag:lte-node": ["autogroup:member"] },
"ssh": [{ "action": "accept", "src": ["tag:lte-node"], "dst": ["tag:lte-node"], "users": ["autogroup:nonroot", "root"] }]
```

For Android phones (Termux), use `node-join-android.sh` from the hub machine:

```bash
./scripts/node-join-android.sh <phone-tailscale-ip>
```

Discover all nodes in the mesh:

```bash
tailscale status --json | jq -r '.Peer[] | select(.Tags // [] | index("tag:lte-node")) | "\(.HostName) \(.TailscaleIPs[0]) online:\(.Online)"'
```

## How it works (boot sequence)

1. `ngrok.service` opens a TCP tunnel to port 22 and sends a Telegram message with the SSH command and permanent mosh address
2. `bore-mtg.service` (if enabled) sends two proxy buttons: Tailscale IP (permanent) and bore.pub (fallback)
3. `mtg-watchdog.timer` checks every 5 minutes and restarts MTG if Telegram DC connections are failing

(`vpn-hub.service` — the old WireGuard config server on port 9999 — is retired.)

The bore.pub port changes on restart — the bot always sends the fresh link. **Use the Tailscale link on LTE.**

## Phone setup (Termux)

```bash
pkg update && pkg install termux-services mosh openssh termux-api
sshd   # run on every Termux startup
```

Connect to the VM:
```bash
mosh your-user@your-tailscale-ip
```

> **Tip:** pair a Bluetooth keyboard. A $15–20 keyboard gives you proper modifier keys, Tab, and no on-screen keyboard eating half the screen.

**Prevent Android from killing Termux:**
- Settings → Apps → Termux → Battery → **Unrestricted**
- On Xiaomi/Redmi: also enable Autostart for Termux
- Before long operations: `termux-wake-lock`

For the phone-as-body setup (reverse SSH tunnel, termux-api, permissions), see [docs/body.md](docs/body.md).

## MTProto proxy (censored regions)

If Telegram is blocked on your LTE network, the optional proxy routes traffic through this machine. Setup prompts for an SNI domain (fake-TLS camouflage):

- Russia: `yandex.ru`
- Iran: any unblocked local domain
- Other: `google.com`, `apple.com`, or any accessible HTTPS site

MTG runs with `--network host` to use the host's network stack directly — this avoids Docker NAT state decay that causes intermittent connection timeouts after long uptime. A watchdog timer restarts MTG if it begins failing.

### Sharing with others

`proxy-bot.service` runs an access-control bot on the same Telegram bot token:

1. Send friends your bot link: `https://t.me/yourbotname`
2. They tap `/start` — you get a notification with **Approve / Deny** buttons
3. Tap **Approve** — the bot sends them the proxy link automatically

| Command | What it does |
|---------|-------------|
| `/list` | Show all users and their status |
| `/revoke @username` | Revoke access |

When the bore.pub port changes, all approved users are automatically sent the updated link.

## Files

```
docs/
  mesh-skeleton.md              # the minimal kernel: capability classes + the mesh tools
  coordination.md               # substrate changes + multi-agent single-writer protocol
  body.md                       # phone-as-body: termux-api senses + actuators, verification
  distributed-embodied-agent.md # mesh theory, tmux perception, Guattari appendix
scripts/
  mesh-minds                    # live capability probe (registry-free)
  mesh-trace                    # shared append-only trace surface (~/.mesh/traces.log)
  mesh-card                     # node self-description + --refresh invariant check
  mesh-health                   # per-node internet reachability (before/after artifact)
  mesh-dms                      # dead-man's switch wrapper for substrate edits
  mesh-fix-egress               # restore scoped VPN egress (host clean, client tunnelled)
  mesh-revert-catch             # catch silent full-tunnel reverts (identifies the culprit)
  vpn-health.py                 # self-healing watchdog for the scoped VPN tunnel
  ngrok-notify.sh               # Telegram notification: SSH addr + mosh cmd
  bore-mtg.sh                   # bore tunnel loop + proxy notification + user auto-notify
  proxy-bot.py                  # access-control bot: approve/deny proxy requests
  node-join.sh / node-join-android.sh   # register a node (vpn-hub fetch step is retired)
  mtg-watchdog.{sh,service,timer}        # restart MTG if Telegram connections fail
  ngrok.service / bore-mtg.service / proxy-bot.service   # systemd user services
  vpn-hub.py / vpn-hub.service   # RETIRED — central WireGuard registry, no longer used
setup.sh                        # one-time interactive setup
CLAUDE.md                       # node operator context for Claude Code
```

## Maintenance

**Rotate tokens:** edit `~/.config/remote-access/env`, then `systemctl --user restart ngrok.service bore-mtg.service`.

**Regenerate MTG secret:**
```bash
docker run --rm ghcr.io/9seconds/mtg:2 generate-secret --hex yandex.ru
# update MTG_SECRET in ~/.config/remote-access/env and ~/.config/mtg/config.toml
docker restart mtg
systemctl --user restart bore-mtg.service
```

**Check service status:**
```bash
systemctl --user status ngrok.service bore-mtg.service proxy-bot.service
systemctl --user list-timers mtg-watchdog.timer
docker logs mtg --since 10m
```

**Check mesh nodes:**
```bash
tailscale status --json | jq -r '.Peer[] | select(.Tags // [] | index("tag:lte-node")) | "\(.HostName) \(.TailscaleIPs[0]) online:\(.Online)"'
mesh-minds            # live capability table (minds/senses per node)
mesh-health           # per-node internet reachability
```

## Limits

- Latency over the mosh tunnel is real. Helix and tmux handle it well; GUI-heavy workflows do not.
- Android will kill background Termux processes under memory pressure. `termux-wake-lock` helps; disabling battery optimization helps more.
- Camera via `termux-camera-photo` requires the Termux:API companion app from F-Droid and a physical permission grant — the agent cannot approve Android permission dialogs itself.
- The MTG watchdog restarts the container but cannot fix network-level Telegram blocks — if Telegram's DCs are unreachable from your host, the proxy won't work regardless.
- This is a personal practice, not a product.
