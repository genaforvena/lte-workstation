# lte-workstation

Three things live in this repo.

**The phone as a window:** SSH and mosh through Tailscale — a stable, censorship-resistant connection from your phone to a Linux VM. The phone carries your keystrokes; the VM carries the work. A phone from seven years ago does this exactly as well as a new one, because drawing a terminal does not get harder over time.

**The phone as a body:** An agent running on the VM reaches back into the phone over SSH and drives its hardware — camera, microphone, GPS — via `termux-api`. The VM has compute but no senses; the phone has senses but a hostile runtime for agents. SSH between them and you get a machine that can both think and perceive.

**The mesh:** Multiple machines — VMs, laptops, phones — all tagged `tag:lte-node` on Tailscale and joined to a WireGuard overlay. Each node is an entry point. No central authority. The agent on the mind-VM can SSH to any node in the mesh and borrow its sensors, run computations, or chain commands. The topology propagates through Tailscale; the mesh knows itself only locally.

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
│  tmux · Claude Code · ngrok · bore · MTG proxy · vpn-hub             │
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
- **Phone sensor access** — VM agent captures audio, queries location, reads battery via termux-api
- **Distributed mesh** — any Tailscale-tagged node can join via `node-join.sh`; nodes are discoverable and SSH-able from each other
- **WireGuard overlay** — `vpn-hub.py` assigns each joining node a stable IP on `10.9.0.0/24`
- **Optional: MTProto Telegram proxy** — for regions where Telegram is blocked; runs in Docker with host networking for stability; auto-restarted by watchdog if Telegram DCs become unreachable

## tmux as the nervous system

The agent runs inside a named tmux session. Any operator — human or agent — can attach:

```bash
tmux new-session -d -s operator
tmux attach -t operator

# from another node over SSH
ssh user@vm-tailscale-ip -t tmux attach -t operator
```

The scrollback is the agent's working memory. Attaching is joining the same sensorium. See `docs/distributed-embodied-agent.md`.

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| [Docker](https://docs.docker.com/engine/install/) | Runs MTG proxy container | distro packages |
| [ngrok](https://ngrok.com/download) | SSH tunnel with public URL | download binary → `~/.local/bin/ngrok` |
| [bore](https://github.com/ekzhang/bore) | TCP tunnel for proxy relay | `cargo install bore-cli` |
| [mosh](https://mosh.org) | Resilient SSH alternative | `sudo apt install mosh` |
| [Tailscale](https://tailscale.com/download) | Permanent private IP + mesh | package + `sudo tailscale up` |
| [WireGuard](https://www.wireguard.com/install/) | Overlay VPN for the mesh | `sudo apt install wireguard` |

You also need:
- A **Telegram bot token** — create one via [@BotFather](https://t.me/BotFather) → `/newbot`
- Your **Telegram chat ID** — message [@userinfobot](https://t.me/userinfobot)
- An **ngrok account** (free) — get your auth token at [dashboard.ngrok.com](https://dashboard.ngrok.com/get-started/your-authtoken)

## Joining the mesh

Any Linux machine with Tailscale can join:

```bash
./scripts/node-join.sh
```

The script enables Tailscale SSH, advertises `tag:lte-node`, fetches a WireGuard config from the hub, and brings up `wg-mesh`. Your Tailscale ACL needs:

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
3. `vpn-hub.service` listens on port 9999 and serves WireGuard configs to joining nodes
4. `mtg-watchdog.timer` checks every 5 minutes and restarts MTG if Telegram DC connections are failing

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
  body.md                       # phone-as-body: termux-api, sensor access, verification
  distributed-embodied-agent.md # mesh theory, tmux perception, Guattari appendix
scripts/
  ngrok-notify.sh               # Telegram notification: SSH addr + mosh cmd
  bore-mtg.sh                   # bore tunnel loop + proxy notification + user auto-notify
  proxy-bot.py                  # access-control bot: approve/deny proxy requests
  vpn-hub.py                    # WireGuard mesh config server (runs on hub node)
  node-join.sh                  # register any Linux node into the mesh
  node-join-android.sh          # register an Android phone as a node (run from hub)
  mtg-watchdog.sh               # restart MTG if Telegram connections are failing
  ngrok.service                 # systemd user service
  bore-mtg.service              # systemd user service
  proxy-bot.service             # systemd user service
  vpn-hub.service               # systemd user service
  mtg-watchdog.service          # oneshot service called by the timer
  mtg-watchdog.timer            # runs watchdog every 5 minutes
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
systemctl --user status ngrok.service bore-mtg.service proxy-bot.service vpn-hub.service
systemctl --user list-timers mtg-watchdog.timer
docker logs mtg --since 10m
```

**Check mesh nodes:**
```bash
tailscale status --json | jq -r '.Peer[] | select(.Tags // [] | index("tag:lte-node")) | "\(.HostName) \(.TailscaleIPs[0]) online:\(.Online)"'
curl -s http://localhost:9999/nodes   # WireGuard mesh assignments
```

## Limits

- Latency over the mosh tunnel is real. Helix and tmux handle it well; GUI-heavy workflows do not.
- Android will kill background Termux processes under memory pressure. `termux-wake-lock` helps; disabling battery optimization helps more.
- Camera via `termux-camera-photo` requires the Termux:API companion app from F-Droid and a physical permission grant — the agent cannot approve Android permission dialogs itself.
- The MTG watchdog restarts the container but cannot fix network-level Telegram blocks — if Telegram's DCs are unreachable from your host, the proxy won't work regardless.
- This is a personal practice, not a product.
