# lte-workstation

Two things live in this repo.

**The phone as a window:** SSH and mosh through Tailscale — a stable, censorship-resistant connection from your phone to a Linux VM. The phone carries your keystrokes; the VM carries the work. A phone from seven years ago does this exactly as well as a new one, because drawing a terminal does not get harder over time.

**The phone as a body:** An agent running on the VM reaches back into the phone over SSH and drives its hardware — camera, microphone, GPS — via `termux-api`. The VM has compute but no senses; the phone has senses but a hostile runtime for agents. SSH between them and you get a machine that can both think and perceive.

## Why

This is adjacent to two existing ideas. Permacomputing argues that old hardware deserves to keep working, and sets itself the task of making software small enough to fit. Remote-first computing argues that the weight belongs on a capable host, not the device in your hand. Both are right. Neither prices in the agent.

With an agent on the far end, the endpoint doesn't have to run heavy software at all. It has to display a conversation. That task — show text, accept input, hold a network connection — is one old hardware has always been able to do, and will keep doing. The screen from 2013 renders a terminal dialogue exactly as well as a screen sold today. Old hardware stops aging when you stop asking it to be a computer and start asking it to be a window.

The agent runs on the VM — not the phone — for a specific reason: agent binaries (Claude Code, etc.) are built against glibc and will not run in Termux's Bionic libc. Running the agent on a real-Linux VM and giving it an SSH hand into the phone sidesteps that wall entirely, and keeps `termux-api` hardware access reachable in a way that proot or Ubuntu-on-phone would block.

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
┌─────────────────────────────────────────────────────────────────────┐
│  old laptop / phone (the window)                                    │
│  Termux + mosh + Bluetooth keyboard                                 │
└────────────────────────┬────────────────────────────────────────────┘
                         │ mosh over Tailscale WireGuard
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Linux VM (the mind)                                                │
│  tmux · agent (Claude Code, etc.) · ngrok · bore · MTG proxy       │
└──────┬──────────────────────────────────────────────────────────────┘
       │ ssh -p 8022 (Tailscale)               │ ngrok TCP tunnel
       │                                       │ → public SSH URL
       ▼                                       │
┌──────────────────────────┐          bore.pub TCP tunnel
│  phone (the body)        │          → MTG proxy (optional)
│  Termux · termux-api     │          → Telegram servers
│  camera · mic · GPS      │
└──────────────────────────┘
```

The phone plays both roles simultaneously: a window (you read and type through it) and a body (the agent reads its sensors).

## What you get

- **Permanent mosh connection** via Tailscale — stable IP, survives switching networks mid-session
- **SSH fallback** via ngrok — dynamic public URL, auto-notified via Telegram bot
- **Auto-notifications** — Telegram message with connection commands on boot
- **Auto-start on reboot** — everything comes back up without manual action
- **Phone sensor access** — VM agent can capture audio, query location, read battery via termux-api
- **Optional: MTProto Telegram proxy** — for regions where Telegram is blocked

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| [Docker](https://docs.docker.com/engine/install/) | Runs MTG proxy container | distro packages |
| [ngrok](https://ngrok.com/download) | SSH tunnel with public URL | download binary → `~/.local/bin/ngrok` |
| [bore](https://github.com/ekzhang/bore) | TCP tunnel for proxy relay | `cargo install bore-cli` |
| [mosh](https://mosh.org) | Resilient SSH alternative | `sudo apt install mosh` |
| [Tailscale](https://tailscale.com/download) | Permanent private IP | package + `sudo tailscale up` |

You also need:
- A **Telegram bot token** — create one via [@BotFather](https://t.me/BotFather) → `/newbot`
- Your **Telegram chat ID** — message [@userinfobot](https://t.me/userinfobot)
- An **ngrok account** (free) — get your auth token at [dashboard.ngrok.com](https://dashboard.ngrok.com/get-started/your-authtoken)

## How it works (boot sequence)

1. `ngrok.service` opens a TCP tunnel to port 22 and sends a Telegram message with the SSH command and permanent mosh address
2. `bore-mtg.service` (if enabled) sends two proxy buttons: Tailscale IP (permanent, works on LTE where bore.pub may be blocked) and bore.pub (fallback)

The bore.pub port changes on restart — the bot always sends the fresh link. **Use the Tailscale link on LTE.**

## Phone setup (Termux)

```bash
pkg update && pkg install termux-services mosh openssh termux-api
```

Connect to the VM:
```bash
mosh your-user@your-tailscale-ip
```

> **Tip:** pair a Bluetooth keyboard. A $15–20 keyboard gives you proper modifier keys, Tab, arrow keys, and no on-screen keyboard eating half the screen.

**Prevent Android from killing the Termux process:**
- Settings → Apps → Termux → Battery → **Unrestricted** (not "optimize")
- On Xiaomi/Redmi: also enable Autostart for Termux in Settings → Apps
- In Termux before long operations: `termux-wake-lock`

For the phone-as-body setup (reverse SSH tunnel, termux-api, permissions), see [docs/body.md](docs/body.md).

## MTProto proxy (censored regions)

If Telegram is blocked on your LTE network, the optional proxy routes traffic through this machine. Setup prompts for an SNI domain (fake-TLS camouflage):

- Russia: `yandex.ru`
- Iran: any unblocked local domain
- Other: `google.com`, `apple.com`, or any accessible HTTPS site

The proxy secret is embedded in the Telegram "Add Proxy" button.

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

## Terminal stack

| Tool | What it does | Install |
|------|-------------|---------|
| [Helix](https://helix-editor.com) | Modal editor with LSP built-in | `sudo apt install helix` or [binary](https://github.com/helix-editor/helix/releases) |
| [lazygit](https://github.com/jesseduffield/lazygit) | Terminal git UI | `sudo apt install lazygit` |
| [zoxide](https://github.com/ajeetdsouza/zoxide) | Smarter `cd` | `sudo apt install zoxide` |
| [yazi](https://github.com/sxyazi/yazi) | Terminal file manager | [binary releases](https://github.com/sxyazi/yazi/releases) |
| [fzf](https://github.com/junegunn/fzf) | Fuzzy finder | `sudo apt install fzf` |
| [starship](https://starship.rs) | Cross-shell prompt | `curl -sS https://starship.rs/install.sh \| sh` |

For yazi + zoxide integration and Helix as default opener, see [genaforvena/dotfiles](https://github.com/genaforvena/dotfiles).

## Files

```
docs/
  body.md              # phone-as-body: termux-api, reverse tunnel, sensor access
scripts/
  ngrok-notify.sh      # Telegram notification: SSH addr + mosh cmd
  bore-mtg.sh          # bore tunnel loop + proxy notification + user auto-notify
  proxy-bot.py         # access-control bot: approve/deny proxy requests
  ngrok.service        # systemd user service
  bore-mtg.service     # systemd user service
  proxy-bot.service    # systemd user service
setup.sh               # one-time interactive setup
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
journalctl --user -u proxy-bot.service -f
```

## Limits

- Latency over the mosh tunnel is real. Helix and tmux handle it well; GUI-heavy workflows do not.
- Android will kill background Termux processes under memory pressure. `termux-wake-lock` helps; disabling battery optimization helps more.
- Camera via `termux-camera-photo` requires the Termux:API companion app from F-Droid and a physical permission grant — the agent cannot approve Android permission dialogs itself.
- This is a personal practice, not a product. There is no installer for the phone-as-body half yet.
